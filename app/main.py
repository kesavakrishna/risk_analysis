import json
import sys
import os
from dotenv import load_dotenv
from agents.research_agent import run_risk_assessment

load_dotenv()

def check_api_keys():
    """Check which API keys are available"""
    keys = {
        "Alpha Vantage": os.getenv("ALPHA_VANTAGE_API_KEY"),
        "IEX Cloud": os.getenv("IEX_API_KEY"),
        "Finnhub": os.getenv("FINNHUB_API_KEY")
    }
    
    available = {name: bool(key) for name, key in keys.items()}
    return available

def main():
    """Main application entry point"""
    print("Enterprise Risk Management (ERM) Risk Assessment System")
    print("=" * 60)
    
    # Check available API keys
    available_apis = check_api_keys()
    
    print("\nAvailable Data Sources:")
    for api, available in available_apis.items():
        status = "✅ Available" if available else "❌ Not configured"
        print(f"  {api}: {status}")
    
    if not any(available_apis.values()):
        print("\n⚠️  No API keys configured. Using demo mode only.")
        print("   Get free API keys from:")
        print("   - Alpha Vantage: https://www.alphavantage.co/support/#api-key")
        print("   - IEX Cloud: https://iexcloud.io/cloud-login#/register")
        print("   - Finnhub: https://finnhub.io/register")
    
    try:
        # Get ticker symbol
        ticker = input("\nEnter company ticker symbol (e.g., TSLA): ").upper().strip()
        
        if not ticker:
            print("Error: Ticker symbol is required")
            return
        
        # Data source selection
        print("\nData Source Options:")
        if any(available_apis.values()):
            print("1. Live API data (using available sources)")
            print("2. Mock data for demonstration")
            print("3. Auto-detect (try live data, fallback to mock)")
            
            choice = input("Choose option (1, 2, or 3): ").strip()
            
            if choice == "1":
                use_mock_data = False
                print("Using live API data...")
            elif choice == "2":
                use_mock_data = True
                print("Using mock data for demonstration...")
            elif choice == "3":
                use_mock_data = None  # Auto-detect
                print("Auto-detecting best data source...")
            else:
                print("Invalid choice. Using auto-detect mode...")
                use_mock_data = None
        else:
            print("1. Mock data for demonstration")
            use_mock_data = True
            print("Using mock data (no API keys available)...")
        
        # Run the assessment
        result = run_risk_assessment(ticker, use_mock_data=use_mock_data)
        
        # Display results
        print("\n" + "=" * 60)
        print("FINAL ERM RISK ASSESSMENT")
        print("=" * 60)
        print(json.dumps(result, indent=2))
        
        # Save results
        filename = f"{ticker.lower()}_erm_assessment.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Enterprise Risk Management (ERM) Assessment\n")
                f.write("=" * 60 + "\n")
                f.write(f"Company: {ticker}\n")
                f.write(f"Assessment Date: {result.get('assessment_date', 'N/A')}\n")
                f.write(f"Data Source: {'Mock Data' if use_mock_data else 'Live API'}\n")
                f.write("=" * 60 + "\n\n")
                f.write(json.dumps(result, indent=2))
            
            print(f"\n✅ Results saved to: {filename}")
        except Exception as e:
            print(f"\n⚠️  Could not save results: {e}")
        
        # Provide next steps
        print("\n" + "=" * 60)
        print("Assessment Complete!")
        print("=" * 60)
        
        # Recommendations
        if not any(available_apis.values()):
            print("\n💡 To get live data, add API keys to your .env file:")
            print("   ALPHA_VANTAGE_API_KEY=your_key_here")
            print("   IEX_API_KEY=your_key_here")
            print("   FINNHUB_API_KEY=your_key_here")
        
        print("\n💡 Test your data sources:")
        print("   python test_alternative_sources.py")
        
    except KeyboardInterrupt:
        print("\n\nAssessment cancelled by user.")
    except Exception as e:
        print(f"\nError during assessment: {e}")
        print("Try using mock data option if you encounter API rate limits.")
        print("Or run: python demo.py")

if __name__ == "__main__":
    main()
