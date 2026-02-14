# Spatio-Temporal Analysis of Surface Water Dynamics (1990–2025)

A Python-based geospatial analysis pipeline to quantify surface water encroachment and loss using Landsat imagery. This project processes MNDWI (Modified Normalized Difference Water Index) data to identify regions of water loss (encroachment), persistent water, and new water bodies over a 35-year period.

## 📊 Key Findings

The analysis of the study area reveals a significant decline in surface water availability:

- **Net Water Loss:** 131.10 sq. km (59.4% decrease from 1990 levels).
- **Encroached Area:** 163.13 sq. km of water bodies converted to land.
- **New Water Area:** 32.04 sq. km of new water formation (likely due to riverbank erosion or excavation).
- **Critical Trend:** Data indicates a rapid acceleration of water loss post-2010.

![Water Area Trend](https://chat.z.ai/c/results/trend_graph.png)

## 🛠️ Tech Stack

- **Data Source:** Google Earth Engine (Landsat 5, 8, 9)
- **Processing:** Python (Rasterio, NumPy)
- **Visualization:** Matplotlib, QGIS 3.40
- **Index Used:** MNDWI (Modified Normalized Difference Water Index)

## 📁 Project Structure

- `scripts/`: Python scripts for binary mask generation, change detection, and statistical analysis.
- `results/`: Output graphs, CSV statistics, and map snapshots.
- `data/`: Raw MNDWI GeoTIFFs (Not uploaded due to file size limits).

## 🚀 Workflow

1. **Data Acquisition:** MNDWI rasters for years 1990–2025 were exported from Google Earth Engine after applying cloud masking and dry-season filters (Jan-Mar).
2. **Binary Masking:** Pixels with MNDWI > 0 were classified as Water (1), others as Land (0).
3. **Change Detection:** A pixel-by-pixel comparison between 1990 and 2025 identified three classes:
    - **Persistent Water:** Water present in both years.
    - **Encroachment:** Water present in 1990 but not in 2025.
    - **New Water:** Land in 1990 but water in 2025.
4. **Visualization:** Results were visualized using Matplotlib for trends and QGIS for spatial mapping.

## 📈 Statistical Output

|Year|Water Area (sq. km)|
|---|---|
|1990|220.68|
|1995|191.76|
|2000|221.45|
|2005|262.39|
|2010|371.93|
|2015|167.01|
|2020|138.95|
|2025|89.58|

## 🗺️ Spatial Output

![Change Detection Map](https://chat.z.ai/c/results/Change_Map_Screenshot.png)_(Red indicates encroached/lost water areas, Blue indicates persistent water)_

## 💻 How to Run

1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Place raw MNDWI GeoTIFFs in the `data/` folder.
4. Run scripts in order:
    - `python scripts/1_generate_masks.py`
    - `python scripts/2_change_detection.py`
    - `python scripts/3_calculate_stats.py`
    - `python scripts/4_plot_graph.py`

## Author

**Mahmudul Hasan Novo**Civil Engineer | Geospatial Data Analyst[LinkedIn Profile Link] | [Email]
