# NOS Trade: Phase 4 - Real-Time Feeds and Signal Processing

This phase of the NOS Trade platform adds real-time data feeds and signal processing capabilities, enabling automated trading decisions based on market events.

## Key Components

### Real-Time Price Feed Server
- `feeds/price_feed_server.js`: Node.js Express server that provides real-time price data
- Simulated market price feed (can be replaced with real exchange APIs)
- REST API endpoints for price data and analysis

### Price Feed Client
- `feeds/price_feed_client.py`: Python client to consume the real-time price feed
- Price history tracking and CSV logging
- Callback mechanism for price analysis

### Signal Processor
- `feeds/signal_processor.py`: Integrates price feed with AI agents
- Multi-threaded monitoring of multiple symbols
- Threshold-based triggering of AI analysis

## How to Run

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Run the system:
```bash
python main.py
```

This will:
- Start the price feed server
- Initialize the AI agent hierarchy
- Start the signal processor
- Begin monitoring prices and triggering AI analysis

## Architecture

The system now follows this flow:
1. Price feed server provides real-time market data
2. Price feed client consumes the data and logs it
3. Signal processor monitors prices and triggers analysis when thresholds are crossed
4. AI agents analyze the data and make trading decisions
5. Smart contract logs rebalancing events on-chain

## Data Storage

Price data is stored in:
- `data/price_history.csv`: CSV file with timestamp and price data

## Next Steps

- Connect to real exchange WebSocket feeds (Binance, Alpaca)
- Implement more sophisticated signal processing algorithms
- Add visualization dashboard for price data and signals
- Enhance AI analysis with more market indicators 