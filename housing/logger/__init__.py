import logging
from datetime import datetime
import os

LOG_DIR = "logs" # Directory name 

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}" # string of current datetime

LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log"  # file name with format 'log_current-time-stamp.log'

os.makedirs(LOG_DIR, exist_ok=True) # Create the log directory if not exisis

LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)  # Entire path of log file

# Configuring what information the log file will contain.
logging.basicConfig(filename=LOG_FILE_PATH,
 filemode="w",
 format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
 level = logging.INFO
 )