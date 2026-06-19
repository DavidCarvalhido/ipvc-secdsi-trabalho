from models import Incident, RiskAssessment
from database import db
from services.policy_engine import find_policies
from services.risk_engine import calculate_risk_score, classify_risk
from services.compliance_engine import evaluate_control
from services.evidence_engine import create_evidence
from services.audit_engine import create_audit_log


def analyze_event(event):
    policies = find_policies(event)

    if not policies:
        print("NO POLICY FOUND")
        return None

    highest_score = 0
    highest_level = "Low"

    #score = calculate_risk_score(policy.probability, policy.impact)
    #incident = Incident(event_id=event.id, severity=classify_risk(score), risk_level=classify_risk(score))
    incident = Incident(event_id=event.id, severity="Low", risk_level="Low")

    db.session.add(incident)
    db.session.flush()

    for policy in policies:
        # compliance
        compliance_results = evaluate_control(event, policy)
        score = calculate_risk_score(policy.probability, policy.impact)
        level = classify_risk(score)

        print(f"Compliance created: {len(compliance_results)}")

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

        create_evidence(incident, event, policy)
        
        create_audit_log(
            entity="incident",
            entity_id=incident.id,
            action="CREATED",
            details=f"""
                    Event:{event.event_type}
                    Policy:{policy.name}
                    Risk:{level}
                    """
            )

        db.session.add(assessment)

    incident.severity = highest_level
    incident.risk_level = highest_level

    db.session.commit()

    return incident