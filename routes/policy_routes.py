from flask import Blueprint, request, jsonify
from database import db
from models import Policy

policy_bp = Blueprint("policy_bp", __name__)

# POST a policy
@policy_bp.route("/policies", methods=["POST"])
def create_policy():
    data = request.json

    policy = Policy(
        name=data["name"],
        description=data.get("description"),
        event_type=data["event_type"],
        enabled=True,
        department=data.get("department"),
        allowed_start_hour=data.get("allowed_start_hour"),
        allowed_end_hour=data.get("allowed_end_hour"),
        device_whitelist=data.get("device_whitelist"),
        probability=data["probability"],
        impact=data["impact"],
        confidentiality=data["confidentiality"],
        integrity=data["integrity"],
        availability=data["availability"]
    )

    db.session.add(policy)
    db.session.commit()

    return jsonify({ "message": "Policy created" }), 201


# GET all policies (development test)
@policy_bp.route('/policies', methods=['GET'])
def get_policies():
    policies = Policy.query.all()

    return jsonify([
        {
            "id": p.id,
            "description": p.description,
            "event_type": p.event_type,
            "enabled": p.enabled,
            "department": p.department,
            "allowed_start_hour": p.allowed_start_hour,
            "impact": p.impact
        } for p in policies
    ])