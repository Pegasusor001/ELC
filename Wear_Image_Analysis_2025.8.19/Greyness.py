import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 图片文件夹路径（存放唇部图片）
image_folder = r'F:\WorkPlace\ELC\Wear_Image_Analysis_2025.8.19\Photo\92A CLR001R92 20X Smack'


# 输出直方图文件夹
hist_folder = os.path.join(image_folder, 'histograms_no_black')
os.makedirs(hist_folder, exist_ok=True)

# 保存亮度数据表格
data_list = []

for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(image_folder, filename)
        
        # 读取图像
        img = cv2.imread(img_path)
        
        # 转为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 生成 mask（只保留非黑色像素）
        mask = gray > 0
        
        # 提取非黑色像素
        non_black_pixels = gray[mask]
        
        # 计算直方图（忽略黑色）
        hist, bins = np.histogram(non_black_pixels, bins=256, range=(0,256))
        
        # 保存直方图图片
        plt.figure()
        plt.title(f'Greyness Histogram (No Black) - {filename}')
        plt.xlabel('Greyness')
        plt.ylabel('Pixel Count')
        plt.bar(range(256), hist, color='gray')
        plt.savefig(os.path.join(hist_folder, f'{filename}_hist.png'))
        plt.close()
        
        # 保存数据到列表
        data_list.append([filename] + hist.tolist())

# 导出 CSV 表格
columns = ['filename'] + [f'Greyness_{i}' for i in range(256)]
df = pd.DataFrame(data_list, columns=columns)
df.to_csv(os.path.join(image_folder, 'Greyness_data_no_black.csv'), index=False)

print("处理完成（忽略黑色背景），直方图和数据表格已保存。")
