
import logging
import os

# Define the base directory for the NancyGate pipeline
base_dir = '/home/user/nancygate_pipeline'

# Ensure the logs directory exists
logs_dir = os.path.join(base_dir, 'logs')
os.makedirs(logs_dir, exist_ok=True)

def setup_logger(name='NancyGateLogger', log_file='pipeline.log', level=logging.INFO):
    """Set up a logger with a file and console handler."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create file handler
    log_file_path = os.path.join(logs_dir, log_file)
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(level)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
