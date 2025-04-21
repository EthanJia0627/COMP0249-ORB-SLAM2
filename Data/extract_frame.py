import cv2
import os

# Input video path
video_path = 'SELF_RAW/calibration_1.MOV'

# Output frame save path
output_dir = 'SELF/fountain_2'
image_dir = 'SELF/fountain_2/image_0'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(image_dir, exist_ok=True)

# Output times.txt path
times_file = os.path.join(output_dir, 'times.txt')

# Open video
cap = cv2.VideoCapture(video_path)
frame_id = 0

# Set target FPS
target_fps = 24.0
video_fps = cap.get(cv2.CAP_PROP_FPS)

# Check actual video fps
if abs(video_fps - target_fps) > 1.0:
    print(f"Warning: Video original FPS is {video_fps:.2f}, which is different from the target {target_fps:.2f}!")

timestamps = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Rotate 90 degrees clockwise
    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # Save image
    frame_filename = os.path.join(image_dir, f'{frame_id:06d}.png')
    cv2.imwrite(frame_filename, rotated_frame)
    print(f"Saving frame {frame_id} to {frame_filename}")

    # Record timestamp
    timestamps.append(frame_id / target_fps)

    frame_id += 1

cap.release()

# Save times.txt
with open(times_file, 'w') as f:
    for t in timestamps:
        f.write(f"{t:.6f}\n")

print(f"Completed! Extracted {frame_id} frames, times.txt generated synchronously.")
