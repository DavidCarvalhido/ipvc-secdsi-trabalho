from flask import Blueprint, jsonify
from models import RiskAssessment, Incident, Event


risk_bp = Blueprint("risk_bp", __name__)


# GET ALL RISK ASSESSMENTS
@risk_bp.route("/risk-assessments", methods=["GET"])
def get_risk_assessments():
    assessments = (RiskAssessment.query.all())

    response = []

    for r in assessments:
        incident = Incident.query.get(r.incident_id)
        event = None

        if incident:
            event = Event.query.get(incident.event_id)

        response.append({
            "id": r.id,
            "incident_id": r.incident_id,
            "event_type":
                event.event_type
                if event
                else None,
            "probability": r.probability,
            "impact": r.impact,
            "risk_score": r.risk_score,
            "risk_level": r.risk_level,
            "cia": {
                "confidentiality": r.confidentiality,
                "integrity": r.integrity,
                "availability": r.availability
            }
        })

    return jsonify(response), 200


# GET SINGLE RISK
@risk_bp.route("/risk-assessments/<int:id>", methods=["GET"])
def get_risk_assessment(id):
    r = (RiskAssessment.query.get_or_404(id))
    incident = (Incident.query.get(r.incident_id))
    event = None

    if incident:
        event = Event.query.get(incident.event_id)

    return jsonify({
        "id": r.id,
        "incident_id": r.incident_id,
        "event_type":
            event.event_type
            if event
            else None,
        "probability": r.probability,
        "impact": r.impact,
        "risk_score": r.risk_score,
        "risk_level": r.risk_level,
        "cia": {
            "confidentiality": r.confidentiality,
            "integrity": r.integrity,
            "availability": r.availability
        }
    }), 200