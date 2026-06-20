from models import Incident, RiskAssessment, ComplianceResult, Evidence, AuditLog
from sqlalchemy import func
from database import db


def get_executive_report():
    return {
        "incidents": Incident.query.count(),
        "risk_assessments": RiskAssessment.query.count(),
        "compliance": ComplianceResult.query.count(),
        "evidence": Evidence.query.count(),
        "audit_logs": AuditLog.query.count()
    }


def get_incident_report():
    incidents = Incident.query.all()

    return {
        "total": len(incidents),
        "critical": len([i for i in incidents if i.risk_level == "Critical"]),
        "open": len([i for i in incidents if i.status == "Open"]),
        "closed": len([i for i in incidents if i.status == "Closed"])
    }


def get_compliance_report():
    items = ComplianceResult.query.all()
    total = len(items)

    compliant = len([x for x in items if x.compliant])
    violations = total - compliant

    return {
        "total": total,
        "compliant": compliant,
        "violations": violations,
        "score": round((compliant / max(total, 1)) * 100, 2)
    }


def get_risk_report():
    risks = RiskAssessment.query.all()

    if not risks:
        return {
            "average_score": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }

    return {
        "average_score": round(sum(r.risk_score for r in risks) / len(risks), 2),
        "critical": len([r for r in risks if r.risk_level == "Critical"]),
        "high": len([r for r in risks if r.risk_level == "High"]),
        "medium": len([r for r in risks if r.risk_level == "Medium"]),
        "low": len([r for r in risks if r.risk_level == "Low"])
    }


def get_full_report():
    return {
        "executive": get_executive_report(),
        "incidents": get_incident_report(),
        "compliance": get_compliance_report(),
        "risk": get_risk_report()
    }


def build_cia_table():
    rows = (RiskAssessment.query.all())
    data = []

    for r in rows:
        data.append([
            f"INC-{r.incident_id}",
            r.confidentiality,
            r.integrity,
            r.availability,
            r.risk_level
        ])

    return data