from pydantic import BaseModel
from typing import Dict, List, Literal


class MonthlySummaryItem(BaseModel):
    month: str
    income: float
    expense: float


class RecentTransactionItem(BaseModel):
    id: str
    amount: float
    type: Literal["income", "expense"]
    category: str
    date: str
    notes: str
    created_by: str


class DashboardSummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    category_wise_totals: Dict[str, float]
    monthly_summary: List[MonthlySummaryItem]
    recent_transactions: List[RecentTransactionItem]