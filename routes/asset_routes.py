from flask import Blueprint, request, jsonify
from database import db
from models import Asset


asset_bp = Blueprint("asset_bp", __name__)


# POST an asset
@asset_bp.route("/assets", methods=["POST"])
def create_asset():
    data = request.json

    asset = Asset(
        name=data["name"],
        asset_type=data["asset_type"],
        department=data.get("department"),
        criticality=data["criticality"],
        owner=data.get("owner")
    )

    db.session.add(asset)
    db.session.commit()

    return jsonify({
        "message": "asset created",
        "id": asset.id
    })


# GET all assets
@asset_bp.route("/assets", methods=["GET"])
def get_assets():
    assets = Asset.query.all()

    return jsonify([
        {
            "id": a.id,
            "name": a.name,
            "type": a.asset_type,
            "criticality": a.criticality,
            "department": a.department
        }
        for a in assets
    ])