"""Authentication routes for JWT token management."""
from flask import Blueprint, jsonify

from src.services.auth import generate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/token", methods=["POST"])
def get_token():
    """Generate a JWT token.
    ---
    tags:
      - Authentication
    responses:
      200:
        description: JWT token generated
        schema:
          type: object
          properties:
            token:
              type: string
    """
    token = generate_token()
    return jsonify({"token": token})
