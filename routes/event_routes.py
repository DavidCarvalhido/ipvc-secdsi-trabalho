from flask import Blueprint, request, jsonify
from app import db
from models import Event
from services.detection_engine import analyze_event

event_bp = Blueprint('event_bp', __name__)


# POST an event
@event_bp.route('/events', methods=['POST'])
def create_event():
    data = request.json

    event = Event(
        user_id=data['user_id'],
        asset_id=data["asset_id"],
        event_type=data['event_type'],
        description=data.get('description', '')
    )

    db.session.add(event)
    db.session.commit()

    analyze_event(event)  # aqui entra a inteligência

    return jsonify({"message": "Event recorded"}), 201


# GET all events (development test)
@event_bp.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()

    return jsonify([
        {
            "id": e.id,
            "user_id": e.user_id,
            "event_type": e.event_type,
            "description": e.description,
            "time": e.timestamp
        } for e in events
    ])