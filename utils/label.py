import cv2
import os
import glob

PATH = "D:\\project\\tools\\position"
img_paths = glob.glob(os.path.join(PATH, '*.png'))
print(f'total imgs:{len(img_paths)}')
for index, img_path in enumerate(img_paths):
    img_name = os.path.split(img_path)[-1]
    json_name = os.path.splitext(img_name)[0] + ".json"
    json_path = os.path.join(PATH, json_name)
    if not os.path.exists(json_path):
        print(f"remove image:{img_path}")
        os.remove(img_path)
