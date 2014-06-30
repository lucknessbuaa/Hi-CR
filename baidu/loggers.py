LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
                'format': '%(levelname)s %(asctime)s %(message)s'
                },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'standard',
        },
        'test1_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'path1',
            'formatter':'standard',
        },
        'test2_handler': {
            'level':'DEBUG',
                   'class':'logging.handlers.RotatingFileHandler',
            'filename':'path2',
            'formatter':'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'test1':{
            'handlers': ['test1_handler'],
            'level': 'INFO',
            'propagate': False
        },
         'test2':{
            'handlers': ['test2_handler'],
            'level': 'INFO',
                          'propagate': False
        },
    }
}

