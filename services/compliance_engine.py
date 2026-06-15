from models import Control, ComplianceResult
from app import db


def evaluate_control(event, policy):
    controls = Control.query.filter_by(policy_id=policy.id, active=True).all()
    results = []

    for control in controls:
        result = ComplianceResult(
            event_id=event.id,
            policy_id=policy.id,
            control_id=control.id,
            compliant=False,
            reason="Policy violation"
        )

        db.session.add(result)

        results.append(result)

    return results