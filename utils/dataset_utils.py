# -*- coding: utf-8 -*-
import sys,time
import cv2
import numpy as np
import copy
import json
import base64
import os,glob,shutil
from math import cos, sin, pi, fabs, radians
import sense.my_logger as my_logger

logger=my_logger.MyLogger()

# 增加labelme数据标注工具

# 读取json
def readJson(jsonfile):
    with open(jsonfile,"r", encoding='utf-8') as f:
        jsonData = json.load(f)
    return jsonData


# 保存json
def writeToJson(filePath, data):
    with open(filePath,"w", encoding='utf-8') as f:
        json.dump(data,f, indent=2,ensure_ascii=False)


def rotate_bound(image, angle):
    """
    旋转图像
    :param image: 图像
    :param angle: 角度
    :return: 旋转后的图像
    """
    h, w, _ = image.shape
    # print(image.shape)
    (cX, cY) = (w // 2, h // 2)
    print(cX, cY)

    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # print(nW,nH)
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    # print( M[0, 2], M[1, 2])
    image_rotate = cv2.warpAffine(image, M, (nW, nH), borderValue=(255, 255, 255))
    return image_rotate, cX, cY, angle


def rotate_xy(x, y, angle, cx, cy):
    """
    点(x,y) 绕(cx,cy)点旋转
    """
    # print(cx,cy)
    angle = angle * pi / 180
    x_new = (x - cx) * cos(angle) - (y - cy) * sin(angle) + cx
    y_new = (x - cx) * sin(angle) + (y - cy) * cos(angle) + cy
    return x_new, y_new


# 转base64
def image_to_base64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code


def dumpRotateImage(img, degree):
    height, width = img.shape[:2]
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))
    matRotation = cv2.getRotationMatrix2D((width // 2, height // 2), degree, 1)
    matRotation[0, 2] += (widthNew - width) // 2
    matRotation[1, 2] += (heightNew - height) // 2
    # print(width // 2, height // 2)
    imgRotation = cv2.warpAffine(img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))
    return imgRotation, matRotation


# 坐标旋转
def rotatePoint(img_rotate, origin_json, M, imagePath):
    json_dict = {}
    for key, value in copy.deepcopy(origin_json).items():
        if key == 'imageHeight':
            json_dict[key] = img_rotate.shape[0]
        elif key == 'imageWidth':
            json_dict[key] = img_rotate.shape[1]
        elif key == 'imageData':
            json_dict[key] = image_to_base64(img_rotate)
        elif key == 'imagePath':
            json_dict[key] = imagePath
        else:
            json_dict[key] = value
    for item in json_dict['shapes']:
        for key, value in item.items():
            if key == 'points':
                for item2 in range(len(value)):
                    pt1 = np.dot(M, np.array([[value[item2][0]], [value[item2][1]], [1]]))
                    value[item2][0], value[item2][1] = pt1[0][0], pt1[1][0]
    return json_dict


# 坐标翻转  direction沿哪个轴反转
def flipPoint(img_flip, origin_json, direction, imagePath):
    json_dict = {}
    height = img_flip.shape[0]
    width = img_flip.shape[1]
    # print(height, width)
    for key, value in copy.deepcopy(origin_json).items():
        if key == 'imageHeight':
            json_dict[key] = value
        elif key == 'imageWidth':
            json_dict[key] = value
        elif key == 'imageData':
            json_dict[key] = image_to_base64(img_flip)
        elif key == 'imagePath':
            json_dict[key] = imagePath
        else:
            json_dict[key] = value
    for item in json_dict['shapes']:
        for key, value in item.items():
            if key == 'points':
                for item2 in value:
                    if direction == 'x':
                        item2[1] = height - item2[1]
                        item2[0] = item2[0]
                    else:
                        item2[1] = item2[1]
                        item2[0] = width - item2[0]
    return json_dict


# 旋转
def rotate(origin_img, origin_json, img_name, degree,output_img_path,output_json_path):
    img_rotate, M = dumpRotateImage(origin_img, degree)
    img_name = str(degree) + '-' + img_name
    jsonData_rotate = rotatePoint(img_rotate, origin_json, M, img_name + ".jpg")
    
    cv2.imwrite(os.path.join(output_img_path,img_name+".jpg"), img_rotate)
    writeToJson(os.path.join(output_json_path,img_name+".json"), jsonData_rotate)


# 反转
def flip(origin_img, origin_json, img_name, direction,output_img_path,output_json_path):
    flipCode = 1
    if direction == 'x':
        flipCode = 0
    img_flip = cv2.flip(origin_img, flipCode)
    img_name = direction + '-' + img_name
    jsonData_flip = flipPoint(img_flip, origin_json, direction, img_name + ".jpg")

    cv2.imwrite(os.path.join(output_img_path,img_name+".jpg"), img_flip)
    writeToJson(os.path.join(output_json_path,img_name+".json"), jsonData_flip)

def add_dataset(input_img_path,input_json_path,train_data_path):
    # 路径
    output_img_path = train_data_path
    output_json_path = output_img_path

    os.makedirs(output_img_path,exist_ok=True)
    os.makedirs(output_json_path,exist_ok=True)

    # filenames = os.listdir(input_json_path)
    # 所有文件
    all_filenames = glob.glob(os.path.join(input_json_path,"*.json"))
    # 之前已经扩展的文件
    expand_filenames = glob.glob(os.path.join(input_json_path,"*-*.json"))
    # 原始文件
    filenames=list(set(all_filenames).difference(set(expand_filenames)))
    origin_count=0
    add_count=0
    
    start_time=time.time()
    for filename in filenames:
        
        imageName = filename[filename.rfind("/")+1:filename.rfind(".")]
        print(filename)
        origin_img_path=os.path.join(input_img_path ,imageName + ".jpg")
        
        if not os.path.exists(origin_img_path):
            print(origin_img_path," - img not exists")
            continue
        # 原始图片
        origin_img = cv2.imread(origin_img_path)
        print(os.path.join(input_img_path ,imageName + ".jpg"))
        # 原始json
        origin_json = readJson(os.path.join(input_json_path , imageName + '.json'))
        cv2.imwrite(os.path.join(output_img_path , imageName + ".jpg"), origin_img)
        writeToJson(os.path.join(output_json_path , imageName + ".json"), origin_json)
        # 旋转图片
        rotate(origin_img, origin_json, imageName, 270,output_img_path,output_json_path)
        rotate(origin_img, origin_json, imageName, 90,output_img_path,output_json_path)
        rotate(origin_img, origin_json, imageName, 180,output_img_path,output_json_path)
        # x轴翻转
        flip(origin_img, origin_json, imageName, 'x',output_img_path,output_json_path)
        # y轴翻转
        flip(origin_img, origin_json, imageName, 'y',output_img_path,output_json_path)
        origin_count+=1
        add_count+=5
    logger.info('train: expand dataset, origin count: {},expand count: {},expand time: {} s'.format(origin_count,add_count,1000*(time.time()-start_time)))
    if origin_count==0:
        logger.info('train data not exist! please check path')
        exit(0)


if __name__ == '__main__':
    add_dataset("data/train/box/img","data/train/box/json")
    sys.exit(0)
