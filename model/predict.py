import joblib
import numpy as np
import pandas as pd

# Load model & features
model = joblib.load("model/artifacts/customer_model.pkl")
FEATURES = joblib.load("model/artifacts/features.pkl")


def predict_risk(customer_data: dict) -> dict:
    """
    Input  : customer details as dictionary
    Output : risk_label + risk_score + probabilities
    """

    # Build input array in correct feature order
    input_values = [customer_data[f] for f in FEATURES]
    input_array = pd.DataFrame([input_values], columns=FEATURES)

    # Predict label
    label = model.predict(input_array)[0]

    # Predict probabilities
    proba = model.predict_proba(input_array)[0]
    classes = model.classes_

    # Map probabilities to labels
    proba_dict = {cls: round(float(prob) * 100, 1)
                  for cls, prob in zip(classes, proba)}

    # Risk score (weighted)
    risk_score = round(
        proba_dict.get("High", 0) * 1.0 +
        proba_dict.get("Medium", 0) * 0.5 +
        proba_dict.get("Low", 0) * 0.1,
        1
    )

    return {
        "risk_label": label,
        "risk_score": risk_score,
        "probabilities": proba_dict
    }


# Test it
if __name__ == "__main__":

    # Test 1 - High risk customer
    high_risk = {
        "age": 27,
        "monthly_income": 18000,
        "credit_score": 560,
        "credit_utilization": 0.88,
        "debt_to_income_ratio": 0.75,
        "missed_payments": 3,
        "payment_history_score": 20
    }

    # Test 2 - Low risk customer
    low_risk = {
        "age": 45,
        "monthly_income": 95000,
        "credit_score": 780,
        "credit_utilization": 0.15,
        "debt_to_income_ratio": 0.20,
        "missed_payments": 0,
        "payment_history_score": 95
    }

    # Test 3 - Medium risk customer
    medium_risk = {
        "age": 33,
        "monthly_income": 45000,
        "credit_score": 630,
        "credit_utilization": 0.55,
        "debt_to_income_ratio": 0.45,
        "missed_payments": 1,
        "payment_history_score": 60
    }

    print("=" * 50)
    print("HIGH RISK CUSTOMER:")
    print(predict_risk(high_risk))

    print("\nLOW RISK CUSTOMER:")
    print(predict_risk(low_risk))

    print("\nMEDIUM RISK CUSTOMER:")
    print(predict_risk(medium_risk))
    print("=" * 50)