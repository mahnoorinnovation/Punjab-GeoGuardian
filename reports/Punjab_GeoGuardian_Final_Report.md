# Punjab GeoGuardian
## Satellite-Based Land Cover and Change Detection

**Study Area:** Peri-urban Lahore, Punjab, Pakistan  
**Comparison Years:** 2019 and 2025  
**Data Source:** Sentinel-2 Satellite Imagery  
**Project:** AIRI Team PITB AI Internship – Task 3

---

## 1. Introduction

Punjab GeoGuardian is a geospatial analysis project designed to monitor land-cover patterns and possible land-cover transitions using satellite imagery. The project focuses on a peri-urban area near Raiwind Road, Lahore, Pakistan.

Satellite imagery from 2019 and 2025 was analyzed to identify changes in vegetation, built-up areas, and other land-cover types. The project uses Google Earth Engine, Python, machine learning, and an interactive Streamlit dashboard.

## 2. Problem Statement

Urban expansion can result in changes to vegetation, agricultural land, and natural surfaces. Identifying these changes through satellite imagery can help understand land-cover patterns and support environmental monitoring.

The objective of Punjab GeoGuardian is to develop a satellite-based workflow for mapping land cover and estimating possible vegetation-to-built-up transitions over time.

## 3. Objectives

- Define an Area of Interest (AOI) near Raiwind Road, Lahore.
- Collect Sentinel-2 imagery for 2019 and 2025.
- Generate RGB, NDVI, and NDBI maps.
- Classify land cover into three classes.
- Perform land-cover change detection.
- Estimate the area of possible vegetation-to-built-up conversion.
- Validate classification results using manual reference points.
- Analyze classification errors.
- Develop an interactive dashboard.

## 4. Study Area

The study area is located in peri-urban Lahore, Punjab, Pakistan.

Approximate coordinates:

- Longitude: 74.20 to 74.28
- Latitude: 31.30 to 31.38

The selected AOI covers approximately 67.59 square kilometers.

## 5. Data Collection

Sentinel-2 Surface Reflectance imagery was collected using Google Earth Engine.

Dataset:
COPERNICUS/S2_SR_HARMONIZED

Selected date windows:

| Year | Date Range | Images |
|---|---|---:|
| 2019 | October 1, 2019 – January 1, 2020 | 14 |
| 2025 | October 1, 2025 – January 1, 2026 | 32 |

The imagery was filtered using a cloud percentage threshold below 20%.

Cloud and shadow masking was performed using the Scene Classification Layer (SCL). Median composites were generated for both periods.

## 6. Spectral Indices

### 6.1 NDVI

The Normalized Difference Vegetation Index (NDVI) is used to identify vegetation and measure vegetation greenness.

Formula:

NDVI = (B8 - B4) / (B8 + B4)

Where:
- B8 = Near Infrared
- B4 = Red

### 6.2 NDBI

The Normalized Difference Built-up Index (NDBI) is used to help identify built-up surfaces.

Formula:

NDBI = (B11 - B8) / (B11 + B8)

Where:
- B11 = Short-Wave Infrared
- B8 = Near Infrared

## 7. Land Cover Classification

The study area was classified into three categories:

| Class Code | Class Name | Description |
|---|---|---|
| 0 | Vegetation | Vegetation and agricultural land |
| 1 | Built-up | Urban and built-up surfaces |
| 2 | Other | Bare land, water, mixed and remaining surfaces |

Two classification approaches were implemented:

1. Rule-Based Classification using NDVI and NDBI thresholds.
2. Random Forest Classification using spectral bands and derived indices.

The Random Forest model used 300 trees.

Features used:
B2, B3, B4, B8, B11, B12, NDVI, and NDBI.

Training samples were derived from ESA WorldCover 2021.

## 8. Land Cover Area Statistics

Random Forest classification results:

| Class | 2019 (km²) | 2025 (km²) | Change (km²) |
|---|---:|---:|---:|
| Vegetation | 30.4550 | 30.7272 | +0.2722 |
| Built-up | 16.1040 | 19.4656 | +3.3616 |
| Other | 20.9648 | 17.3309 | -3.6339 |

The classified built-up area increased by approximately 3.36 square kilometers between the two periods.

## 9. Change Detection

Pixel-wise change detection was performed to identify areas classified as vegetation in 2019 and built-up in 2025.

