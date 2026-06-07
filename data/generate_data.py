import pandas as pd
import numpy as np

# Set seed so same data generates every time
np.random.seed(42)

NUM_CUSTOMERS = 1000

def generate_customers():
    ages = np.random.randint(21, 65, NUM_CUSTOMERS)
    incomes = np.random.randint(15000, 150000, NUM_CUSTOMERS)
    credit_scores = np.random.randint(300, 850, NUM_CUSTOMERS)
    credit_utilization = np.round(np.random.uniform(0.05, 0.99, NUM_CUSTOMERS), 2)
    debt_to_income = np.round(np.random.uniform(0.1, 0.9, NUM_CUSTOMERS), 2)
    missed_payments = np.random.randint(0, 10, NUM_CUSTOMERS)
    payment_history = np.random.randint(0, 100, NUM_CUSTOMERS)

    # Risk logic — realistic rules
    risk_score = (
        (850 - credit_scores) * 0.03 +
        credit_utilization * 25 +
        debt_to_income * 20 +
        missed_payments * 8 +
        (100 - payment_history) * 0.15 +
        np.random.uniform(-5, 5, NUM_CUSTOMERS)
    )

    # Normalize to 0-100
    risk_score = np.clip(risk_score, 0, 100).round(1)

    # Label based on score
    def label(score):
        if score < 35:
            return "Low"
        elif score < 65:
            return "Medium"
        else:
            return "High"

    labels = [label(s) for s in risk_score]

    df = pd.DataFrame({
        "customer_id": [f"CUST{str(i+1).zfill(4)}" for i in range(NUM_CUSTOMERS)],
        "age": ages,
        "monthly_income": incomes,
        "credit_score": credit_scores,
        "credit_utilization": credit_utilization,
        "debt_to_income_ratio": debt_to_income,
        "missed_payments": missed_payments,
        "payment_history_score": payment_history,
        "risk_score": risk_score,
        "risk_label": labels
    })

    return df

if __name__ == "__main__":
    df = generate_customers()
    df.to_csv("data/customers.csv", index=False)
    print(f"✅ Dataset generated: {len(df)} customers")
    print(df["risk_label"].value_counts())
    print(df.head())