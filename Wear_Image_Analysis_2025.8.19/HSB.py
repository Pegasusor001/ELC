import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 图片文件夹路径
image_folder = r'F:\WorkPlace\ELC\Wear_Image_Analysis_2025.8.19\Photo\92A CLR001R92 20X Smack'

# 输出直方图文件夹
hist_folder = os.path.join(image_folder, 'histograms_HSV_Brightness')
os.makedirs(hist_folder, exist_ok=True)

data_list = []

for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(image_folder, filename)
        img = cv2.imread(img_path)

        # 转 HSV，取 Brightness (V 通道)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        v_channel = hsv[:,:,2]

        # 只保留非黑色区域 (排除 V=0)
        mask = v_channel > 0
        non_black_pixels = v_channel[mask]

        # 计算直方图
        hist, bins = np.histogram(non_black_pixels, bins=256, range=(0,256))

        # 保存直方图图像
        plt.figure()
        plt.title(f'HSV Brightness Histogram (No Black) - {filename}')
        plt.xlabel('Brightness (V)')
        plt.ylabel('Pixel Count')
        plt.bar(range(256), hist, color='gray')
        plt.savefig(os.path.join(hist_folder, f'{filename}_hist.png'))
        plt.close()

        # 保存到表格
        data_list.append([filename] + hist.tolist())

# 导出 CSV
columns = ['filename'] + [f'brightness_{i}' for i in range(256)]
df = pd.DataFrame(data_list, columns=columns)
df.to_csv(os.path.join(image_folder, 'brightness_data_HSV.csv'), index=False)

print("处理完成（HSV Brightness，忽略黑色背景）。")
