
from PIL import Image

img = Image.open("D:/_Bian_Cheng/_temp/Img/img_align_celeba/200000.jpg")
img = Image.open("D:/_Bian_Cheng/_temp/Img/img_align_celeba/200000.jpg")
h = img.height
w = img.width
size = min(h, w) - 5
height = (h - size) // 3 + 1
width = (w - size) // 2 + 1
print(size)
print(w)
print(h)
print(height)
print(width)