LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'normal': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },  
        'simple': {
            'format': '%(levelname)s %(module)s %(message)s'
            }   
    },       
    'filters': {
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },  
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },  
        'django': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 1,
            'backupCount': 5,
            'filename': 'logs/django.log',
            'formatter': 'normal'
        },  
        'hicr': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 1,
            'backupCount': 5,
            'filename': 'logs/hicr.log',
            'formatter': 'normal'
        },  
    },
    'loggers': {
        'django': {
            'handlers': ['django'],
            'propagate': False,
            'level': 'DEBUG'
        },
        'mq': {
            'handlers': ['console', 'hicr'],
            'propagate': False,
            'level': 'DEBUG'
        },
        '': {
            'handlers': ['hicr'],
            'level': 'DEBUG'
        }
    }    
}

