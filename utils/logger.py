import logging
import sys
from datetime import datetime

# Configure logging
logger = logging.getLogger('nos_trade')
logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler(f'logs/nos_trade_{datetime.now().strftime("%Y%m%d")}.log')
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler) 