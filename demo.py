#!/usr/bin/env python3
"""
Demo script for the ERM Risk Assessment System
Uses mock data to demonstrate functionality without API rate limits
"""

import json
import os

from app.agents.research_agent import run_risk_assessment

def run_demo():
    """Run a demonstration of the ERM risk assessment system"""
    print("🚀 ERM Risk Assessment System - DEMO MODE")
    print("=" * 60)
    print("This demo uses mock data to showcase the system functionality")
    print("No API calls will be made, so no rate limiting issues.")
    print("=" * 60)
    
    # Demo companies
    demo_companies = ["NVDA", "TSLA", "AAPL", "MSFT", "GOOGL"]
    
    print("\nAvailable demo companies:")
    for i, company in enumerate(demo_companies, 1):
        print(f"{i}. {company}")
    
    try:
        # Get user choice
        choice = input(f"\nSelect a company (1-{len(demo_companies)}) or enter custom ticker: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(demo_companies):
            ticker = demo_companies[int(choice) - 1]
        else:
            ticker = choice.upper().strip()
            if not ticker:
                ticker = "NVDA"  # Default
        
        print(f"\n🎯 Running ERM assessment for {ticker}...")
        print("Using mock data for demonstration...")
        
        # Run assessment with mock data
        result = run_risk_assessment(ticker, use_mock_data=True)
        
        # Display results
        print("\n" + "=" * 60)
        print("📊 FINAL ERM RISK ASSESSMENT")
        print("=" * 60)
        print(json.dumps(result, indent=2))
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ Demo Complete!")
        print(f"📁 Results saved to: outputs/{ticker.lower()}_erm_assessment.txt")
        print("=" * 60)
        
        # Show what the system can do
        print("\n🎯 What this demo shows:")
        print("• Multi-agent risk analysis using ERM framework")
        print("• Structured risk categorization (Strategic, Operational, Financial, etc.)")
        print("• Financial health scoring and metrics")
        print("• Actionable recommendations")
        print("• Professional JSON output format")
        
        print("\n🚀 To try with real data:")
        print("python app/main.py")
        print("(Note: May encounter API rate limits)")
        
    except KeyboardInterrupt:
        print("\n\n❌ Demo cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")

if __name__ == "__main__":
    run_demo() 