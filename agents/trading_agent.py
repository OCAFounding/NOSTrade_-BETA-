from binance.client import Client
from binance.exceptions import BinanceAPIException
from alpaca.trading.client import TradingClient
from config import (
    BINANCE_API_KEY,
    BINANCE_API_SECRET,
    ALPACA_API_KEY,
    ALPACA_API_SECRET,
    ALPACA_BASE_URL,
    MAX_POSITION_SIZE,
    MAX_LEVERAGE,
    STOP_LOSS_PERCENTAGE,
    TAKE_PROFIT_PERCENTAGE
)
from utils.logger import logger
from utils.data_models import OrderReceipt

class BinanceTrader:
    def __init__(self):
        self.client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

    def place_order(self, symbol: str, side: str, qty: float, order_type: str = 'MARKET') -> OrderReceipt:
        try:
            order = self.client.new_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=qty
            )
            return OrderReceipt(
                order_id=order['orderId'],
                symbol=order['symbol'],
                side=order['side'],
                quantity=float(order['origQty']),
                price=float(order['price']) if order_type != 'MARKET' else None,
                status=order['status'],
                exchange='binance'
            )
        except BinanceAPIException as e:
            logger.error(f"Binance order error: {e}")
            raise

    def set_leverage(self, symbol: str, leverage: int):
        try:
            self.client.futures_change_leverage(symbol=symbol, leverage=min(leverage, MAX_LEVERAGE))
        except BinanceAPIException as e:
            logger.error(f"Binance leverage error: {e}")
            raise

class AlpacaTrader:
    def __init__(self):
        self.client = TradingClient(ALPACA_API_KEY, ALPACA_API_SECRET, paper=True)

    def place_order(self, symbol: str, side: str, qty: float, order_type: str = 'market') -> OrderReceipt:
        try:
            order = self.client.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=order_type
            )
            return OrderReceipt(
                order_id=order.id,
                symbol=order.symbol,
                side=order.side,
                quantity=float(order.qty),
                price=float(order.limit_price) if order_type == 'limit' else None,
                status=order.status,
                exchange='alpaca'
            )
        except Exception as e:
            logger.error(f"Alpaca order error: {e}")
            raise

class TradingAgent:
    def __init__(self):
        self.binance = BinanceTrader()
        self.alpaca = AlpacaTrader()

    def execute_trade(self, symbol: str, side: str, qty: float, exchange: str = 'binance') -> OrderReceipt:
        """
        Execute a trade on the specified exchange
        """
        if exchange == 'binance':
            return self.binance.place_order(symbol, side, qty)
        elif exchange == 'alpaca':
            return self.alpaca.place_order(symbol, side, qty)
        else:
            raise ValueError(f"Unsupported exchange: {exchange}")

    def set_stop_loss(self, symbol: str, entry_price: float, side: str, exchange: str = 'binance'):
        """
        Set stop loss order
        """
        stop_price = entry_price * (1 - STOP_LOSS_PERCENTAGE) if side == 'BUY' else entry_price * (1 + STOP_LOSS_PERCENTAGE)
        if exchange == 'binance':
            return self.binance.place_order(symbol, 'SELL' if side == 'BUY' else 'BUY', qty=1, order_type='STOP_LOSS_LIMIT')
        else:
            return self.alpaca.place_order(symbol, 'sell' if side == 'buy' else 'buy', qty=1, order_type='stop')

    def set_take_profit(self, symbol: str, entry_price: float, side: str, exchange: str = 'binance'):
        """
        Set take profit order
        """
        take_profit_price = entry_price * (1 + TAKE_PROFIT_PERCENTAGE) if side == 'BUY' else entry_price * (1 - TAKE_PROFIT_PERCENTAGE)
        if exchange == 'binance':
            return self.binance.place_order(symbol, 'SELL' if side == 'BUY' else 'BUY', qty=1, order_type='LIMIT')
        else:
            return self.alpaca.place_order(symbol, 'sell' if side == 'buy' else 'buy', qty=1, order_type='limit') 