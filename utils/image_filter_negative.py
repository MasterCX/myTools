import os
import cv2
import time
import multiprocessing
import numpy as np

path_origin = "/Users/fors1f/Downloads/1"
path_target = "/Users/fors1f/Downloads/2"

def save_image(image,name,path):
    os.makedirs(path,exist_ok=True)
    save_path = os.path.join(path,f"{name}.png")
    cv2.imwrite(save_path,image)

def my_gray(image):
    '''
    图片转灰度
    '''
    img_gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    return img_gray

def my_threshold(gray):
    '''
    图片二值化
    @gray   灰度值图片
    # 工位1 反面 20 255
    # 工位2 正面 40 255
    '''
    ret, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    return ret, thresh

def my_contours(thresh):
    '''
    寻找边界
    @thresh 二值化图片
    '''
    # contours：返回的轮廓 hierarchy：图像的拓扑信息（轮廓层次） #黑背景白物体
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy

def get_boundingRect(cnt):
    (center_x, center_y), (width, height), angle = cv2.minAreaRect(cnt)
    area = cv2.contourArea(cnt)
    box = cv2.boxPoints(((center_x, center_y), (width, height), angle))  # 计算最小面积矩形的坐标
    box = np.int0(box)                          # 将坐标规范化为整数
    return box,angle,width,height,int(center_x),int(center_y),area

if __name__ == "__main__":
    # 反面工位切割脚本
    for root,dirs,files in os.walk(path_origin):
        for file in files:
            #获取文件路径
            print(os.path.join(root,file))
            path,ifile=os.path.split(os.path.join(root,file))
            file_name,suffix=ifile.split('.')
            if suffix in ["jpg", "jpeg", "png"]:
                start_time = time.time()
                image_cv2 = cv2.imread(os.path.join(root,file))
                h,w,c = image_cv2.shape
                print(f"h:{h},w:{w},c:{c}")
                gray = my_gray(image_cv2)
                ret, thresh = my_threshold(gray)
                contours, hierarchy = my_contours(thresh)
                # 找一个最大的轮廓
                contour_largest = 0
                contour_aera_temp = 0
                for index,contour in enumerate(contours):
                    if contour_aera_temp < cv2.contourArea(contour):
                        contour_aera_temp = cv2.contourArea(contour)
                        contour_largest = index
                if len(contours) >= 1:
                    box,angle,width,height,center_x,center_y,area = get_boundingRect(contours[contour_largest])
                    # print(box)
                    left_point = box.min(axis=0)
                    right_point = box.max(axis=0)
                    # print(left_point,right_point)
                    if left_point[0] < 0 or left_point[1] < 0:
                        left_point = [0, 0]
                    # cv2.circle(image_cv2, (left_point[0], left_point[1]), 5, (255, 0, 0), 5)
                    # cv2.circle(image_cv2, (right_point[0], right_point[1]), 5, (255, 0, 0), 5)
                    image_cv2 = image_cv2[left_point[1]:right_point[1],left_point[0]:right_point[0]]
                    
                    image_path = os.path.join(path_target)
                    save_process = multiprocessing.Process(target=save_image,args=(image_cv2,file_name,image_path))
                    save_process.start()