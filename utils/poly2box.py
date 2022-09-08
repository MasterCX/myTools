import numpy as np
import PIL.Image
import PIL.ImageDraw
import cv2
import json
import os


def getbbox(points, height, width):
    # img = np.zeros([self.height,self.width],np.uint8)
    # cv2.polylines(img, [np.asarray(points)], True, 1, lineType=cv2.LINE_AA)  # 画边界线
    # cv2.fillPoly(img, [np.asarray(points)], 1)  # 画多边形 内部像素值为1
    polygons = points
    mask = polygons_to_mask([height, width], polygons)
    return mask2box(mask)


def mask2box(mask):
    '''从mask反算出其边框
    mask：[h,w]  0、1组成的图片
    1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
    '''
    # np.where(mask==1)
    index = np.argwhere(mask == 1)
    rows = index[:, 0]
    clos = index[:, 1]
    # 解析左上角行列号
    left_top_r = np.min(rows)  # y
    left_top_c = np.min(clos)  # x

    # 解析右下角行列号
    right_bottom_r = np.max(rows)
    right_bottom_c = np.max(clos)

    # return [(left_top_r,left_top_c),(right_bottom_r,right_bottom_c)]
    # return [(left_top_c, left_top_r), (right_bottom_c, right_bottom_r)]
    # return [left_top_c, left_top_r, right_bottom_c, right_bottom_r]  # [x1,y1,x2,y2]
    return [left_top_c, left_top_r, right_bottom_c - left_top_c,
            right_bottom_r - left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式


def polygons_to_mask(img_shape, polygons):
    mask = np.zeros(img_shape, dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    xy = list(map(tuple, polygons))
    PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)
    return mask


def read_poly_from_json(jsonPath):
    with open(jsonPath, 'r', encoding='utf-8') as fw:
        j = json.load(fw)
        polys = []
        for obj in j['shapes']:
            poly = []
            label = obj['label']
            points = obj['points']
            for point in points:
                newP = (point[0], point[1])
                poly.append(newP)
            poly = np.array(poly)
            polys.append([poly, label])
    return polys


# jsonPath = './data/4_val.json'
# imgPath = './data/4_val.png'
# img = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
# hieght, width, c = img.shape
# polys = read_poly_from_json(jsonPath)
# for key, p in enumerate(polys):
#     x, y, w, h = getbbox(p, hieght, width)
#     cv2.imwrite(f'{key}.png', img[y-1:y+h+2, x-1:x+w+2])


def img_to_subImg_with_json(filePath):
    for file in os.listdir(filePath):
        if file.endswith('.png'):
            img = cv2.imread(filePath + file, cv2.IMREAD_UNCHANGED)
            height, width, c = img.shape
            polys = read_poly_from_json(filePath + file[:-4] + '.json')

            for key, p in enumerate(polys):
                x, y, w, h = getbbox(p[0], height, width)
                if w <= 5 or h <= 5:
                    continue
                points = p[0] - np.array([x-1, y-1])
                points = points.tolist()
                jsonObj = {}
                jsonObj['points'] = points
                jsonObj['label'] = p[1]
                cv2.imwrite(f'{file[:-4]}_{key}.png',
                            img[y-1:y+h+1, x-1:x+w+1])
                with open(f'{file[:-4]}_{key}.json', 'w') as f:
                    json.dump(jsonObj, f)


def imgJson_to_yoloTxt(filePath):
    for file in os.listdir(filePath):
        if file.endswith('.png'):
            img = cv2.imread(filePath + file, cv2.IMREAD_UNCHANGED)
            height, width, c = img.shape
            polys = read_poly_from_json(filePath + file[:-4] + '.json')
            writeLines = []
            for key, p in enumerate(polys):
                x, y, w, h = getbbox(p[0], height, width)
                if w <= 5 or h <= 5:
                    continue
                # 这里不需要label 所以可以先写死占位
                writeLine = f'0 {(x + w/2)/width} {(y + h/2)/height} {w/width} {h/height}\n'
                writeLines.append(writeLine)
                # points = p[0] - np.array([x-1, y-1])
                # points = points.tolist()
                # jsonObj = {}
                # jsonObj['points'] = points
                # jsonObj['label'] = p[1]
                # cv2.imwrite(f'{file[:-4]}_{key}.png',
                #             img[y-1:y+h+1, x-1:x+w+1])
            if writeLines:
                with open(f'{file[:-4]}.txt', 'w') as f:
                    f.writelines(writeLines)
            else:
                with open(f'{file[:-4]}.txt', 'w') as f:
                    f.writelines('0 0 0 0 0')


filePath = './data/'
img_to_subImg_with_json(filePath)
# imgJson_to_yoloTxt(filePath)
