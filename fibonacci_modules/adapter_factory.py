import os
import json
import importlib
from typing import Dict, Any, List, Optional

# Import the base adapter
from base_adapter import FibonacciBaseAdapter

class FibonacciAdapterFactory:
    """
    Factory class for creating and managing Fibonacci adapters.
    This class handles the creation, selection, and aggregation of signals from multiple adapters.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the factory with configuration.
        
        Args:
            config_path: Path to the configuration file. If None, uses default path.
        """
        # Set default config path if not provided
        if config_path is None:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize adapters
        self.adapters = self._initialize_adapters()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Dictionary containing configuration
        """
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading configuration: {e}")
            # Return default configuration
            return {
                'enabled_modules': ['repo1', 'repo2', 'repo3'],
                'aggregation_method': 'weighted_vote',
                'confidence_threshold': 0.6,
                'default_timeframe': '1h',
                'default_symbol': 'BTC'
            }
    
    def _initialize_adapters(self) -> Dict[str, FibonacciBaseAdapter]:
        """
        Initialize adapters based on configuration.
        
        Returns:
            Dictionary mapping adapter names to adapter instances
        """
        adapters = {}
        
        # Get the directory of this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Initialize each enabled adapter
        for module_name in self.config.get('enabled_modules', []):
            try:
                # Construct the module path
                module_path = f"fibonacci_modules.{module_name}.adapter"
                
                # Import the module
                module = importlib.import_module(module_path)
                
                # Get the adapter class (assuming it's the only class in the module)
                adapter_class = None
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, FibonacciBaseAdapter) and item != FibonacciBaseAdapter:
                        adapter_class = item
                        break
                
                if adapter_class:
                    # Create an instance of the adapter
                    adapter = adapter_class()
                    adapters[module_name] = adapter
                else:
                    print(f"No adapter class found in module {module_name}")
            
            except (ImportError, AttributeError) as e:
                print(f"Error initializing adapter {module_name}: {e}")
        
        return adapters
    
    def get_levels(self, price_data: Dict[str, Any], adapter_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Fibonacci levels from a specific adapter or aggregate from all adapters.
        
        Args:
            price_data: Dictionary containing price information
            adapter_name: Name of the adapter to use. If None, aggregates from all adapters.
            
        Returns:
            Dictionary containing Fibonacci levels
        """
        if adapter_name:
            # Get levels from specific adapter
            if adapter_name in self.adapters:
                return self.adapters[adapter_name].get_levels(price_data)
            else:
                print(f"Adapter {adapter_name} not found")
                return {}
        
        # Aggregate levels from all adapters
        all_levels = {}
        for name, adapter in self.adapters.items():
            levels = adapter.get_levels(price_data)
            all_levels[name] = levels
        
        # Aggregate support and resistance levels
        support_levels = []
        resistance_levels = []
        
        for levels in all_levels.values():
            if 'support_levels' in levels:
                support_levels.extend(levels['support_levels'])
            if 'resistance_levels' in levels:
                resistance_levels.extend(levels['resistance_levels'])
        
        # Remove duplicates and sort
        support_levels = sorted(list(set(support_levels)), reverse=True)
        resistance_levels = sorted(list(set(resistance_levels)))
        
        # Get nearest support and resistance
        nearest_support = support_levels[0] if support_levels else None
        nearest_resistance = resistance_levels[0] if resistance_levels else None
        
        return {
            'support': nearest_support,
            'resistance': nearest_resistance,
            'support_levels': support_levels,
            'resistance_levels': resistance_levels,
            'all_levels': all_levels
        }
    
    def get_signal(self, price_data: Dict[str, Any], adapter_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get trading signal from a specific adapter or aggregate from all adapters.
        
        Args:
            price_data: Dictionary containing price information
            adapter_name: Name of the adapter to use. If None, aggregates from all adapters.
            
        Returns:
            Dictionary containing signal information
        """
        if adapter_name:
            # Get signal from specific adapter
            if adapter_name in self.adapters:
                return self.adapters[adapter_name].get_signal(price_data)
            else:
                print(f"Adapter {adapter_name} not found")
                return {'action': 'HOLD', 'confidence': 0.0}
        
        # Get signals from all adapters
        signals = {}
        for name, adapter in self.adapters.items():
            signals[name] = adapter.get_signal(price_data)
        
        # Aggregate signals based on configuration
        aggregation_method = self.config.get('aggregation_method', 'weighted_vote')
        
        if aggregation_method == 'weighted_vote':
            # Count votes for each action
            action_counts = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
            total_confidence = 0
            
            for signal in signals.values():
                action = signal.get('action', 'HOLD')
                confidence = signal.get('confidence', 0.0)
                
                action_counts[action] += confidence
                total_confidence += confidence
            
            # Normalize confidence
            if total_confidence > 0:
                for action in action_counts:
                    action_counts[action] /= total_confidence
            
            # Get the action with the highest confidence
            best_action = max(action_counts, key=action_counts.get)
            best_confidence = action_counts[best_action]
            
            # Check if confidence meets threshold
            if best_confidence < self.config.get('confidence_threshold', 0.6):
                best_action = 'HOLD'
                best_confidence = 0.0
            
            return {
                'action': best_action,
                'confidence': best_confidence,
                'all_signals': signals
            }
        
        elif aggregation_method == 'highest_confidence':
            # Find the signal with the highest confidence
            best_signal = {'action': 'HOLD', 'confidence': 0.0}
            
            for signal in signals.values():
                if signal.get('confidence', 0.0) > best_signal.get('confidence', 0.0):
                    best_signal = signal
            
            # Check if confidence meets threshold
            if best_signal.get('confidence', 0.0) < self.config.get('confidence_threshold', 0.6):
                best_signal = {'action': 'HOLD', 'confidence': 0.0}
            
            return {
                'action': best_signal.get('action', 'HOLD'),
                'confidence': best_signal.get('confidence', 0.0),
                'all_signals': signals
            }
        
        else:
            # Default to simple majority vote
            action_counts = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
            
            for signal in signals.values():
                action = signal.get('action', 'HOLD')
                action_counts[action] += 1
            
            # Get the action with the most votes
            best_action = max(action_counts, key=action_counts.get)
            
            return {
                'action': best_action,
                'confidence': action_counts[best_action] / len(signals),
                'all_signals': signals
            } 