from models import Incident, RiskAssessment
from app import db
from services.policy_engine import find_policies
from services.risk_engine import calculate_risk_score, classify_risk


def analyze_event(event):
    policies = find_policies(event)

    if not policies:
        return

    highest_score = 0
    highest_level = "Low"

    #score = calculate_risk_score(policy.probability, policy.impact)
    #incident = Incident(event_id=event.id, severity=classify_risk(score), risk_level=classify_risk(score))
    incident = Incident(event_id=event.id, severity="Low", risk_level="Low")

    db.session.add(incident)
    db.session.flush()

    for policy in policies:
        score = calculate_risk_score(policy.probability, policy.impact)
        level = classify_risk(score)

        if score > highest_score:
            highest_score = score
            highest_level = level

        assessment = RiskAssessment(
            incident_id=incident.id,
            probability=policy.probability,
            impact=policy.impact,
            risk_score=score,
            risk_level=level,
            confidentiality=policy.confidentiality,
            integrity=policy.integrity,
            availability=policy.availability
        )

        db.session.add(assessment)

    incident.severity = highest_level
    incident.risk_level = highest_level

    db.session.commit()