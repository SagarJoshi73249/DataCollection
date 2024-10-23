# %%
import sys
import os
import pandas as pd
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)
os.chdir(ROOT_DIR)

# %%
import numpy as np
from rotation_transformer import RotationTransformer
from rotation_utils import rot6d_to_mat, mat_to_rot6d, normalize, quat_from_rot_m, quat_to_rot_m

# %%
# def test():
#     N = 100
#     d6 = np.random.normal(size=(N,6))
#     rt = RotationTransformer(from_rep='rotation_6d', to_rep='matrix')
#     gt_mat = rt.forward(d6)
#     mat = rot6d_to_mat(d6)
#     assert np.allclose(gt_mat, mat)
    
#     to_d6 = mat_to_rot6d(mat)
#     to_d6_gt = rt.inverse(mat)
#     assert np.allclose(to_d6, to_d6_gt)
#     gt_mat = rt.forward(d6[1])
#     mat = rot6d_to_mat(d6[1])
#     assert np.allclose(gt_mat, mat)
#     print(mat)
#     norm_mat = normalize(mat)
#     print(norm_mat)
#     to_d6 = mat_to_rot6d(norm_mat)
#     to_d6_gt = rt.inverse(norm_mat)
#     print(np.sqrt(to_d6[0]**2+to_d6[1]**2+to_d6[2]**2))
#     print(np.sqrt(to_d6[3]**2+to_d6[4]**2+to_d6[5]**2))
#     print(quat_from_rot_m(norm_mat))
#     assert np.allclose(to_d6, to_d6_gt)
    
def read_quaternions_from_csv(file_path):
    df = pd.read_csv(file_path)
    quaternions = df[['st_robot_qx', 'st_robot_qy', 'st_robot_qz', 'st_robot_qw']].values 
    df = df.drop(['timestamp', 'torque_x','torque_y','torque_z'], axis=1, errors='ignore')
    return df, quaternions

def process_quaternions(quaternions):
    rot_matrices = np.array([quat_to_rot_m(q) for q in quaternions])
    norm_rot_matrices = np.array([normalize(mat) for mat in rot_matrices])
    d6_rep = np.array([mat_to_rot6d(mat) for mat in norm_rot_matrices])

    return d6_rep

def process_csv(file_path, output_file_path=None):
    df, quaternions = read_quaternions_from_csv(file_path)
    d6_rep = process_quaternions(quaternions)
    d6_columns = pd.DataFrame(d6_rep, columns=['rot_6d_1', 'rot_6d_2', 'rot_6d_3', 'rot_6d_4', 'rot_6d_5', 'rot_6d_6'])

    # Find the index of the quaternion columns
    quat_col_index = df.columns.get_loc('st_robot_qx')
    cols_before_quat = df.columns[:quat_col_index]
    cols_after_quat = df.columns[quat_col_index + 4:]

    df = df.drop(['st_robot_qx', 'st_robot_qy', 'st_robot_qz', 'st_robot_qw'], axis=1, errors='ignore')

    # Check that the column slices are valid
    if cols_before_quat.any() and cols_after_quat.any():
        df = pd.concat([df[cols_before_quat], d6_columns, df[cols_after_quat]], axis=1)
    else:
        # Handle cases where there are no columns before or after quaternions
        print(f"Warning: Could not concatenate columns properly for {file_path}.")
        df = pd.concat([df, d6_columns], axis=1)  # Just append 6D columns

    # Save to the output file
    output_file_path = output_file_path or file_path
    df.to_csv(output_file_path, index=False)
    print(f"Processed CSV saved to: {output_file_path}")


def process_folder(folder_path):
    # Create a new folder with "_6d" appended to the name
    new_folder_path = folder_path + "_6d"
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    
    # Process each CSV file in the original folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            output_file_path = os.path.join(new_folder_path, file_name)
            process_csv(file_path, output_file_path)
            print(f"Processed {file_name} and saved to {output_file_path}")

if __name__ == "__main__":
    folder_path  = r"d:\RAL_AAA+AA+D\state_files"
    process_folder(folder_path)