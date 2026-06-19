from flask import Blueprint, request, jsonify
from database import db
from models import Control


control_bp = Blueprint("control_bp", __name__)


# POST a control
@control_bp.route("/controls", methods=["POST"])
def create_control():
    data = request.json

    control = Control(
        name=data["name"],
        description=data.get("description"),
        policy_id=data["policy_id"],
        control_type=data.get("control_type")
    )

    db.session.add(control)
    db.session.commit()

    print("** CONTROL CREATED **")

    return jsonify({ "message":"control created" })


# GET all events (development test)
@control_bp.route('/controls', methods=['GET'])
def get_econtrols():
    controls = Control.query.all()

    return jsonify([
        {
            "id": c.id,
            "description": c.description,
            "policy_id": c.policy_id,
            "control_type": c.control_type,
            "active": c.active
        } for c in controls
    ])