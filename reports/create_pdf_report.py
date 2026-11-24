from pathlib import Path
import re
from xml.sax.saxutils import escape

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak
)

report = Path("reports/Punjab_GeoGuardian_Final_Report.md")
map_dir = Path("reports/maps_png")
output = Path("reports/Punjab_GeoGuardian_Final_Report.pdf")

map_groups = {
    "### 17.1 RGB Composite": [
        ("RGB_2019.png", "RGB Composite - 2019"),
        ("RGB_2025.png", "RGB Composite - 2025"),
    ],
    "### 17.2 NDVI Maps": [
        ("NDVI_2019.png", "NDVI - 2019"),
        ("NDVI_2025.png", "NDVI - 2025"),
    ],
    "### 17.3 NDBI Maps": [
        ("NDBI_2019.png", "NDBI - 2019"),
        ("NDBI_2025.png", "NDBI - 2025"),
    ],
    "### 17.4 Land Cover Classification": [
        ("RF_Classification_2019.png", "Random Forest Classification - 2019"),
        ("RF_Classification_2025.png", "Random Forest Classification - 2025"),
    ],
    "### 17.5 Change Detection Map": [
        ("RF_Vegetation_to_Builtup_Change.png",
         "Possible Vegetation-to-Built-up Change"),
    ],
}

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="MainTitle", parent=styles["Title"],
    fontSize=23, leading=29, alignment=TA_CENTER,
    textColor=colors.HexColor("#17365D"), spaceAfter=18
))

styles.add(ParagraphStyle(
    name="SectionHeading", parent=styles["Heading1"],
    fontSize=15, leading=19, textColor=colors.HexColor("#17365D"),
    spaceBefore=14, spaceAfter=8
))

styles.add(ParagraphStyle(
    name="SubHeading", parent=styles["Heading2"],
    fontSize=12, leading=15, textColor=colors.HexColor("#1F4E79"),
    spaceBefore=10, spaceAfter=6
))

styles.add(ParagraphStyle(
    name="BodyTextCustom", parent=styles["BodyText"],
    fontSize=9.5, leading=14, spaceAfter=7
))

styles.add(ParagraphStyle(
    name="MapTitle", parent=styles["Heading1"],
    fontSize=17, leading=22, alignment=TA_CENTER,
    textColor=colors.HexColor("#17365D"),
    spaceAfter=22
))

doc = SimpleDocTemplate(
    str(output), pagesize=A4,
    rightMargin=0.65 * inch, leftMargin=0.65 * inch,
    topMargin=0.65 * inch, bottomMargin=0.65 * inch
)

story = []
lines = report.read_text(encoding="utf-8").splitlines()
table_buffer = []

def clean_text(value):
    value = escape(value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)
    value = value.replace("`", "")
    return value

def add_table(rows):
    if not rows:
        return

    data = [
        [Paragraph(clean_text(cell), styles["BodyTextCustom"]) for cell in row]
        for row in rows
    ]

    table = Table(data, repeatRows=1, hAlign="CENTER")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    story.append(table)
    story.append(Spacer(1, 10))

def flush_table():
    global table_buffer
    if table_buffer:
        add_table(table_buffer)
        table_buffer = []

def add_maps(heading):
    for map_index, (filename, title) in enumerate(map_groups[heading]):
        image_path = map_dir / filename

        if not image_path.exists():
            story.append(PageBreak())
            story.append(Paragraph(
                f"Map not found: {escape(filename)}",
                styles["MapTitle"]
            ))
            continue

        rgb_dir = Path("reports/maps_pdf_rgb")
        rgb_dir.mkdir(parents=True, exist_ok=True)
        rgb_path = rgb_dir / f"{image_path.stem}_rgb.png"

        with PILImage.open(image_path) as original:
            rgba = original.convert("RGBA")
            white_bg = PILImage.new("RGB", rgba.size, "white")
            white_bg.paste(rgba, mask=rgba.getchannel("A"))
            white_bg.save(rgb_path, format="PNG")

        # Start each map on a new page, but never add a break after it.
        story.append(PageBreak())
        story.append(Paragraph(escape(title), styles["MapTitle"]))

        img = Image(str(rgb_path), hAlign="CENTER")
        img._restrictSize(6.8 * inch, 7.6 * inch)
        story.append(img)

for line in lines:
    text = line.strip()

    if text.startswith("|") and text.endswith("|"):
        cells = [cell.strip() for cell in text.strip("|").split("|")]
        if all(set(cell) <= set("-: ") for cell in cells):
            continue
        table_buffer.append(cells)
        continue
    else:
        flush_table()

    if not text:
        story.append(Spacer(1, 4))

    elif text.startswith("# "):
        story.append(Paragraph(escape(text[2:]), styles["MainTitle"]))

    elif text.startswith("## "):
        story.append(Paragraph(escape(text[3:]), styles["SectionHeading"]))

    elif text.startswith("### "):
        story.append(Paragraph(escape(text[4:]), styles["MapTitle"] if text in map_groups else styles["SubHeading"]))
        if text in map_groups:
            add_maps(text)

    elif text.startswith("- "):
        story.append(Paragraph(
            "â€¢ " + clean_text(text[2:]),
            styles["BodyTextCustom"]
        ))

    elif re.match(r"^\d+\.\s", text):
        story.append(Paragraph(
            clean_text(text),
            styles["BodyTextCustom"]
        ))

    else:
        story.append(Paragraph(
            clean_text(text),
            styles["BodyTextCustom"]
        ))

flush_table()

def add_footer(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(
        A4[0] / 2, 0.35 * inch,
        f"Punjab GeoGuardian | Page {document.page}"
    )
    canvas.restoreState()

doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

print("PDF report created:", output)
print("PDF size (KB):", round(output.stat().st_size / 1024, 2))
print("Dedicated map pages:", sum(len(v) for v in map_groups.values()))


