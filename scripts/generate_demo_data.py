import os
import sys
import random

# Adiciona a raiz do projeto ao 'path'
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

from app import create_app
from database import db

from models import User, Asset, Event
from services.detection_engine import analyze_event


app = create_app()


USERS = [
    {
        "username":"ana",
        "role":"analyst",
        "department":"finance"
    },
    {
        "username":"rui",
        "role":"admin",
        "department":"it"
    },
    {
        "username":"joao",
        "role":"user",
        "department":"hr"
    }
]

ASSETS = [
    {
        "name":"FINANCE-PC-01",
        "asset_type":"workstation",
        "department":"finance",
        "criticality":"high"
    },
    {
        "name":"WEB-SERVER",
        "asset_type":"server",
        "department":"it",
        "criticality":"critical"
    },
    {
        "name":"HR-LAPTOP",
        "asset_type":"laptop",
        "department":"hr",
        "criticality":"medium"
    }
]

EVENTS = [
    "USB_CONNECTED",
    "LOGIN",
    "PATCH_MISSING",
    "LOGIN_FAILED",
    "ACCESS_DENIED"
]


with app.app_context():
    print("GENERATING...")

    User.query.delete()
    Asset.query.delete()
    Event.query.delete()
    User.query.delete()

    db.session.commit()

    users = []

    for u in USERS:
        user = User(
            username=u["username"],
            role=u["role"],
            department=u["department"]
        )

        db.session.add(user)
        users.append(user)

    db.session.commit()

    assets = []

    for a in ASSETS:
        asset = Asset(
            name=a["name"],
            asset_type=a["asset_type"],
            department=a["department"],
            criticality=a["criticality"],
            owner="system",
            active=True
        )

        db.session.add(asset)
        assets.append(asset)

    db.session.commit()

    for i in range(300):
        event = Event(
            user_id=random.choice(users).id,
            asset_id=random.choice(assets).id,
            event_type=random.choice(EVENTS),
            description="Generated"
        )

        db.session.add(event)
        db.session.flush()
        analyze_event(event)
        db.session.commit()

    print("DONE")