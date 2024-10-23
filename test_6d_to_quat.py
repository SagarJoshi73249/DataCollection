import sys
import os
import pandas as pd
import numpy as np
from rotation_utils import rot6d_to_mat, normalize, quat_from_rot_m

# Function to convert 6D representation back to quaternions
def process_6d_to_quaternions(d6_rep):
    # Convert 6D rotation back to rotation matrices
    rot_matrices = np.array([rot6d_to_mat(d6) for d6 in d6_rep])
    # Normalize rotation matrices (if necessary)
    norm_rot_matrices = np.array([normalize(mat) for mat in rot_matrices])
    # Convert rotation matrices to quaternions
    quaternions = np.array([quat_from_rot_m(mat) for mat in norm_rot_matrices])

    return quaternions

# Function to read 6D data from CSV file
def read_6d_from_csv(file_path):
    df = pd.read_csv(file_path)
    d6_rep = df[['rot_6d_1', 'rot_6d_2', 'rot_6d_3', 'rot_6d_4', 'rot_6d_5', 'rot_6d_6']].values
    df = df.drop(['rot_6d_1', 'rot_6d_2', 'rot_6d_3', 'rot_6d_4', 'rot_6d_5', 'rot_6d_6'], axis=1, errors='ignore')
    return df, d6_rep

# Function to process CSV file and convert 6D back to quaternion
def process_csv_6d_to_quat(file_path, output_file_path=None):
    df, d6_rep = read_6d_from_csv(file_path)
    quaternions = process_6d_to_quaternions(d6_rep)
    quat_columns = pd.DataFrame(quaternions, columns=['st_robot_qx', 'st_robot_qy', 'st_robot_qz', 'st_robot_qw'])

    # Append quaternion columns
    df = pd.concat([df, quat_columns], axis=1)

    # Save to the output file
    output_file_path = output_file_path or file_path
    df.to_csv(output_file_path, index=False)
    print(f"Processed CSV saved to: {output_file_path}")

# Function to process all CSV files in a folder
def process_folder_6d_to_quat(folder_path):
    # Create a new folder with "_quat" appended to the name
    new_folder_path = folder_path + "_quat"
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    
    # Process each CSV file in the original folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            output_file_path = os.path.join(new_folder_path, file_name)
            process_csv_6d_to_quat(file_path, output_file_path)
            print(f"Processed {file_name} and saved to {output_file_path}")

if __name__ == "__main__":
    folder_path  = r"d:\RAL_AAA+D\state_files_6d"
    process_folder_6d_to_quat(folder_path)
