import cv2
import numpy as np
import json
import time

import util
import rotate_img


# img1 = cv2.imread(
#     '2022-07-24_1658639428045_J66421181_origin.jpg', cv2.IMREAD_UNCHANGED)
# img2 = cv2.imread(
#     '2022-07-31_1659245052580_00K02486056_origin.jpg', cv2.IMREAD_UNCHANGED)
# f1 = open(
#     '2022-07-24_1658639428045_J66421181_origin.txt', 'r')
# f2 = open(
#     '2022-07-31_1659245052580_00K02486056_origin.txt', 'r')


def label_subImg_info(fileName):
    # 返回(标签名，中心点，对角线一半长度, 宽度一半，高度一半)
    sub = []
    for line in fileName.readlines():
        list = line.strip().split()
        className = int(list[0])
        center = (int(1280*float(list[1])), int(1280*float(list[2])))
        w = int(float(list[3])/2*1280)
        h = int(float(list[4])/2*1280)
        r = int(np.sqrt(w*w + h*h))
        sub.append((className, center, r, w, h))
    return sub


def get_subImg(image, center, halfW, halfH):
    # 在原图中取出给定范围的子图
    # 输入参数应为int
    r = np.sqrt(halfW*halfW + halfH*halfH)
    subImg = image[int(center[1] - r):int(center[1] + r),
                   int(center[0] - r):int(center[0] + r)]
    return subImg


def insert_subImg(sourceImg, subImg, center):
    h, w, c = subImg.shape
    sourceImg[int(center[1]-h / 2):int(center[1] + h / 2),
              int(center[0] - w/2):int(center[0] + w / 2)] = subImg
    return sourceImg


def read_poly_from_json(jsonPath):
    with open(jsonPath, 'r', encoding='utf-8') as fw:
        j = json.load(fw)
    poly = []
    for obj in j['shapes']:
        points = obj['points']
        for (key, point) in enumerate(points):
            newP = (point[0], point[1])
            points[key] = newP

        poly.append(points)
    return poly


def binaryImg(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    start = time.time()
    x, thr = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    end = time.time()
    cv2.imshow('threshold', thr)
    print(thr.shape)
    print(f'time: {end - start}')
    cv2.waitKey(0)


p = 'D:\\img\\1.png'
binaryImg(p)

# print(read_poly_from_json())
# ===================================================
# infoList1 = label_subImg_info(f1)
# infoList2 = label_subImg_info(f2)

# for item in infoList1:

#     sub = get_subImg(img1, item[1], item[3], item[4])
#     h, w, c = sub.shape

#     # for i in range(36):
#     #     deg = (i+1)*10
#     deg = 45
#     rotated = rotate_img.rotated_small_image(
#         sub, (w/2, h/2), deg, infoList2[0][3] * 2, infoList2[0][4] * 2)
#     img1 = insert_subImg(img1, rotated, item[1])
# cv2.imwrite(f'{item[1]}_rotated_{deg}.jpg', img1)
# ===================================================


# cv2.imwrite('hah.jpg', insert_subImg(img1, x, (500, 500)))


# for line in f2.readlines():
#     list = line.strip().split()
#     if

# 然后random一个点坐标，取一个class1的点对每个class2点求距离，如果安全并且不超过img边界
# 则将该点的图代替class2中的图，并将该点放入class2 的list里
