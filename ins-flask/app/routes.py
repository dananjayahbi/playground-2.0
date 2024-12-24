# flask_app/app/routes.py
from flask import Blueprint, request, jsonify
from app.models import db, Quote

bp = Blueprint('routes', __name__)

@bp.route('/add_quote', methods=['POST'])
def add_quote():
    data = request.json
    if 'text' not in data or not data['text']:
        return jsonify({'error': 'Text is required'}), 400
    
    char_count = len(data['text'])
    quote = Quote(text=data['text'], char_count=char_count)
    db.session.add(quote)
    db.session.commit()
    return jsonify({'id': quote.id, 'text': quote.text, 'char_count': char_count, 'created_at': quote.created_at})

@bp.route('/get_quotes', methods=['GET'])
def get_quotes():
    quotes = Quote.query.all()
    return jsonify([{'id': q.id, 'text': q.text, 'char_count': q.char_count, 'created_at': q.created_at} for q in quotes])

@bp.route('/get_quote/<int:quote_id>', methods=['GET'])
def get_quote(quote_id):
    quote = Quote.query.get(quote_id)
    if not quote:
        return jsonify({'error': 'Quote not found'}), 404
    return jsonify({'id': quote.id, 'text': quote.text, 'char_count': quote.char_count, 'created_at': quote.created_at})

@bp.route('/delete_quote/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    quote = Quote.query.get(quote_id)
    if not quote:
        return jsonify({'error': 'Quote not found'}), 404
    db.session.delete(quote)
    db.session.commit()
    return jsonify({'message': 'Quote deleted'})
