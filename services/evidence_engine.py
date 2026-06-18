from database import db
from models import Evidence


def create_evidence(incident, event, policy):
    evidence = Evidence(
        incident_id=incident.id,
        evidence_type="system",
        title=f"{event.event_type} Evidence",
        content=(f"""
                 Event:{event.event_type}
                 Policy:{policy.name}
                 User:{event.user_id}
                 Asset:{event.asset_id}
                 Risk:{incident.risk_level}
                """
        ),

        created_by="system"
    )

    db.session.add(evidence)

    return evidence