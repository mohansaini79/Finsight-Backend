from fastapi import APIRouter, Depends
from app.schemas.dashboard import DashboardSummaryResponse
from app.utils.dependencies import require_roles
from app.services.dashboard_service import get_dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def dashboard_summary(_current_user=Depends(require_roles(["viewer", "analyst", "admin"]))):
    return get_dashboard_summary()