#!/usr/bin/env python3
"""
Simple test script to validate the ERM Risk Assessment System setup
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from config import validate_config
        print("✓ Config module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import config: {e}")
        return False
    
    try:
        from data.data_sources import get_company_profile, get_company_news, get_financial_data
        print("✓ Data sources module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import data sources: {e}")
        return False
    
    try:
        from utils.prompts import RISK_CATEGORIES, RESEARCH_AGENT_PROMPT
        print("✓ Prompts module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import prompts: {e}")
        return False
    
    try:
        from agents.research_agent import run_risk_assessment
        print("✓ Research agent module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import research agent: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration validation"""
    print("\nTesting configuration...")
    
    try:
        from config import validate_config
        validate_config()
        print("✓ Configuration validation passed")
        return True
    except ValueError as e:
        print(f"✗ Configuration validation failed: {e}")
        print("Please ensure you have set up your .env file with required API keys")
        return False
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_data_collection():
    """Test basic data collection functionality"""
    print("\nTesting data collection...")
    
    try:
        from data.data_sources import get_company_profile
        
        # Test with a well-known company
        profile = get_company_profile("AAPL")
        
        if "error" in profile:
            print(f"✗ Data collection failed: {profile['error']}")
            return False
        
        if not profile or len(profile) < 3:
            print("✗ Insufficient profile data collected")
            return False
        
        print(f"✓ Successfully collected profile data for AAPL")
        print(f"  Company: {profile.get('name', 'N/A')}")
        print(f"  Sector: {profile.get('sector', 'N/A')}")
        return True
        
    except Exception as e:
        print(f"✗ Data collection test failed: {e}")
        return False

def test_prompts():
    """Test that prompts are properly formatted"""
    print("\nTesting prompts...")
    
    try:
        from utils.prompts import RISK_CATEGORIES, RESEARCH_AGENT_PROMPT
        
        if not RISK_CATEGORIES or len(RISK_CATEGORIES) < 5:
            print("✗ Insufficient risk categories defined")
            return False
        
        if not RESEARCH_AGENT_PROMPT or len(RISK_CATEGORIES) < 100:
            print("✗ Research agent prompt too short")
            return False
        
        print(f"✓ Found {len(RISK_CATEGORIES)} risk categories")
        print(f"✓ Research agent prompt is {len(RISK_CATEGORIES)} characters")
        return True
        
    except Exception as e:
        print(f"✗ Prompts test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("ERM Risk Assessment System - Setup Test")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    tests = [
        test_imports,
        test_configuration,
        test_data_collection,
        test_prompts
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Your system is ready to use.")
        print("\nTo run a risk assessment:")
        print("  python app/main.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("\nCommon issues:")
        print("  1. Missing API keys in .env file")
        print("  2. Missing dependencies (run: pip install -r requirements.txt)")
        print("  3. Network connectivity issues")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 