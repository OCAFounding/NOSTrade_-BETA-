import requests
import json
from utils.logger import logger

class ParentAgent:
    def __init__(self, children=None):
        self.children = children or []
        self.rebalance_url = "https://your-dapp-interface.com/rebalance"
        
    def add_child(self, child):
        self.children.append(child)
        
    def analyze_and_delegate(self, market_data):
        """
        Analyze market data and delegate tasks to child agents
        """
        # Analyze data and decide strategy
        strategy = self._determine_strategy(market_data)
        
        # Delegate to child agents
        for child in self.children:
            child.execute_strategy(strategy)
            
        # Trigger on-chain rebalance
        self.trigger_onchain_rebalance(strategy)
        
    def _determine_strategy(self, market_data):
        """
        Determine the appropriate strategy based on market data
        """
        # Example strategy determination logic
        if market_data.get('volatility', 0) > 0.05:
            return "shift to stablecoins"
        elif market_data.get('trend', '') == 'bullish':
            return "increase risk exposure"
        else:
            return "maintain current allocation"
        
    def trigger_onchain_rebalance(self, strategy):
        """
        Trigger on-chain portfolio rebalancing via smart contract
        """
        payload = {"strategy": strategy}
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(self.rebalance_url, json=payload, headers=headers)
            if response.status_code == 200:
                logger.info("✅ On-chain rebalance triggered successfully.")
            else:
                logger.error(f"❌ Failed to trigger on-chain rebalance: {response.text}")
        except Exception as e:
            logger.error(f"⚠️ Error triggering smart contract: {str(e)}")
            
    def get_status(self):
        """
        Get the status of all child agents
        """
        return [child.get_status() for child in self.children] 