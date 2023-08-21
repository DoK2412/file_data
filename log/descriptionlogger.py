import logging.config
import os


logger_config = {
    'version': 1,
    'formatters': {
        'formatting_info': {'format': '{asctime} - {msecs} - {funcName} - {levelname} - {message}',
                              'style': '{'},
        'formatting-error': {'format': '{asctime} - {msecs} - {funcName} - {levelname} - {message}',
                              'style': '{'}
    },
    'handlers': {
        'info': {
            'class': 'logging.FileHandler',
            'filename': os.path.dirname(os.path.realpath(__file__)) + '/info.log',
            'mode': 'a',
            'level': 'INFO',
            'formatter': 'formatting_info'
        },
        'error': {
            'class': 'logging.FileHandler',
            'filename': os.path.dirname(os.path.realpath(__file__)) + '/error.log',
            'mode': 'a',
            'level': 'ERROR',
            'formatter': 'formatting-error'
        }

    },

    'loggers': {
        'app_info': {
            'level': 'INFO',
            'handlers': ['info'],
            'propagate': False
        },

        'app_error': {
            'level': 'ERROR',
            'handlers': ['error'],
            'propagate': False
        }
    },

    'disable_existing_loggers': False,
    'filters': {},
}

logging.config.dictConfig(logger_config)
log_info = logging.getLogger('app_info')
log_error = logging.getLogger('app_error')