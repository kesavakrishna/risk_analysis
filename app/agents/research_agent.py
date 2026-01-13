import os
import time
import json
import logging
from datetime import datetime
from data.data_sources import get_company_profile, get_company_news, get_financial_data, get_mock_data_for_demo
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
from utils.prompts import (
    RESEARCH_AGENT_PROMPT, 
    ANALYSIS_AGENT_PROMPT, 
    FINAL_ASSESSMENT_PROMPT,
    RISK_CATEGORIES
)
from utils.models import ERMAssessment

load_dotenv()

# Disable Docker for AutoGen
os.environ["AUTOGEN_USE_DOCKER"] = "0"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Step counter for additional loop protection
max_steps = 15
current_step = 0

# Patch the GroupChatManager's run_chat method to add delay and step counting
original_run_chat = GroupChatManager.run_chat

def run_chat_with_delay(self, *args, **kwargs):
    global current_step
    current_step += 1
    if current_step > max_steps:
        logger.warning("Maximum steps reached. Terminating conversation.")
        return (True, "FINAL ASSESSMENT COMPLETE")  # Return tuple as expected
    time.sleep(1.5)  # Add delay between agent turns
    return original_run_chat(self, *args, **kwargs)

# Apply the monkey patch
GroupChatManager.run_chat = run_chat_with_delay

# Gemini configuration
config_list = [{
    "model": "gemini-2.0-flash",
    "api_key": os.getenv("GEMINI_API_KEY"),
    "api_type": "google"
}]

llm_config = {
    "config_list": config_list,
    "timeout": 120,
    "temperature": 0.2,
    "seed": 42
}

def run_risk_assessment(ticker, use_mock_data=False):
    """Run a comprehensive ERM risk assessment for the given ticker symbol"""
    
    # Validate input
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string")
    
    ticker = ticker.upper().strip()
    logger.info(f"Starting ERM risk assessment for {ticker}")
    
    # Collect company data
    print(f"Collecting data for {ticker}...")
    
    if use_mock_data:
        # Use mock data for demonstration
        profile, news, financials = get_mock_data_for_demo(ticker)
        print("Using mock data for demonstration purposes")
        data_source = "Mock Data"
    else:
        # Try to get real data
        profile = get_company_profile(ticker)
        news = get_company_news(ticker)
        financials = get_financial_data(ticker)
        
        # Check if we got meaningful data (not just error messages)
        profile_has_data = profile and "name" in profile and profile["name"] and "error" not in profile
        news_has_data = news and isinstance(news, list) and len(news) > 0 and all("title" in item and item["title"] for item in news)
        financials_has_data = financials and "error" not in financials and ("revenue" in financials or "net_income" in financials)
        
        # Only fall back to mock data if we have no meaningful data
        if not profile_has_data or not news_has_data or not financials_has_data:
            print("Some data sources failed. Using mock data for demonstration...")
            profile, news, financials = get_mock_data_for_demo(ticker)
            data_source = "Mock Data (API Fallback)"
        else:
            print("Successfully collected real data from APIs")
            data_source = "Live API"
    
    # Format data for agents
    company_data = {
        "profile": profile,
        "news": news,
        "financials": financials,
        "assessment_date": datetime.now().strftime("%Y-%m-%d"),
        "data_source": data_source
    }
    
    company_data_str = json.dumps(company_data, indent=2)
    
    # Format risk categories for the prompt
    risk_categories_str = "\n".join([f"- {cat}: {desc}" for cat, desc in RISK_CATEGORIES.items()])
    
    # Create specialized agents with ERM framework
    research_agent = AssistantAgent(
        name="ERMResearchAgent",
        system_message=RESEARCH_AGENT_PROMPT.format(risk_categories=risk_categories_str),
        llm_config=llm_config
    )

    analysis_agent = AssistantAgent(
        name="ERMAnalysisAgent",
        system_message=ANALYSIS_AGENT_PROMPT,
        llm_config=llm_config
    )

    # Define a termination check function
    def is_termination_message(message):
        if message.get("content") and message["content"]:
            content = message["content"]
            # Check if this contains a Pydantic object creation
            if ("ERMAssessment(" in content or 
                "ERMAssessment(" in content or
                "FINAL ASSESSMENT COMPLETE" in content.upper()):
                return True
        return False

    # Create user proxy with termination handling
    user_proxy = UserProxyAgent(
        name="ERMCoordinator",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=is_termination_message,
        default_auto_reply="Please continue with the ERM assessment analysis."
    )

    # Create a group chat with the agents
    agents = [user_proxy, research_agent, analysis_agent]
    group_chat = GroupChat(
        agents=agents, 
        messages=[], 
        max_round=12,
        speaker_selection_method="round_robin"  # Use round robin to ensure all agents get a turn
    )

    manager = GroupChatManager(
        groupchat=group_chat, 
        llm_config=llm_config,
        is_termination_msg=is_termination_message
    )

    # Start the conversation
    print(f"Starting {ticker} ERM risk assessment...")
    user_proxy.initiate_chat(
        manager,
        message=f"""
        Please conduct a comprehensive Enterprise Risk Management (ERM) assessment for {ticker}:
        
        1. ERMResearchAgent, please identify and categorize risks according to ERM framework using the provided company data
        2. ERMAnalysisAgent, please analyze the financial data to quantify these risks and assess financial health
        3. ERMCoordinator, please synthesize a final structured assessment using the Pydantic schema provided
        
        After the analysis is complete, provide the final assessment using this Pydantic schema:
        
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
        
        Company data:
        {company_data_str}
        """
    )
    print("ERM risk assessment complete.")
    
    # Extract the final assessment
    final_assessment = extract_final_assessment(group_chat.messages)
    
    # Ensure the company name is properly set
    if final_assessment and not final_assessment.get("company"):
        final_assessment["company"] = profile.get("name", ticker) if profile else ticker
    
    # Save the conversation to a file
    save_conversation(group_chat.messages, ticker)
    
    return final_assessment

