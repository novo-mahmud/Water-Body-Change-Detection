import os
import rasterio
import numpy as np

# --- CONFIGURATION ---
input_folder = 'Binary_Masks'
output_folder = 'Results'

# Create output folder
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# --- LOAD DATA ---
# We specifically want to compare 1990 vs 2025
file_1990 = os.path.join(input_folder, 'Binary_Water_1990.tif')
file_2025 = os.path.join(input_folder, 'Binary_Water_2025.tif')

print("Loading maps...")

# Open 1990
with rasterio.open(file_1990) as src:
    water_1990 = src.read(1)
    profile = src.profile # We save the map settings to use later

# Open 2025
with rasterio.open(file_2025) as src:
    water_2025 = src.read(1)

# --- CHANGE DETECTION LOGIC ---
print("Calculating changes...")

# Create an empty array for the result (filled with zeros/no data)
change_map = np.zeros(water_1990.shape, dtype=np.uint8)

# Class 1: Persistent Water (1 in 1990 AND 1 in 2025)
# Logic: Both years have water (value 1)
change_map[(water_1990 == 1) & (water_2025 == 1)] = 1

# Class 2: Encroachment / Lost Water (1 in 1990 AND 0 in 2025)
# Logic: Was water, now land
change_map[(water_1990 == 1) & (water_2025 == 0)] = 2

# Class 3: New Water (0 in 1990 AND 1 in 2025)
# Logic: Was land, now water
change_map[(water_1990 == 0) & (water_2025 == 1)] = 3

# --- SAVE RESULT ---
output_path = os.path.join(output_folder, 'Change_Map_1990_2025.tif')

# Update metadata for the output file
profile.update(
    dtype=rasterio.uint8,
    nodata=0 # 0 will be our "No Change / Land" value
)

with rasterio.open(output_path, 'w', **profile) as dst:
    dst.write(change_map, 1)

print("Success! Change map saved in 'Results' folder.")
print("Legend: 1=Persistent Water, 2=Encroachment (Loss), 3=New Water")