from flask import Blueprint, jsonify, send_file
from models import Incident, RiskAssessment, ComplianceResult
from services.report_engine import (
    get_executive_report,
    get_incident_report,
    get_compliance_report,
    get_risk_report,
    get_full_report,
)
from services.report_pdf_engine import generate_executive_pdf


report_bp = Blueprint("report_bp", __name__)


@report_bp.route("/reports/incidents",methods=['GET'])
def incident_report():
    incidents = Incident.query.all()

    return jsonify({
        "total":len(incidents),
        "critical":len([i for i in incidents if (i.risk_level == "Critical")]),
        "open":len([i for i in incidents if (i.status =="Open")])
    })


@report_bp.route("/reports/compliance")
def compliance_report():
    items = (ComplianceResult.query.all())
    total = len(items)
    compliant = len([x for x in items if x.compliant])
    score = (compliant / total * 100 if total else 0)

    return jsonify({
        "controls":total,
        "compliance":round(score, 2)
    })


@report_bp.route("/reports/risk")
def risk_report():
    risks = (RiskAssessment.query.all())

    return jsonify({
        "average":round(sum([r.risk_score for r in risks]) / len(risks), 2) if risks else 0,
        "critical":len([r for r in risks if (r.risk_level == "Critical")])
    })


# @report_bp.route("/reports/executive")
# def executive():
#     return jsonify({
#         "incidents":Incident.query.count(),
#         "risk":RiskAssessment.query.count(),
#         "compliance":ComplianceResult.query.count(),
#         "evidence":Evidence.query.count(),
#         "audit":AuditLog.query.count()
#     })


@report_bp.route("/reports/executive")
def executive():
    return jsonify(get_executive_report())

@report_bp.route("/reports/incidents")
def incidents():
    return jsonify(get_incident_report())

@report_bp.route("/reports/compliance")
def compliance():
    return jsonify(get_compliance_report())

@report_bp.route("/reports/risk")
def risk():
    return jsonify(get_risk_report())

@report_bp.route("/reports/full")
def full():
    return jsonify(get_full_report())


@report_bp.route("/reports/export/pdf")
def export_pdf():
    pdf = generate_executive_pdf()

    return send_file(
        pdf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="executive_report.pdf"
    )