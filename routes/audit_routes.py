from flask import Blueprint, jsonify
from models import AuditLog


audit_bp = Blueprint("audit_bp", __name__)


@audit_bp.route("/audit", methods=['GET'])
def get_logs():
    logs = (AuditLog.query.order_by(AuditLog.timestamp.desc()).all())

    return jsonify([
        {
            "entity": l.entity,
            "entity_id": l.entity_id,
            "action": l.action,
            "actor": l.actor,
            "details": l.details,
            "timestamp": l.timestamp.isoformat()
        }

        for l in logs
    ])