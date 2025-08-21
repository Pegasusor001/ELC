import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
import glob

mp_face_mesh = mp.solutions.face_mesh

# 光泽度计算函数
def compute_glossiness(image, lip_mask):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    v_channel = hsv[:, :, 2]
    lip_v = v_channel[lip_mask > 0]
    threshold = 200  # 高亮阈值
    gloss_pixels = np.sum(lip_v > threshold)
    total_pixels = lip_v.size
    return gloss_pixels / total_pixels if total_pixels > 0 else 0

# 创建Face Mesh对象
with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as face_mesh:
    
    glossiness_values = []
    time_points = []
    
    # 按时间顺序读取照片
    image_files = sorted(glob.glob("F:\WorkPlace\ELC\Wear_Image_Analysis_2025.8.19\Photo\Lip.jpg"))
    # print("1", image_files)
    # print(len(image_files))
    
    for i, file in enumerate(image_files):
        image = cv2.imread(file)
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if not results.multi_face_landmarks:
            # print(f"No face detected in {file}")
            glossiness_values.append(0)
            time_points.append(i)
            continue
        
        landmarks = results.multi_face_landmarks[0]
        h, w, _ = image.shape
        lip_points = []
        
        # mediapipe嘴唇关键点索引：61-78（外唇部分）
        lip_indices = list(range(61, 79))
        for idx in lip_indices:
            lm = landmarks.landmark[idx]
            x, y = int(lm.x * w), int(lm.y * h)
            lip_points.append([x, y])
        
        lip_points = np.array(lip_points, dtype=np.int32)
        lip_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(lip_mask, [lip_points], 255)
        
        gloss = compute_glossiness(image, lip_mask)
        glossiness_values.append(gloss)
        time_points.append(i)  # 用序号表示时间，也可以换成实际时间

# 绘制光泽度变化曲线
plt.plot(time_points, glossiness_values, marker='o')
plt.xlabel('Time (hours)')
plt.ylabel('Glossiness (high-light pixel ratio)')
plt.title('Lip Glossiness over Time')
plt.show()
