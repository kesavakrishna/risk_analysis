"""
Pydantic models for structured ERM assessment output
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import date

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Likelihood(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class MitigationStatus(str, Enum):
    NONE = "None"
    PARTIAL = "Partial"
    COMPREHENSIVE = "Comprehensive"

class Trend(str, Enum):
    INCREASING = "Increasing"
    STABLE = "Stable"
    DECREASING = "Decreasing"

class FinancialHealthLevel(str, Enum):
    POOR = "Poor"
    FAIR = "Fair"
    GOOD = "Good"
    EXCELLENT = "Excellent"

class Risk(BaseModel):
    category: str = Field(..., description="Risk category (Strategic/Operational/Financial/Compliance/Reputational/Technological/Environmental)")
    description: str = Field(..., description="Brief risk description")
    severity: RiskLevel = Field(..., description="Risk severity level")
    likelihood: Likelihood = Field(..., description="Likelihood of risk occurrence")
    financial_impact: str = Field(..., description="Quantified impact estimate (e.g., '5-15% revenue impact')")
    mitigation_status: MitigationStatus = Field(..., description="Current mitigation status")
    trend: Trend = Field(..., description="Risk trend direction")

class RiskAssessment(BaseModel):
    overall_risk_level: RiskLevel = Field(..., description="Overall risk level for the company")
    risk_score: int = Field(..., ge=1, le=10, description="Risk score on 1-10 scale")
    key_risk_indicators: List[str] = Field(..., min_items=4, max_items=6, description="Key risk indicators to monitor")
    risks: List[Risk] = Field(..., min_items=5, max_items=10, description="List of identified risks")

class FinancialHealthAssessment(BaseModel):
    liquidity_score: int = Field(..., ge=1, le=10, description="Liquidity score on 1-10 scale")
    solvency_score: int = Field(..., ge=1, le=10, description="Solvency score on 1-10 scale")
    profitability_score: int = Field(..., ge=1, le=10, description="Profitability score on 1-10 scale")
    overall_financial_health: FinancialHealthLevel = Field(..., description="Overall financial health assessment")

class ERMAssessment(BaseModel):
    company: str = Field(..., description="Company name")
    assessment_date: date = Field(..., description="Assessment date")
    risk_assessment: RiskAssessment = Field(..., description="Risk assessment details")
    financial_health: FinancialHealthAssessment = Field(..., description="Financial health assessment")
    recommendations: List[str] = Field(..., min_items=5, max_items=8, description="Specific actionable recommendations")
    summary: str = Field(..., min_length=50, max_length=500, description="Executive summary of overall risk position and key concerns")

    class Config:
        json_schema_extra = {
            "example": {
                "company": "Apple Inc",
                "assessment_date": "2025-06-21",
                "risk_assessment": {
                    "overall_risk_level": "Medium",
                    "risk_score": 6,
                    "key_risk_indicators": ["Revenue growth rate", "AI development progress", "Supply chain stability", "Regulatory compliance"],
                    "risks": [
                        {
                            "category": "Strategic",
                            "description": "Failure to maintain innovation leadership in emerging technologies",
                            "severity": "High",
                            "likelihood": "Medium",
                            "financial_impact": "Potential loss of market share, estimated at $20-50 billion annually",
                            "mitigation_status": "Partial",
                            "trend": "Increasing"
                        }
                    ]
                },
                "financial_health": {
                    "liquidity_score": 9,
                    "solvency_score": 8,
                    "profitability_score": 10,
                    "overall_financial_health": "Excellent"
                },
                "recommendations": [
                    "Increase investment in AI research and development",
                    "Strengthen supply chain resilience through diversification",
                    "Enhance cybersecurity measures",
                    "Proactively engage with regulators",
                    "Improve transparency in environmental initiatives"
                ],
                "summary": "Apple faces moderate risks primarily related to innovation and supply chain vulnerabilities. While financially strong, proactive risk management is crucial to maintain competitive edge."
            }
        } 