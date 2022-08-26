import cv2
import numpy as np
# image = cv2.imread('2022-07-24_1658639428045_J66421181_origin.jpg')
# rotateM = cv2.getRotationMatrix2D(center=(900, 550), angle=-30, scale=1)
# rotatedImage = cv2.warpAffine(image, rotateM, (image.shape[1], image.shape[0]))
# cv2.imwrite('image.jpg', image)
# cv2.imwrite('center.jpg', rotatedImage)


def rotated_small_image(image, box_center, angle, w, h):
    r = np.sqrt(w*w + h*h)
    center = (float(box_center[0]), float(box_center[1]))
    rotateM = cv2.getRotationMatrix2D(center, angle, 1)
    rotatedImage = cv2.warpAffine(
        image, rotateM, (image.shape[1], image.shape[0]))
    # small = rotatedImage[int(center[1] - r):int(center[1] + r),
    #                      int(center[0] - r):int(center[0] + r)]
    # rotatedImage = cv2.resize(
    #     rotatedImage, (int(image.shape[1]*0.6), int(image.shape[0]*0.6)))
    return rotatedImage


# ro = rotated_small_image(image, (550, 500), 45, 1280, 1280)
# cv2.imshow('x', ro)
# cv2.waitKey(0)
