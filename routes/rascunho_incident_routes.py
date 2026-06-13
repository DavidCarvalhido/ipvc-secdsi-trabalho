from flask import Blueprint, jsonify, request
from app import db
from models import Incident, Event

incident_bp = Blueprint('incident_bp', __name__)


# GET all incidents
@incident_bp.route("/incidents", methods=['GET'])
def get_incidents():
    incidents = Incident.query.all()

    result = []

    for i in incidents:
        event = Event.query.get(i.event_id)

        result.append({
            "id": i.id,
            "event_id": i.event_id,
            "event_type": event.event_type if event else None,
            "severity": i.severity,
            "risk_level": i.risk_level,
            "probability": i.probability,
            "impact": i.impact,
            "created_at": i.created_at.isoformat() if i.created_at else None
        })

    return jsonify(result), 200


# GET single incident
@incident_bp.route("/incidents/<int:incident_id>", methods=['GET'])
def get_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    event = Event.query.get(incident.event_id)

    return jsonify({
        "id": incident.id,
        "event_id": incident.event_id,
        "event_type": event.event_type if event else None,
        "severity": incident.severity,
        "risk_level": incident.risk_level,
        "probability": incident.probability,
        "impact": incident.impact,
        "created_at": incident.created_at.isoformat() if incident.created_at else None
    })


# UPDATE incident (status ou risco)
@incident_bp.route("/incidents/<int:incident_id>", methods=['PUT'])
def update_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    data = request.json

    if "severity" in data:
        incident.severity = data["severity"]

    if "risk_level" in data:
        incident.risk_level = data["risk_level"]

    if "probability" in data:
        incident.probability = data["probability"]

    if "impact" in data:
        incident.impact = data["impact"]

    db.session.commit()

    return jsonify({"message": "Incident updated"}), 200


# DELETE incident
@incident_bp.route("/incidents/<int:incident_id>", methods=['DELETE'])
def delete_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)

    db.session.delete(incident)
    db.session.commit()

    return jsonify({"message": "Incident deleted"}), 200


# MANUAL create incident (para testes)
@incident_bp.route("/incidents", methods=['POST'])
def create_incident():
    data = request.json

    incident = Incident(
        event_id=data["event_id"],
        severity=data.get("severity", "medium"),
        risk_level=data.get("risk_level", "medium"),
        probability=data.get("probability", "medium"),
        impact=data.get("impact", "medium")
    )

    db.session.add(incident)
    db.session.commit()

    return jsonify({
        "message": "Incident created",
        "incident_id": incident.id
    }), 201



from flask import Blueprint, jsonify, request
from database import db
from models import Incident

incident_bp = Blueprint('incident_bp', __name__)


# GET all incidents
@incident_bp.route('/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()

    return jsonify([
        {
            "id": i.id,
            "event_id": i.event_id,
            "severity": i.severity,
            "risk_level": i.risk_level,
            "probability": i.probability,
            "impact": i.impact,
            "created_at": i.created_at.isoformat() if i.created_at else None
        }
        for i in incidents
    ]), 200


# GET single incident
@incident_bp.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)

    return jsonify({
        "id": incident.id,
        "event_id": incident.event_id,
        "severity": incident.severity,
        "risk_level": incident.risk_level,
        "probability": incident.probability,
        "impact": incident.impact,
        "created_at": incident.created_at.isoformat() if incident.created_at else None
    }), 200


# DELETE incident (useful for admin / false positives)
@incident_bp.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)

    db.session.delete(incident)
    db.session.commit()

    return jsonify({"message": "Incident deleted"}), 200


# UPDATE incident (ex: manual risk adjustment)
@incident_bp.route('/incidents/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    data = request.json
    incident = Incident.query.get_or_404(incident_id)

    incident.severity = data.get("severity", incident.severity)
    incident.risk_level = data.get("risk_level", incident.risk_level)
    incident.probability = data.get("probability", incident.probability)
    incident.impact = data.get("impact", incident.impact)

    db.session.commit()

    return jsonify({"message": "Incident updated"}), 200