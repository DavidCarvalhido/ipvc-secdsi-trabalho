from flask import Blueprint, jsonify, request
from database import db
from datetime import datetime
from models import Incident, IncidentAction, Event
from services.audit_service import audit

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
            #"event_type": event.event_type if event else None,
            "severity": i.severity,
            "risk_level": i.risk_level,
            "status": i.status,
            "assigned_to": i.assigned_to,
            "created_at": i.created_at.isoformat() if i.created_at else None,
            "closed_at": i.closed_at.isoformat() if i.closed_at else None
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


@incident_bp.route("/incidents/<int:id>", methods=['PATCH'])
def update_incident_status(id):
    incident = Incident.query.get_or_404(id)
    data = request.json

    audit(
        entity="incident",
        entity_id=incident.id,
        action="update",
        actor=data.get("assigned_to", "system"),
        details=str(data)
    )

    if "status" in data:
        incident.status = (data["status"])
        if (data["status"] == "Closed"):
            incident.closed_at = (datetime.utcnow())

    if ("assigned_to" in data):
        incident.assigned_to = (data["assigned_to"])

    if ("resolution" in data):
        incident.resolution = (data["resolution"])

    db.session.commit()

    return jsonify({
        "message": "incident updated"
    }), 200


@incident_bp.route("/incidents/<int:id>/actions", methods=['POST'])
def add_action(id):
    incident = Incident.query.get_or_404(id)
    data = request.json

    action = IncidentAction(
        incident_id=id,
        action=data["action"],
        notes=data.get("notes"),
        performed_by=data.get("performed_by")
    )

    db.session.add(action)
    db.session.commit()

    return jsonify({
        "message": "action added"
    })


@incident_bp.route("/incidents/<int:id>/actions", methods=['GET'])
def get_actions(id):
    actions = IncidentAction.query.filter_by(incident_id=id).all()

    return jsonify([
        {
            "action": a.action,
            "notes": a.notes,
            "performed_by": a.performed_by,
            "timestamp": a.timestamp
        }

        for a in actions
    ])


# MANUAL create incident (para testes)
@incident_bp.route("/incidents", methods=['POST'])
def create_incident():
    data = request.json

    incident = Incident(
        event_id=data["event_id"],
        severity=data.get("severity", "medium"),
        risk_level=data.get("risk_level", "medium"),
        # probability=data.get("probability", "medium"),
        # impact=data.get("impact", "medium")
    )

    db.session.add(incident)
    db.session.commit()

    return jsonify({
        "message": "Incident created",
        "incident_id": incident.id
    }), 201