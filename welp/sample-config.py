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