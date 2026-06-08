from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import uuid
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.schemas import CustomerInput, PredictionResponse
from backend.database import init_db, get_connection
from model.predict import predict_risk

# ── App setup ─────────────────────────────────────────
app = FastAPI(
    title="Geldium AI Collections API",
    description="AI-powered delinquency prediction system",
    version="1.0.0"
)

# ── CORS ──────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Initialize DB on startup ──────────────────────────
@app.on_event("startup")
def startup():
    init_db()


# ── Routes ────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "message": "Geldium AI Collections API",
        "status": "running"
    }


@app.post("/predict")
def predict(customer: CustomerInput):
    """Predict delinquency risk for a customer"""

    # Generate unique customer ID
    customer_id = "CUST" + str(uuid.uuid4())[:8].upper()

    # Prepare data for model
    customer_data = {
        "age": customer.age,
        "monthly_income": customer.monthly_income,
        "credit_score": customer.credit_score,
        "credit_utilization": customer.credit_utilization,
        "debt_to_income_ratio": customer.debt_to_income_ratio,
        "missed_payments": customer.missed_payments,
        "payment_history_score": customer.payment_history_score
    }

    # Get prediction
    result = predict_risk(customer_data)

    # Save customer to DB
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO customers
        (customer_id, name, age, monthly_income, credit_score,
         credit_utilization, debt_to_income_ratio,
         missed_payments, payment_history_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        customer_id, customer.name, customer.age,
        customer.monthly_income, customer.credit_score,
        customer.credit_utilization, customer.debt_to_income_ratio,
        customer.missed_payments, customer.payment_history_score
    ))

    # Save prediction to DB
    cursor.execute("""
        INSERT INTO predictions
        (customer_id, risk_label, risk_score,
         prob_high, prob_medium, prob_low)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        customer_id,
        result["risk_label"],
        result["risk_score"],
        result["probabilities"].get("High", 0),
        result["probabilities"].get("Medium", 0),
        result["probabilities"].get("Low", 0)
    ))

    conn.commit()
    conn.close()

    return {
        "customer_id": customer_id,
        "name": customer.name,
        "risk_label": result["risk_label"],
        "risk_score": result["risk_score"],
        "probabilities": result["probabilities"],
        "message": "Prediction saved successfully"
    }


@app.get("/customers")
def get_customers():
    """Get all customers with their latest prediction"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.*, p.risk_label, p.risk_score,
               p.prob_high, p.prob_medium, p.prob_low,
               p.predicted_at
        FROM customers c
        LEFT JOIN predictions p ON c.customer_id = p.customer_id
        ORDER BY p.risk_score DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return {"customers": [dict(row) for row in rows]}


@app.get("/stats")
def get_stats():
    """Get dashboard statistics"""

    conn = get_connection()
    cursor = conn.cursor()

    # Total customers
    cursor.execute("SELECT COUNT(*) as total FROM customers")
    total = cursor.fetchone()["total"]

    # Risk distribution
    cursor.execute("""
        SELECT risk_label, COUNT(*) as count
        FROM predictions
        GROUP BY risk_label
    """)
    distribution = {row["risk_label"]: row["count"]
                    for row in cursor.fetchall()}

    # Average risk score
    cursor.execute("SELECT AVG(risk_score) as avg FROM predictions")
    avg_score = cursor.fetchone()["avg"] or 0

    conn.close()

    return {
        "total_customers": total,
        "risk_distribution": {
            "High": distribution.get("High", 0),
            "Medium": distribution.get("Medium", 0),
            "Low": distribution.get("Low", 0)
        },
        "average_risk_score": round(avg_score, 1)
    }


@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    """Get a specific customer by ID"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.*, p.risk_label, p.risk_score,
               p.prob_high, p.prob_medium, p.prob_low
        FROM customers c
        LEFT JOIN predictions p ON c.customer_id = p.customer_id
        WHERE c.customer_id = ?
    """, (customer_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404,
                            detail="Customer not found")

    return dict(row)