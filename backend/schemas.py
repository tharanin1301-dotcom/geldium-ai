from pydantic import BaseModel


class CustomerInput(BaseModel):
    name: str
    age: int
    monthly_income: float
    credit_score: int
    credit_utilization: float
    debt_to_income_ratio: float
    missed_payments: int
    payment_history_score: int


class PredictionResponse(BaseModel):
    customer_id: str
    name: str
    risk_label: str
    risk_score: float
    prob_high: float
    prob_medium: float
    prob_low: float
    