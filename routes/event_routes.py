from flask import Blueprint, request, jsonify
from app import db
from models import Event
from services.detection_engine import analyze_event

event_bp = Blueprint('event_bp', __name__)

@event_bp.route('/events', methods=['POST'])
def create_event():
    data = request.json

    event = Event(
        user_id=data['user_id'],
        event_type=data['event_type'],
        description=data.get('description', '')
    )

    db.session.add(event)
    db.session.commit()

    analyze_event(event)  # aqui entra a inteligência

    return jsonify({"message": "Event recorded"}), 201