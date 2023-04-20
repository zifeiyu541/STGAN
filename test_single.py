from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from functools import partial
import json
import traceback


import imlib as im
import numpy as np
import pylib
import tensorflow as tf
import tflib as tl

import data
import models

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def generate_single(experiment_name, gpu='all', dataroot='D:\_Bian_Cheng\_temp\Img',
                    img=None, test_atts=None, test_ints=None, test_int=1.0, test_slide=False,
                    n_slide=10, test_att=None, test_int_min=-1.0, test_int_max=1.0):
    with open('./front/public/output/%s/setting.txt' % experiment_name) as f:
        args = json.load(f)

    # model
    atts = args['atts']
    n_att = len(atts)
    img_size = args['img_size']
    shortcut_layers = args['shortcut_layers']
    inject_layers = args['inject_layers']
    enc_dim = args['enc_dim']
    dec_dim = args['dec_dim']
    dis_dim = args['dis_dim']
    dis_fc_dim = args['dis_fc_dim']
    enc_layers = args['enc_layers']
    dec_layers = args['dec_layers']
    dis_layers = args['dis_layers']

    label = args['label']
    use_stu = args['use_stu']
    stu_dim = args['stu_dim']
    stu_layers = args['stu_layers']
    stu_inject_layers = args['stu_inject_layers']
    stu_kernel_size = args['stu_kernel_size']
    stu_norm = args['stu_norm']
    stu_state = args['stu_state']
    multi_inputs = args['multi_inputs']
    rec_loss_weight = args['rec_loss_weight']
    one_more_conv = args['one_more_conv']

    print('Using selected images:', img)

    if gpu != 'all':
        os.environ['CUDA_VISIBLE_DEVICES'] = gpu

    #### testing
    # multiple attributes
    if test_atts is not None and test_ints is None:
        test_ints = [1 for i in range(len(test_atts))]

    thres_int = args['thres_int']
    # others
    use_cropped_img = args['use_cropped_img']


    # ==============================================================================
    # =                                   graphs                                   =
    # ==============================================================================

    # data
    sess = tl.session()
    te_data = data.Celeba(dataroot, atts, img_size, 1, part='test', sess=sess, crop=not use_cropped_img, im_no=img)
    # models
    Genc = partial(models.Genc, dim=enc_dim, n_layers=enc_layers, multi_inputs=multi_inputs)
    Gdec = partial(models.Gdec, dim=dec_dim, n_layers=dec_layers, shortcut_layers=shortcut_layers,
                   inject_layers=inject_layers, one_more_conv=one_more_conv)
    Gstu = partial(models.Gstu, dim=stu_dim, n_layers=stu_layers, inject_layers=stu_inject_layers,
                   kernel_size=stu_kernel_size, norm=stu_norm, pass_state=stu_state)

    # inputs
    xa_sample = tf.placeholder(tf.float32, shape=[None, img_size, img_size, 3])
    _b_sample = tf.placeholder(tf.float32, shape=[None, n_att])
    raw_b_sample = tf.placeholder(tf.float32, shape=[None, n_att])

    # sample
    test_label = _b_sample - raw_b_sample if label == 'diff' else _b_sample
    if use_stu:
        x_sample = Gdec(Gstu(Genc(xa_sample, is_training=False),
                             test_label, is_training=False), test_label, is_training=False)
    else:
        x_sample = Gdec(Genc(xa_sample, is_training=False), test_label, is_training=False)

    # ==============================================================================
    # =                                    test                                    =
    # ==============================================================================

    # initialization
    ckpt_dir = './front/public/output/%s/checkpoints' % experiment_name
    tl.load_checkpoint(ckpt_dir, sess)

    # test
    try:
        multi_atts = test_atts is not None
        for idx, batch in enumerate(te_data):
            xa_sample_ipt = batch[0]
            a_sample_ipt = batch[1]
            b_sample_ipt_list = [a_sample_ipt.copy() for _ in range(n_slide if test_slide else 1)]
            if test_slide: # test_slide
                for i in range(n_slide):
                    test_int = (test_int_max - test_int_min) / (n_slide - 1) * i + test_int_min
                    b_sample_ipt_list[i] = (b_sample_ipt_list[i]*2-1) * thres_int
                    b_sample_ipt_list[i][..., atts.index(test_att)] = test_int
            elif multi_atts: # test_multiple_attributes
                for a in test_atts:
                    i = atts.index(a)
                    b_sample_ipt_list[-1][:, i] = 1 - b_sample_ipt_list[-1][:, i]
                    b_sample_ipt_list[-1] = data.Celeba.check_attribute_conflict(b_sample_ipt_list[-1], atts[i], atts)
            else: # test_single_attributes
                for i in range(len(atts)):
                    tmp = np.array(a_sample_ipt, copy=True)
                    tmp[:, i] = 1 - tmp[:, i]   # inverse attribute
                    tmp = data.Celeba.check_attribute_conflict(tmp, atts[i], atts)
                    b_sample_ipt_list.append(tmp)

            x_sample_opt_list = [xa_sample_ipt, np.full((1, img_size, img_size // 10, 3), -1.0)]
            raw_a_sample_ipt = a_sample_ipt.copy()
            raw_a_sample_ipt = (raw_a_sample_ipt * 2 - 1) * thres_int
            for i, b_sample_ipt in enumerate(b_sample_ipt_list):
                _b_sample_ipt = (b_sample_ipt * 2 - 1) * thres_int
                if not test_slide:
                    if multi_atts: # i must be 0
                        for t_att, t_int in zip(test_atts, test_ints):
                            _b_sample_ipt[..., atts.index(t_att)] = _b_sample_ipt[..., atts.index(t_att)] * t_int
                    if i > 0:   # i == 0 is for reconstruction
                        _b_sample_ipt[..., i - 1] = _b_sample_ipt[..., i - 1] * test_int
                x_sample_opt_list.append(sess.run(x_sample, feed_dict={xa_sample: xa_sample_ipt,
                                                                       _b_sample: _b_sample_ipt,
                                                                       raw_b_sample: raw_a_sample_ipt}))
            sample = np.concatenate(x_sample_opt_list, 2)

            if test_slide:     save_folder = 'sample_testing_slide'
            elif multi_atts:   save_folder = 'sample_testing_multi'
            else:              save_folder = 'sample_testing'
            save_dir = './front/public/output/%s/%s' % (experiment_name, save_folder)
            pylib.mkdir(save_dir)
            im.imwrite(sample.squeeze(0), '%s/%06d%s.png' % (save_dir,
                                                             idx + 182638 if img is None else img[idx],
                                                             '_%s'%(str(test_atts)) if multi_atts else ''))

            print('%06d.png done!' % (idx + 182638 if img is None else img[idx]))
    except:
        traceback.print_exc()
    finally:
        sess.close()


# generate_single(experiment_name="128", img=[1])
