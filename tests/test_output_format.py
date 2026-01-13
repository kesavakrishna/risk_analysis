#!/usr/bin/env python3
"""
Test script to verify the output format of the ERM risk assessment system
"""

import json
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_output_format():
    """Test the output format generation"""
    print("Testing ERM Risk Assessment Output Format")
    print("=" * 50)
    
    try:
        from agents.research_agent import create_structured_assessment_from_conversation
        
        # Test with mock conversation
        mock_messages = [
            {
                "name": "ERMCoordinator",
                "content": 'Company data: {"name": "Tesla, Inc.", "sector": "Technology"}'
            }
        ]
        
        # Generate structured assessment
        assessment = create_structured_assessment_from_conversation(mock_messages)
        
        # Validate the structure
        required_fields = [
            "company", "assessment_date", "risk_assessment", 
            "financial_health", "recommendations", "summary"
        ]
        
        risk_assessment_fields = [
            "overall_risk_level", "risk_score", "key_risk_indicators", "risks"
        ]
        
        financial_health_fields = [
            "liquidity_score", "solvency_score", "profitability_score", "overall_financial_health"
        ]
        
        print("✓ Assessment generated successfully")
        
        # Check required fields
        for field in required_fields:
            if field in assessment:
                print(f"✓ {field} field present")
            else:
                print(f"✗ {field} field missing")
        
        # Check risk assessment fields
        if "risk_assessment" in assessment:
            for field in risk_assessment_fields:
                if field in assessment["risk_assessment"]:
                    print(f"✓ risk_assessment.{field} present")
                else:
                    print(f"✗ risk_assessment.{field} missing")
        
        # Check financial health fields
        if "financial_health" in assessment:
            for field in financial_health_fields:
                if field in assessment["financial_health"]:
                    print(f"✓ financial_health.{field} present")
                else:
                    print(f"✗ financial_health.{field} missing")
        
        # Check risks array
        if "risk_assessment" in assessment and "risks" in assessment["risk_assessment"]:
            risks = assessment["risk_assessment"]["risks"]
            if len(risks) > 0:
                print(f"✓ {len(risks)} risks identified")
                
                # Check first risk structure
                first_risk = risks[0]
                risk_fields = ["category", "description", "severity", "likelihood", "financial_impact", "mitigation_status", "trend"]
                for field in risk_fields:
                    if field in first_risk:
                        print(f"✓ risk.{field} present")
                    else:
                        print(f"✗ risk.{field} missing")
            else:
                print("✗ No risks identified")
        
        # Check recommendations
        if "recommendations" in assessment:
            recommendations = assessment["recommendations"]
            if len(recommendations) > 0:
                print(f"✓ {len(recommendations)} recommendations provided")
            else:
                print("✗ No recommendations provided")
        
        # Display sample output
        print("\n" + "=" * 50)
        print("SAMPLE OUTPUT FORMAT:")
        print("=" * 50)
        print(json.dumps(assessment, indent=2))
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_output_format()
    sys.exit(0 if success else 1) 