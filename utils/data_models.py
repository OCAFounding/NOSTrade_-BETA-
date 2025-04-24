from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class PriceUpdate:
    symbol: str
    price: float
    timestamp: int
    source: str
    volume: Optional[float] = None
    indicators: Optional[Dict[str, Any]] = None

@dataclass
class AIResult:
    analysis: str
    source: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class OrderReceipt:
    order_id: str
    symbol: str
    side: str
    quantity: float
    price: Optional[float]
    status: str
    exchange: str
    metadata: Optional[Dict[str, Any]] = None 