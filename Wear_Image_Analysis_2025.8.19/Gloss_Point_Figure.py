import cv2
import numpy as np
import os

# 图片文件夹
image_folder = r'F:\WorkPlace\ELC\Wear_Image_Analysis_2025.8.19\Photo'

# 输出高光点处理图片的文件夹
output_folder = os.path.join(image_folder, 'highlight_blackened')
os.makedirs(output_folder, exist_ok=True)

# 高光阈值
threshold = 240

for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(image_folder, filename)
        img = cv2.imread(img_path)

        # 转 HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        v_channel = hsv[:,:,2]

        # 找高光区域 (V > threshold)
        mask = v_channel > threshold

        # 将高光点设为黑色 (0,0,0)
        img[mask] = [0, 0, 0]

        # 保存处理后的图片
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, img)

print("处理完成，高光点已改为黑色并保存。")
