import os
from sqlalchemy import except_all

from sympy import arg


def rename():
    path = 'smallImg'
    format = '.png'
    filelist = os.listdir(path)
    total_num = len(filelist)
    i = 0
    for item in filelist:

        if item.endswith(format):
            src = os.path.join(os.path.abspath(path), item)
            dst = os.path.join(os.path.abspath(path), '' + str(i) + format)
            print(dst)
            try:
                os.rename(src, dst)
                i += 1
            except BaseException as e:
                i += 1
    print('total %d to rename & converted %d png' % (total_num, i))


if __name__ == '__main__':
    rename()
