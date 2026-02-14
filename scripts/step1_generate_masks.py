import os
import rasterio
import numpy as np

# --- CONFIGURATION ---
input_folder = 'Raw_Data'       # Where your original files are
output_folder = 'Binary_Masks'  # Where the new files will go
threshold = 0.0                 # The water cutoff line

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created folder: {output_folder}")

# --- PROCESSING LOOP ---
print("Starting processing...")

# Get all .tif files
file_list = [f for f in os.listdir(input_folder) if f.endswith('.tif')]

for filename in file_list:
    # 1. Open the file
    file_path = os.path.join(input_folder, filename)
    
    with rasterio.open(file_path) as src:
        # Read the data
        mndwi_data = src.read(1)
        profile = src.profile
        
        # 2. Get NoData value (important for GEE exports, usually it is None or a specific number)
        nodata_val = src.nodata

        # 3. Apply the Threshold (Logic)
        # Start with an array of zeros (Land)
        binary_mask = np.zeros(mndwi_data.shape, dtype=np.uint8)
        
        # Condition: Value > 0 means Water (1)
        # We use np.where or simple boolean indexing
        if nodata_val is not None:
            # If NoData exists, only process valid pixels
            binary_mask[(mndwi_data > threshold) & (mndwi_data != nodata_val)] = 1
        else:
            # If no NoData value, just check threshold
            binary_mask[mndwi_data > threshold] = 1

        # 4. Update Metadata for the new file
        profile.update(
            dtype=rasterio.uint8,  # Smaller file size (0 and 1 are small numbers)
            nodata=255             # Standard practice: set NoData to a value outside 0-1
        )

        # 5. Save the result
        output_filename = filename.replace("MNDWI", "Binary_Water")
        output_path = os.path.join(output_folder, output_filename)
        
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(binary_mask, 1)
            
    print(f"Processed: {filename} -> {output_filename}")

print("\nDone! Check your 'Binary_Masks' folder.")