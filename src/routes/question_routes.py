"""Question CRUD and evaluation routes — questions are independent entities."""
import json

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from src.extensions import db
from src.models.models import Question, QuestionCategory, QuestionDifficulty
from src.schemas import AnswerSubmit, QuestionCreate, QuestionImport, QuestionUpdate
from src.services.auth import token_required
from src.services.evaluator import evaluate_coding, evaluate_general_knowledge, evaluate_multiple_choice

question_bp = Blueprint("questions", __name__, url_prefix="/api/questions")


def _serialize_question(q):
    data = {
        "id": q.id,
        "question_number": q.question_number,
        "category": q.category.value,
        "difficulty": q.difficulty.value,
        "description": q.description,
        "correct_answer": q.correct_answer,
        "hint": q.hint,
        "question_banks": [{"id": b.id, "name": b.name} for b in q.question_banks],
        "times_passed": q.times_passed,
        "times_hint_used": q.times_hint_used,
        "times_incorrect": q.times_incorrect,
        "times_correct": q.times_correct,
        "created_at": q.created_at.isoformat(),
        "updated_at": q.updated_at.isoformat(),
    }
    if q.category == QuestionCategory.MultipleChoice and q.options:
        try:
            data["options"] = json.loads(q.options)
        except json.JSONDecodeError:
            data["options"] = []
    if q.category == QuestionCategory.Coding:
        data["code_sample_input"] = q.code_sample_input
        data["code_sample_output"] = q.code_sample_output
        data["code_hidden_input"] = q.code_hidden_input
        data["code_hidden_output"] = q.code_hidden_output
    return data


def _next_question_number():
    """Get the next global sequential question number."""
    last = Question.query.order_by(Question.question_number.desc()).first()
    return (last.question_number + 1) if last else 1


@question_bp.route("", methods=["GET"])
@token_required
def list_questions():
    """List all questions.
    ---
    tags:
      - Questions
    security:
      - Bearer: []
    responses:
      200:
        description: List of all questions
    """
    questions = Question.query.order_by(Question.question_number).all()
    return jsonify([_serialize_question(q) for q in questions])