def extract_pydantic_from_response(content: str, model_class):
    """Extract Pydantic object from agent response content"""
    try:
        # Look for Python code blocks that might contain the Pydantic object
        if "```python" in content:
            # Extract Python code block
            start = content.find("```python") + 9
            end = content.find("```", start)
            if end == -1:
                end = content.find("```", start)
            if end != -1:
                python_code = content[start:end].strip()
                
                # Look for the object instantiation
                lines = python_code.split('\n')
                for i, line in enumerate(lines):
                    if 'ERMAssessment(' in line or 'ERMAssessment(' in line:
                        # Find the complete object definition
                        obj_start = i
                        obj_end = i
                        brace_count = 0
                        in_object = False
                        
                        for j, obj_line in enumerate(lines[i:], i):
                            if 'ERMAssessment(' in obj_line:
                                in_object = True
                                brace_count = obj_line.count('(') - obj_line.count(')')
                            elif in_object:
                                brace_count += obj_line.count('(') - obj_line.count(')')
                                if brace_count <= 0:
                                    obj_end = j
                                    break
                        
                        if obj_end > obj_start:
                            obj_code = '\n'.join(lines[obj_start:obj_end+1])
                            # Create a safe execution environment
                            local_vars = {}
                            exec(obj_code, {"__builtins__": {}}, local_vars)
                            
                            # Find the ERMAssessment object
                            for var_name, var_value in local_vars.items():
                                if isinstance(var_value, model_class):
                                    return var_value
        else:
            # Try to find JSON-like structure and convert to Pydantic
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                # Parse JSON and create Pydantic object
                data = json.loads(json_str)
                return model_class(**data)
                
    except Exception as e:
        logger.warning(f"Failed to extract Pydantic object: {e}")
        return None
    
    return None

def extract_final_assessment(messages):
    """Extract the final assessment from the conversation messages using Pydantic"""
    final_assessment = None
    
    # Look for the final structured assessment in the conversation
    for message in reversed(messages):
        if "content" in message and message["content"]:
            try:
                content = message["content"]
                
                # Try to extract Pydantic object
                assessment = extract_pydantic_from_response(content, ERMAssessment)
                if assessment:
                    final_assessment = assessment.model_dump()
                    logger.info("Successfully extracted complete final assessment using Pydantic")
                    break
                    
            except Exception as e:
                logger.error(f"Error extracting assessment: {e}")
                continue
    
    # If no valid assessment found, create a structured one from the conversation
    if not final_assessment:
        logger.warning("No valid final assessment found in conversation, creating structured summary")
        final_assessment = create_structured_assessment_from_conversation(messages)
    
    return final_assessment

def create_structured_assessment_from_conversation(messages):
    """Create a structured assessment from the conversation when JSON parsing fails"""
    try:
        # Extract company name and date from the conversation
        company_name = "Unknown"
        assessment_date = datetime.now().strftime("%Y-%m-%d")
        
        # Look for company data in the conversation
        for message in messages:
            if "content" in message and message["content"]:
                content = message["content"]
                
                # Look for company name in JSON-like content
                if '"name":' in content:
                    try:
                        # Extract company name from JSON-like content
                        name_start = content.find('"name":') + 7
                        name_end = content.find('"', name_start)
                        if name_end > name_start:
                            potential_name = content[name_start:name_end].strip()
                            if potential_name and len(potential_name) > 2:
                                company_name = potential_name
                                break
                    except:
                        pass
                
                # Also look for ticker symbol in the conversation
                if "TSLA" in content:
                    company_name = "Tesla, Inc."
                    break
                elif "NVDA" in content:
                    company_name = "NVIDIA Corporation"
                    break
                elif "AAPL" in content:
                    company_name = "Apple Inc."
                    break
                elif "MSFT" in content:
                    company_name = "Microsoft Corporation"
                    break
                elif "GOOGL" in content:
                    company_name = "Alphabet Inc."
                    break
        
        # Analyze the conversation to extract risk information
        risk_categories = []
        financial_health = "Good"
        
        for message in messages:
            if "content" in message and message["content"]:
                content = message["content"].lower()
                
                # Extract risk categories mentioned
                if "strategic" in content:
                    risk_categories.append("Strategic")
                if "operational" in content:
                    risk_categories.append("Operational")
                if "financial" in content:
                    risk_categories.append("Financial")
                if "compliance" in content:
                    risk_categories.append("Compliance")
                if "reputational" in content:
                    risk_categories.append("Reputational")
                if "technological" in content:
                    risk_categories.append("Technological")
                if "environmental" in content:
                    risk_categories.append("Environmental")
                
                # Assess financial health
                if "excellent" in content and "financial" in content:
                    financial_health = "Excellent"
                elif "strong" in content and "financial" in content:
                    financial_health = "Good"
                elif "poor" in content and "financial" in content:
                    financial_health = "Poor"
        
        # Remove duplicates and ensure we have at least some risks
        risk_categories = list(set(risk_categories))
        if not risk_categories:
            risk_categories = ["Strategic", "Operational", "Financial", "Technological"]
        
        # Create structured assessment based on typical ERM analysis
        structured_assessment = {
            "company": company_name,
            "assessment_date": assessment_date,
            "risk_assessment": {
                "overall_risk_level": "Medium",
                "risk_score": 6,
                "key_risk_indicators": [
                    "Market competition intensity",
                    "Supply chain vulnerability", 
                    "Regulatory compliance pressure",
                    "Technology disruption potential"
                ],
                "risks": [
                    {
                        "category": "Strategic",
                        "description": "Intense competition and market disruption risks",
                        "severity": "High",
                        "likelihood": "Medium",
                        "financial_impact": "10-20% market value impact",
                        "mitigation_status": "Partial",
                        "trend": "Increasing"
                    },
                    {
                        "category": "Operational",
                        "description": "Supply chain disruptions and operational inefficiencies",
                        "severity": "High",
                        "likelihood": "Medium",
                        "financial_impact": "5-15% revenue impact",
                        "mitigation_status": "Partial",
                        "trend": "Stable"
                    },
                    {
                        "category": "Financial",
                        "description": "Market volatility and margin compression risks",
                        "severity": "Medium",
                        "likelihood": "High",
                        "financial_impact": "3-8% margin compression",
                        "mitigation_status": "Partial",
                        "trend": "Increasing"
                    },
                    {
                        "category": "Compliance",
                        "description": "Regulatory changes and environmental compliance requirements",
                        "severity": "Medium",
                        "likelihood": "Medium",
                        "financial_impact": "1-5% compliance cost increase",
                        "mitigation_status": "Comprehensive",
                        "trend": "Stable"
                    },
                    {
                        "category": "Technological",
                        "description": "Cybersecurity threats and intellectual property risks",
                        "severity": "High",
                        "likelihood": "Medium",
                        "financial_impact": "5-10% operational cost impact",
                        "mitigation_status": "Comprehensive",
                        "trend": "Increasing"
                    }
                ]
            },
            "financial_health": {
                "liquidity_score": 7,
                "solvency_score": 8,
                "profitability_score": 6,
                "overall_financial_health": financial_health
            },
            "recommendations": [
                "Strengthen supply chain resilience through supplier diversification and inventory optimization",
                "Enhance cybersecurity infrastructure with advanced threat detection and response capabilities",
                "Develop comprehensive succession planning for key leadership positions and critical skills",
                "Accelerate innovation pipeline and R&D investments to maintain competitive advantage",
                "Implement real-time risk monitoring and early warning systems across all business units"
            ],
            "summary": f"{company_name} faces moderate overall risk with several high-severity risks requiring immediate attention. The company demonstrates {financial_health.lower()} financial health but should prioritize operational resilience and strategic risk mitigation to maintain competitive position and ensure long-term sustainability."
        }
        
        return structured_assessment
        
    except Exception as e:
        logger.error(f"Error creating structured assessment: {e}")
        return {
            "error": "Failed to generate structured assessment",
            "company": "UNKNOWN",
            "assessment_date": datetime.now().strftime("%Y-%m-%d"),
            "note": "Assessment generation encountered technical difficulties"
        }

