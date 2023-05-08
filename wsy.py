from PIL import Image, ImageTk

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

IMG_PATH = "D:/_Bian_Cheng/_temp/Img/output"

IMG_ID = "182651"

img = Image.open(IMG_PATH + "/128/sample_testing_slide/" + IMG_ID + ".png")
# save_img = img.crop((0, 0, 128, 128))
# save_img.save(IMG_PATH + '/temp/' + IMG_ID + ".png")

for i in range(5):
    save_img = img.crop((i*128+140, 0, i*128+268, 128))
    save_img.save(IMG_PATH + '/temp/' + IMG_ID + '_Mustache_' + str(i+1) + ".png")
    print(i)


# for att in atts:
#     save_img = img.crop((site[att]*128+128+140, 0, site[att]*128+128+268, 128))
#     save_img.save(IMG_PATH + '/temp/' + IMG_ID + '_' + att + ".png")
#     print(att)


# for i in range(182638, 183638):
#     img = Image.open(IMG_PATH + '/128/mustache/' + str(i) + "_['Mustache'].png")
#     save_img = img.crop((140, 0, 268, 128))
#     save_img.save(IMG_PATH + '/mustache/' + str(i) + "_Mustache.png")
#     print(str(i))
