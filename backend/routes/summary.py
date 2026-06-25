from flask import Blueprint, jsonify
from models import User

summary_bp = Blueprint('summary', __name__)

@summary_bp.route('/summary/<user_id>', methods=['GET'])
def get_summary(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": user.id,
        "balance": user.balance,
        "total_credits": user.total_credits,
        "total_debits": user.total_debits,
        "transaction_count": user.transaction_count,
        "member_since": user.created_at.isoformat()
    }), 200