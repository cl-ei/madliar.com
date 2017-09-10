import os
import logging


from etc.config import APP_LOG_PATH

__all__ = ("logger", )

logger = logging.getLogger("madliar_app")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(APP_LOG_PATH, "madliar_app.log"))
formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s:%(lineno)d:%(funcName)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
