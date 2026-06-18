import os
import sys

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


CASES = {
    1:{
        "name":"USB Restricted",
        "user":"rui",
        "asset":"FINANCE-PC-01",
        "event":"USB_CONNECTED"
    },

    2:{
        "name":"After Hours Login",
        "user":"rui",
        "asset":"WEB-SERVER",
        "event":"LOGIN"
    },

    3:{
        "name":"Patch Missing",
        "user":"rui",
        "asset":"WEB-SERVER",
        "event":"PATCH_MISSING"
    },

    4:{
        "name":"Brute Force",
        "user":"rui",
        "asset":"WEB-SERVER",
        "event":"LOGIN_FAILED"
    },

    5:{
        "name":"Cross Department",
        "user":"joao",
        "asset":"FINANCE-PC-01",
        "event":"ACCESS_DENIED"
    }
}


with app.app_context():
    print()

    for k,v in CASES.items():
        print(k, "-", v["name"])

    option = int(input("\nCase: "))

    case = CASES[option]
    user = (User.query.filter_by(username=case["user"]).first())
    asset = (Asset.query.filter_by(name=case["asset"]).first())

    if not user:
        print("User not found")
        exit()

    if not asset:
        print("Asset not found")
        exit()

    event = Event(
        user_id=user.id,
        asset_id=asset.id,
        event_type=case["event"],
        description=case["name"]
    )

    db.session.add(event)
    db.session.commit()

    incident = (analyze_event(event))

    print()
    print("CASE EXECUTED")

    if incident:
        print(incident.id)