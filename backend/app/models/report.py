"""Report Pydantic models"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class IssueCategory(str, Enum):
    """Issue categories"""
    POTHOLE = "pothole"
    STREETLIGHT = "streetlight"
    WATER_LEAK = "water_leak"
    GARBAGE = "garbage"
    GRAFFITI = "graffiti"
    ROAD_DAMAGE = "road_damage"
    TRAFFIC_SIGNAL = "traffic_signal"
    ILLEGAL_DUMPING = "illegal_dumping"
    OTHER = "other"


class ReportStatus(str, Enum):
    """Report status"""
    PENDING = "pending"
    VERIFIED = "verified"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class SeverityLevel(str, Enum):
    """Severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Location(BaseModel):
    """Location data"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None
    ward: Optional[str] = None
    municipality: Optional[str] = None


class ReportCreate(BaseModel):
    """Create report request"""
    category: IssueCategory
    description: str = Field(..., min_length=10, max_length=1000)
    location: Location
    photo_url: Optional[str] = None
    reporter_name: Optional[str] = None
    reporter_phone: Optional[str] = None
    reporter_email: Optional[str] = None
    language: str = "en"


class AIClassification(BaseModel):
    """AI classification result"""
    category: IssueCategory
    severity: SeverityLevel
    confidence: float = Field(..., ge=0, le=1)
    reasoning: str
    recommended_actions: List[str]
    estimated_resolution_time: Optional[str] = None
    priority_score: int = Field(..., ge=1, le=10)


class BlockchainAnchor(BaseModel):
    """Blockchain anchor data"""
    tx_hash: str
    block_number: int
    timestamp: datetime
    data_hash: str


class Report(BaseModel):
    """Full report model"""
    id: str
    category: IssueCategory
    description: str
    location: Location
    photo_url: Optional[str] = None
    status: ReportStatus = ReportStatus.PENDING
    severity: Optional[SeverityLevel] = None
    
    # Reporter info
    reporter_name: Optional[str] = None
    reporter_phone: Optional[str] = None
    reporter_email: Optional[str] = None
    
    # AI Classification
    ai_classification: Optional[AIClassification] = None
    
    # Blockchain
    blockchain_anchors: List[BlockchainAnchor] = []
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    
    # Metadata
    language: str = "en"
    upvotes: int = 0
    views: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "RPT-2024-001234",
                "category": "pothole",
                "description": "Large pothole on Main Street causing traffic issues",
                "location": {
                    "latitude": -26.2041,
                    "longitude": 28.0473,
                    "address": "123 Main St, Johannesburg",
                    "ward": "Ward 77",
                    "municipality": "City of Johannesburg"
                },
                "status": "pending",
                "severity": "high"
            }
        }


class ReportUpdate(BaseModel):
    """Update report request"""
    status: Optional[ReportStatus] = None
    severity: Optional[SeverityLevel] = None
    notes: Optional[str] = None


class ReportListResponse(BaseModel):
    """List reports response"""
    reports: List[Report]
    total: int
    page: int
    page_size: int
    has_more: bool