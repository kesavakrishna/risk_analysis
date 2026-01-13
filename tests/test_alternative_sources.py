#!/usr/bin/env python3
"""
Test script for alternative data sources
Tests Alpha Vantage, IEX Cloud, and Finnhub APIs
"""

import os
import sys
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from data.data_sources import (
    get_company_profile_alpha_vantage,
    get_company_profile_iex,
    get_financial_data_alpha_vantage,
    get_mock_data_for_demo
)

load_dotenv()

def test_alpha_vantage():
    """Test Alpha Vantage API"""
    print("=" * 60)
    print("Testing Alpha Vantage API")
    print("=" * 60)
    
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        print("❌ ALPHA_VANTAGE_API_KEY not found in .env file")
        print("   Get free API key from: https://www.alphavantage.co/support/#api-key")
        return False
    
    print(f"✅ API Key found: {api_key[:8]}...")
    
    # Test company profile
    print("\nTesting company profile...")
    try:
        profile = get_company_profile_alpha_vantage("AAPL")
        if profile:
            print("✅ Company profile successful")
            print(f"   Company: {profile.get('name', 'N/A')}")
            print(f"   Sector: {profile.get('sector', 'N/A')}")
            print(f"   Market Cap: ${profile.get('market_cap', 0):,.0f}")
        else:
            print("❌ Company profile failed")
            return False
    except Exception as e:
        print(f"❌ Company profile error: {e}")
        return False
    
    # Test financial data
    print("\nTesting financial data...")
    try:
        financials = get_financial_data_alpha_vantage("AAPL")
        if financials:
            print("✅ Financial data successful")
            print(f"   Revenue: ${financials.get('revenue', 0):,.0f}")
            print(f"   Net Income: ${financials.get('net_income', 0):,.0f}")
            print(f"   Profit Margin: {financials.get('profit_margin', 0):.1f}%")
        else:
            print("❌ Financial data failed")
            return False
    except Exception as e:
        print(f"❌ Financial data error: {e}")
        return False
    
    return True

def test_iex_cloud():
    """Test IEX Cloud API"""
    print("\n" + "=" * 60)
    print("Testing IEX Cloud API")
    print("=" * 60)
    
    api_key = os.getenv("IEX_API_KEY")
    if not api_key:
        print("❌ IEX_API_KEY not found in .env file")
        print("   Get free API key from: https://iexcloud.io/cloud-login#/register")
        return False
    
    print(f"✅ API Key found: {api_key[:8]}...")
    
    # Test company profile
    print("\nTesting company profile...")
    try:
        profile = get_company_profile_iex("AAPL")
        if profile:
            print("✅ Company profile successful")
            print(f"   Company: {profile.get('name', 'N/A')}")
            print(f"   Sector: {profile.get('sector', 'N/A')}")
            print(f"   Market Cap: ${profile.get('market_cap', 0):,.0f}")
        else:
            print("❌ Company profile failed")
            return False
    except Exception as e:
        print(f"❌ Company profile error: {e}")
        return False
    
    return True

def test_mock_data():
    """Test mock data functionality"""
    print("\n" + "=" * 60)
    print("Testing Mock Data")
    print("=" * 60)
    
    try:
        profile, news, financials = get_mock_data_for_demo("TSLA")
        
        print("✅ Mock data generation successful")
        print(f"   Company: {profile.get('name', 'N/A')}")
        print(f"   Sector: {profile.get('sector', 'N/A')}")
        print(f"   News Articles: {len(news)}")
        print(f"   Revenue: ${financials.get('revenue', 0):,.0f}")
        
        return True
    except Exception as e:
        print(f"❌ Mock data error: {e}")
        return False

def main():
    """Main test function"""
    print("Alternative Data Sources Test")
    print("=" * 60)
    print("This script tests the alternative data sources")
    print("Make sure you have API keys in your .env file")
    print("=" * 60)
    
    results = []
    
    # Test Alpha Vantage
    results.append(("Alpha Vantage", test_alpha_vantage()))
    
    # Test IEX Cloud
    results.append(("IEX Cloud", test_iex_cloud()))
    
    # Test Mock Data
    results.append(("Mock Data", test_mock_data()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name:15} {status}")
    
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    if any(success for _, success in results):
        print("✅ At least one data source is working")
        print("   You can run the risk assessment system")
    else:
        print("❌ No data sources are working")
        print("   Please check your API keys and network connection")
    
    print("\nFor immediate testing, use demo mode:")
    print("   python demo.py")

if __name__ == "__main__":
    main() 