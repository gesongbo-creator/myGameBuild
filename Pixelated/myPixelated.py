import cv2
import numpy as np

# 读取图片（默认 BGR 彩色）
img = cv2.imread("try.png")

# 获取尺寸
height, width, channels = img.shape
print(f"尺寸: {width} x {height}, 通道数: {channels}")

# 访问像素 (y, x)，返回 [B, G, R]
pixel = img[200, 100]
print(f"(100,200) 的 BGR 像素: {pixel}")

# 如果习惯用 RGB，可以转换
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# print(f"(100,200) 的 RGB 像素: {img_rgb[200, 100]}")

mymap = []
for y in range(height):
    for x in range(width):
        b= int(img[y, x][0])
        g= int(img[y, x][1])
        r= int(img[y, x][2])
        mymap.append([b, g, r])

print(mymap[:3])


