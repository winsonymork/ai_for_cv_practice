import numpy as np
import math
import cv2 as cv
import random
import math
import os
import copy
from matplotlib import pyplot as plt


f = input("pls enter the path of  your pic:")

# 准备素材
def changeBGR2RGB(img):
    B, G, R = cv.split(img)
    return cv.merge((R, G, B))

# img = changeBGR2RGB(cv.imread(r'F:/1.jpg'))
img = cv.imread(f)

# plt.imshow(img)
# 裁剪 crop   start: 开始坐标   w：宽  h:高
def crop(img):
    #     img = copy.deepcopy(img)
    rows, cols, channel = img.shape
    rate = random.uniform(0.1, 0.9)
    w = math.ceil(cols * rate)
    h = math.ceil(rows * rate)
    yStart = random.randint(0, rows - h)
    xStart = random.randint(0, cols - w)
    return img[yStart:h + yStart, xStart:w + xStart]


# Test crop
# imgCrop = crop(img)
# plt.imshow(imgCrop)

# 颜色迁移 color shift
# 颜色迁移 color shift
def colorShif(img):
    B, G, R = cv.split(img)
    shift = 100
    b_rand = random.randint(-shift, shift)
    if b_rand == 0:
        pass
    elif b_rand > 0:
        lim = 255 - b_rand
        B[B > lim] = 255
        B[B <= lim] = (b_rand + B[B <= lim]).astype(img.dtype)
    elif b_rand < 0:
        lim = 0 - b_rand
        B[B < lim] = 0
        B[B >= lim] = (b_rand + B[B >= lim]).astype(img.dtype)

    g_rand = random.randint(-shift, shift)
    if g_rand == 0:
        pass
    elif g_rand > 0:
        lim = 255 - g_rand
        G[G > lim] = 255
        G[G <= lim] = (g_rand + G[G <= lim]).astype(img.dtype)
    elif g_rand < 0:
        lim = 0 - g_rand
        G[G < lim] = 0
        G[G >= lim] = (g_rand + G[G >= lim]).astype(img.dtype)

    r_rand = random.randint(-shift, shift)
    if r_rand == 0:
        pass
    elif r_rand > 0:
        lim = 255 - r_rand
        R[R > lim] = 255
        R[R <= lim] = (r_rand + R[R <= lim]).astype(img.dtype)
    elif r_rand < 0:
        lim = 0 - r_rand
        R[R < lim] = 0
        R[R >= lim] = (r_rand + R[R >= lim]).astype(img.dtype)

    img = cv.merge((B, G, R))
    return img


# # test
# img2 = colorShif(img)
# plt.imshow(img)


# 旋转 Rotation
def rotation(img):
    #     img = copy.deepcopy(img)
    rows, cols, channel = img.shape
    #     angle = random.randint(30,180)
    angle = 90
    M = cv.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), angle, 1)
    dst = cv.warpAffine(img, M, (cols, rows))
    return dst


# test rotation
# img2 = rotation(img,30)
# plt.imshow(img2)


# 投影变换 perspective transform
def perspectiveTransform(img):
    #     img = copy.deepcopy(img)
    rows, cols, channel = img.shape
    random_margin = random.randint(10, 100)
    height, width, channels = img.shape
    x1 = random.randint(-random_margin, random_margin)
    y1 = random.randint(-random_margin, random_margin)
    x2 = random.randint(width - random_margin - 1, width - 1)
    y2 = random.randint(-random_margin, random_margin)
    x3 = random.randint(width - random_margin - 1, width - 1)
    y3 = random.randint(height - random_margin - 1, height - 1)
    x4 = random.randint(-random_margin, random_margin)
    y4 = random.randint(height - random_margin - 1, height - 1)

    dx1 = random.randint(-random_margin, random_margin)
    dy1 = random.randint(-random_margin, random_margin)
    dx2 = random.randint(width - random_margin - 1, width - 1)
    dy2 = random.randint(-random_margin, random_margin)
    dx3 = random.randint(width - random_margin - 1, width - 1)
    dy3 = random.randint(height - random_margin - 1, height - 1)
    dx4 = random.randint(-random_margin, random_margin)
    dy4 = random.randint(height - random_margin - 1, height - 1)

    pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    pts2 = np.float32([[dx1, dy1], [dx2, dy2], [dx3, dy3], [dx4, dy4]])

    M = cv.getPerspectiveTransform(pts1, pts2)
    dst = cv.warpPerspective(img, M, (rows, cols))
    return dst


# test perspective
# img2 = perspectiveTransform(img)
# plt.imshow(img2)

# 整合
def together(img):
    return perspectiveTransform(rotation(colorShif(crop(img))))


img = together(img)
plt.imshow(img)

# cv.imshow('lenna', img)
# key = cv.waitKey()
# if key == 27:
#     cv.destroyAllWindows()
outpath= os.path.dirname(f)
cv.imwrite(outpath+"GEN.jpg",img)