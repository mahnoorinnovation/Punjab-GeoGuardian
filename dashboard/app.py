
from pathlib import Path

import streamlit as st
import pandas as pd
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Punjab GeoGuardian",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"
VALIDATION = ROOT / "data" / "validation_data"

# ---------------- DESIGN / CSS ----------------
st.markdown("""
<style>
.stApp {
    background: #0b1220;
    color: #e5e7eb;
}
[data-testid="stSidebar"] {
    background: #111c2e;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #f8fafc;
}
.hero {
    background: linear-gradient(120deg, #123b36, #142b48);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #28534d;
    margin-bottom: 22px;
}
.hero h1 {
    font-size: 36px;
    margin-bottom: 8px;
}
.hero p {
    color: #cbd5e1;
    font-size: 16px;
}
.metric-card {
    background: #152238;
    border: 1px solid #263a56;
    padding: 20px;
    border-radius: 14px;
    min-height: 115px;
}
.metric-label {
    color: #a8b5c7;
    font-size: 14px;
}
.metric-value {
    color: #6ee7b7;
    font-size: 28px;
    font-weight: 700;
    margin-top: 8px;
}
.section-note {
    color: #a8b5c7;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- DATA HELPERS ----------------
def load_csv(path):
    if path.exists():
        return pd.read_csv(path)
    return None


def show_metric(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_map(title, relative_path, caption):
    image_path = OUTPUTS / relative_path

    st.markdown(f"### {title}")

    if image_path.exists():
        try:
            with Image.open(image_path) as img:
                st.image(img.copy(), use_container_width=True)
            st.caption(caption)
        except Exception as error:
            st.error(f"Could not display this map: {error}")
    else:
        st.warning(f"Map file not found: {image_path}")


# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 🌍 GeoGuardian")
st.sidebar.caption("Punjab Land Monitoring System")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Satellite Maps",
        "Land Cover Analysis",
        "Change Detection",
        "Model Validation",
        "Error Analysis"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("**Study Area**")
st.sidebar.write("Lahore Peri-Urban Region")
st.sidebar.markdown("**Study Period**")
st.sidebar.write("2019 – 2025")

area_df = load_csv(OUTPUTS / "random_forest_area_statistics.csv")
validation_df = load_csv(VALIDATION / "validation_points.csv")
error_df = load_csv(VALIDATION / "error_analysis.csv")


# ---------------- OVERVIEW ----------------
if page == "Overview":

    st.markdown("""
    <div class="hero">
        <h1>🌍 Punjab GeoGuardian</h1>
        <p>AI-powered satellite monitoring for urban expansion
        and possible agricultural land conversion.</p>
        <p><b>Study Region:</b> Lahore, Punjab, Pakistan
        &nbsp; | &nbsp; <b>Years:</b> 2019 and 2025</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Project at a Glance")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        show_metric("Study Area", "67.59 km²")

    with c2:
        show_metric("Satellite", "Sentinel-2")

    with c3:
        show_metric("Comparison", "2019–2025")

    with c4:
        show_metric("Land Classes", "3")

    st.write("")

    left, right = st.columns([1.3, 1])

    with left:
        st.subheader("Project Objective")
        st.write(
            "Punjab GeoGuardian uses satellite imagery and machine "
            "learning to examine changes in vegetation, built-up areas, "
            "and other land cover."
        )

        st.subheader("Monitoring Workflow")
        st.markdown("""
        1. Collect Sentinel-2 satellite imagery.
        2. Calculate NDVI and NDBI indices.
        3. Classify land cover using Random Forest.
        4. Compare land-cover maps from both years.
        5. Validate predictions using manually reviewed points.
        """)

    with right:
        st.subheader("Land Cover Classes")

        st.markdown("""
        🟢 **Class 0 — Vegetation / Agriculture**

        🔴 **Class 1 — Built-up / Urban**

        🟤 **Class 2 — Other land cover**
        """)

        st.info(
            "Detected changes indicate possible land conversion. "
            "They should not be treated as confirmed farmland loss."
        )

    st.divider()
    st.subheader("Satellite Comparison")

    col1, col2 = st.columns(2)

    with col1:
        show_map(
            "2019 Satellite Image",
            "rgb_maps/RGB_2019.tif",
            "Sentinel-2 RGB composite — 2019"
        )

    with col2:
        show_map(
            "2025 Satellite Image",
            "rgb_maps/RGB_2025.tif",
            "Sentinel-2 RGB composite — 2025"
        )


# ---------------- SATELLITE MAPS ----------------
elif page == "Satellite Maps":

    st.title("🛰️ Satellite Map Explorer")
    st.caption("Explore imagery and derived maps for both study years.")

    map_options = {
        "RGB 2019": "rgb_maps/RGB_2019.tif",
        "RGB 2025": "rgb_maps/RGB_2025.tif",
        "NDVI 2019": "ndvi_maps/NDVI_2019.tif",
        "NDVI 2025": "ndvi_maps/NDVI_2025.tif",
        "NDBI 2019": "ndbi_maps/NDBI_2019.tif",
        "NDBI 2025": "ndbi_maps/NDBI_2025.tif",
        "Random Forest Classification 2019":
            "classification_maps/RF_Classification_2019.tif",
        "Random Forest Classification 2025":
            "classification_maps/RF_Classification_2025.tif",
        "Possible Vegetation-to-Built-up Change":
            "change_detection/RF_Vegetation_to_Builtup_Change.tif"
    }

    selected_map = st.selectbox(
        "Select a map",
        list(map_options.keys())
    )

    show_map(
        selected_map,
        map_options[selected_map],
        "GeoGuardian satellite analysis output"
    )

    st.divider()
    st.subheader("Map Gallery")

    gallery = [
        ("RGB 2019", "rgb_maps/RGB_2019.tif"),
        ("RGB 2025", "rgb_maps/RGB_2025.tif"),
        ("NDVI 2019", "ndvi_maps/NDVI_2019.tif"),
        ("NDVI 2025", "ndvi_maps/NDVI_2025.tif"),
        ("NDBI 2019", "ndbi_maps/NDBI_2019.tif"),
        ("NDBI 2025", "ndbi_maps/NDBI_2025.tif")
    ]

    for start in range(0, len(gallery), 2):
        cols = st.columns(2)
        for col, (title, path) in zip(cols, gallery[start:start + 2]):
            with col:
                show_map(title, path, "Satellite-derived map")


# ---------------- LAND COVER ANALYSIS ----------------
elif page == "Land Cover Analysis":

    st.title("📊 Land Cover Analysis")
    st.caption("Random Forest land-cover area statistics.")

    if area_df is None:
        st.error("Area statistics CSV was not found.")
    else:
        st.dataframe(area_df, use_container_width=True)

        required = {"Class", "2019_km2", "2025_km2"}

        if required.issubset(area_df.columns):
            chart_df = area_df.set_index("Class")[
                ["2019_km2", "2025_km2"]
            ]

            st.subheader("2019 vs 2025 Land Cover")
            st.bar_chart(chart_df)

            area_df["Change_km2"] = (
                area_df["2025_km2"] - area_df["2019_km2"]
            )

            st.subheader("Net Area Change")
            st.dataframe(
                area_df[["Class", "Change_km2"]],
                use_container_width=True
            )

            st.caption(
                "Net class-area change is different from the total "
                "area of individual pixels changing from vegetation "
                "to built-up."
            )
        else:
            st.warning(
                "Expected columns: Class, 2019_km2, 2025_km2. "
                "Check the CSV column names."
            )

        st.download_button(
            "⬇️ Download Area Statistics",
            area_df.to_csv(index=False),
            file_name="land_cover_statistics.csv",
            mime="text/csv"
        )


# ---------------- CHANGE DETECTION ----------------
elif page == "Change Detection":

    st.title("🔎 Change Detection")
    st.write(
        "This section highlights locations classified as vegetation "
        "in 2019 and built-up in 2025."
    )

    c1, c2 = st.columns(2)

    with c1:
        show_metric("Possible Converted Area", "5.51 km²")

    with c2:
        show_metric("Approximate Hectares", "551.07 ha")

    st.warning(
        "This is a model-derived estimate, not verified farmland loss. "
        "Classification errors and mixed land-cover pixels may affect it."
    )

    show_map(
        "Vegetation-to-Built-up Change",
        "change_detection/RF_Vegetation_to_Builtup_Change.tif",
        "Possible vegetation-to-built-up transition, 2019–2025"
    )



# ---------------- MODEL VALIDATION ----------------
elif page == "Model Validation":

    st.title("🎯 Model Validation")
    st.caption("Random Forest performance on manually reviewed validation points.")

    if validation_df is None:
        st.error("Validation CSV not found.")

    else:
        data = validation_df.copy()
        data = data[data["Correct/Incorrect"].astype(str).str.strip() != "Needs Review"].copy()

        class_names = ["Vegetation", "Built-up", "Other"]

        data["Actual Class"] = data["Actual Class"].astype(str).str.strip()
        data["RF Predicted Class"] = (
            data["RF Predicted Class"].astype(str).str.strip()
        )

        data = data[
            data["Actual Class"].isin(class_names)
            & data["RF Predicted Class"].isin(class_names)
        ].copy()

        if data.empty:
            st.warning("No usable validation records found.")
        else:
            from sklearn.metrics import (
                accuracy_score,
                confusion_matrix,
                classification_report
            )

            actual = data["Actual Class"]
            predicted = data["RF Predicted Class"]

            accuracy = accuracy_score(actual, predicted) * 100
            correct = int((actual == predicted).sum())
            incorrect = len(data) - correct

            st.subheader("Performance Summary")

            c1, c2, c3 = st.columns(3)

            with c1:
                show_metric("Accuracy", f"{accuracy:.2f}%")

            with c2:
                show_metric("Correct Predictions", correct)

            with c3:
                show_metric("Incorrect Predictions", incorrect)

            st.progress(accuracy / 100)

            st.divider()
            st.subheader("Confusion Matrix")

            matrix = confusion_matrix(
                actual,
                predicted,
                labels=class_names
            )

            matrix_df = pd.DataFrame(
                matrix,
                index=[f"Actual {name}" for name in class_names],
                columns=[f"Predicted {name}" for name in class_names]
            )

            st.dataframe(matrix_df, use_container_width=True)

            st.subheader("Class-wise Performance")

            report = classification_report(
                actual,
                predicted,
                labels=class_names,
                target_names=class_names,
                output_dict=True,
                zero_division=0
            )

            report_df = pd.DataFrame(report).transpose()
            st.dataframe(report_df.round(2), use_container_width=True)

            st.divider()
            st.subheader("Validation Records")
            st.dataframe(data, use_container_width=True)

            st.download_button(
                "⬇️ Download Validation Results",
                data.to_csv(index=False),
                file_name="validation_results.csv",
                mime="text/csv"
            )



# ---------------- ERROR ANALYSIS ----------------
elif page == "Error Analysis":

    st.title("⚠️ Error Analysis")
    st.write(
        "Review cases where the Random Forest prediction differs "
        "from the manually assigned reference class."
    )

    if error_df is None:
        st.error("Error analysis CSV was not found.")
    else:
        st.metric("Recorded Error Cases", len(error_df))

        st.dataframe(error_df, use_container_width=True)

        st.download_button(
            "⬇️ Download Error Analysis",
            error_df.to_csv(index=False),
            file_name="error_analysis.csv",
            mime="text/csv"
        )


# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<p style='text-align:center;color:#8292a8;'>"
    "Punjab GeoGuardian | Satellite-based Land Monitoring Prototype"
    "</p>",
    unsafe_allow_html=True
)
