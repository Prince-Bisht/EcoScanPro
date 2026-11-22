from flask import Blueprint,jsonify
from services.news_service import get_news
bp=Blueprint('news',__name__)
@bp.get('/api/news')
def news(): return jsonify(get_news())
