import cv2 as cv
import numpy as np
import os

class Stitcher:
    def __init__(self):
        pass

    def detectAndDesc(self, img):
        # 转成灰度图
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        sift = cv.xfeatures2d.SIFT_create()
        # 使用SIFT算法获取特征点及特征描述
        (kps, desc) = sift.detectAndCompute(img, None)
        return (kps, desc)

    # 鲁棒算法使用 ransac, ransacReprojThreshold ransac ransac外点阀值 ration 匹配点的距离
    def match(self, kp1, desc1, kp2, desc2, ratio=0.75, ransacReprojThreshold=4.0):
        # 使用BruteForce进行匹配
        bf = cv.BFMatcher()
        matchers = bf.knnMatch(desc1, desc2,k=2)
        good = []
        for m in matchers:
            if len(m) == 2 and m[0].distance < ratio * m[1].distance:
                good.append((m[0].trainIdx, m[0].queryIdx))

        # 需要最少找到四个匹配点，从而找到单应矩阵，转到同一个坐标系后再进行拼接,少于四个点显然这图片是不能拼接成功的
        print(len(good))
        if (len(good) < 4):
            return None
        # 获取关键点的坐标
        srcPts = np.float32([kp1[i].pt for (_, i) in good])
        destPts = np.float32([kp2[i].pt for (i, _) in good])
        # 通过ransac算法
        (M, mask) = cv.findHomography(srcPts, destPts, cv.RANSAC, ransacReprojThreshold)
        return (good, M, mask)

    def stitch(self, imgpaths):
        (img1, img2) = (cv.imread(i) for i in imgpaths)
        (kp1, desc1) = self.detectAndDesc(img1)
        (kp2, desc2) = self.detectAndDesc(img2)
        print("找到的关键点数量:img1", str(len(kp1)), ",img2", str(len(kp2)))
        R = self.match(kp1, desc1, kp2, desc2)
        if R == None:
            print("没有找到匹配的特征点！")
            return None
        (good, M, mask) = R
        print(M)
        # 获取图片1到图片2的投影
        result = cv.warpPerspective(img1, M, (img1.shape[1] + img2.shape[1], img1.shape[0]))
        # 将图片2拼接到图片1上
        result[0:img2.shape[0], 0:img2.shape[1]] = img2
        return result

    # 这里是直接使用opencv的stitch类。。
    def stitch2(self,imgs):
        st = cv.createStitcher(False)
        img1 = cv.imread(imgs[0])
        img2 = cv.imread(imgs[1])
        (_result, pano) =st.stitch((img1,img2))
        return pano

if __name__ == "__main__":
    stitcher = Stitcher()
    img1path = input("注意!!该程序中没有分辨图片的位置!!!\n只实现了简单拼接功能,也没有进行很好的裁剪\n请输入 左边 图片的路径:")
    img2path = input("请输入 右边 图片的路径:")
    res = stitcher.stitch([img1path, img2path])
    # res = stitcher.stitch2([img1path,img2path])
    path = os.path.dirname(img1path)+"/"+os.path.basename(img1path).split(".")[0]+os.path.basename(img2path).split(".")[0]+".jpg"
    cv.imwrite(path,res)
    print("图片拼接完成，路径为："+path)
