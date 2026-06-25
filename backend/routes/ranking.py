from flask import Blueprint, jsonify
from models import User
from datetime import datetime

ranking_bp = Blueprint('ranking', __name__)

def calculate_score(user):
    
    volume_score = (user.total_credits + user.total_debits) * 0.4
    
    txn_score = user.transaction_count * 10 * 0.3

    age_days = (datetime.utcnow() - user.created_at).days + 1
    age_score = age_days * 5 * 0.2

    balance_score = max(user.balance, 0) * 0.1

    return round(volume_score + txn_score + age_score + balance_score, 2)

@ranking_bp.route('/ranking', methods=['GET'])
def get_ranking():
    users = User.query.all()

    if not users:
        return jsonify({"message": "No users found"}), 404

    ranked = []
    for user in users:
        score = calculate_score(user)
        ranked.append({
            "user_id": user.id,
            "score": score,
            "balance": user.balance,
            "total_credits": user.total_credits,
            "total_debits": user.total_debits,
            "transaction_count": user.transaction_count
        })

    ranked.sort(key=lambda x: x['score'], reverse=True)

    for i, user in enumerate(ranked):
        user['rank'] = i + 1

    return jsonify(ranked), 200