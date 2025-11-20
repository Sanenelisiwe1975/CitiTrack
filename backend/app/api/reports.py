"""Report API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db import get_db, crud
from ..models.report import (
    ReportCreate, Report, ReportUpdate, ReportListResponse,
    ReportStatus, IssueCategory, SeverityLevel, Location, AIClassification
)
from ..services import ai_agent, blockchain_service, sms_service, storage_service
from ..utils import get_translation
from datetime import datetime

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.post("", response_model=Report, status_code=201)
async def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):
    """Create a new report"""
    
    # Create report in database
    db_report = crud.create_report(db, report)
    
    # AI Classification (async, don't wait)
    try:
        ai_classification = await ai_agent.classify_report(
            category=report.category.value,
            description=report.description,
            location=report.location.dict(),
            photo_url=report.photo_url
        )
        
        # Update report with AI classification
        crud.update_report(
            db,
            db_report.id,
            ai_classification=ai_classification.dict(),
            severity=ai_classification.severity
        )
        
    except Exception as e:
        print(f"AI classification error: {e}")
    
    # Blockchain anchoring (async, don't wait)
    try:
        anchor_result = await blockchain_service.anchor_report(
            report_id=db_report.id,
            event_type="created",
            data={
                "category": report.category.value,
                "location": report.location.dict(),
                "timestamp": db_report.created_at.isoformat()
            }
        )
        
        if anchor_result:
            # Save blockchain anchor
            blockchain_anchors = [{
                "tx_hash": anchor_result["tx_hash"],
                "block_number": anchor_result["block_number"],
                "timestamp": anchor_result["timestamp"].isoformat(),
                "data_hash": anchor_result["data_hash"]
            }]
            crud.update_report(db, db_report.id, blockchain_anchors=blockchain_anchors)
            
    except Exception as e:
        print(f"Blockchain anchor error: {e}")
    
    # Send SMS notification
    if report.reporter_phone:
        try:
            await sms_service.notify_report_created(
                phone_number=report.reporter_phone,
                report_id=db_report.id,
                language=report.language
            )
        except Exception as e:
            print(f"SMS notification error: {e}")
    
    # Refresh report from database
    db_report = crud.get_report(db, db_report.id)
    
    return _db_report_to_response(db_report)


@router.get("", response_model=ReportListResponse)
async def get_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[ReportStatus] = None,
    category: Optional[IssueCategory] = None,
    severity: Optional[SeverityLevel] = None,
    municipality: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all reports with filters"""
    
    reports, total = crud.get_reports(
        db,
        skip=skip,
        limit=limit,
        status=status,
        category=category,
        severity=severity,
        municipality=municipality
    )
    
    return ReportListResponse(
        reports=[_db_report_to_response(r) for r in reports],
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        has_more=(skip + limit) < total
    )


@router.get("/{report_id}", response_model=Report)
async def get_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    """Get specific report"""
    
    db_report = crud.get_report(db, report_id)
    
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Increment views
    crud.increment_report_views(db, report_id)
    
    return _db_report_to_response(db_report)


@router.patch("/{report_id}", response_model=Report)
async def update_report(
    report_id: str,
    update: ReportUpdate,
    db: Session = Depends(get_db)
):
    """Update report status"""
    
    db_report = crud.get_report(db, report_id)
    
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Update report
    updated_report = crud.update_report(
        db,
        report_id,
        status=update.status,
        severity=update.severity
    )
    
    # Send SMS notification if status changed
    if update.status and db_report.reporter_phone:
        try:
            await sms_service.notify_status_update(
                phone_number=db_report.reporter_phone,
                report_id=report_id,
                new_status=update.status.value,
                language=db_report.language
            )
        except Exception as e:
            print(f"SMS notification error: {e}")
    
    # Blockchain anchor status change
    if update.status:
        try:
            await blockchain_service.anchor_report(
                report_id=report_id,
                event_type=f"status_changed_{update.status.value}",
                data={
                    "old_status": db_report.status.value,
                    "new_status": update.status.value,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            print(f"Blockchain anchor error: {e}")
    
    return _db_report_to_response(updated_report)


@router.post("/{report_id}/resolve", response_model=Report)
async def resolve_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    """Mark report as resolved"""
    
    db_report = crud.resolve_report(db, report_id)
    
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Blockchain anchor resolution
    try:
        await blockchain_service.anchor_report(
            report_id=report_id,
            event_type="resolved",
            data={
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        print(f"Blockchain anchor error: {e}")
    
    return _db_report_to_response(db_report)


@router.post("/{report_id}/upvote")
async def upvote_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    """Upvote a report"""
    
    db_report = crud.get_report(db, report_id)
    
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    crud.increment_report_upvotes(db, report_id)
    
    return {"message": "Upvoted successfully", "upvotes": db_report.upvotes + 1}


@router.post("/upload-photo")
async def upload_photo(
    file: UploadFile = File(...)
):
    """Upload photo for report"""
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read file content
    content = await file.read()
    
    # Upload to storage
    url = await storage_service.upload_file(
        file_content=content,
        filename=file.filename,
        content_type=file.content_type
    )
    
    if not url:
        raise HTTPException(status_code=500, detail="Failed to upload file")
    
    return {"url": url}


def _db_report_to_response(db_report) -> Report:
    """Convert DB report to response model"""
    
    return Report(
        id=db_report.id,
        category=db_report.category,
        description=db_report.description,
        location=Location(
            latitude=db_report.latitude,
            longitude=db_report.longitude,
            address=db_report.address,
            ward=db_report.ward,
            municipality=db_report.municipality
        ),
        photo_url=db_report.photo_url,
        status=db_report.status,
        severity=db_report.severity,
        reporter_name=db_report.reporter_name,
        reporter_phone=db_report.reporter_phone,
        reporter_email=db_report.reporter_email,
        ai_classification=AIClassification(**db_report.ai_classification) if db_report.ai_classification else None,
        blockchain_anchors=db_report.blockchain_anchors or [],
        created_at=db_report.created_at,
        updated_at=db_report.updated_at,
        resolved_at=db_report.resolved_at,
        language=db_report.language,
        upvotes=db_report.upvotes,
        views=db_report.views
    )