# Punjab GeoGuardian
## Satellite-Based Land Cover Classification and Change Detection

Punjab GeoGuardian is a geospatial analysis project developed as part of the AIRI Team PITB AI Internship Task 3. It analyzes Sentinel-2 satellite imagery to identify land-cover patterns and possible vegetation-to-built-up transitions in peri-urban Lahore, Pakistan.

## Project Overview

- Study Area: Peri-urban Lahore, near Raiwind Road
- Comparison Years: 2019 and 2025
- Satellite Data: Sentinel-2 Surface Reflectance
- AOI Area: Approximately 67.59 km2
- Classification: Vegetation, Built-up, Other

## Objectives

- Analyze Sentinel-2 satellite imagery.
- Calculate NDVI and NDBI.
- Generate land-cover classification maps.
- Identify possible land-cover transitions.
- Estimate changed area.
- Validate classification results.
- Develop an interactive dashboard.

## Technologies Used

- Python
- Google Earth Engine
- Sentinel-2
- Pandas and NumPy
- Scikit-learn
- Rasterio
- Matplotlib
- Streamlit
- Jupyter Notebook

## Methodology

1. Define the Area of Interest.
2. Collect Sentinel-2 imagery for both comparison periods.
3. Apply cloud and shadow masking.
4. Generate median satellite composites.
5. Calculate NDVI and NDBI.
6. Perform rule-based and Random Forest classification.
7. Generate land-cover maps.
8. Perform pixel-wise change detection.
9. Validate predictions using manually reviewed points.
10. Visualize results in a Streamlit dashboard.

## Land Cover Classes

| Code | Class | Description |
|---|---|---|
| 0 | Vegetation | Vegetation and agricultural land |
| 1 | Built-up | Urban and built-up surfaces |
| 2 | Other | Bare land, water, and mixed surfaces |

## Key Results

### Land Cover Area Statistics

| Class | 2019 (km2) | 2025 (km2) |
|---|---:|---:|
| Vegetation | 30.4550 | 30.7272 |
| Built-up | 16.1040 | 19.4656 |
| Other | 20.9648 | 17.3309 |

### Change Detection

- Possible vegetation-to-built-up transition: 5.5107 km2
- Approximate area: 551.07 hectares
- Net built-up class increase: 3.3616 km2

The transition value is a model-derived estimate, not verified farmland loss.

### Model Validation

- Total manually reviewed points: 50
- Usable points: 49
- Correct predictions: 30
- Incorrect predictions: 19
- Random Forest accuracy: 61.22%
- Rule-based baseline accuracy: 77.55%

The Random Forest model did not outperform the rule-based baseline in this experiment.

## Project Structure

```text
Punjab-GeoGuardian/
├── dashboard/
│   └── app.py
├── data/
│   ├── satellite_imagery/
│   ├── training_samples/
│   └── validation_data/
├── documentation/
├── notebooks/
│   └── 01_AOI_and_Sentinel2.ipynb
├── outputs/
│   ├── change_detection/
│   ├── classification_maps/
│   ├── ndbi_maps/
│   ├── ndvi_maps/
│   ├── rgb_maps/
│   ├── land_cover_area_statistics.csv
│   ├── random_forest_area_statistics.csv
│   └── random_forest_model.pkl
├── reports/
│   ├── maps_png/
│   ├── Punjab_GeoGuardian_Final_Report.md
│   ├── Punjab_GeoGuardian_Final_Report.docx
│   └── Punjab_GeoGuardian_Final_Report.pdf
├── README.md
└── requirements.txt
