__version__ = '1.4.1'

import logging
import logging.handlers

logger = logging.getLogger( 'CRED Corelib' )
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
logger.addHandler(handler)
