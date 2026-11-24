from pathlib import Path
import rasterio
import matplotlib.pyplot as plt
import numpy as np

root = Path("outputs")
destination = Path("reports/maps_png")
destination.mkdir(parents=True, exist_ok=True)

maps = [
    ("rgb_maps/RGB_2019.tif", "RGB 2019", "rgb"),
    ("rgb_maps/RGB_2025.tif", "RGB 2025", "rgb"),
    ("ndvi_maps/NDVI_2019.tif", "NDVI 2019", "index"),
    ("ndvi_maps/NDVI_2025.tif", "NDVI 2025", "index"),
    ("ndbi_maps/NDBI_2019.tif", "NDBI 2019", "index"),
    ("ndbi_maps/NDBI_2025.tif", "NDBI 2025", "index"),
    ("classification_maps/RF_Classification_2019.tif", "Classification 2019", "class"),
    ("classification_maps/RF_Classification_2025.tif", "Classification 2025", "class"),
    ("change_detection/RF_Vegetation_to_Builtup_Change.tif", "Change Detection", "class"),
]

for filename, title, kind in maps:
    path = root / filename

    if not path.exists():
        print("Missing:", path)
        continue

    with rasterio.open(path) as src:
        data = src.read()
        data = np.where(data == src.nodata, np.nan, data)

    fig, ax = plt.subplots(figsize=(10, 8))

    if kind == "rgb":
        image = np.moveaxis(data[:3], 0, -1)
        image = np.nan_to_num(image)
        image = np.clip(image / 255.0, 0, 1)
        ax.imshow(image)

    elif kind == "index":
        image = data[0]
        im = ax.imshow(image, cmap="RdYlGn" if "NDVI" in title else "coolwarm")
        plt.colorbar(im, ax=ax, shrink=0.75)

    else:
        image = data[0]
        im = ax.imshow(image, cmap="viridis")
        plt.colorbar(im, ax=ax, shrink=0.75)

    ax.set_title(title, fontsize=16)
    ax.axis("off")

    output = destination / (path.stem + ".png")
    plt.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print("Saved:", output)

print("\nAll map conversions completed!")
