"""Dashboard API endpoints"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db, crud

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    
    stats = crud.get_dashboard_stats(db)
    
    return {
        "summary": {
            "total_reports": stats["total_reports"],
            "pending": stats["pending"],
            "in_progress": stats["in_progress"],
            "resolved": stats["resolved"],
            "recent_reports": stats["recent_reports"],
            "resolution_rate": round(stats["resolution_rate"], 2)
        },
        "by_category": stats["category_breakdown"],
        "by_severity": stats["severity_breakdown"]
    }


@router.get("/recent")
async def get_recent_reports(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent reports"""
    
    reports, _ = crud.get_reports(db, skip=0, limit=limit)
    
    return {
        "reports": [
            {
                "id": r.id,
                "category": r.category.value,
                "status": r.status.value,
                "severity": r.severity.value if r.severity else None,
                "location": r.address or f"{r.latitude}, {r.longitude}",
                "created_at": r.created_at.isoformat()
            }
            for r in reports
        ]
    }


@router.get("/trending")
async def get_trending_issues(db: Session = Depends(get_db)):
    """Get trending issues (most upvoted)"""
    
    # Get reports ordered by upvotes
    from ..db.schemas import ReportDB
    reports = db.query(ReportDB)\
        .order_by(ReportDB.upvotes.desc())\
        .limit(10)\
        .all()
    
    return {
        "trending": [
            {
                "id": r.id,
                "category": r.category.value,
                "description": r.description[:100] + "...",
                "upvotes": r.upvotes,
                "location": r.address or "Unknown"
            }
            for r in reports
        ]
    }