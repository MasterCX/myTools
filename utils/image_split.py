import os
import cv2
import time
import multiprocessing

number_w = 6            # 水平6份
number_h = 2            # 垂直2份
number_o = 0            # 重叠部分

path_origin = "E:\\img\\input"
path_target = "E:\\img\\output"


def save_image(image, name, path):
    os.makedirs(path, exist_ok=True)
    save_path = os.path.join(path, f"{name}.png")
    cv2.imwrite(save_path, image)


if __name__ == "__main__":
    for root, dirs, files in os.walk(path_origin):
        for file in files:
            # 获取文件路径
            print(os.path.join(root, file))
            path, ifile = os.path.split(os.path.join(root, file))
            file_name, suffix = ifile.split('.')
            if suffix in ["jpg", "jpeg", "png"]:
                start_time = time.time()
                image_cv2 = cv2.imread(os.path.join(root, file))
                h, w, c = image_cv2.shape
                print(f"h:{h},w:{w},c:{c}")

                delta_w = w//number_w   # 模块水平大小
                delta_h = h//number_h   # 模块竖直大小

                for n_h in range(number_h):
                    if n_h == 0:
                        start_y = 0
                        end_y = int((n_h + 1 + number_o) * delta_h)
                    else:
                        start_y = int((n_h - number_o) * delta_h)
                        end_y = int((n_h + 1) * delta_h)
                    for n_w in range(number_w):
                        time.sleep(0.5)
                        if n_w == 0:  # 为了截成正方形
                            start_x = 0
                            end_x = int((n_w + 1 + number_o) * delta_w)
                        else:
                            start_x = int((n_w - number_o) * delta_w)
                            end_x = int((n_w + 1) * delta_w)
                        print(
                            f"start_y:{start_y},end_y:{end_y},start_x:{start_x},end_x:{end_x}")
                        image_temp = image_cv2[start_y:end_y, start_x:end_x]
                        # image_name = time_name=time.strftime('%Y%m%d%H%M%S',time.localtime())
                        image_name = "".join(str(time.time()*1000).split("."))
                        image_name = f"{n_w*delta_w}x{n_h*delta_h}_{file_name}_" + image_name
                        # image_path = os.path.join(path_target, file_name)
                        image_path = path_target
                        save_process = multiprocessing.Process(
                            target=save_image, args=(image_temp, image_name, image_path))
                        save_process.start()
                        image_temp = None

                end_time = time.time()
                print(f"单张时间:{end_time - start_time}")
