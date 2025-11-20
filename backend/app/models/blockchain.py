"""Blockchain models"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BlockchainEvent(BaseModel):
    """Blockchain event"""
    report_id: str
    event_type: str
    timestamp: datetime
    data_hash: str
    tx_hash: str
    block_number: int


class BlockchainVerification(BaseModel):
    """Blockchain verification result"""
    report_id: str
    is_verified: bool
    trail: List[BlockchainEvent]
    total_events: int
    first_anchor: Optional[datetime] = None
    last_anchor: Optional[datetime] = None


class AnchorRequest(BaseModel):
    """Anchor report to blockchain"""
    report_id: str
    event_type: str
    data: dict