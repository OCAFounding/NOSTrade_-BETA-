import asyncio
from binance import AsyncClient
from alpaca.trading.stream import Stream
from config import BINANCE_API_KEY, BINANCE_API_SECRET, ALPACA_API_KEY, ALPACA_API_SECRET
from utils.logger import logger
from utils.data_models import PriceUpdate

class MarketDataAgent:
    def __init__(self):
        self._binance_client = None
        self._alpaca_stream = None
        self._price_callbacks = []

    async def initialize(self):
        self._binance_client = await AsyncClient(BINANCE_API_KEY, BINANCE_API_SECRET)
        self._alpaca_stream = Stream(ALPACA_API_KEY, ALPACA_API_SECRET)

    async def start(self):
        await asyncio.gather(
            self._run_binance_ws(),
            self._run_alpaca_ws()
        )

    async def _run_binance_ws(self):
        while True:
            try:
                ts = self._binance_client.symbol_ticker_socket('BTCUSDT')
                async with ts as stream:
                    while True:
                        res = await stream.recv()
                        self._publish_price(PriceUpdate(
                            symbol=res['s'],
                            price=float(res['c']),
                            timestamp=res['E'],
                            source='binance'
                        ))
            except Exception as e:
                logger.error(f"Binance WebSocket error: {e}")
                await asyncio.sleep(5)

    async def _run_alpaca_ws(self):
        try:
            await self._alpaca_stream.connect()
            self._alpaca_stream.subscribe_trades(self._handle_alpaca_trade)
            await self._alpaca_stream.run()
        except Exception as e:
            logger.error(f"Alpaca WebSocket error: {e}")
            await asyncio.sleep(5)

    def _handle_alpaca_trade(self, trade):
        self._publish_price(PriceUpdate(
            symbol=trade.symbol,
            price=float(trade.price),
            timestamp=trade.timestamp,
            source='alpaca'
        ))

    def _publish_price(self, price_update: PriceUpdate):
        for callback in self._price_callbacks:
            callback(price_update)

    def subscribe_to_prices(self, callback):
        self._price_callbacks.append(callback)

    async def cleanup(self):
        if self._binance_client:
            await self._binance_client.close_connection()
        if self._alpaca_stream:
            await self._alpaca_stream.close() 