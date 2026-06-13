from models import Incident, RiskAssessment
from app import db
from services.risk_engine import evaluate_event


def analyze_event(event):

    result = evaluate_event(event)

    # só criamos incidente se risco for relevante
    if result["risk_level"] in ["High", "Critical", "Medium"]:

        incident = Incident(
            event_id=event.id,
            severity=result["risk_level"],
            risk_level=result["risk_level"]
        )

        db.session.add(incident)
        db.session.commit()

        assessment = RiskAssessment(
            incident_id=incident.id,
            probability=result["probability"],
            impact=result["impact"],
            risk_score=result["score"],
            risk_level=result["risk_level"],
            confidentiality=result["cia"]["C"],
            integrity=result["cia"]["I"],
            availability=result["cia"]["A"]
        )

        db.session.add(assessment)
        db.session.commit()

        return incident

    return None