#!/usr/bin/env python3
"""
Diagnostic script to test rate limiting and API behavior
"""

import time
import requests
import yfinance as yf
from datetime import datetime

def test_yahoo_finance_api():
    """Test Yahoo Finance API with different approaches"""
    print("Testing Yahoo Finance API Rate Limits")
    print("=" * 50)
    
    test_tickers = ["AAPL", "MSFT", "GOOGL"]
    
    for i, ticker in enumerate(test_tickers):
        print(f"\nTest {i+1}: Fetching data for {ticker}")
        print("-" * 30)
        
        try:
            # Test 1: Basic yfinance call
            print(f"Attempting to fetch {ticker} data...")
            start_time = time.time()
            
            company = yf.Ticker(ticker)
            info = company.info
            
            end_time = time.time()
            duration = end_time - start_time
            
            if info and len(info) > 5:
                print(f"✓ Success! Duration: {duration:.2f}s")
                print(f"  Company: {info.get('shortName', 'N/A')}")
                print(f"  Sector: {info.get('sector', 'N/A')}")
                print(f"  Market Cap: ${info.get('marketCap', 0):,}")
            else:
                print(f"✗ Failed - insufficient data")
                
        except Exception as e:
            print(f"✗ Error: {e}")
        
        # Add delay between tests
        if i < len(test_tickers) - 1:
            print("Waiting 10 seconds before next test...")
            time.sleep(10)

def test_network_connectivity():
    """Test basic network connectivity"""
    print("\nTesting Network Connectivity")
    print("=" * 50)
    
    test_urls = [
        "https://finance.yahoo.com",
        "https://www.google.com",
        "https://httpbin.org/status/200"
    ]
    
    for url in test_urls:
        try:
            print(f"Testing {url}...")
            response = requests.get(url, timeout=10)
            print(f"✓ Status: {response.status_code}")
        except Exception as e:
            print(f"✗ Error: {e}")

def test_rate_limit_simulation():
    """Simulate rate limiting behavior"""
    print("\nRate Limit Simulation")
    print("=" * 50)
    
    print("This will test how the system handles rapid requests...")
    
    for i in range(3):
        print(f"\nRapid request {i+1}/3...")
        try:
            company = yf.Ticker("AAPL")
            info = company.info
            if info:
                print(f"✓ Request {i+1} successful")
            else:
                print(f"✗ Request {i+1} failed - no data")
        except Exception as e:
            print(f"✗ Request {i+1} failed: {e}")
        
        # Very short delay to trigger rate limiting
        time.sleep(1)

def main():
    """Run all tests"""
    print("Yahoo Finance API Rate Limit Diagnostics")
    print("=" * 60)
    print(f"Test started at: {datetime.now()}")
    print("=" * 60)
    
    # Test 1: Network connectivity
    test_network_connectivity()
    
    # Test 2: Basic API functionality
    test_yahoo_finance_api()
    
    # Test 3: Rate limit simulation
    test_rate_limit_simulation()
    
    print("\n" + "=" * 60)
    print("Diagnostic Complete")
    print("=" * 60)
    
    print("\nRecommendations:")
    print("1. If network tests fail: Check your internet connection")
    print("2. If API tests fail: Yahoo Finance may be rate limiting")
    print("3. If rapid requests fail: Use longer delays between requests")
    print("4. Consider using mock data for demonstrations")

if __name__ == "__main__":
    main() 