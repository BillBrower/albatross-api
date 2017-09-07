"""
Django settings for albatross project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import requests, os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zre$(5&9ax$y_kcnm=q#ec9v8hz8t37=_*twb(_fo5dup31%%r'

# SECURITY WARNING: don't run with debug turned on in production!
CONFIG_NAME = os.environ.get('CONFIG_NAME')
if CONFIG_NAME == 'production':
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    '34.195.47.179',
    'getalbatross.com',
    'localhost',
    'www.getalbatross.com'
]
try:
    EC2_PRIVATE_IP = requests.get(
        'http://169.254.169.254/latest/meta-data/local-ipv4',
        timeout = 0.01
    ).text
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

    ELB_HOST_NAME = requests.get(
        'http://169.254.169.254/latest/meta-data/public-hostname',
        timeout = 0.01
    ).text
    ALLOWED_HOSTS.append(ELB_HOST_NAME)
except requests.exceptions.RequestException:
    pass


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'authentication',
    'behave_django',
    'storages',
    'ember_web_app',
    'registration',
    'invitations',
    'teams',
    'projects',
    'toggl',
    'django_extensions'
]

SITE_ID = 1 # For rest_auth.registration

# TODO: Get CSRF working with Ember and add 'django.middleware.csrf.CsrfViewMiddleware', back here
MIDDLEWARE = [
    'albatross_api.middleware.DisableCSRF',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'albatross_api.urls'

ROOT_URLPREFIX = 'api/v1/'

REST_SESSION_LOGIN = True

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

WSGI_APPLICATION = 'albatross_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD', None), # CircleCI doesn't have a db password
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}


# Django Auth Settings

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_USERNAME_REQUIRED = False



# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# Django CORS settings
# TODO: Get CORS working on production without CORS_ORIGIN_ALLOW_ALL

CORS_ORIGIN_ALLOW_ALL = True

CORS_URLS_REGEX = r'^/api/.*$'


# Django Email settings
# https://github.com/elbuo8/sendgrid-django

EMAIL_BACKEND = "sgbackend.SendGridBackend"

SENDGRID_API_KEY = "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"


# Django REST Framework Settings

REST_FRAMEWORK = {
    'PAGE_SIZE': 25,
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.PageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'authentication.serializers.PasswordResetSerializer',
}


# Django Rest Auth Settings

LOGOUT_ON_PASSWORD_CHANGE = False

OLD_PASSWORD_FIELD_ENABLED = True


# Registration settings

SIGNUP_URL = 'https://getalbatross.com/signup'
RESET_PASSWORD_URL = 'https://getalbatross.com/reset-password'

# Django Storages Settings

AWS_ACCESS_KEY_ID = os.environ.get('S3_API_KEY')

from boto.s3.connection import OrdinaryCallingFormat
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

AWS_S3_HOST = 's3.amazonaws.com'

AWS_S3_REGION_NAME = 'us-east-1'

AWS_SECRET_ACCESS_KEY = os.environ.get('S3_API_SECRET')

AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_WEB_APP_ASSETS_BUCKET')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

S3_USE_SIGV4 = True