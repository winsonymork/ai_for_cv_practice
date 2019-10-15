import cv2 as cv
import numpy as np
import os
from matplotlib import pyplot as plt

# 
def changeBGR2RGB(img):
    B,G,R = cv.split(img)
    return cv.merge((R,G,B))

#中位数计算，3*3的图片，直接取排序后的第五个像素
def media(args):
    args = sorted(args)
    mediaIdx = int(len(args)/2)
#     mediaNum = (args[mediaIdx]+args[~mediaIdx])/2
    return(args[mediaIdx])

#采用边缘像素不计算中位数，不使用padding的方法
def towDimElemMedia(ary,row,col):
    arows = len(ary)
    acols = len(ary[0])
    #边缘不计算
    if(col==0 or row==0 or col== acols or row==arows):
        return
    elems = ary[row-1:row+2,col-1:col+2].reshape(-1)
    result = media(elems)
    ary[row][col]=result
    

    
# 计算单通道的
def mediaChannelFilter(channel):
    row = len(channel)
    col = len(channel[0])
    for rIdx,row in enumerate(channel):
        for cIdx,cellValue in enumerate(row):
            towDimElemMedia(channel,rIdx,cIdx)

            
# 中位数滤镜实现
def mediaFilter(img):
    B,G,R = cv.split(img)
    mediaChannelFilter(R)
    mediaChannelFilter(G)
    mediaChannelFilter(B)
    return cv.merge((B,G,R))

if __name__ == "__main__":
    picPath = input("输入需要使用中位数滤镜的图片路径:  ")
    img = cv.imread(picPath)

    print("图片开始处理，请等待...")
    img = mediaFilter(img)

    outpath= os.path.dirname(picPath)+os.path.basename(picPath).split('.')[0]+"_GEN_MEDIAN_FILTER.jpg"
    cv.imwrite(outpath,img)
    print("处理完成, 图片的生成路径为："+outpath)