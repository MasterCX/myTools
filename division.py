import cv2


def divide(img, numX, numY):
    w, h, c = img.shape
    


if __name__ == '__main__':
    img = cv2.imread('img/Image_20220815104036839.jpg', cv2.IMREAD_UNCHANGED)
    divide(img, 4, 3)
