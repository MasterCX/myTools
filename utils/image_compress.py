import os
import cv2

def enlarge(cv2_image,fx=0.5,fy=0.5):
    enlarge_CUBIC = cv2.resize(cv2_image, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
    return enlarge_CUBIC

def shrink(cv2_image,fx=0.5,fy=0.5):
    height, width = cv2_image.shape[:2]
    size = (int(width*fx), int(height*fy))
    shrink_CUBIC = cv2.resize(cv2_image, size, interpolation=cv2.INTER_CUBIC)
    return shrink_CUBIC

def compress_im(im_path):
    """
    图像压缩到5m以内
    :param file_path:
    :return:
    """
    target_m = 3
    img = cv2.imread(im_path)
    new_im_path = os.path.splitext(im_path)[0]+'_compression.jpg'
    quality = 95
    while quality > 10:
        cv2.imwrite(new_im_path, img, [cv2.IMWRITE_JPEG_QUALITY, quality])
        file_size = os.stat(new_im_path).st_size / 1000 / 1000
        if file_size <= target_m:
            break
        quality -= 10 if file_size >= 6.5 else 5   # 图像大小大于6.5M时以-10衰减，否则以5衰减
    file = open(new_im_path, 'rb')
    # os.system('rm {}'.format(new_im_path))
    return file, new_im_path

if __name__ == "__main__":
    old_path = "/Users/fors1f/Downloads/3/掉膜.jpg"
    new_path = os.path.splitext(old_path)[0]+'_on.jpg'
    image = cv2.imread(old_path)
    image = shrink(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(new_path,image)
    file, new_im_path = compress_im(new_path)

