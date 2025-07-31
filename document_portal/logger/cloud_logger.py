import os
import logging
from datetime import datetime
from document_portal.utils.config_loader import load_config
from logging.handlers import RotatingFileHandler
import structlog

class CustomLogger():
    def __init__(self, log_dir="logs"): 
        # Loading configurations  
        config = load_config("cloud_logger")
        
        self.file_handler_level = config['file_handler']['level'].upper()
        self.file_format = config['file_handler']['format']
        
        self.console_handler_level = config['console_handler']['level'].upper()
        self.console_format = config['console_handler']['format']
        
        self.log_max_bytes = config['log_max_bytes'] 
        self.log_backup_counts = config['log_backup_counts']
        self.date_format = config['date_format']
        
        # Ensure logs directory exists
        self.log_dir = os.path.abspath(config['log_dir'])
        os.makedirs(self.log_dir, exist_ok=True)

        log_file = f"{datetime.now().strftime(self.date_format)}.log"
        self.log_file = os.path.join(self.log_dir, log_file)

    def get_logger(self, name:str=__file__):
        logger_name = os.path.basename(name)
        
        # <--- File Handler --->
        file_handler = RotatingFileHandler(
            self.log_file, 
            maxBytes=self.log_max_bytes, 
            backupCount=self.log_backup_counts
        )
        file_formatter = logging.Formatter(
            self.file_format
            # Add lines for customization
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(self.file_handler_level)
        
        # <--- Console Handler --->
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            self.console_format
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(self.console_handler_level)
        
        logging.basicConfig(
            
        )
        
        
        
        
