#Author:ZJF
import os,logging,sys
from conf import settings
def logger(log_type):
    #create_logger
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)

    log_file = os.path.join(settings.LOG_PATH,settings.LOG_TYPES[log_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)
    formatter = settings.LOG_FORMAT

    #add formatter to ch and fh
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger