#!/usr/bin/env python3
"""
Test script for final assessment generation
Ensures the system produces complete ERM assessments with all required components
"""

import json
import sys
import os
from datetime import datetime

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from agents.research_agent import run_risk_assessment

def test_final_assessment():
    """Test the final assessment generation"""
    print("Testing Final Assessment Generation")
    print("=" * 60)
    
    # Test with a simple company
    ticker = "AAPL"
    print(f"Testing with {ticker}...")
    
    try:
        # Run assessment with mock data
        result = run_risk_assessment(ticker, use_mock_data=True)
        
        print("\n" + "=" * 60)
        print("ASSESSMENT RESULT")
        print("=" * 60)
        print(json.dumps(result, indent=2))
        
        # Validate the result
        print("\n" + "=" * 60)
        print("VALIDATION")
        print("=" * 60)
        
        required_fields = [
            "company",
            "assessment_date",
            "risk_assessment",
            "financial_health", 
            "recommendations",
            "summary"
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in result:
                missing_fields.append(field)
            else:
                print(f"✅ {field}: Present")
        
        if missing_fields:
            print(f"❌ Missing fields: {missing_fields}")
        else:
            print("✅ All required fields present")
        
        # Check risk_assessment structure
        if "risk_assessment" in result:
            risk_assessment = result["risk_assessment"]
            risk_fields = ["overall_risk_level", "risk_score", "key_risk_indicators", "risks"]
            
            for field in risk_fields:
                if field in risk_assessment:
                    print(f"✅ risk_assessment.{field}: Present")
                else:
                    print(f"❌ risk_assessment.{field}: Missing")
        
        # Check financial_health structure
        if "financial_health" in result:
            financial_health = result["financial_health"]
            health_fields = ["liquidity_score", "solvency_score", "profitability_score", "overall_financial_health"]
            
            for field in health_fields:
                if field in financial_health:
                    print(f"✅ financial_health.{field}: Present")
                else:
                    print(f"❌ financial_health.{field}: Missing")
        
        # Check recommendations
        if "recommendations" in result:
            recommendations = result["recommendations"]
            if isinstance(recommendations, list) and len(recommendations) >= 3:
                print(f"✅ recommendations: {len(recommendations)} recommendations present")
            else:
                print(f"❌ recommendations: Insufficient recommendations ({len(recommendations) if isinstance(recommendations, list) else 'not a list'})")
        
        # Check summary
        if "summary" in result:
            summary = result["summary"]
            if isinstance(summary, str) and len(summary) > 50:
                print(f"✅ summary: Present ({len(summary)} characters)")
            else:
                print(f"❌ summary: Too short or missing ({len(summary) if isinstance(summary, str) else 'not a string'})")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during assessment: {e}")
        return None

def create_complete_assessment_example():
    """Create an example of what a complete assessment should look like"""
    print("\n" + "=" * 60)
    print("COMPLETE ASSESSMENT EXAMPLE")
    print("=" * 60)
    
    example = {
        "company": "NVIDIA Corporation",
        "assessment_date": "2025-06-21",
        "risk_assessment": {
            "overall_risk_level": "Medium",
            "risk_score": 6,
            "key_risk_indicators": [
                "Market competition intensity",
                "Supply chain vulnerability",
                "Technology disruption potential",
                "Regulatory compliance pressure"
            ],
            "risks": [
                {
                    "category": "Strategic",
                    "description": "Intense competition in GPU and AI markets",
                    "severity": "High",
                    "likelihood": "High",
                    "financial_impact": "10-20% market value impact",
                    "mitigation_status": "Partial",
                    "trend": "Increasing"
                },
                {
                    "category": "Operational",
                    "description": "Supply chain disruptions and manufacturing risks",
                    "severity": "High",
                    "likelihood": "Medium",
                    "financial_impact": "5-15% revenue impact",
                    "mitigation_status": "Partial",
                    "trend": "Stable"
                },
                {
                    "category": "Technological",
                    "description": "Cybersecurity threats and IP protection",
                    "severity": "Critical",
                    "likelihood": "Medium",
                    "financial_impact": "5-10% operational cost impact",
                    "mitigation_status": "Comprehensive",
                    "trend": "Increasing"
                }
            ]
        },
        "financial_health": {
            "liquidity_score": 8,
            "solvency_score": 9,
            "profitability_score": 7,
            "overall_financial_health": "Excellent"
        },
        "recommendations": [
            "Strengthen supply chain resilience through supplier diversification",
            "Enhance cybersecurity infrastructure and threat detection",
            "Accelerate innovation pipeline to maintain competitive advantage",
            "Develop comprehensive risk monitoring and early warning systems",
            "Implement strategic partnerships to reduce market concentration risks"
        ],
        "summary": "NVIDIA Corporation faces moderate overall risk with strong financial health providing a solid foundation for risk management. Key concerns include intense market competition and supply chain vulnerabilities, requiring immediate attention to strategic positioning and operational resilience."
    }
    
    print(json.dumps(example, indent=2))
    return example

def main():
    """Main test function"""
    print("Final Assessment Generation Test")
    print("=" * 60)
    
    # Test the current system
    result = test_final_assessment()
    
    # Show what a complete assessment should look like
    create_complete_assessment_example()
    
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    if result and all(field in result for field in ["company", "assessment_date", "risk_assessment", "financial_health", "recommendations", "summary"]):
        print("✅ System is generating complete assessments")
    else:
        print("❌ System needs improvement to generate complete assessments")
        print("   Missing components need to be added to the final assessment generation")

if __name__ == "__main__":
    main() 