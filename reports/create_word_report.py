from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

report = Path("reports/Punjab_GeoGuardian_Final_Report.md")
map_dir = Path("reports/maps_png")
output = Path("reports/Punjab_GeoGuardian_Final_Report.docx")

doc = Document()
section = doc.sections[0]
section.top_margin = Inches(0.7)
section.bottom_margin = Inches(0.7)
section.left_margin = Inches(0.8)
section.right_margin = Inches(0.8)

doc.styles["Normal"].font.name = "Calibri"
doc.styles["Normal"].font.size = Pt(10)

map_groups = {
    "### 17.1 RGB Composite": [
        ("RGB_2019.png", "RGB Composite — 2019"),
        ("RGB_2025.png", "RGB Composite — 2025"),
    ],
    "### 17.2 NDVI Maps": [
        ("NDVI_2019.png", "NDVI — 2019"),
        ("NDVI_2025.png", "NDVI — 2025"),
    ],
    "### 17.3 NDBI Maps": [
        ("NDBI_2019.png", "NDBI — 2019"),
        ("NDBI_2025.png", "NDBI — 2025"),
    ],
    "### 17.4 Land Cover Classification": [
        ("RF_Classification_2019.png", "Random Forest Classification — 2019"),
        ("RF_Classification_2025.png", "Random Forest Classification — 2025"),
    ],
    "### 17.5 Change Detection Map": [
        ("RF_Vegetation_to_Builtup_Change.png", "Possible Vegetation-to-Built-up Change"),
    ],
}

lines = report.read_text(encoding="utf-8").splitlines()

for line in lines:
    text = line.strip()

    if not text:
        continue

    if text.startswith("# "):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text[2:])
        r.bold = True
        r.font.size = Pt(24)
        r.font.color.rgb = RGBColor(23, 54, 93)

    elif text.startswith("## "):
        doc.add_heading(text[3:], level=1)

    elif text.startswith("### "):
        doc.add_heading(text[4:], level=2)

        if text in map_groups:
            for filename, caption in map_groups[text]:
                image_path = map_dir / filename
                if image_path.exists():
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.add_run().add_picture(str(image_path), width=Inches(5.8))
                    cap = doc.add_paragraph(caption)
                    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    doc.add_paragraph(f"Map not found: {filename}")

    elif text.startswith("|") and text.endswith("|"):
        cells = [c.strip() for c in text.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if not hasattr(doc, "_table_buffer"):
            doc._table_buffer = []
        doc._table_buffer.append(cells)

    elif text.startswith("- "):
        doc.add_paragraph(text[2:], style="List Bullet")

    elif text.startswith("**") and text.endswith("**"):
        p = doc.add_paragraph()
        p.add_run(text.strip("*")).bold = True

    else:
        doc.add_paragraph(text)

# Add page numbers in footer
for sec in doc.sections:
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("Punjab GeoGuardian | Final Report")

doc.save(output)
print("Word report created:", output)
print("Maps inserted:", sum(len(v) for v in map_groups.values()))
