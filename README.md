# TransactRank

A backend service with a live frontend demonstrating API design, data consistency, duplicate prevention, and fair multi-factor ranking.

**Live Frontend:** https://transact-rank-1.onrender.com  
**Backend API:** https://transact-rank.onrender.com

---

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Migrate
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Vanilla JS
- **Deployment:** Render (backend + frontend)

---

## How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOURUSERNAME/TransactRank.git
cd TransactRank
```

### 2. Setup backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create `.env` file in `backend/`
DATABASE_URL=postgresql://postgres:yourpassword@localhost/transactrank

SECRET_KEY=mysecretkey

### 4. Run migrations
```bash
flask db upgrade
```

### 5. Start backend
```bash
python app.py
```

### 6. Open frontend
Open `frontend/index.html` in your browser.

---

## API Reference

### POST /transaction
Creates a new transaction (credit or debit).

**Request Body:**
```json
{
  "user_id": "alice@example.com",
  "amount": 500.00,
  "type": "credit",
  "request_id": "txn_001"
}
```

**Response:**
```json
{
  "message": "success",
  "transaction_id": 1,
  "balance": 500.00
}
```

**Validations:**
- `user_id`, `amount`, `type`, `request_id` are required
- `amount` must be positive
- `type` must be `credit` or `debit`
- Debit is rejected if balance is insufficient

---

### GET /summary/:userId
Returns account summary for a user.

**Response:**
```json
{
  "user_id": "alice@example.com",
  "balance": 500.00,
  "total_credits": 500.00,
  "total_debits": 0.00,
  "transaction_count": 1,
  "member_since": "2026-06-25T10:00:00"
}
```

---

### GET /ranking
Returns all users ranked by score.

**Response:**
```json
[
  {
    "rank": 1,
    "user_id": "alice@example.com",
    "score": 210.5,
    "balance": 500.00,
    "total_credits": 500.00,
    "total_debits": 0.00,
    "transaction_count": 1
  }
]
```

---

## How Ranking Works

Each user gets a score based on 4 weighted factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Total Volume (credits + debits) | 40% | Higher activity = higher score |
| Transaction Count | 30% | More transactions = higher score |
| Account Age (days) | 20% | Older accounts rewarded |
| Balance Health | 10% | Positive balance contributes |

**Formula:**
score = (volume × 0.4) + (txn_count × 10 × 0.3) + (age_days × 5 × 0.2) + (balance × 0.1)

This prevents single large transactions from dominating the ranking — a user needs consistent activity and account age to rank high.

---

## How Duplicate Requests Are Prevented

Every transaction request includes a `request_id` (idempotency key).

- Before processing, the backend checks if `request_id` already exists in the database
- If found → returns the original response without re-processing
- If not found → processes and stores the transaction

This prevents double charges in case of network retries or repeated form submissions.

---

## How Concurrency Is Handled

- PostgreSQL row-level locking (`SELECT FOR UPDATE`) is used when reading a user's balance
- This ensures two simultaneous requests for the same user cannot both pass the balance check
- All balance updates happen inside a single database transaction — either fully committed or rolled back

---

## Assumptions & Mock Data

- Users are auto-created on first transaction — no separate registration flow
- `request_id` is generated client-side (timestamp + random string) and must be unique per transaction
- Account age starts from the first transaction date
- Ranking score is recalculated live on every `/ranking` request

---

## Project Structure
TransactRank/

├── backend/

│   ├── app.py

│   ├── wsgi.py

│   ├── config.py

│   ├── extensions.py

│   ├── models.py

│   ├── Procfile

│   ├── requirements.txt

│   └── routes/

│       ├── transactions.py

│       ├── summary.py

│       └── ranking.py

└── frontend/

└── index.html