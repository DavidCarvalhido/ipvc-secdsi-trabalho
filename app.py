from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from config import Config
from database import db

#db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    print(id(db))
    from models import User, Event, Incident
    print(id(db))

    with app.app_context():
        print(db.metadata.tables.keys())
        db.create_all()

    from routes.user_routes import user_bp
    from routes.event_routes import event_bp
    from routes.incident_routes import incident_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(incident_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)