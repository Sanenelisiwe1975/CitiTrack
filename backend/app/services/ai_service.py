"""AI Agent Service using LangChain"""
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from ..models.report import AIClassification, IssueCategory, SeverityLevel
from ..config import settings
import json
from typing import Optional


class AIAgentService:
    """AI Agent for report classification and analysis"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.AI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.2
        )
        
        self.classification_prompt = ChatPromptTemplate.from_template(
            """You are an expert municipal issue classifier for South African cities.
            
Analyze the following civic issue report and provide a comprehensive classification.

Report Details:
Category: {category}
Description: {description}
Location: {location}

Your task:
1. Confirm or correct the issue category
2. Assess the severity level (LOW, MEDIUM, HIGH, CRITICAL)
3. Provide reasoning for your assessment
4. Recommend specific actions for resolution
5. Estimate resolution time
6. Assign a priority score (1-10)

Consider factors like:
- Public safety impact
- Number of people affected
- Urgency of resolution
- Infrastructure criticality
- Potential for escalation

Respond in JSON format:
{{
    "category": "one of: pothole, streetlight, water_leak, garbage, graffiti, road_damage, traffic_signal, illegal_dumping, other",
    "severity": "one of: low, medium, high, critical",
    "confidence": 0.95,
    "reasoning": "Detailed explanation of your assessment",
    "recommended_actions": ["Action 1", "Action 2", "Action 3"],
    "estimated_resolution_time": "e.g., 24-48 hours",
    "priority_score": 8
}}"""
        )
    
    async def classify_report(
        self,
        category: str,
        description: str,
        location: dict,
        photo_url: Optional[str] = None
    ) -> AIClassification:
        """Classify and analyze a report"""
        
        try:
            # Format location string
            location_str = f"{location.get('address', 'Unknown address')}, "
            location_str += f"Ward: {location.get('ward', 'Unknown')}, "
            location_str += f"{location.get('municipality', 'Unknown municipality')}"
            
            # Create prompt
            messages = self.classification_prompt.format_messages(
                category=category,
                description=description,
                location=location_str
            )
            
            # Get response from LLM
            response = await self.llm.ainvoke(messages)
            
            # Parse response
            result = json.loads(response.content)
            
            # Create AIClassification object
            classification = AIClassification(
                category=IssueCategory(result["category"]),
                severity=SeverityLevel(result["severity"]),
                confidence=result["confidence"],
                reasoning=result["reasoning"],
                recommended_actions=result["recommended_actions"],
                estimated_resolution_time=result.get("estimated_resolution_time"),
                priority_score=result["priority_score"]
            )
            
            return classification
            
        except Exception as e:
            print(f"AI Classification error: {e}")
            # Fallback to basic classification
            return self._fallback_classification(category, description)
    
    def _fallback_classification(self, category: str, description: str) -> AIClassification:
        """Fallback classification if AI fails"""
        
        # Simple keyword-based severity assessment
        description_lower = description.lower()
        
        critical_keywords = ["emergency", "danger", "hazard", "urgent", "critical", "life-threatening"]
        high_keywords = ["major", "severe", "serious", "blocked", "flooding"]
        medium_keywords = ["moderate", "needs attention", "problematic"]
        
        if any(word in description_lower for word in critical_keywords):
            severity = SeverityLevel.CRITICAL
            priority = 9
        elif any(word in description_lower for word in high_keywords):
            severity = SeverityLevel.HIGH
            priority = 7
        elif any(word in description_lower for word in medium_keywords):
            severity = SeverityLevel.MEDIUM
            priority = 5
        else:
            severity = SeverityLevel.LOW
            priority = 3
        
        return AIClassification(
            category=IssueCategory(category),
            severity=severity,
            confidence=0.6,
            reasoning="Automated classification based on keywords",
            recommended_actions=[
                f"Dispatch team to inspect the {category}",
                "Document the issue with photos",
                "Create work order for resolution"
            ],
            estimated_resolution_time="3-5 business days",
            priority_score=priority
        )
    
    async def generate_action_plan(
        self,
        report_data: dict
    ) -> dict:
        """Generate detailed action plan for report resolution"""
        
        action_prompt = ChatPromptTemplate.from_template(
            """Based on the following civic issue, create a detailed action plan for municipal workers.

Issue: {category}
Severity: {severity}
Description: {description}
Location: {location}

Provide:
1. Immediate actions (if critical)
2. Required resources and equipment
3. Estimated personnel needed
4. Step-by-step resolution process
5. Safety precautions
6. Estimated timeline

Format as JSON."""
        )
        
        try:
            messages = action_prompt.format_messages(**report_data)
            response = await self.llm.ainvoke(messages)
            return json.loads(response.content)
        except Exception as e:
            print(f"Action plan generation error: {e}")
            return {
                "status": "error",
                "message": "Could not generate action plan"
            }


# Singleton instance
ai_agent = AIAgentService()
ai_service = ai_agent