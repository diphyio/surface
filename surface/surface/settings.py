"""
Django settings for surface project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import ppbenviron

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENV_VAR = ppbenviron.CustomEnv()
ENV_VAR.read_env(BASE_DIR / 'local.env')

# Application definition

INSTALLED_APPS = [
    'theme',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'impersonate',
    'surfapp',
    'dkron',
    'notifications',
    'slackbot',
    'dbcleanup',
    'inventory',
    'dns_ips',
    'scanners',
    'scanner_baseline',
    'knox',
    'apitokens',
    'vulns',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
]

ROOT_URLCONF = 'surface.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # surfapp templates required here as well to override `theme` ones,
        # (as theme needs to come first in INSTALLED_APPS)
        'DIRS': [BASE_DIR / 'surfapp' / 'templates'],
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

WSGI_APPLICATION = 'surface.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

## custom settings ##

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {'default': ENV_VAR.db('SURF_DATABASE_URL', default='sqlite:////' + str(BASE_DIR / 'db.sqlite3'))}
if ENV_VAR('SURF_DATABASE_USER', default=None):
    DATABASES['default']['USER'] = ENV_VAR('SURF_DATABASE_USER')
if ENV_VAR('SURF_DATABASE_PASSWORD', default=None):
    DATABASES['default']['PASSWORD'] = ENV_VAR('SURF_DATABASE_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': ENV_VAR('DATABASE_ENGINE', default='NOT_THIS_ONE'), # 'django.db.backends.postgresql_psycopg2',
        'NAME': ENV_VAR('DATABASE_NAME', default='NOT_THIS_ONE'),
        'USER': ENV_VAR('DATABASE_USER', default='NOT_THIS_ONE'),
        'PASSWORD': ENV_VAR('DATABASE_PASS', default='NOT_THIS_ONE'),
        'HOST': ENV_VAR('DATABASE_HOST', default='NOT_THIS_ONE'),
        'PORT': ENV_VAR('DATABASE_PORT', default='NOT_THIS_ONE')
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_VAR('SURF_SECRET_KEY', default='NOT_THIS_ONE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV_VAR.bool('SURF_DEBUG', default=True)
ALLOWED_HOSTS = ENV_VAR.list('SURF_ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SCANNERS_REGISTRY_AUTH = ENV_VAR.json('SURF_SCANNERS_REGISTRY_AUTH', default={})
SCANNERS_DOCKER_CA_CERT = ENV_VAR('SURF_SCANNERS_DOCKER_CA_CERT', default=None)
SCANNERS_DOCKER_CA_CERT_PATH = ENV_VAR('SURF_SCANNERS_DOCKER_CA_CERT_PATH', default=None)
SCANNERS_DOCKER_CLIENT_KEY = ENV_VAR('SURF_SCANNERS_DOCKER_CLIENT_KEY', default='')
SCANNERS_DOCKER_CLIENT_KEY_PATH = ENV_VAR('SURF_SCANNERS_DOCKER_CLIENT_KEY_PATH', default='')
SCANNERS_DOCKER_CLIENT_CERT = ENV_VAR('SURF_SCANNERS_DOCKER_CLIENT_CERT', default='')
SCANNERS_DOCKER_CLIENT_CERT_PATH = ENV_VAR('SURF_SCANNERS_DOCKER_CLIENT_CERT_PATH', default='')

DKRON_URL = ENV_VAR('SURF_DKRON_URL', default='http://localhost:8888/')
# used for authenticating dkron webhook calls (first line in payload)
DKRON_TOKEN = ENV_VAR('SURF_DKRON_TOKEN', default=None)
DKRON_BIN_DIR = ENV_VAR('SURF_DKRON_BIN_DIR', default=BASE_DIR.parent / 'dev' / 'dkron')
DKRON_TAGS = ENV_VAR.list('SURF_DKRON_TAGS', default=[])
DKRON_JOB_LABEL = ENV_VAR('SURF_DKRON_JOB_LABEL', default='surf')
DKRON_JOIN = ENV_VAR.list('SURF_DKRON_JOIN', default=None)
DKRON_ENCRYPT = ENV_VAR('SURF_DKRON_ENCRYPT', default=None)
DKRON_WORKDIR = ENV_VAR('SURF_DKRON_WORKDIR', default=BASE_DIR)
DKRON_SERVER = ENV_VAR('SURF_DKRON_SERVER', default=True)
DKRON_API_AUTH = ENV_VAR('SURF_DKRON_API_AUTH', default=None)
DKRON_VERSION = ENV_VAR('SURF_DKRON_VERSION', default='3.1.10')
DKRON_WEBHOOK_URL = ENV_VAR('SURF_DKRON_WEBHOOK_URL', default=None)
DKRON_NAMESPACE = ENV_VAR('SURF_DKRON_NAMESPACE', default=None)
DKRON_NODE_NAME = ENV_VAR('SURF_DKRON_NODE_NAME', default=None)

# settings docs in https://github.com/surface-security/django-notification-sender#readme
NOTIFICATIONS_SLACK_APP_TOKEN = ENV_VAR('SURF_NOTIFICATIONS_SLACK_APP_TOKEN', default=None)
NOTIFICATIONS_MAIL_FROM = ENV_VAR('SURF_NOTIFICATIONS_MAIL_FROM', default=None)

# settings docs in https://github.com/surface-security/django-slack-processor#readme
SLACKBOT_BOT_TOKEN = ENV_VAR('SURF_SLACKBOT_BOT_TOKEN', default=None)
SLACKBOT_APP_TOKEN = ENV_VAR('SURF_SLACKBOT_APP_TOKEN', default=None)

AVZONE = ENV_VAR('SURF_AVZONE', default='dev')

# FIXME: SHOULD NOT BE REQUIRED
DATABASE_LOCKS_STATUS_FILE = None
DATABASE_LOCKS_ENABLED = False

SURFACE_LINKS_ITEMS = None
SURFACE_MENU_ITEMS = None

LOGBASECOMMAND_PREFIX = 'surface.command'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'},
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'},
    },
    'formatters': {
        'verbose': {'format': '[%(asctime)s] [%(process)s] [%(levelname)s] [%(name)s] %(message)s'},
        'minimal': {'format': '[%(levelname)s] [%(name)s] %(message)s'},
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'console_minimal': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'minimal',
        },
        'console_debug_minimal': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'minimal',
        },
    },
    'loggers': {
        '': {'handlers': ['console', 'console_debug'], 'level': 'INFO', 'propagate': True},
        'django': {'handlers': ['console', 'console_debug'], 'level': 'INFO'},
        'django.server': {'handlers': ['console', 'console_debug'], 'level': 'DEBUG', 'propagate': False},
        'surface.command': {
            'handlers': ['console_minimal', 'console_debug_minimal'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

TITLE = 'Surface'
VERSION = 'dev'