Results:

- Possible Converted Area: 5.5107 km²
- Approximate Area: 551.07 hectares

This is a model-derived estimate of possible vegetation-to-built-up conversion. It is not verified farmland loss. Classification errors, mixed land-cover pixels, and temporal differences may affect the result.

## 10. Model Validation

A total of 50 manual validation points were prepared.

One point was marked as Needs Review and excluded from the validation metrics.

| Metric | Result |
|---|---:|
| Total Validation Points | 50 |
| Usable Points | 49 |
| Correct Predictions | 30 |
| Incorrect Predictions | 19 |
| Overall Accuracy | 61.22% |

Random Forest class-wise results:

| Class | Precision | Recall | F1-Score |
|---|---:|---:|---:|
| Vegetation | 0.75 | 0.90 | 0.82 |
| Built-up | 0.33 | 0.40 | 0.36 |
| Other | 0.62 | 0.42 | 0.50 |

The Random Forest model achieved 61.22% accuracy on the usable manually reviewed validation points.

The rule-based baseline achieved 77.55% accuracy on the same validation points.

Therefore, the Random Forest model did not outperform the rule-based baseline in this experiment.

## 11. Error Analysis

A total of 19 Random Forest misclassification cases were analyzed.

Common errors included:

- Built-up areas classified as Other.
- Other areas classified as Built-up.
- Other areas classified as Vegetation.
- Mixed land-cover pixels.
- Bare land and urban surfaces with similar spectral characteristics.

These errors indicate that distinguishing built-up and other land-cover classes remains challenging.

## 12. Interactive Dashboard

A Streamlit dashboard was developed to visualize the project results.

Dashboard pages:

- Overview
- Satellite Maps
- Land Cover Analysis
- Change Detection
- Model Validation
- Error Analysis

The dashboard provides access to satellite maps, land-cover area statistics, possible transition estimates, validation metrics, and error-analysis records.

## 13. Project Outputs

The project generated the following outputs:

- RGB maps for 2019 and 2025.
- NDVI maps for 2019 and 2025.
- NDBI maps for 2019 and 2025.
- Random Forest classification maps for 2019 and 2025.
- Vegetation-to-built-up change map.
- Land-cover area statistics.
- Manual validation dataset.
- Error-analysis dataset.
- Trained Random Forest model.
- Interactive Streamlit dashboard.

## 14. Limitations

- Training labels were derived from ESA WorldCover 2021 and may not represent exact land-cover conditions in 2019 or 2025.
- The validation dataset contains only 49 usable points.
- Mixed land-cover pixels may affect classification accuracy.
- Bare land and built-up areas may have similar spectral characteristics.
- The possible conversion estimate is model-derived and has not been independently verified.
- Seasonal and atmospheric differences may affect comparison results.

## 15. Conclusion

Punjab GeoGuardian demonstrates a satellite-based workflow for land-cover classification and change detection in peri-urban Lahore.

The project analyzed Sentinel-2 imagery from 2019 and 2025, generated RGB, NDVI, and NDBI maps, classified land cover, and estimated possible vegetation-to-built-up transitions.

The Random Forest classification achieved 61.22% accuracy on 49 usable manually reviewed validation points. The mapped built-up class increased by approximately 3.36 km², while the estimated possible vegetation-to-built-up transition area was 5.51 km².

These results should be interpreted cautiously due to classification uncertainty and mixed land-cover pixels. Future improvements should include additional validation points, better training labels, and higher-resolution imagery for verification.

---

## 16. References

1. Copernicus Sentinel-2 Surface Reflectance Harmonized Dataset – Google Earth Engine.
2. ESA WorldCover 2021.
3. Google Earth Engine Documentation – https://developers.google.com/earth-engine
4. Streamlit Documentation – https://docs.streamlit.io/

## 17. Maps and Visual Results

### 17.1 RGB Composite
RGB imagery provides a natural-color visual representation of the study area.

### 17.2 NDVI Maps
NDVI maps highlight vegetation patterns for both comparison years.

### 17.3 NDBI Maps
NDBI maps help visualize built-up surfaces.

### 17.4 Land Cover Classification
The Random Forest classification maps show Vegetation, Built-up, and Other classes.

### 17.5 Change Detection Map
The change detection map highlights possible Vegetation-to-Built-up transitions between 2019 and 2025.
