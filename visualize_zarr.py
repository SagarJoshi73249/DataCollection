import zarr
import numpy as np
import matplotlib.pyplot as plt

# Path to your Zarr file
zarr_file_path = r'd:/RAL_AAA+D/RAL_AAA+D.zarr'

# Open the Zarr file
zarr_data = zarr.open(zarr_file_path, mode='r')

# Access the 'image_A' subfolder under the 'data' group
image_A_data = zarr_data['data/images_b']

# Access the 'state' dataset under the 'data' group
state_data = zarr_data['data/action']

# Access the 'episode_ends' dataset under the 'meta' group
episode_ends = zarr_data['meta/episode_ends']

# Convert episode_ends to a NumPy array if needed
episode_ends_array = np.array(episode_ends)

# Print episode_ends to check the values
print(f"Episode ends: {episode_ends_array}")

# Check the shape and first few rows of state data
print(f"State data shape: {state_data.shape}")
print(f"First few rows of state data: {np.array(state_data[:5])}")
# Specify the range or slice to visualize based on episode ends
# Here, we're using the first 100 points for images and corresponding states
images_to_visualize = image_A_data[1:50]  # Adjust the slice to select the points
states_to_visualize = state_data[1:50]  # Adjust the slice for states

# Loop through and visualize each image along with the corresponding state
for i, (image, state) in enumerate(zip(images_to_visualize, states_to_visualize)):
    image_array = np.array(image)
    state_array = np.array(state)

    # Display the image
    plt.figure(figsize=(6, 6))
    plt.imshow(image_array)
    plt.title(f'Image {i+1}')
    plt.axis('off')  # Turn off the axis
    plt.show()
    
    # Display the corresponding state data for the image
    print(f"State data for image {i+1}: {state_array}")
