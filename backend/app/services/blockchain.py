"""Blockchain integration service"""
from web3 import Web3
from web3.middleware import geth_poa_middleware
from ..config import settings
import json
import hashlib
from datetime import datetime
from typing import Optional


class BlockchainService:
    """Service for blockchain anchoring"""
    
    def __init__(self):
        # Connect to Ethereum network (Polygon Mumbai testnet)
        self.w3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_RPC_URL))
        
        # Add PoA middleware for Polygon
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Contract ABI (simplified)
        self.contract_abi = [
            {
                "inputs": [
                    {"internalType": "string", "name": "reportId", "type": "string"},
                    {"internalType": "string", "name": "eventType", "type": "string"},
                    {"internalType": "string", "name": "dataHash", "type": "string"}
                ],
                "name": "anchorReport",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "string", "name": "reportId", "type": "string"}],
                "name": "getReportTrail",
                "outputs": [
                    {
                        "components": [
                            {"internalType": "string", "name": "reportId", "type": "string"},
                            {"internalType": "string", "name": "eventType", "type": "string"},
                            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                            {"internalType": "string", "name": "dataHash", "type": "string"}
                        ],
                        "internalType": "struct CitiTrackReport.ReportEvent[]",
                        "name": "",
                        "type": "tuple[]"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        # Initialize contract
        if settings.CONTRACT_ADDRESS and settings.CONTRACT_ADDRESS != "0x...":
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(settings.CONTRACT_ADDRESS),
                abi=self.contract_abi
            )
            self.account = self.w3.eth.account.from_key(settings.PRIVATE_KEY)
        else:
            self.contract = None
            self.account = None
    
    def is_connected(self) -> bool:
        """Check if connected to blockchain"""
        try:
            return self.w3.is_connected() and self.contract is not None
        except:
            return False
    
    def create_data_hash(self, data: dict) -> str:
        """Create SHA-256 hash of data"""
        data_string = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    async def anchor_report(
        self,
        report_id: str,
        event_type: str,
        data: dict
    ) -> Optional[dict]:
        """Anchor report event to blockchain"""
        
        if not self.is_connected():
            print("Blockchain not connected, skipping anchor")
            return None
        
        try:
            # Create data hash
            data_hash = self.create_data_hash(data)
            
            # Build transaction
            transaction = self.contract.functions.anchorReport(
                report_id,
                event_type,
                data_hash
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                private_key=settings.PRIVATE_KEY
            )
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                "tx_hash": tx_hash.hex(),
                "block_number": tx_receipt['blockNumber'],
                "data_hash": data_hash,
                "timestamp": datetime.now(),
                "gas_used": tx_receipt['gasUsed']
            }
            
        except Exception as e:
            print(f"Blockchain anchor error: {e}")
            return None
    
    async def verify_report(self, report_id: str) -> dict:
        """Verify report on blockchain"""
        
        if not self.is_connected():
            return {
                "is_verified": False,
                "error": "Blockchain not connected"
            }
        
        try:
            # Get report trail from contract
            trail = self.contract.functions.getReportTrail(report_id).call()
            
            events = []
            for event in trail:
                events.append({
                    "report_id": event[0],
                    "event_type": event[1],
                    "timestamp": datetime.fromtimestamp(event[2]),
                    "data_hash": event[3]
                })
            
            return {
                "is_verified": len(events) > 0,
                "trail": events,
                "total_events": len(events)
            }
            
        except Exception as e:
            print(f"Blockchain verification error: {e}")
            return {
                "is_verified": False,
                "error": str(e)
            }
    
    def get_transaction_url(self, tx_hash: str) -> str:
        """Get block explorer URL for transaction"""
        # For Polygon Mumbai testnet
        return f"https://mumbai.polygonscan.com/tx/{tx_hash}"


# Singleton instance
blockchain_service = BlockchainService()