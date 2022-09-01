import cv2
import os


def divide(path, fileName, outputPath):
    img = cv2.imread(path + '/' + fileName, cv2.IMREAD_UNCHANGED)
    h, w, c = img.shape
    half = int(w/2)
    img1 = img[:, 0:half]
    img2 = img[:, half:]
    cv2.imwrite(outputPath + '/1_' + fileName, img1)
    cv2.imwrite(outputPath + '/2_' + fileName, img2)


if __name__ == '__main__':
    path = '../img_output'
    outputPath = '../img_others'
    fileList = os.listdir(path)
    for fileName in fileList:
        divide(path, fileName, outputPath)
