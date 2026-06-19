from flask import Blueprint, request, jsonify
from database import db
from models import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json

    user = User(
        username=data['username'],
        role=data.get('role', 'user'),
        department=data.get('department', 'unknown')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "department": u.department
        } for u in users
    ])