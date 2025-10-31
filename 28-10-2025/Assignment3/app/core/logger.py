import logging
from datetime import datetime

logging.basicConfig(
    level= logging.INFO,
    format = '%(asctime)s -%(name)s -%(levelname)s -%(message)s',
    handlers=[
        logging.FileHandler(f'api_logs_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)