from flask import Blueprint, request, jsonify
from database import db
from models import Evidence, Incident


evidence_bp = Blueprint("evidence_bp", __name__)


@evidence_bp.route("/incidents/<int:id>/evidence", methods=['POST'])
def add_evidence(id):
    Incident.query.get_or_404(id)

    data = request.json

    evidence = Evidence(
        incident_id=id,
        evidence_type=data["type"],
        title=data["title"],
        content=data["content"],
        created_by=data.get("created_by")
    )

    db.session.add(evidence)
    db.session.commit()

    return jsonify({
        "message": "evidence added"
    })


@evidence_bp.route("/incidents/<int:id>/evidence", methods=['GET'])
def get_evidence(id):
    evidence = (Evidence.query.filter_by(incident_id=id).all())

    return jsonify([
        {
            "id": e.id,
            "type": e.evidence_type,
            "title": e.title,
            "content": e.content,
            "created_by": e.created_by,
            "created_at": e.created_at.isoformat()
        }

        for e in evidence
    ])


# GET all evidences
@evidence_bp.route("/evidence", methods=['GET'])
def all_evidence():
    evidence = Evidence.query.all()

    return jsonify([
        {
            "id": e.id,
            "type": e.evidence_type,
            "title": e.title,
            "content": e.content,
            "created_by": e.created_by,
            "created_at": e.created_at.isoformat()
        }
        for e in evidence
    ])