from fileinput import filename
import cv2 as cv
import os


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


def augmentation(path, outputPath, file):
    if file.endswith(format):
        img = cv.imread(path + '/' + file, cv.IMREAD_UNCHANGED)
        # flip y:
        img_flip_y = cv.flip(img, 1)
        cv.imwrite(outputPath + '/flip_y_' + file, img_flip_y)

        # flip x:
        img_flip_x = cv.flip(img, 0)
        cv.imwrite(outputPath + '/flip_x_' + file, img_flip_x)

    else:
        print(f'this file does not end with format {format}')


if __name__ == '__main__':
    imgPath = 'img'
    format = '.jpg'
    imgOutputPath = 'img_output'
    fileList = os.listdir(imgPath)
    for file in fileList:
        augmentation(imgPath, imgOutputPath, file)
    # imgList = os.listdir(imgOutputPath)
    # labelPath = 'labels'
    # labelOutputPath = 'labels_output'
    # for img in imgList:
    #     change_labels(img, labelPath, labelOutputPath)
