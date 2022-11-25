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
        print(fileDir+'created')
        os.makedirs(fileDir)
    else:
        print(fileDir+'already exists!!!')


def randomCopyFile(sourDir, dstDir, ifTest, num, className):
    pathDir = os.listdir(sourDir + className + '\\')
    trainPath = dstDir + 'train\\' +  className + '\\'
    testPath = dstDir + "test\\" + className + '\\' 
    newDir(trainPath)
    if len(pathDir) < num:
        num = int(len(pathDir) * 0.8)
    samples = random.sample(pathDir, num)
    
    for sample in samples:
        if os.path.isfile(os.path.join(sourDir + className + '\\', sample)):
            shutil.copy(sourDir + className + '\\' + sample, trainPath + sample)
    if ifTest:
        newDir(testPath)
        samples = set(samples)
        pathDir = set(pathDir)
        remain = pathDir - samples
        for r in remain:
            if os.path.isfile(os.path.join(sourDir + className + '\\', r)):
                shutil.copy(sourDir + className + '\\' + r, testPath + r)


if __name__ == '__main__':
    # source = "F:\\image\\meat\\full_data\\纯瘦肉肉末（带颗粒）\\"
    # dst = "E:\\project\\meat\\source\\"
    source = "E:\\project\\meat\\test\\"
    dst = "E:\\project\\meat\\train\\"
    # num = 600
    # randomCopyFile(source, dst, True, num)
    # source = "F:\\image\\meat\\1026dajiang\\"
    # dst = "E:\\project\\meat\\source\\"
    
    for folder in os.listdir(source):
        num = 230
        randomCopyFile(source, dst, True, num, folder)
