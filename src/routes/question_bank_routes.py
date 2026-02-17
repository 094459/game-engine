"""Question Bank CRUD routes."""
import json

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from src.extensions import db
from src.models.models import Question, QuestionBank, QuestionCategory, QuestionDifficulty
from src.schemas import QuestionBankCreate, QuestionBankUpdate
from src.services.auth import token_required

bank_bp = Blueprint("banks", __name__, url_prefix="/api/banks")


def _serialize_bank(bank):
    return {
        "id": bank.id,
        "name": bank.name,
        "question_count": len(bank.questions),
        "created_at": bank.created_at.isoformat(),
        "updated_at": bank.updated_at.isoformat(),
    }


@bank_bp.route("", methods=["GET"])
@token_required
def list_banks():
    """List all question banks.
    ---
    tags:
      - Question Banks
    security:
      - Bearer: []
    responses:
      200:
        description: List of question banks
    """
    banks = QuestionBank.query.all()
    return jsonify([_serialize_bank(b) for b in banks])


@bank_bp.route("", methods=["POST"])
@token_required
def create_bank():
    """Create a new question bank.
    ---
    tags:
      - Question Banks
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
    responses:
      201:
        description: Question bank created
    """
    try:
        data = QuestionBankCreate(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    if QuestionBank.query.filter_by(name=data.name).first():
        return jsonify({"error": "A bank with this name already exists"}), 409

    bank = QuestionBank(name=data.name)
    db.session.add(bank)
    db.session.commit()
    return jsonify(_serialize_bank(bank)), 201


@bank_bp.route("/<int:bank_id>", methods=["GET"])
@token_required
def get_bank(bank_id):
    """Get a question bank by ID.
    ---
    tags:
      - Question Banks
    security:
      - Bearer: []
    parameters:
      - name: bank_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Question bank details
    """
    bank = QuestionBank.query.get_or_404(bank_id)
    return jsonify(_serialize_bank(bank))


@bank_bp.route("/<int:bank_id>", methods=["PUT"])
@token_required
def update_bank(bank_id):
    """Update a question bank.
    ---
    tags:
      - Question Banks
    security:
      - Bearer: []
    parameters:
      - name: bank_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          type: object
          properties:
            name:
              type: string
    responses:
      200:
        description: Question bank updated
    """
    bank = QuestionBank.query.get_or_404(bank_id)
    try:
        data = QuestionBankUpdate(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    if data.name:
        bank.name = data.name
    db.session.commit()
    return jsonify(_serialize_bank(bank))


@bank_bp.route("/<int:bank_id>", methods=["DELETE"])
@token_required
def delete_bank(bank_id):
    """Delete a question bank.
    ---
    tags:
      - Question Banks
    security:
      - Bearer: []
    parameters:
      - name: bank_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Question bank deleted
    """
    bank = QuestionBank.query.get_or_404(bank_id)
    db.session.delete(bank)
    db.session.commit()
    return jsonify({"message": "Deleted"})
