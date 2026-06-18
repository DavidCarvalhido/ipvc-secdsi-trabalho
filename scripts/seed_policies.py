import os
import sys

# Adiciona a raiz do projeto ao 'path'
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from app import create_app
from database import db
from models import Policy, Control


app = create_app()


POLICIES = [
    {
        "name":"USB Critical",
        "description":"USB em IT",
        "event_type":"USB_CONNECTED",
        "department":"it",
        "asset_type":"workstation",
        "minimum_criticality":"high",
        "enabled":True,
        "allowed_start_hour":8,
        "allowed_end_hour":18,
        "probability":5,
        "impact":5,
        "confidentiality":5,
        "integrity":5,
        "availability":4
    },
    {
        "name":"Login After Hours",
        "description":"Login fora horário",
        "event_type":"LOGIN",
        "department":"it",
        "asset_type":"server",
        "minimum_criticality":"medium",
        "enabled":True,
        "allowed_start_hour":8,
        "allowed_end_hour":20,
        "probability":3,
        "impact":3,
        "confidentiality":3,
        "integrity":2,
        "availability":2
    },
    {
        "name":"Patch Required",
        "description":"Servidor sem patch",
        "event_type":"PATCH_MISSING",
        "department":"it",
        "asset_type":"server",
        "minimum_criticality":"critical",
        "enabled":True,
        "probability":5,
        "impact":4,
        "confidentiality":3,
        "integrity":5,
        "availability":5
    },
    {
        "name":"Brute Force",
        "description":"Falhas sucessivas",
        "event_type":"LOGIN_FAILED",
        "department":"it",
        "asset_type":"server",
        "minimum_criticality":"critical",
        "enabled":True,
        "probability":5,
        "impact":5,
        "confidentiality":5,
        "integrity":4,
        "availability":3
    },
    {
        "name":"Cross Department Access",
        "description":"Acesso não autorizado",
        "event_type":"ACCESS_DENIED",
        "department":"finance",
        "asset_type":"workstation",
        "minimum_criticality":"high",
        "enabled":True,
        "probability":4,
        "impact":5,
        "confidentiality":5,
        "integrity":5,
        "availability":2
    }
]


with app.app_context():
    print("Creating policies...")
    
    for p in POLICIES:
        exists = (
            Policy
            .query
            .filter_by(name=p["name"])
            .first()
        )

        if exists:
            continue

        policy = Policy(
            name=p["name"],
            description=p["description"],
            event_type=p["event_type"],
            department=p["department"],
            asset_type=p["asset_type"],
            minimum_criticality=p["minimum_criticality"],
            enabled=p["enabled"],
            allowed_start_hour=p.get("allowed_start_hour"),
            allowed_end_hour=p.get("allowed_end_hour"),
            probability=p["probability"],
            impact=p["impact"],
            confidentiality=p["confidentiality"],
            integrity=p["integrity"],
            availability=p["availability"]
        )

        db.session.add(policy)

    db.session.commit()

    print("Policies created")