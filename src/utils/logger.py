import os
import logging

DEFAULT_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

def setup_logging(log_name='dns_updater', log_file=None, log_level=logging.INFO, log_format=DEFAULT_FORMAT):
    """Set up logging to the specified log file."""
    logging.basicConfig(level=log_level, format=log_format)
    logger = logging.getLogger(log_name)

    if log_file:
        if not os.path.exists(log_file):
            with open(log_file, 'w'):
                pass  # Create the log file if it doesn't exist
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info(f"Logging initialized to file: {log_file}")
    
    else:
        logger.info("Logging initialized to console.")


    return logger