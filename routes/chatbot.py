
from flask import Blueprint, request, jsonify
from services.chatbot_service import answer

bp = Blueprint("chatbot", __name__)


@bp.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True)

    if not isinstance(body, dict):
        return jsonify(error="Invalid JSON request"), 400

    message = body.get("message", "")
    history = body.get("history", [])

    if not isinstance(message, str) or not message.strip():
        return jsonify(error="Message cannot be empty"), 400

    if len(message) > 2000:
        return jsonify(error="Message is too long"), 400

    if not isinstance(history, list):
        return jsonify(error="Invalid chat history"), 400

    result = answer(message.strip(), history)

    return jsonify(result)
