from fastapi import APIRouter, Depends, Query

from app.api.deps import get_current_business

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
def alerts(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    _business=Depends(get_current_business),
) -> dict:
    rows = [
        {
            "id": "liquidity-risk",
            "title": "High Liquidity Risk",
            "description": "Stress probability is elevated based on the latest analysis.",
            "severity": "high",
        },
        {
            "id": "expense-spike",
            "title": "Expense Spike Detected",
            "description": "Operating expenses are trending above the safe threshold.",
            "severity": "medium",
        },
        {
            "id": "cash-reserve",
            "title": "Low Cash Reserve",
            "description": "Cash reserve coverage is below the recommended operating buffer.",
            "severity": "medium",
        },
    ]
    return {"items": rows[offset : offset + limit], "total": len(rows), "limit": limit, "offset": offset}
