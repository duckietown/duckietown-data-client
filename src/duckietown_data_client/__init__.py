

__version__ = '1.0.0'

import logging

logging.basicConfig()

logger = logging.getLogger('dt-data-client')
logger.setLevel(logging.DEBUG)

from .main_entry_point import main

