from fastapi import FastAPI, HTTPException, Request
import requests
import logging
import json
import os
from utils.logger import logger

app = FastAPI(title="NOS Trade Decision API")

# --- AI Model Integration (Gemini / Azure Placeholder Calls) ---
def call_ai_model(input_text: str) -> str:
    """
    Placeholder function for AI decision-making logic using Gemini or Azure AI models.
    """
    # In production, this will be replaced with actual Gemini / Azure API integration
    if "sell" in input_text.lower():
        return "SELL"
    return "HOLD"

# --- Smart Contract Simulation (Placeholder Logic) ---
class SmartContract:
    def __init__(self):
        self.holdings = 10
        self.trade_history = []
        
    def execute_trade(self, action: str, symbol: str = "BTC", amount: float = 1.0):
        if action == "SELL":
            self.holdings -= amount
            trade = {
                "action": "SELL",
                "symbol": symbol,
                "amount": amount,
                "holdings_after": self.holdings
            }
            self.trade_history.append(trade)
            logger.info(f"Executed SELL for {symbol}. Holdings now: {self.holdings}")
            return trade
        elif action == "BUY":
            self.holdings += amount
            trade = {
                "action": "BUY",
                "symbol": symbol,
                "amount": amount,
                "holdings_after": self.holdings
            }
            self.trade_history.append(trade)
            logger.info(f"Executed BUY for {symbol}. Holdings now: {self.holdings}")
            return trade
        else:
            logger.info(f"No action taken. Holdings remain: {self.holdings}")
            return {"action": "HOLD", "holdings": self.holdings}
    
    def get_holdings(self):
        return self.holdings
    
    def get_trade_history(self):
        return self.trade_history

# Simulated smart contract instance
contract = SmartContract()

@app.post("/api/execute")
async def execute_trade_decision(request: Request):
    try:
        data = await request.json()
        market_text = data.get("market_text", "")
        symbol = data.get("symbol", "BTC")
        amount = data.get("amount", 1.0)
        
        logger.info(f"Received market_text: {market_text}, symbol: {symbol}, amount: {amount}")
        
        # Call AI model to decide action
        decision = call_ai_model(market_text)
        logger.info(f"AI Decision: {decision}")
        
        # Execute smart contract logic
        result = contract.execute_trade(decision, symbol, amount)
        logger.info(f"Smart Contract Result: {result}")
        
        return {"ai_decision": decision, "execution_result": result}
    except Exception as e:
        logger.error(f"Error in /api/execute: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/api/holdings")
async def get_holdings():
    return {"holdings": contract.get_holdings()}

@app.get("/api/trade-history")
async def get_trade_history():
    return {"trade_history": contract.get_trade_history()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 