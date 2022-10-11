import os
import random
import shutil


# 随机拷贝指定文件夹内的文件到其他文件夹。

# 如果文件夹内的文件数量少于设置的拷贝文件数量，取80%
# 如果目的文件夹不存在，会新建文件夹。
# 只会拷贝文件，不会拷贝子文件夹。

def newDir(fileDir):
    fileDir = fileDir.strip()
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)
    else:
        print(fileDir+'already exists!!!')



def randomCopyFile(sourDir, dstDir, num):
    pathDir = os.listdir(sourDir)
    newDir(dstDir)
    if len(pathDir) < num:
        num = int(len(pathDir) * 0.8)
    samples = random.sample(pathDir, num)
    for sample in samples:
        print(sample)
        if os.path.isfile(os.path.join(sourDir, sample)):
            shutil.copy(sourDir+sample, dstDir+sample)


if __name__ == '__main__':
    source = "../../wood/images/C花纹/"
    dst = "../../wood/train/flower/"
    num = 500
    randomCopyFile(source, dst, num)
