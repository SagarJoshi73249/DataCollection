import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from rotation_utils import rot6d_to_mat, mat_to_rot6d, normalize, quat_from_rot_m, quat_to_rot_m

def read_quaternions_from_csv(file_path):
    df = pd.read_csv(file_path)
    # Extract XYZ positions and quaternions
    positions = df[['st_robot_x', 'st_robot_y', 'st_robot_z']].values
    quaternions = df[['st_robot_qx', 'st_robot_qy', 'st_robot_qz', 'st_robot_qw']].values 
    return positions, quaternions

def quaternion_to_6d(quaternions):
    rot_matrices = np.array([quat_to_rot_m(q) for q in quaternions])
    norm_rot_matrices = np.array([normalize(mat) for mat in rot_matrices])
    d6_rep = np.array([mat_to_rot6d(mat) for mat in norm_rot_matrices])
    d6_matrices = np.array([rot6d_to_mat(d6) for d6 in d6_rep])
    return d6_rep, rot_matrices, d6_matrices

def plot_trajectory_with_axes(ax, positions, quaternions):
    # Plot the trajectory points
    # ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], marker='o', color='b', label='Trajectory')

    # Plot the rotation axes at each point
    for i in range(len(positions)):
        # Extract position
        x, y, z = positions[i]

        # Calculate rotation matrix from quaternion
        rot_matrix = quat_to_rot_m(quaternions[i])
        
        # Adjust the length of the axes for better fitting
        length = 0.05  # Decrease the length of the axes

        # Plot the axes
        ax.quiver(x, y, z, rot_matrix[0, 0], rot_matrix[1, 0], rot_matrix[2, 0], color='r', length=length, arrow_length_ratio=0.1)  # X-axis
        ax.quiver(x, y, z, rot_matrix[0, 1], rot_matrix[1, 1], rot_matrix[2, 1], color='g', length=length, arrow_length_ratio=0.1)  # Y-axis
        ax.quiver(x, y, z, rot_matrix[0, 2], rot_matrix[1, 2], rot_matrix[2, 2], color='b', length=length, arrow_length_ratio=0.1)  # Z-axis
        
        # Annotate the points with their index (starting from 1)
        ax.text(x, y, z, str(i + 1), color='black', fontsize=10, ha='center')

    # Set labels and title
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('3D Trajectory with Orientation Axes')
    ax.legend()
    ax.grid()

    # Adjust the limits to better fit the data
    ax.set_xlim([np.min(positions[:, 0]) - 0.02, np.max(positions[:, 0]) + 0.02])
    ax.set_ylim([np.min(positions[:, 1]) - 0.02, np.max(positions[:, 1]) + 0.02])
    ax.set_zlim([np.min(positions[:, 2]) - 0.02, np.max(positions[:, 2]) + 0.02])

    # Optionally, adjust the view angle
    ax.view_init(elev=20, azim=30)

def plot_6d_trajectory(ax, positions, d6_matrices):
    # Plot the trajectory and 6D orientations
    # ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], marker='o', color='b', label='Trajectory')
    for i in range(len(positions)):
        # Extract position
        x, y, z = positions[i]

        # Calculate rotation matrix from quaternion
        rot_matrix = d6_matrices[i]
        
        # Adjust the length of the axes for better fitting
        length = 0.05  # Increase the length for better visibility

        # Plot the rotation axes as a 6D representation
        ax.quiver(x, y, z, rot_matrix[0, 0], rot_matrix[1, 0], rot_matrix[2, 0], color='r', length=length, arrow_length_ratio=0.1)  # X-axis
        ax.quiver(x, y, z, rot_matrix[0, 1], rot_matrix[1, 1], rot_matrix[2, 1], color='g', length=length, arrow_length_ratio=0.1)  # Y-axis
        ax.quiver(x, y, z, rot_matrix[0, 2], rot_matrix[1, 2], rot_matrix[2, 2], color='b', length=length, arrow_length_ratio=0.1)  # Z-axis
        
        # Annotate the points with their index (starting from 1)
        ax.text(x, y, z, str(i + 1), color='black', fontsize=10, ha='center')

    # Set labels and title
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('6D Trajectory Visualization')
    ax.grid()

    # Adjust the limits to better fit the data
    ax.set_xlim([np.min(positions[:, 0]) - 0.02, np.max(positions[:, 0]) + 0.02])
    ax.set_ylim([np.min(positions[:, 1]) - 0.02, np.max(positions[:, 1]) + 0.02])
    ax.set_zlim([np.min(positions[:, 2]) - 0.02, np.max(positions[:, 2]) + 0.02])

def verify_rotations(file_path):
    positions, quaternions = read_quaternions_from_csv(file_path)
    d6_rep, rot_matrices, d6_matrices = quaternion_to_6d(quaternions)
    # Create a figure with subplots
    fig = plt.figure(figsize=(18, 8))
    
    # Create 3D trajectory subplot
    ax1 = fig.add_subplot(121, projection='3d')
    plot_trajectory_with_axes(ax1, positions, quaternions)

    # Create 6D trajectory subplot
    ax2 = fig.add_subplot(122, projection='3d')
    plot_6d_trajectory(ax2, positions, d6_matrices)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    file_path = r"d:\RAL_AAA+D\state_files_6d\state_columns_t1_obj2_robot_poses.csv"  # Replace with your actual file path
    verify_rotations(file_path)
