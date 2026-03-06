import logging
import os
from datetime import datetime
from src.config.config import config

def setup_logger(module_name):
    """Sets up a logger that writes to both console and file."""
    os.makedirs(config.LOGS_DIR, exist_ok=True)
    
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers if setup_logger is called multiple times for the same module
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File Handler (Daily logs)
        log_filename = f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(os.path.join(config.LOGS_DIR, log_filename))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger
