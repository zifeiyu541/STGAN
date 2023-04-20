import os
import shutil
import os.path as path
from collections import OrderedDict as odict
from PIL import Image, ImageTk
import random

import numpy as np

import tkinter as t
import tkinter.filedialog as fd

import test_single as ts

from datetime import datetime

from flask import Flask, request, make_response
# request用于接收数据
from flask import request
# 解决跨域问题
from flask_cors import CORS

#  创建flask服务对象
app = Flask(__name__)
#  动态解决前端跨域问题
CORS(app, supports_credentials=True)

raw_img = 'Ours'

paths = odict([
    ('Ours', './front/public/output/128/sample_testing')
])

atts = ['Bald', 'Bangs', 'Black_Hair', 'Blond_Hair', 'Brown_Hair',
        'Bushy_Eyebrows', 'Eyeglasses', 'Male', 'Mouth_Slightly_Open'
        ,'Mustache', 'No_Beard', 'Pale_Skin', 'Young']

num_att = len(atts)

site = {'Bald': 0,
        'Bangs': 1,
        'Black_Hair': 2,
        'Blond_Hair': 3,
        'Brown_Hair': 4,
        'Bushy_Eyebrows': 5,
        'Eyeglasses': 6,
        'Male': 7,
        'Mouth_Slightly_Open': 8,
        'Mustache': 9,
        'No_Beard': 10,
        'Pale_Skin': 11,
        'Young': 12}

crop_dict = {
    'Ours': [(i*128+140, 0, i*128+268, 128) for i in range(1, num_att+1)]
}

IMG_PATH = "./front/public/output/128/sample_testing"

att_dict = {'5_o_Clock_Shadow': 0, 'Arched_Eyebrows': 1, 'Attractive': 2,
                'Bags_Under_Eyes': 3, 'Bald': 4, 'Bangs': 5, 'Big_Lips': 6,
                'Big_Nose': 7, 'Black_Hair': 8, 'Blond_Hair': 9, 'Blurry': 10,
                'Brown_Hair': 11, 'Bushy_Eyebrows': 12, 'Chubby': 13,
                'Double_Chin': 14, 'Eyeglasses': 15, 'Goatee': 16,
                'Gray_Hair': 17, 'Heavy_Makeup': 18, 'High_Cheekbones': 19,
                'Male': 20, 'Mouth_Slightly_Open': 21, 'Mustache': 22,
                'Narrow_Eyes': 23, 'No_Beard': 24, 'Oval_Face': 25,
                'Pale_Skin': 26, 'Pointy_Nose': 27, 'Receding_Hairline': 28,
                'Rosy_Cheeks': 29, 'Sideburns': 30, 'Smiling': 31,
                'Straight_Hair': 32, 'Wavy_Hair': 33, 'Wearing_Earrings': 34,
                'Wearing_Hat': 35, 'Wearing_Lipstick': 36,
                'Wearing_Necklace': 37, 'Wearing_Necktie': 38, 'Young': 39}
att_file = 'D:\_Bian_Cheng\_temp\Img\list_attr_celeba.txt'
att_cols = [att_dict[i]+1 for i in atts]
attr = np.loadtxt(att_file, skiprows=2, usecols=att_cols, dtype=str)


#  指定请求路径、方法
@app.route('/getPicture', methods=['GET'])
def getPicture():
    # request_begin_time = datetime.today()
    # print("request_begin_time", request_begin_time)
    pid = request.args.get("pid")
    attribute = request.args.get("attribute")

    if request.method == 'GET':
        if pid is None:
            pass
        else:
            try:  # 尝试打开对应属性的图片
                single_img = open(IMG_PATH + '/' + pid + '_' + attribute + ".png", "rb").read()
                # response = make_response(single_img)
                # response.headers['Content-Type'] = 'image/png'
                if attribute == 'raw':
                    return pid + '_' + attribute + ".png"
                else:
                    return pid + '_' + attribute + ".png$" + attr[int(pid)-1][site[attribute]]
            except:  # 该图片的该属性之前未访问过
                print('Can\'t open %s_%s.png' % (str(pid), attribute))
                try:  # 尝试打开对应图片
                    img = Image.open(IMG_PATH + '/' + pid + ".png")
                    try:  # 裁剪该图片对应的属性
                        if attribute == 'raw':
                            save_img = img.crop((0, 0, 128, 128))
                        else:
                            i = site[attribute]+1
                            save_img = img.crop((i*128+140, 0, i*128+268, 128))
                        save_img.save(IMG_PATH + '/' + pid + '_' + attribute + ".png")
                        return getPicture()
                    except:  # 属性不存在
                        # return 'The attribute of %s is unavailable' % attribute
                        return "unavailable attribute"
                except:  # 该图片未生成过
                    print('Can\'t open %s.png' % (str(pid)))
                    if int(pid) < 100000 or int(pid) > 200000:
                        return 'The pid of %s is unavailable' % pid
                    else:  # 若图片id符合要求，则生成该图片
                        ts.generate_single(experiment_name="128", img=[int(pid)])
                        return getPicture()

    else:
        pass

    # imgs = {}
    # for cat in paths:
    #     try:
    #         wimg = Image.open(path.join(paths[cat], str(pid) + '.png'))
    #     except:
    #         try:
    #             wimg = Image.open(path.join(paths[cat], str(pid) + '.jpg'))
    #         except:
    #             print('Can\'t open %s of %s' % (str(pid), cat))
    #             continue
    #     if cat == raw_img:
    #         rimg = wimg.crop((0, 0, 128, 128))
    #         imgs['raw'] = rimg
    #     imgs[cat] = [wimg.crop(crop_dict[cat][i]) for i in range(num_att)]
    #     # if cat == 'StarGAN':
    #     #     imgs[cat] = [wimg.crop(crop_stargan[i]) for i in range(num_att)]
    #     # else:
    #     #     imgs[cat] = [wimg.crop(crop_others[i]) for i in range(num_att)]
    #     wimg.close()
    # return imgs


if __name__== "__main__":
    #  指定端口号和地址
    app.run(port=1234)

