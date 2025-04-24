import threading
import time
from feeds.price_feed_client import PriceFeedClient
from ai_agents.parent_agent import ParentAgent
from utils.logger import logger

class SignalProcessor:
    def __init__(self, parent_agent, symbols=None, thresholds=None):
        self.parent_agent = parent_agent
        self.symbols = symbols or ["BTC", "ETH", "EUR/USD"]
        self.thresholds = thresholds or {"BTC": 1050, "ETH": 2000, "EUR/USD": 1.1}
        self.price_feed = PriceFeedClient()
        self.monitoring_threads = {}
        self.running = False
        
    def start(self):
        """
        Start monitoring all symbols
        """
        self.running = True
        logger.info("Starting signal processor")
        
        # Start monitoring each symbol in a separate thread
        for symbol in self.symbols:
            threshold = self.thresholds.get(symbol, 1000)
            thread = threading.Thread(
                target=self._monitor_symbol,
                args=(symbol, threshold),
                daemon=True
            )
            self.monitoring_threads[symbol] = thread
            thread.start()
            logger.info(f"Started monitoring thread for {symbol}")
            
    def stop(self):
        """
        Stop all monitoring threads
        """
        self.running = False
        logger.info("Stopping signal processor")
        
        # Wait for all threads to finish
        for symbol, thread in self.monitoring_threads.items():
            thread.join(timeout=5)
            logger.info(f"Stopped monitoring thread for {symbol}")
            
    def _monitor_symbol(self, symbol, threshold):
        """
        Monitor a specific symbol and trigger AI analysis when threshold is crossed
        """
        logger.info(f"Monitoring {symbol} with threshold {threshold}")
        
        # Add callback for price analysis
        self.price_feed.add_callback(self._handle_price_analysis)
        
        # Start monitoring
        self.price_feed.start_monitoring(symbol, threshold)
        
    def _handle_price_analysis(self, symbol, price, analysis_result):
        """
        Handle price analysis result and trigger AI agent
        """
        logger.info(f"Price analysis for {symbol}: {analysis_result}")
        
        # Create market data for AI agent
        market_data = {
            'symbol': symbol,
            'price': price,
            'analysis': analysis_result,
            'volatility': 0.03,  # Example value
            'trend': 'bullish' if price > self.thresholds.get(symbol, 1000) else 'bearish'
        }
        
        # Trigger AI agent analysis
        self.parent_agent.analyze_and_delegate(market_data)
        
    def add_symbol(self, symbol, threshold):
        """
        Add a new symbol to monitor
        """
        self.symbols.append(symbol)
        self.thresholds[symbol] = threshold
        
        if self.running:
            # Start monitoring the new symbol
            thread = threading.Thread(
                target=self._monitor_symbol,
                args=(symbol, threshold),
                daemon=True
            )
            self.monitoring_threads[symbol] = thread
            thread.start()
            logger.info(f"Added monitoring for {symbol}")
            
    def remove_symbol(self, symbol):
        """
        Remove a symbol from monitoring
        """
        if symbol in self.symbols:
            self.symbols.remove(symbol)
            if symbol in self.thresholds:
                del self.thresholds[symbol]
            logger.info(f"Removed monitoring for {symbol}") 