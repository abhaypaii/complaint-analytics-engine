from io import BytesIO

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

def create_pdf(report: str):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        topMargin=0.7*inch,
        bottomMargin=0.7*inch,
        leftMargin=0.8*inch,
        rightMargin=0.8*inch,
    )

    styles = getSampleStyleSheet()

    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=20,
        textColor=HexColor("#002060"),
    )

    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        textColor=HexColor("#003366"),
        spaceBefore=14,
        spaceAfter=8,
    )

    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        leading=18,
        spaceAfter=6,
    )

    story = []

    story.append(
        Paragraph(
            "Reserve Bank of India<br/>Policy Analytics Report",
            title,
        )
    )

    story.append(Spacer(1, 10))

    for line in report.split("\n"):

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):

            text = line.replace("#", "").strip()

            story.append(Paragraph(text, heading))

        elif line.startswith("-"):

            story.append(
                Paragraph(
                    "• " + line[1:].strip(),
                    body,
                )
            )

        else:

            story.append(
                Paragraph(line, body)
            )

    doc.build(story)

    buffer.seek(0)

    return buffer