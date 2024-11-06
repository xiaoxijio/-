import cv2
import matplotlib.pyplot as plt
import numpy as np


def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def sort_contours(cnts, method):
    reverse = False
    i = 0

    if method == 'right-to-left' or method == 'bottom-to-top':
        reverse = True

    if method == 'top-to-bottom' or method == 'bottom-to-top':
        i = 1

    boundingBoxes = [cv2.boundingRect(c) for c in cnts]  # 外接矩阵
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b: b[1][i], reverse=reverse))  # 打包排序

    return cnts, boundingBoxes


def resize_img(image, new_width):
    height, width = image.shape[:2]

    ratio = new_width / width
    new_height = int(height * ratio)

    resize_img = cv2.resize(image, (new_width, new_height))
    return resize_img


img = cv2.imread('img/ocr_a_reference.png')  # 读取模版
# cv_show('img', img)
ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转灰度图
# cv_show('ref', ref)
# 转二值图 (所有低于 10 的像素会被处理成白色，高于 10 的像素会被处理成黑色)
ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]
# cv_show('ref', ref)
# 轮廓检测 (RETR_EXTERNAL:只检测外轮廓 CHAIN_APPROX_SIMPLE:只保留终点坐标)  注意:findContours()只接受二值图(黑白,非灰度图)
refCnts, _ = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, refCnts, -1, (0, 0, 255), 3)

# cv_show('template', img)


refCnts = sort_contours(refCnts, method='left-to-right')[0]  # 对轮廓排序
digits = {}

for (i, c) in enumerate(refCnts):
    (x, y, w, h) = cv2.boundingRect(c)
    roi = ref[y:y + h, x:x + w]
    roi = cv2.resize(roi, (57, 88))
    digits[i] = roi

rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))  # 因为图片内容复杂，需要排除干扰项，卷积它！
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 初始化卷积核

image = cv2.imread('img/credit_card_01.png')
# cv_show('image', image)
image = resize_img(image, 300)  # 缩小
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 灰度图
# cv_show('gray', gray)

# 开运算 = 腐蚀 -> 膨胀  (去除比结构核小的噪声点, 因此较小的亮点会被削弱或去除, 比如信用卡上的数字)
# 礼帽 = 原始 - 开运算  (滤除图像中的大区域背景, 只保留局部的亮度突出的结构)
# opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, rectKernel)
# cv_show('opening', opening)
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)  # 礼帽(突出图像中比背景亮的小区域)
# cv_show('tophat', tophat)
gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
gradX = cv2.convertScaleAbs(gradX)
# gradY = cv2.Sobel(tophat, cv2.CV_32F, 0, 1, ksize=-1)
# gradY = cv2.convertScaleAbs(gradY)
# gradXY = cv2.addWeighted(gradX, 0.5, gradY, 0.5, 0)
(minVal, maxVal) = (np.min(gradX), np.max(gradX))  # 归一化图像
gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))  # 将所有梯度值拉伸到 0-255 的范围
gradXY = gradX.astype('uint8')
# cv_show('gradXY', gradXY)

gradXY = cv2.morphologyEx(gradXY, cv2.MORPH_CLOSE, rectKernel)  # 闭运算 = 膨胀->腐蚀 (将数字糊在一块)
# cv_show('gradXY', gradXY)
thresh = cv2.threshold(gradXY, 160, 255, cv2.THRESH_BINARY)[1]
# thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
# cv_show('thresh', thresh)

threshCnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cur_img = image.copy()
cv2.drawContours(cur_img, threshCnts, -1, (0, 0, 255), 2)
# cv_show('cur_img', cur_img)

locs = []
for (i, c) in enumerate(threshCnts):
    (x, y, w, h) = cv2.boundingRect(c)
    # aaa = image.copy()
    # cv2.rectangle(aaa, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv_show('aaa', aaa)
    ar = w / float(h)

    if 2.5 < ar < 3.4:
        if 47 < w < 54 and 15 < h < 21:
            locs.append((x, y, w, h))

locs = sorted(locs, key=lambda x: x[0])
output = []

for (i, (gx, gy, gw, gh)) in enumerate(locs):
    groupOutput = []
    group = gray[gy - 3:gy + gh + 3, gx - 3:gx + gw + 3]  # 扩点 防止贴着数字
    # cv_show('group', group)

    group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv_show('group', group)
    digitCnts, _ = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    digitCnts = sort_contours(digitCnts, method='left-to-right')[0]

    for c in digitCnts:
        (x, y, w, h) = cv2.boundingRect(c)
        roi = group[y:y + h, x:x + w]
        roi = cv2.resize(roi, (57, 88))
        # cv_show('roi', roi)

        scores = []
        for (digit, digitROI) in digits.items():
            result = cv2.matchTemplate(roi, digitROI, cv2.TM_CCOEFF)
            (_, score, _, _) = cv2.minMaxLoc(result)
            scores.append(score)

        groupOutput.append(str(np.argmax(scores)))

    # print(groupOutput)
    cv2.rectangle(image, (gx - 5, gy - 5), (gx + gw + 5, gy + gh + 5), (0, 0, 255), 1)
    cv2.putText(image, ''.join(groupOutput), (gx, gy - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
    output.extend(groupOutput)

print(output)
cv_show('image', image)
