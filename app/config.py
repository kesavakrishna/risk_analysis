"""
Configuration settings for the ERM Risk Assessment System
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Model Configuration
DEFAULT_MODEL = "gemini-2.0-flash"
DEFAULT_API_TYPE = "google"

# LLM Configuration
LLM_CONFIG = {
    "timeout": 120,
    "temperature": 0.2,
    "seed": 42
}

# Agent Configuration
MAX_STEPS = 15
AGENT_DELAY = 1.5  # seconds
MAX_ROUNDS = 12

# Data Collection Configuration
NEWS_ARTICLES_COUNT = 5
REQUEST_TIMEOUT = 10

# File Configuration
OUTPUT_DIR = "assessments"
LOG_LEVEL = "INFO"

# Risk Assessment Configuration
RISK_LEVELS = ["Low", "Medium", "High", "Critical"]
LIKELIHOOD_LEVELS = ["Low", "Medium", "High"]

# Financial Health Scores
FINANCIAL_SCORES = {
    "Poor": (1, 3),
    "Fair": (4, 6), 
    "Good": (7, 8),
    "Excellent": (9, 10)
}

# Validation
def validate_config():
    """Validate that required configuration is present"""
    missing_keys = []
    
    if not GEMINI_API_KEY:
        missing_keys.append("GEMINI_API_KEY")
    
    if missing_keys:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")
    
    return True 