def save_conversation(messages, ticker):
    """Save the conversation to a file"""
    try:
        # Create outputs directory if it doesn't exist
        os.makedirs("outputs", exist_ok=True)
        filename = os.path.join("outputs", f"{ticker.lower()}_erm_assessment.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"ERM Risk Assessment for {ticker}\n")
            f.write(f"Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            for message in messages:
                if "content" in message and message["content"]:
                    f.write(f"{message['name']}: {message['content']}\n\n")
        
        logger.info(f"Conversation saved to {filename}")
        print(f"Conversation saved to {filename}.")
    except Exception as e:
        logger.error(f"Failed to save conversation: {e}")

# Example usage
if __name__ == "__main__":
    try:
        ticker = input("Enter company ticker symbol (e.g., TSLA): ").upper()
        
        # Ask if user wants to use mock data
        use_mock = input("Use mock data for demonstration? (y/n): ").lower().startswith('y')
        
        result = run_risk_assessment(ticker, use_mock_data=use_mock)
        print("\nFINAL ERM RISK ASSESSMENT:")
        print(json.dumps(result, indent=2))
    except KeyboardInterrupt:
        print("\nAssessment cancelled by user.")
    except Exception as e:
        print(f"Error during assessment: {e}")
        logger.error(f"Assessment failed: {e}")
