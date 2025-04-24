# NOS Trade (BETA)

A sophisticated multi-agent trading system with advanced Fibonacci analysis, AI decision making, and comprehensive monitoring.

## Features

- **Multi-Agent Architecture**
  - Parent AI for signal analysis and decision making
  - Specialized agents for different trading strategies
  - Inter-agent communication and coordination

- **Fibonacci Analysis**
  - Multiple Fibonacci adapters for different market conditions
  - Dynamic level calculation and signal generation
  - Configurable retracement and extension levels

- **Decision Making**
  - AI-powered signal analysis
  - Historical trend analysis
  - Confidence-based decision making
  - Risk management integration

- **Monitoring & Compliance**
  - Real-time system monitoring
  - Performance metrics tracking
  - Compliance checks and alerts
  - Comprehensive logging

- **Stress Testing**
  - Multi-agent simulation
  - Configurable test parameters
  - Statistical analysis
  - Visualization tools

- **AI Chat Interface**
  - Modern React-based UI
  - Integration with Gemini Pro AI
  - Real-time trading advice
  - Fallback to mock responses

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- MongoDB
- Redis
- Docker (optional)
- Gemini API key (for AI chat)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/nostrade.git
   cd nostrade
   ```

2. Install dependencies:
   ```bash
   # Install Node.js dependencies
   npm install

   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   # Make sure to add your Gemini API key for AI chat functionality
   ```

4. Start the services:
   ```bash
   # Using Docker
   docker-compose up -d

   # Or manually on Windows
   .\run_windows.bat
   ```

### Usage

1. Start the trading system:
   ```bash
   npm run start
   ```

2. Run stress tests:
   ```bash
   python -m stress_test.run_stress_test
   ```

3. Monitor the system:
   ```bash
   # Access the monitoring dashboard
   http://localhost:3000/monitoring
   ```

4. Use the AI Chat interface:
   ```bash
   # Access the chat interface
   http://localhost:3000
   ```

## Project Structure

```
nostrade/
├── api/                    # API endpoints
│   ├── compliance/        # Compliance monitoring
│   ├── monitoring/        # System monitoring
│   ├── ai_chat.py        # AI chat endpoint
│   └── decision_client.py # Decision server client
├── fibonacci_modules/     # Fibonacci analysis
│   └── base_adapter.py   # Base Fibonacci adapter
├── frontend/              # React frontend
│   ├── src/              # Source code
│   │   ├── components/   # React components
│   │   └── ...
│   └── ...
├── stress_test/          # Stress testing module
│   ├── multi_agent_simulator.py
│   ├── visualization.py
│   └── run_stress_test.py
├── ai_agent_parent.py    # Parent AI implementation
├── docker-compose.yml    # Docker configuration
├── requirements.txt      # Python dependencies
└── package.json         # Node.js dependencies
```

## Configuration

The system can be configured through environment variables in the `.env` file:

- `NODE_ENV`: Environment (development/production)
- `PORT`: API server port
- `MONGODB_URI`: MongoDB connection string
- `REDIS_URL`: Redis connection URL
- `JWT_SECRET`: JWT secret key
- `LOG_LEVEL`: Logging level
- `BINANCE_API_KEY`: Binance API key
- `BINANCE_API_SECRET`: Binance API secret
- `GEMINI_API_KEY`: Gemini API key for AI chat
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key (optional)
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint (optional)
- `MAX_POSITION_SIZE`: Maximum position size
- `RISK_PER_TRADE`: Risk per trade percentage
- `MAX_DAILY_TRADES`: Maximum daily trades
- `MONITORING_INTERVAL`: Monitoring update interval
- `ALERT_THRESHOLD`: Alert threshold
- `COMPLIANCE_CHECK_INTERVAL`: Compliance check interval
- `MAX_DRAWDOWN`: Maximum allowed drawdown

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is in beta and should not be used for production trading without thorough testing and validation. Use at your own risk. 