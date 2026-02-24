"""Question Bank CRUD and question assignment routes."""

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from src.extensions import db
from src.models.models import Question, QuestionBank
from src.routes.question_routes import _serialize_question
from src.schemas import BankAssignQuestions, QuestionBankCreate, QuestionBankUpdate
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
    """Delete a question bank (does not delete the questions themselves).
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


# --- Question assignment to banks ---

@bank_bp.route("/<int:bank_id>/questions", methods=["GET"])
@token_required
def list_bank_questions(bank_id):
    """List all questions assigned to a bank.
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
        description: List of questions in this bank
    """
    bank = QuestionBank.query.get_or_404(bank_id)
    return jsonify([_serialize_question(q) for q in bank.questions])


@bank_bp.route("/<int:bank_id>/questions", methods=["POST"])
@token_required
def assign_questions(bank_id):
    """Assign questions to a bank.
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
          required:
            - question_ids
          properties:
            question_ids:
              type: array
              items:
                type: integer
    responses:
      200:
        description: Questions assigned to bank
    """
    bank = QuestionBank.query.get_or_404(bank_id)
    try:
        data = BankAssignQuestions(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    added = []
    already = []
    not_found = []
    for qid in data.question_ids:
        q = Question.query.get(qid)
        if not q:
            not_found.append(qid)
            continue
        if q in bank.questions:
            already.append(qid)
            continue
        bank.questions.append(q)
        added.append(qid)

    db.session.commit()
    return jsonify({
        "assigned": added,
        "already_assigned": already,
        "not_found": not_found,
    })


@bank_bp.route("/<int:bank_id>/questions", methods=["DELETE"])
@token_required
def unassign_questions(bank_id):
    """Remove questions from a bank (does not delete the questions).
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
          required:
            - question_ids
          properties:
            question_ids:
              type: array
              items:
                type: integer
    responses:
      200:
        description: Questions removed from bank
    """
    bank = QuestionBank.query.get_or_404(bank_id)
    try:
        data = BankAssignQuestions(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    removed = []
    not_in_bank = []
    for qid in data.question_ids:
        q = Question.query.get(qid)
        if q and q in bank.questions:
            bank.questions.remove(q)
            removed.append(qid)
        else:
            not_in_bank.append(qid)

    db.session.commit()
    return jsonify({"removed": removed, "not_in_bank": not_in_bank})


@bank_bp.route("/<int:bank_id>/questions/export", methods=["GET"])
@token_required
def export_bank_questions(bank_id):
    """Export all questions from a bank as JSON.
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
        description: Exported questions for this bank
    """
    bank = QuestionBank.query.get_or_404(bank_id)
    return jsonify({
        "bank_name": bank.name,
        "questions": [_serialize_question(q) for q in bank.questions],
    })
