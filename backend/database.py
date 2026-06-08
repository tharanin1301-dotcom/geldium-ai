import sqlite3
import os

DB_PATH = "data/geldium.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            monthly_income REAL,
            credit_score INTEGER,
            credit_utilization REAL,
            debt_to_income_ratio REAL,
            missed_payments INTEGER,
            payment_history_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Predictions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            risk_label TEXT NOT NULL,
            risk_score REAL NOT NULL,
            prob_high REAL,
            prob_medium REAL,
            prob_low REAL,
            predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized!")


if __name__ == "__main__":
    init_db()