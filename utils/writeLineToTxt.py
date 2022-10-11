import os

path = 'D:\\project\\smallObjectAug\\SmallObjectAugmentation\\background\\'
fileList = os.listdir(path)
files = []
for file in fileList:
    if file.endswith('.png'):
        files.append(f'./background/{file}\n')

with open('train.txt', 'w') as f:
    f.writelines(files)


# path = './data'
# fileList = os.listdir(path)
# for file in fileList:
#     if file.endswith('.png'):
#         with open(file[:-4]+'.txt', 'w') as f:
#             f.write('0 0.0 0.0 0.0 0.0')
