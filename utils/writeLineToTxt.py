import os

path = './smallImg'
fileList = os.listdir(path)
files = []
for file in fileList:
    if file.endswith('.png'):
        files.append(f'./smallImg/{file}\n')

with open('small.txt', 'w') as f:
    f.writelines(files)


# path = './data'
# fileList = os.listdir(path)
# for file in fileList:
#     if file.endswith('.png'):
#         with open(file[:-4]+'.txt', 'w') as f:
#             f.write('0 0.0 0.0 0.0 0.0')
