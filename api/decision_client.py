import requests
import json
from utils.logger import logger

class DecisionClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
    def execute_trade_decision(self, market_text, symbol="BTC", amount=1.0):
        """
        Send market data to the decision server and get back AI decision and execution result
        """
        try:
            payload = {
                "market_text": market_text,
                "symbol": symbol,
                "amount": amount
            }
            
            response = requests.post(
                f"{self.base_url}/api/execute",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Decision execution successful: {result}")
                return result
            else:
                logger.error(f"Failed to execute decision: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error executing trade decision: {e}")
            return None
    
    def get_holdings(self):
        """
        Get current holdings from the smart contract
        """
        try:
            response = requests.get(f"{self.base_url}/api/holdings")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Current holdings: {result}")
                return result
            else:
                logger.error(f"Failed to get holdings: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting holdings: {e}")
            return None
    
    def get_trade_history(self):
        """
        Get trade history from the smart contract
        """
        try:
            response = requests.get(f"{self.base_url}/api/trade-history")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Trade history retrieved: {len(result.get('trade_history', []))} trades")
                return result
            else:
                logger.error(f"Failed to get trade history: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting trade history: {e}")
            return None 