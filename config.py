# API credentials and endpoints
BINANCE_API_KEY = "..."
BINANCE_API_SECRET = "..."
ALPACA_API_KEY = "..."
ALPACA_API_SECRET = "..."
ALPACA_BASE_URL = "https://paper-api.alpaca.markets"
AZURE_OPENAI_ENDPOINT = "https://ocapulse.openai.azure.com/"
AZURE_OPENAI_KEY = "Bod8Um..."
AZURE_OPENAI_DEPLOYMENT = "gpt-4-llamav2"
GEMINI_API_KEY = "AIzaSyDfnYm..."

# Trading settings
MAX_POSITION_SIZE = 1000  # Maximum position size in USD
MAX_LEVERAGE = 3  # Maximum leverage allowed
STOP_LOSS_PERCENTAGE = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENTAGE = 0.04  # 4% take profit

# Rate limits
BINANCE_RATE_LIMIT = 1200  # requests per minute
ALPACA_RATE_LIMIT = 200  # requests per minute
AI_RATE_LIMIT = 60  # requests per minute

# Fallback settings
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds 