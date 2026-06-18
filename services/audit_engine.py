from database import db
from models import AuditLog


def create_audit_log(entity, entity_id, action, details, actor="system"):
    log = AuditLog(
        entity=entity,
        entity_id=entity_id,
        action=action,
        actor=actor,
        details=details
    )

    db.session.add(log)

    return log