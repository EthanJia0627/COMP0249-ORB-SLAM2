import open3d as o3d
import numpy as np

def visualize_xyz_trajectory(trajectory_file):
    """
    Visualize the trajectory from a .txt file.
    The file should contain lines of the form:
    timestamp tx ty tz qx qy qz qw
    """
    # Load trajectory data
    data = np.loadtxt(trajectory_file)
    
    # Extract positions and orientations
    positions = data[:, 1:4]
    print("Maximum position:", np.max(positions, axis=0))
    print("Minimum position:", np.min(positions, axis=0))
    print("Max-Min position:", np.max(positions, axis=0) - np.min(positions, axis=0))
    
    # Create a list of lines for the trajectory
    points = o3d.utility.Vector3dVector(positions)
    lines = o3d.utility.Vector2iVector([[i, i + 1] for i in range(len(positions) - 1)])
    # Create colors for the lines from blue to red
    colors = np.zeros((len(lines), 3))
    for i in range(len(lines)):
        colors[i] = [i / len(lines), 0, 1 - i / len(lines)]  # Blue to red gradient
    colors = o3d.utility.Vector3dVector(colors)
    # Create a LineSet object

    line_set = o3d.geometry.LineSet()
    line_set.points = points
    line_set.lines = lines
    line_set.colors = o3d.utility.Vector3dVector(colors)

    # 可视化
    o3d.visualization.draw_geometries([line_set])

if __name__ == "__main__":
    # trajectory_file = 'Data/SELF/colmap/fountain_2_5fps_pc/trajectory.txt'
    trajectory_file = 'Data/SELF/fountain_2_5fps_results.txt'
    visualize_xyz_trajectory(trajectory_file)
    