@question_bp.route("", methods=["POST"])
@token_required
def create_question():
    """Create a new question (not assigned to any bank yet).
    ---
    tags:
      - Questions
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        schema:
          type: object
          required:
            - category
            - difficulty
            - description
            - correct_answer
          properties:
            category:
              type: string
              enum: [Coding, General, MultipleChoice]
            difficulty:
              type: string
              enum: [Easy, Moderate, Hard]
            description:
              type: string
            correct_answer:
              type: string
            hint:
              type: string
            options:
              type: array
              items:
                type: string
            code_sample_input:
              type: string
            code_sample_output:
              type: string
            code_hidden_input:
              type: string
            code_hidden_output:
              type: string
    responses:
      201:
        description: Question created
    """
    try:
        data = QuestionCreate(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    q = Question(
        question_number=_next_question_number(),
        category=QuestionCategory(data.category),
        difficulty=QuestionDifficulty(data.difficulty),
        description=data.description,
        correct_answer=data.correct_answer,
        hint=data.hint,
        options=json.dumps(data.options) if data.options else None,
        code_sample_input=data.code_sample_input,
        code_sample_output=data.code_sample_output,
        code_hidden_input=data.code_hidden_input,
        code_hidden_output=data.code_hidden_output,
    )
    db.session.add(q)
    db.session.commit()
    return jsonify(_serialize_question(q)), 201


@question_bp.route("/<int:question_id>", methods=["GET"])
@token_required
def get_question(question_id):
    """Get a question by ID.
    ---
    tags:
      - Questions
    security:
      - Bearer: []
    parameters:
      - name: question_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Question details
    """
    q = Question.query.get_or_404(question_id)
    return jsonify(_serialize_question(q))


@question_bp.route("/<int:question_id>", methods=["PUT"])
@token_required
def update_question(question_id):
    """Update a question.
    ---
    tags:
      - Questions
    security:
      - Bearer: []
    parameters:
      - name: question_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Question updated
    """
    q = Question.query.get_or_404(question_id)
    try:
        data = QuestionUpdate(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    if data.category:
        q.category = QuestionCategory(data.category)
    if data.difficulty:
        q.difficulty = QuestionDifficulty(data.difficulty)
    if data.description is not None:
        q.description = data.description
    if data.correct_answer is not None:
        q.correct_answer = data.correct_answer
    if data.hint is not None:
        q.hint = data.hint
    if data.options is not None:
        q.options = json.dumps(data.options)
    if data.code_sample_input is not None:
        q.code_sample_input = data.code_sample_input
    if data.code_sample_output is not None:
        q.code_sample_output = data.code_sample_output
    if data.code_hidden_input is not None:
        q.code_hidden_input = data.code_hidden_input
    if data.code_hidden_output is not None:
        q.code_hidden_output = data.code_hidden_output

    db.session.commit()
    return jsonify(_serialize_question(q))


@question_bp.route("/<int:question_id>", methods=["DELETE"])
@token_required
def delete_question(question_id):
    """Delete a question (removes from all banks too).
    ---
    tags:
      - Questions
    security:
      - Bearer: []
    parameters:
      - name: question_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Question deleted
    """
    q = Question.query.get_or_404(question_id)
    db.session.delete(q)
    db.session.commit()
    return jsonify({"message": "Deleted"})


# --- Evaluation, Hints, Export/Import ---

@question_bp.route("/<int:question_id>/answer", methods=["POST"])
@token_required
def submit_answer(question_id):
    """Submit an answer for evaluation.
    ---
    tags:
      - Questions
    security:
      - Bearer: []
    parameters:
      - name: question_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          type: object
          required:
            - answer
          properties:
            answer:
              type: string
    responses:
      200:
        description: Evaluation result
    """
    q = Question.query.get_or_404(question_id)
    try:
        data = AnswerSubmit(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    if q.category == QuestionCategory.MultipleChoice:
        result = evaluate_multiple_choice(q, data.answer)
    elif q.category == QuestionCategory.General:
        result = evaluate_general_knowledge(q, data.answer)
    elif q.category == QuestionCategory.Coding:
        result = evaluate_coding(q, data.answer)
    else:
        return jsonify({"error": "Unknown question category"}), 400

    return jsonify(result)


@question_bp.route("/<int:question_id>/hint", methods=["GET"])
@token_required
def get_hint(question_id):
    """Get a hint for a question.
    ---
    tags:
      - Questions
    security:
      - Bearer: []
    parameters:
      - name: question_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Hint for the question
    """
    q = Question.query.get_or_404(question_id)

    q.times_hint_used += 1
    db.session.commit()

    hint_data = {"hint": q.hint}

    if q.category == QuestionCategory.MultipleChoice and q.options:
        try:
            options = json.loads(q.options)
            correct = q.correct_answer.strip()
            incorrect = [o for o in options if o.strip() != correct]
            if incorrect:
                removed = incorrect[0]
                remaining = [o for o in options if o != removed]
                hint_data["reduced_options"] = remaining
                hint_data["hint"] = f"One wrong answer removed. Remaining options: {remaining}"
        except json.JSONDecodeError:
            pass
    elif q.category == QuestionCategory.Coding:
        hint_data["sample_input"] = q.code_sample_input
        hint_data["sample_output"] = q.code_sample_output

    return jsonify(hint_data)


@question_bp.route("/export", methods=["GET"])
@token_required
def export_questions():
    """Export all questions as JSON.
    ---
    tags:
      - Questions
    security:
      - Bearer: []
    responses:
      200:
        description: Exported questions
    """
    questions = Question.query.order_by(Question.question_number).all()

    export_data = {"questions": []}
    for q in questions:
        qdata = {
            "question_number": q.question_number,
            "category": q.category.value,
            "difficulty": q.difficulty.value,
            "description": q.description,
            "correct_answer": q.correct_answer,
            "hint": q.hint,
        }
        if q.options:
            try:
                qdata["options"] = json.loads(q.options)
            except json.JSONDecodeError:
                qdata["options"] = []
        if q.category == QuestionCategory.Coding:
            qdata["code_sample_input"] = q.code_sample_input
            qdata["code_sample_output"] = q.code_sample_output
            qdata["code_hidden_input"] = q.code_hidden_input
            qdata["code_hidden_output"] = q.code_hidden_output
        export_data["questions"].append(qdata)

    return jsonify(export_data)


@question_bp.route("/import", methods=["POST"])
@token_required
def import_questions():
    """Import questions from JSON.
    ---
    tags:
      - Questions
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        schema:
          type: object
          required:
            - questions
          properties:
            questions:
              type: array
    responses:
      201:
        description: Questions imported
    """
    try:
        data = QuestionImport(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    imported = []
    for qdata in data.questions:
        q = Question(
            question_number=_next_question_number(),
            category=QuestionCategory(qdata.category),
            difficulty=QuestionDifficulty(qdata.difficulty),
            description=qdata.description,
            correct_answer=qdata.correct_answer,
            hint=qdata.hint,
            options=json.dumps(qdata.options) if qdata.options else None,
            code_sample_input=qdata.code_sample_input,
            code_sample_output=qdata.code_sample_output,
            code_hidden_input=qdata.code_hidden_input,
            code_hidden_output=qdata.code_hidden_output,
        )
        db.session.add(q)
        db.session.flush()
        imported.append(_serialize_question(q))

    db.session.commit()
    return jsonify({"imported": len(imported), "questions": imported}), 201
