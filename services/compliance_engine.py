from models import Control, ComplianceResult
from database import db


def evaluate_control(event, policy):
    controls = Control.query.filter_by(policy_id=policy.id, active=True).all()
    results = []

    for control in controls:
        passed = (event.event_type == policy.event_type)
        
        result = ComplianceResult(
            event_id=event.id,
            policy_id=policy.id,
            control_id=control.id,
            compliant=passed,
            reason="Control validated"
            #reason="OK" if compliant else "Policy violation"
        )

        db.session.add(result)

        results.append(result)

    return results