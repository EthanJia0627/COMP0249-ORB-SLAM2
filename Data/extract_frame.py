import cv2
import os

# Input video path
video_path = 'Data/SELF_RAW/KYJT6400.MOV'

# Output frame save path
output_dir = 'Data/SELF/fountain_2_1080'
image_dir = 'Data/SELF/fountain_2_1080/image_0'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(image_dir, exist_ok=True)

# Output times.txt path
times_file = os.path.join(output_dir, 'times.txt')

# Open video
cap = cv2.VideoCapture(video_path)
frame_id = 0
save_frame_id = 0    # Continuous frame id

# Set target FPS
target_fps = 5
video_fps = cap.get(cv2.CAP_PROP_FPS)

timestamps = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_id % int(video_fps / target_fps) != 0:
        frame_id += 1
        continue
    # Rotate 90 degrees clockwise
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # Resize to 1080p
    frame = cv2.resize(frame, (1080, 720))  # Resize to 1080p for better visualization

    # Save image
    frame_filename = os.path.join(image_dir, f'{save_frame_id:06d}.png')

    cv2.imwrite(frame_filename, frame)
    print(f"Saving frame {save_frame_id} to {frame_filename}")

    # Record timestamp
    timestamps.append(frame_id / video_fps)
    save_frame_id += 1
    frame_id += 1

cap.release()

# Save times.txt
with open(times_file, 'w') as f:
    for t in timestamps:
        f.write(f"{t:.6f}\n")

print(f"Completed! Extracted {frame_id} frames, times.txt generated synchronously.")
