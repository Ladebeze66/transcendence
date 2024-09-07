# /pong/settings.py

"""
Django settings for pong project.

Generated by 'django-admin startproject' using Django 3.2.
"""

import os
import logging.config
from pathlib import Path

try:
    redis_instance = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    redis_instance.ping()
    print("Connexion à Redis réussie")
except redis.ConnectionError:
    raise ImproperlyConfigured("Échec de la connexion à Redis")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '12345678'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'channels',
	'pong.game',
	'rest_framework'
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

ROOT_URLCONF = 'pong.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'pong', 'static')],  # Ensure templates are found
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

ASGI_APPLICATION = 'pong.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.getenv('DB_NAME'),
		'USER': os.getenv('DB_USER'),
		'PASSWORD': os.getenv('DB_PASSWORD'),
		'HOST': os.getenv('DB_HOST'),
		'PORT': '5432',
	}
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'pong/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Channels
# Configuration des couches de canaux
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
    'chat': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'json': {
			'()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
			'format': '%(asctime)s %(levelname)s %(name)s %(module)s %(process)d %(thread)d %(message)s',
		},
		'default': {
			'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
		},
		'verbose': {
			'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s [%(process)d:%(thread)d]',
		},
		'simple': {
			'format': '%(levelname)s %(message)s',
		},
	},
	'filters': {
		'require_debug_true': {
			'()': 'django.utils.log.RequireDebugTrue',
		},
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse',
		},
	},
	'handlers': {
		'file': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': os.path.join(BASE_DIR, 'logs/django.log'),
			'formatter': 'json',
			'maxBytes': 1024 * 1024 * 5,  # 5 MB
			'backupCount': 5,
		},
		'error_file': {
			'level': 'ERROR',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': os.path.join(BASE_DIR, 'logs/django_errors.log'),
			'formatter': 'json',
			'maxBytes': 1024 * 1024 * 5,  # 5 MB
			'backupCount': 5,
		},
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'verbose',
			'filters': ['require_debug_true'],
		},
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler',
			'filters': ['require_debug_false'],
		},
	},
	'loggers': {
		'django': {
			'handlers': ['file', 'console', 'mail_admins'],
			'level': 'DEBUG',
			'propagate': True,
		},
		'django.request': {
			'handlers': ['error_file', 'mail_admins'],
			'level': 'ERROR',
			'propagate': False,
		},
		'django.security': {
			'handlers': ['error_file', 'mail_admins'],
			'level': 'ERROR',
			'propagate': False,
		},
	},
	'root': {
		'handlers': ['console', 'file'],
		'level': 'INFO',
	},
}
