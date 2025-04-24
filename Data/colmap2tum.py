import pycolmap
import os
import numpy as np
from pyquaternion import Quaternion


colmap_path = 'Data/SELF/colmap/room_2_5fps_pc/'

# Read images.bin file
reconstruction = pycolmap.Reconstruction(colmap_path)

# Read times.txt file
times_file = os.path.join(colmap_path, 'times.txt')
with open(times_file, 'r') as f:
    lines = f.readlines()
timestamps = []
for line in lines:
    timestamps.append(float(line.strip()))
timestamps = np.array(timestamps)
print(f"Loaded {len(timestamps)} timestamps from {times_file}")

# get tx, ty, tz, qx, qy, qz, qw
def get_camera_pose(images,timestamps):
    camera_poses = np.zeros((len(images), 8))
    for image in images.values():
        tx, ty, tz = image.cam_from_world.translation
        qx, qy, qz, qw = image.cam_from_world.rotation.quat

        # COLMAP 提供的 pose：T_cw
        R_cw = Quaternion(qw, qx, qy, qz).rotation_matrix
        t_cw = np.array([tx, ty, tz])

        # 得到 T_wc：世界从相机
        R_wc = R_cw.T     
        t_wc = -R_wc @ t_cw
        tx, ty, tz = t_wc
        qx, qy, qz, qw = Quaternion(matrix=R_wc).elements
        camera_poses[image.image_id-1] = [timestamps[image.image_id-1],tx, ty, tz, qx, qy, qz, qw]
    return camera_poses


images = reconstruction.images
camera_poses = get_camera_pose(images,timestamps)
print(camera_poses.shape)

# Save to tum
output_file = os.path.join(colmap_path, 'trajectory.txt')
with open(output_file, 'w') as f:
    for i in range(camera_poses.shape[0]):
        f.write(f"{camera_poses[i, 0]} {camera_poses[i, 1]} {camera_poses[i, 2]} {camera_poses[i, 3]} {camera_poses[i, 4]} {camera_poses[i, 5]} {camera_poses[i, 6]} {camera_poses[i, 7]}\n")
print(f"Saved camera poses to {output_file}")