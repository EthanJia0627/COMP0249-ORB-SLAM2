import numpy as np
import cv2
import glob

# Number of internal corners in the chessboard (columns-1, rows-1), note that this is the number of internal corners, not the number of squares
chessboard_size = (7, 10)  # 8 squares->7 internal points, 11 squares->10 internal points
square_size = 15.91  # Length of each square (unit: mm)

# Prepare chessboard corners in world coordinate system (0,0,0), (1,0,0), ..., (6,9,0)
objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# Store corners of all images
objpoints = []  # 3d points
imgpoints = []  # 2d points

# Read all extracted frames
images = glob.glob('Data/SELF/calibration_frames/*.jpg') # Adjust the path if necessary

for fname in images:
    img = cv2.imread(fname)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    # img = cv2.resize(img, (1080, 720))  # Resize to 1080p for better visualization
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    # Add points after finding them
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Visualize detected corners
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('Chessboard', img)
        cv2.waitKey(100)

cv2.destroyAllWindows()

# Calibrate camera
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

print("Camera Matrix:")
print(camera_matrix)
print("\nDistortion Coefficients:")
print(dist_coeffs)

# Save calibration results to a txt file
with open('Data/SELF/calibration_result.txt', 'w') as f:
    f.write("Camera Matrix:\n")
    f.write(np.array2string(camera_matrix, separator=', ') + '\n\n')
    f.write("Distortion Coefficients:\n")
    f.write(np.array2string(dist_coeffs, separator=', ') + '\n')

print("Calibration completed and saved")