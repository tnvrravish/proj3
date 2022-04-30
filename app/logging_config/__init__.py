import logging
import os
from logging.config import dictConfig

import flask
from flask import request, current_app

# from app.logging_config.log_formatters import RequestFormatter
from app import config

log_con = flask.Blueprint('log_con', __name__)


@log_con.before_app_request
def before_request_logging():
    log = logging.getLogger("myApp")
    log.info("REQUEST")


@log_con.after_app_request
def after_request_logging(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response
    elif request.path.startswith('/bootstrap'):
        return response

    log = logging.getLogger("myApp")
    log.info("RESPONSE")
    return response


@log_con.before_app_first_request
def setup_logs():
    # set the name of the apps log folder to logs
    logdir = config.Config.LOG_DIR
    # make a directory if it doesn't exist
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger("myApp")
    log.info("first log message before first request")


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'RequestFormatter': {
            '()': 'app.logging_config.log_formatters.RequestFormatter',
            'format': '%(levelname)s : %(message)s'
        },
        'UploadFormatter': {
            '()': 'app.logging_config.log_formatters.RequestFormatter',
            'format': '%(asctime)s : %(message)s'
        },
        'InfoFormatter': {
            '()': 'app.logging_config.log_formatters.RequestFormatter',
            'format': '%(message)s :[%(asctime)s] [%(process)d] %(remote_addr)s requested %(url)s'

        }

    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file.handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'handler.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.myapp': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'InfoFormatter',
            'filename': os.path.join(config.Config.LOG_DIR, 'myapp.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.myupload': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'UploadFormatter',
            'filename': os.path.join(config.Config.LOG_DIR, 'csvupload.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.errors': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'errors.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },

    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'file.handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default', 'file.handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'myApp': {  # if __name__ == '__main__'
            'handlers': ['file.handler.myapp'],
            'level': 'DEBUG',
            'propagate': False
        },
        'myUpload': {  # if __name__ == '__main__'
            'handlers': ['file.handler.myupload'],
            'level': 'INFO',
            'propagate': False
        },
        'myerrors': {  # if __name__ == '__main__'
            'handlers': ['file.handler.errors'],
            'level': 'DEBUG',
            'propagate': False
        },

    }
}
