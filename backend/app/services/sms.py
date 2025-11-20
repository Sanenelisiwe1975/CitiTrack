"""SMS notification service using Africa's Talking"""
import africastalking
from ..config import settings
from typing import Optional


class SMSService:
    """Service for sending SMS notifications"""
    
    def __init__(self):
        # Initialize Africa's Talking
        if settings.AT_USERNAME and settings.AT_API_KEY:
            africastalking.initialize(
                username=settings.AT_USERNAME,
                api_key=settings.AT_API_KEY
            )
            self.sms = africastalking.SMS
            self.enabled = True
        else:
            self.sms = None
            self.enabled = False
    
    async def send_sms(
        self,
        phone_number: str,
        message: str
    ) -> dict:
        """Send SMS to phone number"""
        
        if not self.enabled:
            print(f"SMS not configured, would send to {phone_number}: {message}")
            return {
                "status": "disabled",
                "message": "SMS service not configured"
            }
        
        try:
            # Ensure phone number has country code
            if not phone_number.startswith('+'):
                phone_number = '+27' + phone_number.lstrip('0')
            
            # Send SMS
            response = self.sms.send(
                message=message,
                recipients=[phone_number],
                sender_id=settings.AT_SENDER_ID
            )
            
            return {
                "status": "sent",
                "response": response
            }
            
        except Exception as e:
            print(f"SMS sending error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def notify_report_created(
        self,
        phone_number: str,
        report_id: str,
        language: str = "en"
    ):
        """Send notification when report is created"""
        
        messages = {
            "en": f"Your CitiTrack report {report_id} has been received. Track it at: cititrack.app/track/{report_id}",
            "zu": f"Umbiko wakho we-CitiTrack {report_id} umukelwe. Ukulandelela lapha: cititrack.app/track/{report_id}",
            "af": f"Jou CitiTrack-verslag {report_id} is ontvang. Volg dit by: cititrack.app/track/{report_id}",
            "st": f"Tlaleho ya hao ya CitiTrack {report_id} e amohelitsoe. E latele ho: cititrack.app/track/{report_id}"
        }
        
        message = messages.get(language, messages["en"])
        return await self.send_sms(phone_number, message)
    
    async def notify_status_update(
        self,
        phone_number: str,
        report_id: str,
        new_status: str,
        language: str = "en"
    ):
        """Send notification when report status changes"""
        
        status_messages = {
            "en": {
                "verified": "verified and assigned to a team",
                "in_progress": "being worked on",
                "resolved": "resolved! Thank you for reporting."
            },
            "zu": {
                "verified": "iqinisekisiwe futhi yabelwe iqembu",
                "in_progress": "iyasebenza kukho",
                "resolved": "ixazululiwe! Siyabonga ngokubika."
            }
        }
        
        status_text = status_messages.get(language, status_messages["en"]).get(
            new_status,
            f"updated to {new_status}"
        )
        
        message = f"CitiTrack Update: Your report {report_id} has been {status_text}"
        
        return await self.send_sms(phone_number, message)
    
    async def notify_critical_issue(
        self,
        phone_number: str,
        report_id: str
    ):
        """Send immediate notification for critical issues"""
        
        message = f"URGENT: CitiTrack report {report_id} has been marked as CRITICAL. Our team has been notified and will respond immediately."
        
        return await self.send_sms(phone_number, message)


# Singleton instance
sms_service = SMSService()