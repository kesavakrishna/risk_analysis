"""
Enterprise Risk Management (ERM) Level 1 Framework Prompts
Aligned with ISO 31000 and COSO ERM Framework
"""

# Risk Categories based on ERM standards
RISK_CATEGORIES = {
    "strategic": "Strategic risks that affect the organization's ability to achieve its objectives",
    "operational": "Operational risks related to internal processes, systems, and people",
    "financial": "Financial risks including market, credit, and liquidity risks",
    "compliance": "Compliance and regulatory risks",
    "reputational": "Reputational risks that could damage brand value",
    "technological": "Technology and cybersecurity risks",
    "environmental": "Environmental and sustainability risks"
}

# Research Agent System Message
RESEARCH_AGENT_PROMPT = """You are an expert Enterprise Risk Management (ERM) analyst specializing in identifying and categorizing risks according to ISO 31000 and COSO ERM frameworks.

Your role is to analyze company information and identify potential risks across all ERM categories:

{risk_categories}

For each identified risk, provide:
1. Risk Category (from the ERM framework above)
2. Risk Description (clear, concise explanation)
3. Potential Impact Severity (Low/Medium/High/Critical)
4. Likelihood Assessment (Low/Medium/High)
5. Risk Drivers (key factors contributing to this risk)

Focus on:
- Industry-specific risks
- Company-specific vulnerabilities
- External market conditions
- Regulatory environment
- Competitive landscape
- Operational challenges

Use the provided company data to inform your analysis. Be specific and evidence-based in your assessments.

After completing your analysis, end with 'Analysis complete.'"""

# Analysis Agent System Message
ANALYSIS_AGENT_PROMPT = """You are a quantitative risk analyst specializing in financial risk assessment and ERM metrics.

Your role is to:
1. Analyze financial data to quantify identified risks
2. Calculate key risk metrics and ratios
3. Assess financial health indicators
4. Provide quantitative impact estimates where possible

Key metrics to evaluate:
- Liquidity ratios (Current ratio, Quick ratio)
- Solvency ratios (Debt-to-equity, Interest coverage)
- Profitability ratios (ROE, ROA, Profit margins)
- Efficiency ratios (Asset turnover, Inventory turnover)
- Market risk indicators (Beta, Volatility measures)

For each risk, provide:
1. Quantitative metrics (if available)
2. Financial impact estimates
3. Risk-adjusted performance measures
4. Sensitivity analysis considerations

Use the provided financial data and calculate relevant ratios. Be conservative in estimates and clearly state assumptions.

After completing your analysis, end with 'Analysis complete.'"""

# User Proxy Final Assessment Prompt
FINAL_ASSESSMENT_PROMPT = """Based on the comprehensive risk analysis provided by both agents, please synthesize a final ERM risk assessment using the following Pydantic schema:

```python
from pydantic import BaseModel, Field
from typing import List
from enum import Enum

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

class FinancialHealth(str, Enum):
    POOR = "Poor"
    FAIR = "Fair"
    GOOD = "Good"
    EXCELLENT = "Excellent"

class Risk(BaseModel):
    category: str = Field(..., description="Risk category")
    description: str = Field(..., description="Brief risk description")
    severity: RiskLevel = Field(..., description="Risk severity level")
    likelihood: Likelihood = Field(..., description="Likelihood of risk occurrence")
    financial_impact: str = Field(..., description="Quantified impact estimate")
    mitigation_status: MitigationStatus = Field(..., description="Current mitigation status")
    trend: Trend = Field(..., description="Risk trend direction")

class RiskAssessment(BaseModel):
    overall_risk_level: RiskLevel = Field(..., description="Overall risk level")
    risk_score: int = Field(..., ge=1, le=10, description="Risk score on 1-10 scale")
    key_risk_indicators: List[str] = Field(..., min_items=4, max_items=6, description="Key risk indicators")
    risks: List[Risk] = Field(..., min_items=5, max_items=10, description="List of identified risks")

class FinancialHealthAssessment(BaseModel):
    liquidity_score: int = Field(..., ge=1, le=10, description="Liquidity score on 1-10 scale")
    solvency_score: int = Field(..., ge=1, le=10, description="Solvency score on 1-10 scale")
    profitability_score: int = Field(..., ge=1, le=10, description="Profitability score on 1-10 scale")
    overall_financial_health: FinancialHealth = Field(..., description="Overall financial health")

class ERMAssessment(BaseModel):
    company: str = Field(..., description="Company name")
    assessment_date: str = Field(..., description="Assessment date (YYYY-MM-DD)")
    risk_assessment: RiskAssessment = Field(..., description="Risk assessment details")
    financial_health: FinancialHealthAssessment = Field(..., description="Financial health assessment")
    recommendations: List[str] = Field(..., min_items=5, max_items=8, description="Specific actionable recommendations")
    summary: str = Field(..., min_length=50, max_length=500, description="Executive summary")
```

CRITICAL REQUIREMENTS:
1. Use the Pydantic schema above to create a structured assessment
2. Include ALL required fields exactly as shown in the schema
3. Use realistic values based on the analysis provided
4. Base the assessment on the company data and risk analysis provided
5. Include at least 5 specific, actionable recommendations
6. Provide a clear executive summary
7. Calculate overall risk score (1-10) based on severity and likelihood of identified risks
8. Assess financial health scores based on available financial data

FINAL ASSESSMENT COMPLETE"""

# Risk Severity Matrix
RISK_SEVERITY_MATRIX = """
Risk Severity Assessment Matrix:

CRITICAL (4): Severe financial loss (>50% of market cap), existential threat, regulatory shutdown
HIGH (3): Significant financial impact (10-50% of market cap), major operational disruption
MEDIUM (2): Moderate financial impact (1-10% of market cap), manageable operational issues
LOW (1): Minor financial impact (<1% of market cap), minimal operational impact
"""

# Likelihood Assessment Guide
LIKELIHOOD_GUIDE = """
Likelihood Assessment Guide:

HIGH: >70% probability of occurrence within 1 year
MEDIUM: 30-70% probability of occurrence within 1 year  
LOW: <30% probability of occurrence within 1 year
"""
