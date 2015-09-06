import os
import logging

from settings import LOG_DIR

logger = logging.getLogger(__name__)
fp = os.path.abspath(os.path.dirname(__file__))
# Create Handler
ch_log_file = os.path.join(LOG_DIR, 'modules.log')
ch_handler = logging.FileHandler(filename = ch_log_file)
# Create a basic formatter
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(module)s : %(message)s')
ch_handler.setFormatter(formatter)
# Add handler to logger
logger.addHandler(ch_handler)
logger.setLevel(logging.DEBUG)

