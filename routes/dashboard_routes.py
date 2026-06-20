from flask import Blueprint, jsonify, render_template
from database import db
from sqlalchemy import func
from models import Event, Incident, RiskAssessment, ComplianceResult, Asset


dashboard_bp = Blueprint('dashboard_bp', __name__)


@dashboard_bp.route("/")
def dashboard():
    return render_template("dashboard.html")


@dashboard_bp.route("/dashboard/summary", methods=['GET'])
def summary():
    total_events = Event.query.count()
    total_incidents = (Incident.query.count())
    total_risks = (RiskAssessment.query.count())
    violations = (ComplianceResult.query.filter_by(compliant=False).count())

    return jsonify({
        "events": total_events,
        "incidents": total_incidents,
        "risk_assessments": total_risks,
        "policy_violations": violations
    })


@dashboard_bp.route("/dashboard/risk-distribution", methods=['GET'])
def risk_distribution():
    rows = (
        RiskAssessment
        .query
        .with_entities(
            RiskAssessment.risk_level,
            func.count()
        )
        .group_by(
            RiskAssessment.risk_level).all()
    )

    return jsonify([
        {
            "risk_level": r[0],
            "count": r[1]
        }

        for r in rows
    ])


@dashboard_bp.route("/dashboard/compliance", methods=['GET'])
def compliance():
    total = (ComplianceResult.query.count())
    failed = (ComplianceResult.query.filter_by(compliant=False).count())
    success = (total - failed)

    return jsonify({
        "compliant": success,
        "violations": failed,
        "compliance_rate": round((success / max(total, 1)) * 100, 2)
    })


@dashboard_bp.route("/dashboard/top-assets", methods=['GET'])
def top_assets():
    rows = (
        db.session
        .query(Asset.name, func.count(Incident.id))
        .join(Event, Event.asset_id == Asset.id)
        .join(Incident, Incident.event_id == Event.id)
        .group_by(Asset.name)
        .order_by(func.count(Incident.id).desc())
        .limit(5)
        .all()
    )

    return jsonify([
        {
            "asset": r[0],
            "incidents": r[1]
        }

        for r in rows
    ])


@dashboard_bp.route("/dashboard/incidents/timeline", methods=['GET'])
def timeline():
    rows = (
        Incident
        .query
        .with_entities(func.date(Incident.created_at), func.count())
        .group_by(func.date(Incident.created_at))
        .all()
    )

    return jsonify([
        {
            "date": str(r[0]),
            "incidents": r[1]
        }

        for r in rows
    ])


@dashboard_bp.route("/dashboard/incidents/status", methods=['GET'])
def incident_status():
    rows = (
        Incident
        .query
        .with_entities(Incident.status,func.count())
        .group_by(Incident.status)
        .all()
    )

    return jsonify([
        {
            "status": r[0],
            "count": r[1]
        }

        for r in rows
    ])


@dashboard_bp.route("/dashboard/incidents/critical", methods=['GET'])
def active_critical():
    count = (
        Incident
        .query
        .filter(Incident.risk_level == "Critical", Incident.status != "Closed")
        .count()
    )

    return jsonify({ "active_critical": count })


# Mean Time To Resolution
@dashboard_bp.route("/dashboard/incidents/mttr", methods=['GET'])
def mttr():
    incidents = (
        Incident
        .query
        .filter(Incident.closed_at != None)
        .all()
    )

    if not incidents:
        return jsonify({ "mttr_hours": 0 })

    total = 0

    for i in incidents:
        duration = (i.closed_at - i.created_at)
        total += (duration.total_seconds() / 3600)

    return jsonify({
        "mttr_hours": round(total / len(incidents), 2)
    })


@dashboard_bp.route("/dashboard/incidents/recent", methods=['GET'])
def recent_incidents():
    incidents = (
        Incident
        .query
        .order_by(Incident.created_at.desc())
        .limit(10)
        .all()
    )

    return jsonify([
        {
            "id": i.id,
            "status": i.status,
            "risk":i.risk_level,
            "assigned": i.assigned_to,
            "created": i.created_at.isoformat()
        }

        for i in incidents
    ])


@dashboard_bp.route("/dashboard/cia", methods=["GET"])
def cia():
    row = (
        db.session.query(
            func.avg(RiskAssessment.confidentiality),
            func.avg(RiskAssessment.integrity),
            func.avg(RiskAssessment.availability)
        )
        .first()
    )

    return jsonify({
        "confidentiality": round(row[0] or 0, 2),
        "integrity": round(row[1] or 0, 2),
        "availability": round(row[2] or 0, 2)
    })


@dashboard_bp.route("/dashboard/cases", methods=['GET'])
def list_cases():
    rows = (Incident.query.order_by(Incident.created_at.desc()).all())

    return jsonify([
        {
            "id": i.id,
            "label": (
                f"INC-{i.id} | "
                f"{i.risk_level} | "
                f"{i.status}"
            )
        }

        for i in rows
    ])


@dashboard_bp.route("/dashboard/cia/<int:incident_id>", methods=['GET'])
def cia_case(incident_id):
    incident = (Incident.query.get_or_404(incident_id))
    risk = (RiskAssessment.query.filter_by(incident_id=incident.id).first())

    if not risk:
        return jsonify({
            "confidentiality":0,
            "integrity":0,
            "availability":0
        })

    return jsonify({
        "incident":incident.id,
        "confidentiality":risk.confidentiality,
        "integrity":risk.integrity,
        "availability":risk.availability,
        "risk":risk.risk_level
    })