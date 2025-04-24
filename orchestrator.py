import asyncio
from agents.market_data import MarketDataAgent
from agents.ai_agent import AIAgent
from agents.trading_agent import TradingAgent
from utils.logger import logger
from utils.data_models import PriceUpdate, AIResult, OrderReceipt

class Orchestrator:
    def __init__(self):
        self.market_data = MarketDataAgent()
        self.ai_agent = AIAgent()
        self.trading_agent = TradingAgent()
        self.running = False

    async def start(self):
        """
        Start the trading system
        """
        try:
            self.running = True
            await self.market_data.initialize()
            
            # Subscribe to market data updates
            self.market_data.subscribe_to_prices(self._handle_price_update)
            
            # Start market data streams
            await self.market_data.start()
            
        except Exception as e:
            logger.error(f"Failed to start orchestrator: {e}")
            await self.cleanup()
            raise

    async def _handle_price_update(self, price_update: PriceUpdate):
        """
        Handle incoming price updates
        """
        try:
            # Get AI analysis
            ai_result = self.ai_agent.analyze({
                'symbol': price_update.symbol,
                'price': price_update.price,
                'timestamp': price_update.timestamp,
                'source': price_update.source
            })
            
            # Execute trading logic based on AI analysis
            await self._execute_trading_strategy(price_update, ai_result)
            
        except Exception as e:
            logger.error(f"Error handling price update: {e}")

    async def _execute_trading_strategy(self, price_update: PriceUpdate, ai_result: AIResult):
        """
        Execute trading strategy based on AI analysis
        """
        try:
            # Example trading logic - replace with your strategy
            if ai_result.confidence > 0.8:
                if "BUY" in ai_result.analysis.upper():
                    order = self.trading_agent.execute_trade(
                        symbol=price_update.symbol,
                        side="BUY",
                        qty=1.0,
                        exchange=price_update.source
                    )
                    # Set stop loss and take profit
                    self.trading_agent.set_stop_loss(
                        symbol=price_update.symbol,
                        entry_price=price_update.price,
                        side="BUY",
                        exchange=price_update.source
                    )
                    self.trading_agent.set_take_profit(
                        symbol=price_update.symbol,
                        entry_price=price_update.price,
                        side="BUY",
                        exchange=price_update.source
                    )
                    logger.info(f"Executed buy order: {order}")
                
                elif "SELL" in ai_result.analysis.upper():
                    order = self.trading_agent.execute_trade(
                        symbol=price_update.symbol,
                        side="SELL",
                        qty=1.0,
                        exchange=price_update.source
                    )
                    logger.info(f"Executed sell order: {order}")
                    
        except Exception as e:
            logger.error(f"Error executing trading strategy: {e}")

    async def cleanup(self):
        """
        Cleanup resources
        """
        self.running = False
        await self.market_data.cleanup() 