import cv2

def clahe(img):
    '''
    直方图均衡
    '''
    clahe = cv2.createCLAHE(3, (8, 8))
    dst = clahe.apply(img)

    return dst


p =  "F:\\image\\test\\test1.jpg"
path = "F:\\image\\test\\"
img = cv2.imread(p,0)
cv2.imwrite(path + "gray.jpg", img)
dst = clahe(img)
cv2.imwrite(path + "test.jpg",dst)
