import os
import numpy as np
from PIL import Image
import zarr
import pandas as pd
import re

# Define the paths to the image folders and CSV folders
folder1 = r'd:\RAL_AAA+AA+D\img_a'
folder2 = r'd:\RAL_AAA+AA+D\img_b'
action_folder = r'd:\RAL_AAA+AA+D\delta_action_dir_6d'
state_folder = r'd:\RAL_AAA+AA+D\state_files_6d'

# Configure Blosc compressor with zstd for high compression
compressor = zarr.Blosc(cname='zstd', clevel=9, shuffle=zarr.Blosc.SHUFFLE)

# Function to extract numbers from filenames for natural sorting
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

# Function to process images in batches and store them in Zarr
def process_images_in_batches(folder, zarr_dataset, batch_size=500):
    image_files = []
    for root, dirs, files in os.walk(folder):
        for filename in sorted(files, key=natural_sort_key):  # Apply natural sorting
            img_path = os.path.join(root, filename)
            if os.path.isfile(img_path) and filename.endswith('.png'):
                image_files.append(img_path)
    
    # Print the sorted image files
    print(f"Sorted image files in {folder}:")
    for img_path in image_files:
        print(img_path)
    
    num_files = len(image_files)
    for i in range(0, num_files, batch_size):
        batch_files = image_files[i:i + batch_size]
        images = []
        for img_path in batch_files:
            img = Image.open(img_path).convert('RGB')
            img_array = np.array(img, dtype=np.float32)
            img_array /= 255.0
            images.append(img_array)

        # Convert to a NumPy array and append to the Zarr dataset
        images_batch = np.array(images)
        zarr_dataset[i:i + len(images_batch)] = images_batch

# Function to load all CSV files from a folder into a single array and print filename with length
def load_csvs_into_single_array(folder, calculate_episode_ends=False):
    csv_data = []
    n_columns = None

    for root, dirs, files in os.walk(folder):
        for filename in sorted(files, key=natural_sort_key):  # Apply natural sorting
            csv_path = os.path.join(root, filename)
            if os.path.isfile(csv_path) and filename.endswith('.csv'):
                data = pd.read_csv(csv_path).values
                num_rows = len(data)
                print(f"File: {filename}, Number of rows: {num_rows}, Number of columns: {data.shape[1]}")
                csv_data.append(data)
                if n_columns is None:
                    n_columns = data.shape[1]

    print(f"Total CSV files loaded from {folder}: {len(csv_data)}")
    
    if calculate_episode_ends:
        return np.vstack(csv_data), n_columns
    else:
        return np.vstack(csv_data), n_columns

