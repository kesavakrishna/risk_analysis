# Enterprise Risk Management (ERM) Assessment System

A multi-agent AI system for comprehensive enterprise risk assessment using ERM Level 1 standards, leveraging real-time financial data and news analysis.

## Recent Improvements

- **Organized codebase**: Moved test files to `tests/` directory
- **Fixed critical bug**: Resolved naming conflict in Pydantic models (`FinancialHealth` enum vs class)
- **Improved output management**: Assessment outputs now save to `outputs/` directory
- **Proper Python packaging**: Added `__init__.py` files for clean imports
- **Updated .gitignore**: Excluded generated files, outputs, and cache directories
- **Removed unnecessary files**: Cleaned up debug scripts and duplicate documentation

## Project Structure

```
risk_analysis/
├── app/                          # Main application package
│   ├── agents/                   # Multi-agent system
│   │   └── research_agent.py     # Main orchestrator
│   ├── data/                     # Data collection layer
│   │   └── data_sources.py       # API integrations
│   ├── utils/                    # Utilities
│   │   ├── models.py             # Pydantic schemas
│   │   └── prompts.py            # ERM prompts
│   ├── config.py                 # Configuration
│   └── main.py                   # CLI entry point
├── tests/                        # Test suite
│   ├── test_final_assessment.py
│   ├── test_alternative_sources.py
│   ├── test_system.py
│   ├── test_rate_limits.py
│   └── test_output_format.py
├── docs/                         # Documentation
│   └── MISSING_COMPONENTS_ANALYSIS.md
├── outputs/                      # Generated assessments (git-ignored)
├── demo.py                       # Demo script (mock data)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 **Quick Start**

### 1. **Installation**
```bash
# Clone the repository
git clone <repository-url>
cd risk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Environment Setup**
Create a `.env` file in the root directory:

```env
# Required: Choose at least one data source
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
IEX_API_KEY=your_iex_api_key_here
FINNHUB_API_KEY=your_finnhub_api_key_here

# Optional: LLM API Keys (if not using local models)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
```

### 3. **Get API Keys (Free Options)**

#### **Alpha Vantage** (Recommended - Free tier available)
- Visit: https://www.alphavantage.co/support/#api-key
- Free tier: 25 requests/day, 500 requests/month
- Perfect for testing and small-scale use

#### **IEX Cloud** (Good alternative)
- Visit: https://iexcloud.io/cloud-login#/register
- Free tier: 50,000 messages/month
- Comprehensive financial data

#### **Finnhub** (For news data)
- Visit: https://finnhub.io/register
- Free tier: 60 API calls/minute
- Great for company news

### 4. **Run the System**

#### **Demo Mode (No API Keys Required)**
```bash
python demo.py
```

#### **Full Mode (With API Keys)**
```bash
python app/main.py
```

## 📊 **Data Sources & Fallback Strategy**

The system uses a **multi-source approach** with intelligent fallback:

### **Primary Sources** (in order of preference):
1. **Alpha Vantage** - Most reliable, good free tier
2. **IEX Cloud** - Comprehensive data, generous limits
3. **Yahoo Finance** - Fallback option (currently rate-limited)

### **News Sources**:
1. **Finnhub** - Company-specific news
2. **Google News** - Web scraping fallback

### **Automatic Fallback**:
- If all APIs fail → Uses realistic mock data
- Maintains full functionality for demonstrations
- No interruption to risk assessment process

## 🔧 **Configuration**

### **Rate Limiting Settings**
```python
# In app/data/data_sources.py
RATE_LIMIT_DELAY = 5  # seconds between requests
MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds
```

### **Demo Mode**
The system automatically detects API failures and switches to demo mode with realistic mock data for:
- NVDA, TSLA, AAPL, MSFT, GOOGL
- Comprehensive financial profiles
- Realistic news articles

## 📈 **Features**

