"""SQLAlchemy database schemas"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from .database import Base
from ..models.report import IssueCategory, ReportStatus, SeverityLevel
from ..models.user import UserRole
import enum


class ReportDB(Base):
    """Report database model"""
    __tablename__ = "reports"
    
    id = Column(String(20), primary_key=True, index=True)
    category = Column(SQLEnum(IssueCategory), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(500))
    ward = Column(String(100), index=True)
    municipality = Column(String(100), index=True)
    
    # Media
    photo_url = Column(String(500))
    
    # Status
    status = Column(SQLEnum(ReportStatus), default=ReportStatus.PENDING, index=True)
    severity = Column(SQLEnum(SeverityLevel), index=True)
    
    # Reporter info
    reporter_name = Column(String(200))
    reporter_phone = Column(String(20))
    reporter_email = Column(String(200))
    
    # AI Classification
    ai_classification = Column(JSON)
    
    # Blockchain
    blockchain_anchors = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True))
    
    # Metadata
    language = Column(String(10), default="en")
    upvotes = Column(Integer, default=0)
    views = Column(Integer, default=0)


class UserDB(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(String(20), primary_key=True, index=True)
    email = Column(String(200), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True)
    full_name = Column(String(200), nullable=False)
    hashed_password = Column(String(200), nullable=False)
    
    role = Column(SQLEnum(UserRole), default=UserRole.CITIZEN)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reports_count = Column(Integer, default=0)


class BlockchainEventDB(Base):
    """Blockchain event database model"""
    __tablename__ = "blockchain_events"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String(20), index=True, nullable=False)
    event_type = Column(String(50), nullable=False)
    tx_hash = Column(String(100), unique=True, index=True)
    block_number = Column(Integer)
    data_hash = Column(String(100))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())