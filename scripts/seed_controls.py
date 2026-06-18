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


with app.app_context():
    policies = Policy.query.all()

    print("Creating controls...")

    for p in policies:
        exists = (
            Control
            .query
            .filter_by(policy_id=p.id)
            .first()
        )

        if exists:
            continue

        control = Control(
            name=f"{p.name} Control",
            description=f"Generated from {p.name}",
            policy_id=p.id,
            control_type="Preventive",
            active=True
        )

        db.session.add(control)

    db.session.commit()

    print("Controls created")