from app import db
from models import AuditLog


def audit(entity, entity_id, action, actor, details):
    log = AuditLog(
        entity=entity,
        entity_id=entity_id,
        action=action,
        actor=actor,
        details=details
    )

    db.session.add(log)