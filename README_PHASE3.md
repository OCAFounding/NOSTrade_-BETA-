# NOS Trade: Phase 3 - Real-Time Market Interaction & Smart Contract Integration

This phase of the NOS Trade platform integrates real-time market interaction with smart contract functionality for portfolio rebalancing.

## Key Components

### Smart Contract Integration
- `contracts/portfolioRebalance.sol`: Solidity smart contract for portfolio rebalancing
- Event logging for rebalancing actions
- Owner-only access control

### AI Agent Hierarchy
- `ai_agents/parent_agent.py`: Parent agent with smart contract triggering capability
- `ai_agents/child_agent.py`: Child agents for specific assets
- `ai_agents/strategies.py`: Strategy implementations for different market conditions

### Strategy Implementation
- Shift to stablecoins during high volatility
- Increase risk exposure during bullish markets
- Maintain current allocation during stable conditions

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Deploy the smart contract:
```bash
# Using Truffle or Hardhat
truffle migrate --network development
```

3. Update the rebalance URL in `ai_agents/parent_agent.py` to point to your deployed contract interface.

4. Run the system:
```bash
python main.py
```

## Architecture

The system now follows a hierarchical structure:
1. Parent Agent analyzes market data and determines strategy
2. Child Agents execute specific strategies for their assigned assets
3. Smart Contract logs rebalancing events on-chain

## Next Steps

- Implement actual on-chain execution of portfolio rebalancing
- Add more sophisticated strategy implementations
- Integrate with DeFi protocols for automated rebalancing
- Add monitoring and analytics dashboard 