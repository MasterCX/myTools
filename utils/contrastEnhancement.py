import imageio
import imgaug as ia
import imgaug.augmenters as iaa
import cv2

inputImg = imageio.imread('test.png')
contrast_sig = iaa.SigmoidContrast(gain=(5, 10), cutoff=(0.4, 0.6))
sigImg = contrast_sig.augment_image(inputImg)
cv2.imshow('contrast', sigImg)
cv2.waitKey(0)
