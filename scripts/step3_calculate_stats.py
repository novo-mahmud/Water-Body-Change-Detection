import os
import rasterio
import numpy as np
import csv
import re # For extracting year from filename

# --- CONFIGURATION ---
input_folder = 'Binary_Masks'
results_folder = 'Results'
change_map_path = os.path.join(results_folder, 'Change_Map_1990_2025.tif')

# Approximate Pixel Area in Sq. Km (for EPSG:4326 ~30m)
PIXEL_AREA_SQKM = 0.0009 

# --- FUNCTION TO COUNT PIXELS ---
def count_water_pixels(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1)
        count = np.count_nonzero(data == 1)
    return count

# --- AUTOMATIC YEAR DETECTION ---
# We will scan the folder and extract years from filenames automatically
stats_data = []
print("--- Calculating Yearly Water Area ---")

# Get all files in the binary mask folder
files = sorted(os.listdir(input_folder))

for filename in files:
    if filename.endswith('.tif'):
        # Extract the year (looks for 4 digits in the filename)
        match = re.search(r'\d{4}', filename)
        if match:
            year = int(match.group(0))
            
            file_path = os.path.join(input_folder, filename)
            pixels = count_water_pixels(file_path)
            area_sqkm = pixels * PIXEL_AREA_SQKM
            
            stats_data.append({
                'Year': year,
                'Area_SqKm': round(area_sqkm, 2)
            })
            print(f"{year}: {round(area_sqkm, 2)} sq. km")

# Sort by year just in case
stats_data.sort(key=lambda x: x['Year'])

# --- ANALYZE CHANGE MAP ---
print("\n--- Calculating Change (1990-2025) ---")

if os.path.exists(change_map_path):
    with rasterio.open(change_map_path) as src:
        change_data = src.read(1)

    persistent_pixels = np.count_nonzero(change_data == 1)
    encroached_pixels = np.count_nonzero(change_data == 2)
    new_water_pixels = np.count_nonzero(change_data == 3)

    encroached_area = encroached_pixels * PIXEL_AREA_SQKM
    new_water_area = new_water_pixels * PIXEL_AREA_SQKM

    print(f"Encroached Area (Lost): {round(encroached_area, 2)} sq. km")
    print(f"New Water Area (Gained): {round(new_water_area, 2)} sq. km")
else:
    print("Change map not found, skipping change summary.")

# --- SAVE TO CSV ---
csv_path = os.path.join(results_folder, 'Water_Statistics.csv')

with open(csv_path, 'w', newline='') as csvfile:
    fieldnames = ['Year', 'Area_SqKm']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(stats_data)
    
    # Add summary at the bottom
    csvfile.write('\nSummary,1990-2025\n')
    csvfile.write(f'Encroached_Area_SqKm,{round(encroached_area, 2)}\n')
    csvfile.write(f'New_Water_Area_SqKm,{round(new_water_area, 2)}\n')

print(f"\nData saved to {csv_path}")