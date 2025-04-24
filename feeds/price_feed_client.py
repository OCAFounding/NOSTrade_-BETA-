import requests
import time
import json
from datetime import datetime
import os
from utils.logger import logger

class PriceFeedClient:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        self.price_history = []
        self.callbacks = []
        
    def get_current_price(self):
        """
        Fetch the current price from the feed server
        """
        try:
            response = requests.get(f"{self.base_url}/api/price")
            if response.status_code == 200:
                data = response.json()
                price = data.get('price')
                
                # Log the price
                self._log_price(price)
                
                return price
            else:
                logger.error(f"Failed to fetch price: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching price: {e}")
            return None
    
    def analyze_price(self, symbol, threshold):
        """
        Trigger AI analysis based on price threshold
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/analyze",
                json={"symbol": symbol, "threshold": threshold}
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Analysis result for {symbol}: {result}")
                return result
            else:
                logger.error(f"Failed to analyze price: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error analyzing price: {e}")
            return None
    
    def start_monitoring(self, symbol, threshold, interval=5):
        """
        Start monitoring price and trigger analysis when threshold is crossed
        """
        logger.info(f"Starting price monitoring for {symbol} with threshold {threshold}")
        
        try:
            while True:
                price = self.get_current_price()
                
                if price is not None:
                    # Check if price crosses threshold
                    if price > threshold:
                        logger.info(f"Price {price} exceeded threshold {threshold} for {symbol}")
                        result = self.analyze_price(symbol, threshold)
                        
                        # Notify callbacks
                        for callback in self.callbacks:
                            callback(symbol, price, result)
                
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Price monitoring stopped")
    
    def add_callback(self, callback):
        """
        Add a callback function to be called when price analysis is triggered
        """
        self.callbacks.append(callback)
    
    def _log_price(self, price):
        """
        Log price to history and file
        """
        timestamp = datetime.now().isoformat()
        self.price_history.append({"timestamp": timestamp, "price": price})
        
        # Save to CSV file
        self._save_to_csv(timestamp, price)
    
    def _save_to_csv(self, timestamp, price):
        """
        Save price data to CSV file
        """
        try:
            # Create data directory if it doesn't exist
            os.makedirs('data', exist_ok=True)
            
            # Append to CSV file
            with open('data/price_history.csv', 'a') as f:
                f.write(f"{timestamp},{price}\n")
        except Exception as e:
            logger.error(f"Error saving price to CSV: {e}") 