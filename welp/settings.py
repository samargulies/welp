"""
Django settings for welp project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from . import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cx2f^7#-vc&wfem=dg__t=oubggjndiz=j1!rkm7=zahc+1n04'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = config.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'places',
    'svg',
    'nested_admin',
    'martor',
    'localflavor',
    'imagekit',
    'storages',
    'mapwidgets',
    'django.contrib.sites',
    'django_comments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'welp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'welp.wsgi.application'

MAP_WIDGETS = config.MAP_WIDGETS

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = config.DATABASES

SITE_ID = config.SITE_ID

# Caches
# https://docs.djangoproject.com/en/2.0/topics/cache/
CACHES = config.CACHES

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# S3 Storage
# http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
if config.USE_S3:
    AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = config.AWS_STORAGE_BUCKET_NAME

    AWS_IS_GZIPPED = True
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_S3_CUSTOM_DOMAIN = f'{config.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_LOCATION = 'static'

    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'welp.custom_storages.MediaStorage'
        
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'dist/static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Fix for S3 and ImageKit
# https://github.com/matthewwithanm/django-imagekit/issues/391
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'welp.image_generators.FixJustInTime'

# GeoDjango configuration
# https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/spatialite/#spatialite-macos
if config.SPATIALITE_LIBRARY_PATH:
    SPATIALITE_LIBRARY_PATH = config.SPATIALITE_LIBRARY_PATH