# Use the exact episode ends provided
episode_ends =  [25, 49, 77, 97, 119, 139, 169, 191, 211, 231, 256, 270, 294, 316, 336, 358, 381, 409, 429, 446, 465, 490, 512, 533, 554, 585, 621, 639, 656, 671, 699, 719, 745, 768, 790, 820, 845, 869, 909, 933, 949, 967, 989, 1016, 1041, 1067, 1088, 1117, 1138, 1160, 1184, 1211, 1234, 1264, 1290, 1312, 1341, 1371, 1400, 1424, 1444, 1466, 1495, 1513, 1532, 1558, 1579, 1598, 1625, 1652, 1672, 1694, 1713, 1733, 1762, 1786, 1815, 1833, 1853, 1881, 1904, 1935, 1956, 1974, 2010, 2030, 2061, 2085, 2104, 2135, 2154, 2182, 2198, 2218, 2237, 2260, 2287, 2312, 2331, 2349, 2366, 2396, 2416, 2458, 2484, 2505, 2528, 2548, 2574, 2597, 2617, 2646, 2664, 2681, 2711, 2729, 2758, 2800, 2829, 2846, 2870, 2891, 2922, 2940, 2972, 2999, 3022, 3041, 3072, 3096, 3116, 3134, 3158, 3188, 3214, 3233, 3259, 3283, 3304, 3324, 3346, 3368, 3393, 3409, 3435, 3468, 3485, 3508, 3532, 3554, 3574, 3594, 3619, 3652, 3671, 3691, 3710, 3738, 3761, 3784, 3812, 3835, 3859, 3882, 3912, 3934, 3955, 3969, 3993, 4019, 4046, 4071, 4099, 4121, 4148, 4166, 4196, 4221, 4246, 4269, 4288, 4312, 4336, 4362, 4389, 4407, 4429, 4446, 4466, 4495, 4522, 4539, 4560, 4576, 4605, 4626, 4661, 4684, 4703, 4722, 4759, 4778, 4796, 4818, 4842, 4864, 4886, 4907, 4932, 4955, 4976, 5000, 5018, 5039, 5061, 5088, 5115, 5138, 5154, 5171, 5197, 5221, 5239, 5258, 5286, 5312, 5331, 5350, 5381, 5399, 5418, 5444, 5467, 5484, 5512, 5528, 5549, 5570, 5589, 5612, 5629, 5656, 5682, 5703, 5721, 5744, 5769, 5790, 5818, 5839, 5861, 5889, 5905, 5924, 5950, 5966, 5990, 6013, 6039, 6061, 6081, 6105, 6125, 6145, 6164, 6189, 6215, 6240, 6256, 6284, 6299, 6313, 6333, 6353, 6370, 6391, 6410, 6428, 6449, 6468, 6489, 6520, 6544, 6561, 6591, 6612, 6627, 6646, 6666, 6689, 6719, 6740, 6763, 6792, 6813, 6830, 6857, 6882, 6899, 6927, 6946, 6967, 6990, 7011, 7036, 7062, 7084, 7111, 7147, 7172, 7193, 7213, 7234, 7261, 7283, 7306, 7336, 7363, 7383, 7416, 7434, 7463, 7482, 7507, 7534, 7556, 7575, 7599, 7625, 7654, 7673, 7701, 7717, 7742, 7767, 7797, 7819, 7849, 7873, 7900, 7921, 7944, 7971, 7997, 8024, 8051, 8071, 8092, 8110, 8134, 8156, 8183, 8205, 8229, 8254, 8278, 8298, 8320, 8356, 8377, 8401, 8426, 8446, 8476, 8503, 8529, 8549, 8571]
# Create a Zarr file to store the images and CSV data with folder structure
zarr_file = zarr.open('d:/RAL_AAA+AA+D/RAL_AAA+AA+D.zarr', mode='w')

# Create groups for data and meta
data_group = zarr_file.create_group('data')
meta_group = zarr_file.create_group('meta')

# Determine the shape of the Zarr datasets
total_images1 = len([name for name in os.listdir(folder1) if name.endswith('.png')])
total_images2 = len([name for name in os.listdir(folder2) if name.endswith('.png')])

# Create the datasets with the appropriate shape
zarr_images_A = data_group.create_dataset('images_A', shape=(total_images1, 240, 320, 3), dtype='<f4', chunks=(500, 240, 320, 3), compression=compressor)
zarr_images_B = data_group.create_dataset('images_B', shape=(total_images2, 240, 320, 3), dtype='<f4', chunks=(500, 240, 320, 3), compression=compressor)

# Process and store images in batches
process_images_in_batches(folder1, zarr_images_A, batch_size=500)
process_images_in_batches(folder2, zarr_images_B, batch_size=500)

# Load CSV data from the action folder and skip episode ends calculation
action_data_array, n_action_columns = load_csvs_into_single_array(action_folder)

# Load CSV data from the state folder (no episode ends needed here)
state_data_array, n_state_columns = load_csvs_into_single_array(state_folder)

# Store all CSV data from the action folder directly in the data group
data_group.create_dataset('action', data=action_data_array, dtype='<f4', chunks=(500, n_action_columns),compression=compressor)

# Store all CSV data from the state folder directly in the data group
data_group.create_dataset('state', data=state_data_array, dtype='<f4', chunks=(500, n_state_columns), compression=compressor)

# Store the provided episode_ends array in the Zarr file under the 'meta' group
meta_group.create_dataset('episode_ends', data=np.array(episode_ends), dtype='<i4', chunks=True, compression=compressor)

print("Images, CSV data, and episode ends have been successfully saved to the Zarr file with the specified folder structure.")
