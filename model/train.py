import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# ── Load dataset ──────────────────────────────────────
df = pd.read_csv("data/customers.csv")

# ── Features & Target ─────────────────────────────────
FEATURES = [
    "age",
    "monthly_income",
    "credit_score",
    "credit_utilization",
    "debt_to_income_ratio",
    "missed_payments",
    "payment_history_score"
]

X = df[FEATURES]
y = df["risk_label"]

# ── Split data ────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✅ Training samples : {len(X_train)}")
print(f"✅ Testing samples  : {len(X_test)}")

# ── Train Random Forest ───────────────────────────────
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)
print("✅ Model trained successfully!")

# ── Evaluate ──────────────────────────────────────────
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n📊 Model Accuracy: {accuracy * 100:.2f}%")
print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

# ── Feature Importance ────────────────────────────────
print("🔍 Feature Importance:")
for feat, imp in sorted(
    zip(FEATURES, model.feature_importances_),
    key=lambda x: x[1],
    reverse=True
):
    print(f"   {feat:<30} {imp:.4f}")

# ── Save model ────────────────────────────────────────
os.makedirs("model/artifacts", exist_ok=True)
joblib.dump(model, "model/artifacts/customer_model.pkl")
joblib.dump(FEATURES, "model/artifacts/features.pkl")
print("\n✅ Model saved to model/artifacts/customer_model.pkl")