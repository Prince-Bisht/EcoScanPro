from flask import Blueprint,request,jsonify
from services.chatbot_service import answer
bp=Blueprint('chatbot',__name__)
@bp.post('/api/chat')
def chat():
    body=request.get_json(silent=True) or {}; msg=body.get('message',''); history=body.get('history',[])
    if not isinstance(msg,str) or not msg.strip() or len(msg)>2000: return jsonify(error='Message must contain 1–2000 characters'),400
    if not isinstance(history,list): return jsonify(error='History must be a list'),400
    return jsonify(answer(msg.strip(),history))