### **Multi-Agent Risk Assessment**
- **Research Agent**: Data collection and analysis
- **Risk Analyst**: ERM framework application
- **Compliance Officer**: Regulatory compliance review
- **Strategic Advisor**: Strategic risk evaluation

### **ERM Level 1 Standards**
- Strategic Risk
- Operational Risk
- Financial Risk
- Compliance Risk
- Reputational Risk
- Technological Risk
- Environmental Risk

### **Comprehensive Output**
- Detailed risk analysis
- Risk scoring (1-10 scale)
- Mitigation recommendations
- Executive summary
- Structured JSON format

## 🛠 **Troubleshooting**

### **Rate Limiting Issues**
If you encounter rate limiting:

1. **Check your API limits**:
   ```bash
   python test_rate_limits.py
   ```

2. **Use demo mode**:
   ```bash
   python demo.py
   ```

3. **Increase delays** in `app/data/data_sources.py`:
   ```python
   RATE_LIMIT_DELAY = 10  # Increase from 5 to 10
   ```

### **API Key Issues**
- Verify keys are in `.env` file
- Check API provider dashboards for usage limits
- Ensure keys have correct permissions

### **Network Issues**
- Test connectivity: `python test_system.py`
- Check firewall settings
- Try different network if possible

## 📋 **Example Output**

The system generates comprehensive risk assessments:

```json
{
  "company": "TSLA",
  "assessment_date": "2024-01-15",
  "risk_categories": {
    "strategic_risk": {
      "score": 7,
      "description": "High competition in EV market...",
      "mitigation": "Diversify product portfolio..."
    },
    "operational_risk": {
      "score": 6,
      "description": "Supply chain dependencies...",
      "mitigation": "Strengthen supplier relationships..."
    }
  },
  "overall_risk_score": 6.5,
  "recommendations": [...]
}
```

## 🔄 **Alternative Data Sources**

### **If Yahoo Finance Continues Rate Limiting:**

1. **Alpha Vantage** (Recommended)
   - Most reliable free option
   - Good documentation
   - 25 requests/day free

2. **IEX Cloud**
   - 50K messages/month free
   - Real-time data
   - Comprehensive coverage

3. **Finnhub**
   - 60 calls/minute free
   - Good for news data
   - Real-time quotes

4. **Polygon.io**
   - 5 requests/minute free
   - Real-time data
   - Good documentation

### **Setup Instructions for Each:**

#### **Alpha Vantage Setup:**
```bash
# 1. Get free API key from alphavantage.co
# 2. Add to .env file:
ALPHA_VANTAGE_API_KEY=your_key_here

# 3. Test the connection:
python -c "
from app.data.data_sources import get_company_profile_alpha_vantage
print(get_company_profile_alpha_vantage('AAPL'))
"
```

#### **IEX Cloud Setup:**
```bash
# 1. Register at iexcloud.io
# 2. Add to .env file:
IEX_API_KEY=your_key_here

# 3. Test the connection:
python -c "
from app.data.data_sources import get_company_profile_iex
print(get_company_profile_iex('AAPL'))
"
```

## 🎯 **Best Practices**

1. **Start with Demo Mode**: Test the system without API keys
2. **Use Multiple Sources**: Set up 2-3 API keys for redundancy
3. **Monitor Usage**: Check API provider dashboards regularly
4. **Cache Results**: Store assessments to avoid repeated API calls
5. **Batch Processing**: Group multiple assessments to optimize API usage

## 📞 **Support**

If you encounter issues:
1. Check the troubleshooting section above
2. Run diagnostic scripts: `python test_system.py`
3. Review API provider documentation
4. Use demo mode for immediate testing

## 🚀 **Next Steps**

- Set up your preferred API keys
- Run `python demo.py` to test the system
- Customize risk assessment criteria
- Integrate with your existing risk management processes

The system is designed to work seamlessly with or without API keys, ensuring you can always perform risk assessments using realistic mock data when external APIs are unavailable. 