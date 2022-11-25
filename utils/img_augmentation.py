from fileinput import filename
import cv2 as cv
import os
import random
from PIL import Image
import numpy as np

from scipy import rand
from change_val import aug


def change_labels(fileName, labelPath, labelOutputPath):
    # open labels
    sourceImgName = fileName[7:-4] + '.txt'
    flipDirection = fileName[5]
    if flipDirection == 'y':
        with open(labelPath + '/' + sourceImgName, 'r', encoding='utf-8') as f:
            for line in f:
                # delete \n and turn it to array by ' ', take second value which is X
                line = line.strip('\n')
                if (len(line) != 0):
                    x = float(line.split()[1])
                    newLine = line.split()
                    newLine[1] = str(round(1-x, 6))
                    newLine = ' '.join(newLine)
                    newLine = newLine + '\n'
                    print(newLine)
                    with open(labelOutputPath + '/flip_y_' + sourceImgName, 'a', encoding='utf-8') as newFile:
                        newFile.writelines(newLine)
    elif flipDirection == 'x':
        with open(labelPath + '/' + sourceImgName, 'r', encoding='utf-8') as f:
            for line in f:
                # delete \n and turn it to array by ' ', take second value which is X
                line = line.strip('\n')
                if (len(line) != 0):
                    y = float(line.split()[2])
                    newLine = line.split()
                    newLine[2] = str(round(1-y, 6))
                    newLine = ' '.join(newLine)
                    newLine = newLine + '\n'
                    print(newLine)
                    with open(labelOutputPath + '/flip_x_' + sourceImgName, 'a', encoding='utf-8') as newFile:
                        newFile.writelines(newLine)
    else:
        print('input file name err!!!')

def newDir(fileDir):
    fileDir = fileDir.strip()
    if not os.path.exists(fileDir):
        print(fileDir+'created')
        os.makedirs(fileDir)
    else:
        print(fileDir+'already exists!!!')


def augmentation(path, outputPath, file, possibility):
    if file.endswith(format):
        img = Image.open(path + file)
        # img = cv.cvtColor(np.asarray(img),cv.COLOR_RGB2BGR)
        if randomDo(possibility):
            aug(path + file, '', 1, file, outputPath)

        # if randomDo(possibility):
        #     # flip y:
        #     img_flip_y = cv.flip(img, 1)
        #     cv.imencode('.jpg', img_flip_y)[1].tofile(outputPath + 'flip_y_' + file)
        #     # cv.imwrite(outputPath + 'flip_y_' + file, img_flip_y)

        # if randomDo(possibility):
        #     # flip x:
        #     img_flip_x = cv.flip(img, 0)
        #     cv.imencode('.jpg', img_flip_x)[1].tofile(outputPath + 'flip_x_' + file)
        #     # cv.imwrite(outputPath + 'flip_x_' + file, img_flip_x)
        
        # if randomDo(possibility/2):
        #     img_flip_y = cv.flip(img, 1)
        #     img_flip_xy = cv.flip(img_flip_y, 0)
        #     cv.imencode('.jpg', img_flip_xy)[1].tofile(outputPath + 'flip_xy_' + file)
        #     # cv.imwrite(outputPath + 'flip_xy_' + file, img_flip_xy)


    else:
        print(f'this file does not end with format {format}')


def randomDo(possibilities):
    randomNum = random.random()
    if randomNum <= possibilities:
        return True
    else: return False

if __name__ == '__main__':
    # 对图像进行翻转
    inputPath = 'E:\\project\\meat\\test\\'
    format = '.jpg'
    fileList = os.listdir(inputPath)
    maxNum = 230
    for objClass in fileList:
        outputPath = inputPath + objClass + '\\'
        newDir(outputPath)
        trainImg = inputPath + objClass + '\\'
        imgs = os.listdir(trainImg)
        print(f'this is {objClass}, {len(imgs)} in total')
        if len(imgs) < 0.25*maxNum:
            for img in os.listdir(trainImg):
                augmentation(trainImg, outputPath, img, 0.5)
        
        elif len(imgs) < 0.5*maxNum:
            for img in os.listdir(trainImg):
                augmentation(trainImg, outputPath, img, 0.25)

        elif len(imgs) < 0.75*maxNum:
            for img in os.listdir(trainImg):
                augmentation(trainImg, outputPath, img, 0.15)

        elif len(imgs) < maxNum:
            for img in os.listdir(trainImg):
                augmentation(trainImg, outputPath, img, 0.075)
        else:
            for img in os.listdir(trainImg):
                augmentation(trainImg, outputPath, img, 0.005)
       

    # imgList = os.listdir(imgOutputPath)
    # labelPath = 'labels'
    # labelOutputPath = 'labels_output'
    # for img in imgList:
    #     change_labels(img, labelPath, labelOutputPath)
