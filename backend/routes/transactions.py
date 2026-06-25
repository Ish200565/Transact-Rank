from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Transaction
from sqlalchemy import select

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()

    # Validation
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    required = ['user_id', 'amount', 'type', 'request_id']
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    if data['type'] not in ['credit', 'debit']:
        return jsonify({"error": "type must be credit or debit"}), 400

    if not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
        return jsonify({"error": "amount must be positive number"}), 400

    # Idempotency check
    existing = Transaction.query.filter_by(request_id=data['request_id']).first()
    if existing:
        return jsonify({"message": "duplicate request", "transaction_id": existing.id}), 200

    # Lock user row for concurrency
    user = db.session.execute(
        select(User).where(User.id == data['user_id']).with_for_update()
    ).scalar_one_or_none()

    if not user:
        user = User(id=data['user_id'])
        db.session.add(user)
        db.session.flush()

    # Debit check
    if data['type'] == 'debit' and user.balance < data['amount']:
        return jsonify({"error": "insufficient balance"}), 400

    # Update balance
    if data['type'] == 'credit':
        user.balance += data['amount']
        user.total_credits += data['amount']
    else:
        user.balance -= data['amount']
        user.total_debits += data['amount']

    user.transaction_count += 1

    txn = Transaction(
        user_id=data['user_id'],
        amount=data['amount'],
        type=data['type'],
        request_id=data['request_id']
    )
    db.session.add(txn)
    db.session.commit()

    return jsonify({"message": "success", "transaction_id": txn.id, "balance": user.balance}), 201