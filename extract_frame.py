import cv2
import os

# 输入视频路径
video_path = 'Data/SELF/KYJT6400.MOV'

# 输出帧保存路径
output_dir = 'part2/self/fountain_2'
image_dir = 'part2/self/fountain_2/image_0'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(image_dir, exist_ok=True)

# 输出 times.txt 路径
times_file = os.path.join(output_dir, 'times.txt')

# 打开视频
cap = cv2.VideoCapture(video_path)
frame_id = 0

# 设定保存FPS
target_fps = 24.0
video_fps = cap.get(cv2.CAP_PROP_FPS)

# 检查实际视频fps
if abs(video_fps - target_fps) > 1.0:
    print(f"警告：视频原始FPS为 {video_fps:.2f}，和目标 {target_fps:.2f} 不同！")

timestamps = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 顺时针旋转90度
    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # 保存图片
    frame_filename = os.path.join(image_dir, f'{frame_id:06d}.png')
    cv2.imwrite(frame_filename, rotated_frame)
    print(f"保存帧 {frame_id} 到 {frame_filename}")

    # 记录timestamp
    timestamps.append(frame_id / target_fps)

    frame_id += 1

cap.release()

# 保存 times.txt
with open(times_file, 'w') as f:
    for t in timestamps:
        f.write(f"{t:.6f}\n")

print(f"完成！共提取 {frame_id} 帧，times.txt 同步生成。")
