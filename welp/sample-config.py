import os

AWS_ACCESS_KEY_ID = 'abc'
AWS_SECRET_ACCESS_KEY = 'abc'
AWS_STORAGE_BUCKET_NAME = 'welp-app'
SPATIALITE_LIBRARY_PATH = '/usr/lib/x86_64-linux-gnu/libspatialite.so.5'
USE_S3 = True
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'imagekit': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': None,
    }
}
MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocationName", "london"),
        ("GooglePlaceAutocompleteOptions", {'componentRestrictions': {'country': 'uk'}}),
        ("markerFitZoom", 12),
    ),
    "GOOGLE_MAP_API_KEY": "<google-api-key>"
}
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
SITE_ID = 1
DEBUG = True
ALLOWED_HOSTS = ["*"]
GOOGLE_RECAPTCHA_SECRET_KEY = '6LdRSRYUAAAAAOnk5yomm1dI9BmQkJWTg_wIlMJ_'
GOOGLE_RECAPTCHA_SITE_KEY = '6LdRSRYUAAAAAOnk5yomm1dI9BmQkJWTg_wIlMJ_'
GOOGLE_ANALYTICS_TRACKING_ID = 'UA-12341231-1'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file_log': {
              'level':'DEBUG',
              'class':'logging.handlers.RotatingFileHandler',
              'filename': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'welp.log'),
              'maxBytes': 1024 * 1024 * 15, # 15MB
              'backupCount': 10,
          },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file_log'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}