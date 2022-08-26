import imageio
import imgaug as ia
from imgaug import augmenters as iaa
import os
from imgaug.augmentables.polys import Polygon, PolygonsOnImage
import numpy as np
import json
import cv2
import base64


def output_json(psoi_aug, fileName, imgdata):
    shapes = []
    for key, p in enumerate(psoi_aug):
        points = {}
        points['points'] = p.exterior.tolist()
        points['label'] = p.label
        points['group_id'] = None
        points['shape_type'] = 'polygon'
        points['flags'] = {}
        # print(points)
        # print(p.exterior)
        shapes.append(points)
        for p in points['points']:
            if p[0] < 0 or p[0] > 2730 or p[1] < 0 or p[1] > 3000:
                return None
    outputJsonVal = {}
    outputJsonVal['shapes'] = shapes
    outputJsonVal['version'] = "4.6.0"
    outputJsonVal['flags'] = {}
    outputJsonVal['imageHeight'] = 3000
    outputJsonVal['imageWidth'] = 2730
    outputJsonVal['imagePath'] = fileName
    outputJsonVal['imageData'] = imgdata

    # print(outputJsonVal)
    return outputJsonVal


def read_poly_from_json(jsonPath):
    with open(jsonPath, 'r', encoding='utf-8') as fw:
        j = json.load(fw)
    polys = []
    labelList = []
    for obj in j['shapes']:
        poly = []
        points = obj['points']
        label = obj['label']
        labelList.append(label)
        for point in points:
            newP = (point[0], point[1])
            poly.append(newP)
        polys.append(poly)
    return polys, labelList


def aug(imagePath, jsonPath, fileNum):
    # 读图和label
    image = imageio.imread(imagePath)
    polys, labelList = read_poly_from_json(jsonPath)

    # 生成需要的多边形对象
    PolygonList = []
    for key, p in enumerate(polys):
        PolygonList.append(Polygon(p, labelList[key]))
    psoi = ia.PolygonsOnImage(PolygonList, shape=image.shape)

    # 添加增强方法
    aug = iaa.Sequential([
        iaa.Flipud(1.0)
    ])
    # 将增强方法作用到原图和原多边形label上
    image_aug, psoi_aug = aug(image=image, polygons=psoi)

    _, imgEncode = cv2.imencode('.png', image_aug)
    imgdata: str = str(base64.b64encode(imgEncode))[2:-1]
    jsonObj = output_json(psoi_aug, f'data_out/{fileNum}_Flipud.png', imgdata)
    if jsonObj:
        with open(f'data_out/{fileNum}_Flipud.json', "w") as f:
            json.dump(jsonObj, f)
    # ia.imshow(psoi_aug.draw_on_image(image_aug, alpha_face=0.2, size_points=7))
    # save
    # imageio.imwrite(f'data_out/{fileNum}_Flipud.png', image_aug)

    aug = iaa.Sequential([
        iaa.Fliplr(1.0)
    ])
    image_aug, psoi_aug = aug(image=image, polygons=psoi)
    # print(image_aug.shape)
    _, imgEncode = cv2.imencode('.png', image_aug)
    imgdata: str = str(base64.b64encode(imgEncode))[2:-1]
    jsonObj = output_json(psoi_aug, f'data_out/{fileNum}_Fliplr.png', imgdata)
    if jsonObj:
        with open(f'data_out/{fileNum}_Fliplr.json', "w") as f:
            json.dump(jsonObj, f)
    # ia.imshow(psoi_aug.draw_on_image(image_aug, alpha_face=0.2, size_points=7))
    # save
    # imageio.imwrite(f'data_out/{fileNum}_Fliplr.png', image_aug)

    for i in range(4):
        aug = iaa.Sequential([
            iaa.Affine(rotate=(-35, 35))
        ])
        image_aug, psoi_aug = aug(image=image, polygons=psoi)

        _, imgEncode = cv2.imencode('.png', image_aug)
        imgdata: str = str(base64.b64encode(imgEncode))[2:-1]
        jsonObj = output_json(
            psoi_aug, f'data_out/{fileNum}_rotate{i}.png', imgdata)
        if jsonObj:
            with open(f'data_out/{fileNum}_rotate{i}.json', "w") as f:
                json.dump(jsonObj, f)
        # ia.imshow(psoi_aug.draw_on_image(
        #     image_aug, alpha_face=0.2, size_points=7))
        # save
        # imageio.imwrite(f'data_out/{fileNum}_rotate{i}.png', image_aug)

    for i in range(3):
        aug = iaa.Sequential([
            iaa.ScaleY((0.8, 1.2))
        ])
        image_aug, psoi_aug = aug(image=image, polygons=psoi)

        _, imgEncode = cv2.imencode('.png', image_aug)
        imgdata: str = str(base64.b64encode(imgEncode))[2:-1]

        jsonObj = output_json(
            psoi_aug, f'data_out/{fileNum}_ScaleY{i}.png', imgdata)
        if jsonObj:
            with open(f'data_out/{fileNum}_ScaleY{i}.json', "w") as f:
                json.dump(jsonObj, f)
        # ia.imshow(psoi_aug.draw_on_image(
        #     image_aug, alpha_face=0.2, size_points=7))
        # save
        # imageio.imwrite(f'data_out/{fileNum}_ScaleY{i}.png', image_aug)

    for i in range(3):
        aug = iaa.Sequential([
            iaa.ScaleX((0.8, 1.2))
        ])
        image_aug, psoi_aug = aug(image=image, polygons=psoi)
        _, imgEncode = cv2.imencode('.png', image_aug)
        imgdata: str = str(base64.b64encode(imgEncode))[2:-1]
        jsonObj = output_json(
            psoi_aug, f'data_out/{fileNum}_ScaleX{i}.png', imgdata)
        if jsonObj:
            with open(f'data_out/{fileNum}_ScaleX{i}.json', "w") as f:
                json.dump(jsonObj, f)
        # ia.imshow(psoi_aug.draw_on_image(
        #     image_aug, alpha_face=0.2, size_points=7))
        # save
        # imageio.imwrite(f'data_out/{fileNum}_ScaleX{i}.png', image_aug)


if __name__ == '__main__':

    # aug(f'data\\16612608596399.png', f'data/16612608596399.json')

    i = 1
    fileList = os.listdir('./data')
    for file in fileList:
        if file.endswith('png'):
            aug(f'data\\{file}', f'data/{file[:-4]}.json', i)
            # print(i)
            i += 1
