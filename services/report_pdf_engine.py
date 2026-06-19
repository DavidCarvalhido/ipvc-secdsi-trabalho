from io import BytesIO
from datetime import datetime
from sqlalchemy import func
from database import db
from models import RiskAssessment
from services.report_engine import (
    get_executive_report,
    get_incident_report,
    get_compliance_report,
    get_risk_report
)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_executive_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Executive Security Report", styles["Heading1"]))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Generated: {datetime.utcnow()}", styles["Normal"]))
    content.append(Spacer(1, 20))

    cia = (
        db.session.query(
            func.avg(RiskAssessment.confidentiality),
            func.avg(RiskAssessment.integrity),
            func.avg(RiskAssessment.availability)
        ).first()
    )

    c = round(cia[0] or 0, 2)
    i = round(cia[1] or 0, 2)
    a = round(cia[2] or 0, 2)

    primary = max(
        [
            ("Confidentiality", c),
            ("Integrity", i),
            ("Availability", a)
        ],
        key=lambda x: x[1]
    )[0]

    content.append(Paragraph("CIA Impact Profile", styles["Heading2"]))

    cia_rows = [
        ["Metric", "Value"],
        ["Confidentiality", f"{c}/5"],
        ["Integrity", f"{i}/5"],
        ["Availability", f"{a}/5"]
    ]

    cia_table = Table(cia_rows, colWidths=[250, 150])

    cia_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("PADDING", (0, 0), (-1, -1), 10)
        ])
    )

    content.append(cia_table)
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"<b>Primary Concern:</b> {primary}", styles["Normal"]))

    content.append(Spacer(1, 25))

    executive = get_executive_report()
    incidents = get_incident_report()
    compliance = get_compliance_report()
    risk = get_risk_report()

    sections = [
        ("Executive KPIs", executive),
        ("Incident Summary", incidents),
        ("Compliance", compliance),
        ("Risk Analysis", risk)
    ]

    for section_title, data in sections:
        content.append(Paragraph(section_title, styles["Heading2"]))
        rows = [["Metric", "Value"]]

        for k, v in data.items():
            rows.append([str(k), str(v)])

        table = Table(rows, colWidths=[250, 150])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("PADDING", (0, 0), (-1, -1), 10)
            ])
        )

        content.append(table)
        content.append(Spacer(1, 25))

    content.append(Paragraph("Generated automatically by GRC Security Platform", styles["Italic"]))
    doc.build(content)
    buffer.seek(0)

    return buffer