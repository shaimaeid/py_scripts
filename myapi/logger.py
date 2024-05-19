import logging
from logging.handlers import RotatingFileHandler
#levels of severity:
# You can use logger.debug(), logger.info(), 
# logger.warning(), logger.error(), and logger.critical()

def setup_logger():
    # Configure logging settings
    logging.basicConfig(level=logging.INFO)

    # Create a file handler for the log file
    #file_handler = logging.FileHandler('api.log')
    file_handler = RotatingFileHandler('api.log', maxBytes=1e6, backupCount=3)
    file_handler.setLevel(logging.INFO)

    # Create a log formatter
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_formatter)

    # Create and return the logger object
    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)

    return logger

# Create the logger object
mylogger = setup_logger()
