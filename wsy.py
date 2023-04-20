import numpy as np

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
atts = ['Bald', 'Bangs', 'Black_Hair', 'Blond_Hair', 'Brown_Hair',
        'Bushy_Eyebrows', 'Eyeglasses', 'Male', 'Mouth_Slightly_Open'
        ,'Mustache', 'No_Beard', 'Pale_Skin', 'Young']
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
att_file = 'D:\_Bian_Cheng\_temp\Img\list_attr_celeba.txt'
att_cols = [att_dict[i]+1 for i in atts]
attr = np.loadtxt(att_file, skiprows=2, usecols=att_cols, dtype=str)

pid = 100000
attribute = 'Male'

print(attr[int(pid)-1][site[attribute]])

