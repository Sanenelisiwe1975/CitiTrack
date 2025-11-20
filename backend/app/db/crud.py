"""CRUD operations for database"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta
from .schemas import ReportDB, UserDB, BlockchainEventDB
from ..models.report import ReportCreate, ReportStatus, IssueCategory, SeverityLevel
from ..models.user import UserCreate
import secrets
import string


def generate_report_id() -> str:
    """Generate unique report ID"""
    return f"RPT-{datetime.now().year}-{secrets.randbelow(999999):06d}"


def generate_user_id() -> str:
    """Generate unique user ID"""
    return f"USR-{''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10))}"


# Report CRUD operations
def create_report(db: Session, report: ReportCreate) -> ReportDB:
    """Create a new report"""
    db_report = ReportDB(
        id=generate_report_id(),
        category=report.category,
        description=report.description,
        latitude=report.location.latitude,
        longitude=report.location.longitude,
        address=report.location.address,
        ward=report.location.ward,
        municipality=report.location.municipality,
        photo_url=report.photo_url,
        reporter_name=report.reporter_name,
        reporter_phone=report.reporter_phone,
        reporter_email=report.reporter_email,
        language=report.language
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_report(db: Session, report_id: str) -> Optional[ReportDB]:
    """Get report by ID"""
    return db.query(ReportDB).filter(ReportDB.id == report_id).first()


def get_reports(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[ReportStatus] = None,
    category: Optional[IssueCategory] = None,
    severity: Optional[SeverityLevel] = None,
    municipality: Optional[str] = None
) -> tuple[List[ReportDB], int]:
    """Get reports with filters"""
    query = db.query(ReportDB)
    
    # Apply filters
    if status:
        query = query.filter(ReportDB.status == status)
    if category:
        query = query.filter(ReportDB.category == category)
    if severity:
        query = query.filter(ReportDB.severity == severity)
    if municipality:
        query = query.filter(ReportDB.municipality == municipality)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    reports = query.order_by(ReportDB.created_at.desc()).offset(skip).limit(limit).all()
    
    return reports, total


def update_report(db: Session, report_id: str, **kwargs) -> Optional[ReportDB]:
    """Update report"""
    db_report = get_report(db, report_id)
    if not db_report:
        return None
    
    for key, value in kwargs.items():
        if value is not None and hasattr(db_report, key):
            setattr(db_report, key, value)
    
    db.commit()
    db.refresh(db_report)
    return db_report


def resolve_report(db: Session, report_id: str) -> Optional[ReportDB]:
    """Mark report as resolved"""
    return update_report(
        db,
        report_id,
        status=ReportStatus.RESOLVED,
        resolved_at=datetime.now()
    )


def increment_report_views(db: Session, report_id: str):
    """Increment report view count"""
    db_report = get_report(db, report_id)
    if db_report:
        db_report.views += 1
        db.commit()


def increment_report_upvotes(db: Session, report_id: str):
    """Increment report upvote count"""
    db_report = get_report(db, report_id)
    if db_report:
        db_report.upvotes += 1
        db.commit()


# User CRUD operations
def create_user(db: Session, user: UserCreate, hashed_password: str) -> UserDB:
    """Create a new user"""
    db_user = UserDB(
        id=generate_user_id(),
        email=user.email,
        phone=user.phone,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[UserDB]:
    """Get user by email"""
    return db.query(UserDB).filter(UserDB.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[UserDB]:
    """Get user by ID"""
    return db.query(UserDB).filter(UserDB.id == user_id).first()


# Blockchain CRUD operations
def create_blockchain_event(
    db: Session,
    report_id: str,
    event_type: str,
    tx_hash: str,
    block_number: int,
    data_hash: str
) -> BlockchainEventDB:
    """Create blockchain event"""
    event = BlockchainEventDB(
        report_id=report_id,
        event_type=event_type,
        tx_hash=tx_hash,
        block_number=block_number,
        data_hash=data_hash
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_blockchain_events(db: Session, report_id: str) -> List[BlockchainEventDB]:
    """Get all blockchain events for a report"""
    return db.query(BlockchainEventDB)\
        .filter(BlockchainEventDB.report_id == report_id)\
        .order_by(BlockchainEventDB.timestamp.asc())\
        .all()


# Dashboard statistics
def get_dashboard_stats(db: Session):
    """Get dashboard statistics"""
    total_reports = db.query(func.count(ReportDB.id)).scalar()
    
    pending = db.query(func.count(ReportDB.id))\
        .filter(ReportDB.status == ReportStatus.PENDING)\
        .scalar()
    
    in_progress = db.query(func.count(ReportDB.id))\
        .filter(ReportDB.status == ReportStatus.IN_PROGRESS)\
        .scalar()
    
    resolved = db.query(func.count(ReportDB.id))\
        .filter(ReportDB.status == ReportStatus.RESOLVED)\
        .scalar()
    
    # Reports in last 7 days
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_reports = db.query(func.count(ReportDB.id))\
        .filter(ReportDB.created_at >= seven_days_ago)\
        .scalar()
    
    # Category breakdown
    category_stats = db.query(
        ReportDB.category,
        func.count(ReportDB.id)
    ).group_by(ReportDB.category).all()
    
    # Severity breakdown
    severity_stats = db.query(
        ReportDB.severity,
        func.count(ReportDB.id)
    ).group_by(ReportDB.severity).all()
    
    return {
        "total_reports": total_reports,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved,
        "recent_reports": recent_reports,
        "resolution_rate": (resolved / total_reports * 100) if total_reports > 0 else 0,
        "category_breakdown": {cat: count for cat, count in category_stats},
        "severity_breakdown": {sev: count for sev, count in severity_stats}
    }
