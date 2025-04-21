import numpy as np
import cv2
import glob

# 棋盘格内角点数量（列数 -1，行数 -1），注意是内角点数量，不是格子数
chessboard_size = (7, 10)  # 8格->7内点，11格->10内点
square_size = 15.91  # 每格的边长（单位：mm）

# 准备世界坐标系下的棋盘格角点 (0,0,0), (1,0,0), ..., (6,9,0)
objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# 存储所有图像的角点
objpoints = []  # 3d点
imgpoints = []  # 2d点

# 读取提取的所有帧
images = glob.glob('part2/calibration_frames/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 寻找棋盘格角点
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    # 找到后添加点
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

        # 可视化检测到的角点
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('Chessboard', img)
        cv2.waitKey(100)

cv2.destroyAllWindows()

# 标定相机
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

print("相机矩阵 (Camera Matrix):")
print(camera_matrix)
print("\n畸变系数 (Distortion Coefficients):")
print(dist_coeffs)

# 保存标定结果到一个txt文件
with open('part2/calibration_result.txt', 'w') as f:
    f.write("Camera Matrix:\n")
    f.write(np.array2string(camera_matrix, separator=', ') + '\n\n')
    f.write("Distortion Coefficients:\n")
    f.write(np.array2string(dist_coeffs, separator=', ') + '\n')

print("标定完成并已保存到 'part2/calibration_result.txt'！")
