import os

path = 'D:\\project\\smallObjectAug\\SmallObjectAugmentation\\'


def writeTxt(path, backgroundOrSub):
    files = []
    folder = ''
    fileName = ''
    if backgroundOrSub == 'sub':
        folder = 'smallImg'
        fileName = 'small'
    elif backgroundOrSub == 'background':
        folder = 'background'
        fileName = 'train'

    fileList = os.listdir(path + folder + '\\')
    for file in fileList:
        if file.endswith('.png'):
            if folder == '' or fileName == '':
                print('errrrrrrr!!!!!')
            files.append(f'./{folder}/{file}\n')

    with open(f'{fileName}.txt', 'w') as f:
        f.writelines(files)


writeTxt(path, 'background')
# writeTxt(path, 'sub')


# path = './data'
# fileList = os.listdir(path)
# for file in fileList:
#     if file.endswith('.png'):
#         with open(file[:-4]+'.txt', 'w') as f:
#             f.write('0 0.0 0.0 0.0 0.0')
