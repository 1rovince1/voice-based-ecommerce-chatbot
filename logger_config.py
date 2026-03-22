import logging
import logging.config
import sys
import os


def setup_logging():
    """
    Configures logging for the entire application using only the standard library.
    
    This setup provides two handlers:
    1. A console handler that logs INFO and higher level messages.
    2. A rotating file handler that logs DEBUG and higher level messages.
    """
    LOG_DIR = 'logs'
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    LOG_FILE_PATH = os.path.join(LOG_DIR, 'app.log')

    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        
        'formatters': {
            'console_formatter': {
                # A clean, aligned format for the console. NO COLORS.
                'format': '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s',
            },
            'file_formatter': {
                # A more detailed format for file logs.
                'format': '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d (%(process)d) - %(message)s',
            },
        },
        
        'handlers': {
            'console_handler': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',  # Log INFO and above to the console
                'formatter': 'console_formatter',
                'stream': sys.stdout,
            },
            'file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG', # Log DEBUG and above to the file
                'formatter': 'file_formatter',
                'filename': LOG_FILE_PATH,      # Name of the log file
                'maxBytes': 10 * 1024 * 1024, # 10 MB
                'backupCount': 5,           # Keep 5 old log files
                'encoding': 'utf-8',
            },
        },
        
        'root': {
            'level': 'DEBUG',
            'handlers': ['console_handler', 'file_handler']
        }
    }
    
    logging.config.dictConfig(LOGGING_CONFIG)