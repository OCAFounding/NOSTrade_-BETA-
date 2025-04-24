from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from typing import Dict, Any
import random
import os
import google.generativeai as genai
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    reply: str

# Load API keys from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# Initialize Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-pro')
    logger.info("Gemini AI configured successfully")
else:
    logger.warning("GEMINI_API_KEY not found. Using mock responses.")
    gemini_model = None

# Mock responses for fallback
MOCK_RESPONSES = [
    "I've analyzed the market data and recommend a slight rebalance towards BTC.",
    "Based on current Fibonacci levels, I suggest maintaining your current position.",
    "Market volatility is increasing. Consider reducing exposure to high-risk assets.",
    "The AI ensemble suggests increasing your ETH allocation by 5%.",
    "Technical indicators show a potential trend reversal. Proceed with caution.",
    "Your portfolio is well-diversified. No immediate action needed.",
    "I've detected an opportunity in the DeFi sector. Consider allocating 10% of your portfolio there.",
    "The Fibonacci retracement levels suggest a potential support at $45,000 for BTC.",
    "Your current risk metrics are within acceptable parameters.",
    "Based on recent market movements, I recommend a defensive stance."
]

@router.post("/ai-chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest) -> Dict[str, Any]:
    """
    Process a chat request and return an AI response using Gemini Pro.
    
    Args:
        request: The chat request containing the user's prompt
        
    Returns:
        A response from the AI
    """
    try:
        logger.info(f"Received chat request: {request.prompt}")
        
        # Try to use Gemini if configured
        if gemini_model:
            try:
                response = gemini_model.generate_content(request.prompt)
                reply = response.text
                logger.info("Successfully generated response with Gemini")
            except Exception as e:
                logger.error(f"Error with Gemini: {str(e)}")
                # Fall back to mock responses
                reply = random.choice(MOCK_RESPONSES)
                logger.info("Using mock response as fallback")
        else:
            # Use mock responses if Gemini is not configured
            reply = random.choice(MOCK_RESPONSES)
            logger.info("Using mock response (Gemini not configured)")
        
        logger.info(f"Sending response: {reply}")
        return {"reply": reply}
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}") 