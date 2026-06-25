from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    balance = db.Column(db.Float, default=0.0)
    total_credits = db.Column(db.Float, default=0.0)
    total_debits = db.Column(db.Float, default=0.0)
    transaction_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String, nullable=False)  # 'credit' or 'debit'
    request_id = db.Column(db.String, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)