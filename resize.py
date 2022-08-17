import cv2
import os


def resize(path, outputPath, xR, yR, fileName):
    img = cv2.imread(path + '/' + fileName, 2)
    imgShape = img.shape
    newH = int(imgShape[0]*xR)
    newW = int(imgShape[1]*yR)
    newImg = cv2.resize(img, (newW, newH))
    cv2.imwrite(outputPath + '/new' + fileName, newImg)


if __name__ == '__main__':
    path = 'img'
    outputPath = 'img_output'
    # 在xy轴上的系数
    xR = 0.5
    yR = 0.5
    fileList = os.listdir(path)
    for fileName in fileList:
        resize(path, outputPath, xR, yR, fileName)
