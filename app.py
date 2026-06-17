from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from config import Config
from database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    print(id(db))
    from models import User, Event, Asset, \
                    Policy, Control, Incident
    print(id(db))

    with app.app_context():
        print(db.metadata.tables.keys())
        db.create_all()

    from routes.user_routes import user_bp
    from routes.event_routes import event_bp
    from routes.asset_routes import asset_bp
    from routes.policy_routes import policy_bp
    from routes.control_routes import control_bp
    from routes.compliance_routes import compliance_bp
    from routes.incident_routes import incident_bp
    from routes.risk_routes import risk_bp
    from routes.evidence_routes import evidence_bp
    from routes.audit_routes import audit_bp
    from routes.dashboard_routes import dashboard_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(asset_bp)
    app.register_blueprint(policy_bp)
    app.register_blueprint(control_bp)
    app.register_blueprint(compliance_bp)
    app.register_blueprint(incident_bp)
    app.register_blueprint(risk_bp)
    app.register_blueprint(evidence_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(dashboard_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)