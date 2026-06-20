from io import BytesIO
from datetime import datetime
from sqlalchemy import func
from database import db
from models import RiskAssessment, Incident
from services.report_engine import (
    get_executive_report,
    get_incident_report,
    get_compliance_report,
    get_risk_report
)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


TABLE_STYLE = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ("PADDING", (0, 0), (-1, -1), 10),
])


def build_metric_table(data: dict, col_widths=(250, 150)):
    rows = [["Metric", "Value"]] + [[str(k), str(v)] for k, v in data.items()]
    table = Table(rows, colWidths=col_widths)
    table.setStyle(TABLE_STYLE)
    return table


def calculate_cia(query):
    c, i, a = query.first()
    return (
        round(c or 0, 2),
        round(i or 0, 2),
        round(a or 0, 2),
    )


def get_primary_cia(c, i, a):
    return max([("Confidentiality", c), ("Integrity", i), ("Availability", a)], key=lambda x: x[1])[0]


def add_section(content, title, data, styles):
    content.append(Paragraph(title, styles["Heading2"]))
    content.append(build_metric_table(data))
    content.append(Spacer(1, 25))


def generate_executive_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = []

    # Header
    content.append(Paragraph("Executive Security Report", styles["Heading1"]))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Generated: {datetime.utcnow()}", styles["Normal"]))
    content.append(Spacer(1, 20))

    # Data sources
    reports = [
        ("Executive KPIs", get_executive_report()),
        ("Incident Summary", get_incident_report()),
        ("Compliance", get_compliance_report()),
        ("Risk Analysis", get_risk_report()),
    ]

    for title, data in reports:
        add_section(content, title, data, styles)

    # CIA global
    cia_query = db.session.query(
        func.avg(RiskAssessment.confidentiality),
        func.avg(RiskAssessment.integrity),
        func.avg(RiskAssessment.availability)
    )

    c, i, a = calculate_cia(cia_query)
    primary = get_primary_cia(c, i, a)

    content.append(Paragraph("CIA Impact Profile", styles["Heading2"]))
    content.append(build_metric_table({
        "Confidentiality": f"{c}/5",
        "Integrity": f"{i}/5",
        "Availability": f"{a}/5",
    }))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"<b>Primary Concern:</b> {primary}", styles["Normal"]))
    content.append(Spacer(1, 25))

    # CIA por incidente
    content.append(Paragraph("CIA Per Incident Analysis", styles["Heading1"]))
    content.append(Spacer(1, 15))

    incidents = db.session.query(Incident).all()

    for incident in incidents:
        cia_query = (
            db.session.query(
                func.avg(RiskAssessment.confidentiality),
                func.avg(RiskAssessment.integrity),
                func.avg(RiskAssessment.availability),
            )
            .filter(RiskAssessment.incident_id == incident.id)
        )

        c, i, a = calculate_cia(cia_query)
        primary = get_primary_cia(c, i, a)

        content.append(Paragraph(f"Incident #{incident.id}", styles["Heading2"]))
        content.append(build_metric_table({
            "Confidentiality": f"{c}/5",
            "Integrity": f"{i}/5",
            "Availability": f"{a}/5",
        }))

        content.append(Spacer(1, 10))
        content.append(Paragraph(f"<b>Primary Concern:</b> {primary}", styles["Normal"]))
        content.append(Spacer(1, 20))

    content.append(Paragraph("Generated automatically by GRC Security Platform", styles["Italic"]))

    doc.build(content)
    buffer.seek(0)
    return buffer