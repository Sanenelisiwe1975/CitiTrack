"""Blockchain verification API endpoints"""
from fastapi import APIRouter, HTTPException
from ..services import blockchain_service
from ..models.blockchain import BlockchainVerification

router = APIRouter(prefix="/api/blockchain", tags=["blockchain"])


@router.get("/verify/{report_id}", response_model=BlockchainVerification)
async def verify_report(report_id: str):
    """Verify report on blockchain"""
    
    result = await blockchain_service.verify_report(report_id)
    
    if not result.get("is_verified") and result.get("error"):
        raise HTTPException(
            status_code=503,
            detail=f"Blockchain verification unavailable: {result['error']}"
        )
    
    return BlockchainVerification(
        report_id=report_id,
        is_verified=result["is_verified"],
        trail=result.get("trail", []),
        total_events=result.get("total_events", 0),
        first_anchor=result["trail"][0]["timestamp"] if result.get("trail") else None,
        last_anchor=result["trail"][-1]["timestamp"] if result.get("trail") else None
    )


@router.get("/status")
async def blockchain_status():
    """Get blockchain connection status"""
    
    is_connected = blockchain_service.is_connected()
    
    return {
        "connected": is_connected,
        "network": "Polygon Mumbai Testnet" if is_connected else "Not connected",
        "contract_address": blockchain_service.contract.address if is_connected else None
    }


@router.get("/transaction/{tx_hash}")
async def get_transaction_info(tx_hash: str):
    """Get transaction information"""
    
    url = blockchain_service.get_transaction_url(tx_hash)
    
    return {
        "tx_hash": tx_hash,
        "explorer_url": url,
        "network": "Polygon Mumbai Testnet"
    }