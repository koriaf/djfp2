import os
from envparse import env

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = env.bool('PL_DEBUG', default=True)
SECRET_KEY = env('PL_SECRET_KEY', default="DefaultSecretKey")

ALLOWED_HOSTS = ['*']  # change to actual before production

CSRF_COOKIE_SECURE = not DEBUG  # change it to False if you are not using HTTPS

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djfp2',
    'djfp2.calendar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'djfp2.urls'

WSGI_APPLICATION = 'djfp2.wsgi.application'
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = False
USE_L10N = False
USE_TZ = True
TIME_ZONE = env('PL_TIMEZONE', default='UTC')

STATIC_URL = '/static/'
MEDIA_URL = '/static/media/'

# for collectstatic
STATIC_ROOT = env(
    'PL_STATIC_ROOT',
    default=os.path.join(BASE_DIR, "../../var/static_root")
)

DATABASES = {
    'default': {
        'ENGINE': env('PL_DB_ENGINE', default='django.db.backends.postgresql_psycopg2'),
        'NAME': env('PL_DB_NAME', default='django_planner'),
        'HOST': env('PL_DB_HOST', default='db'),
        'PORT': env('PL_DB_PORT', default=5432),
        'USER': env('PL_DB_USERNAME', default='django_planner'),
        'PASSWORD': env('PL_DB_PASSWORD', default='replace it in django.env file'),
        'ATOMIC_REQUESTS': True,
    }
}

RAVEN_DSN = env('PL_RAVEN_DSN', default=None)
if RAVEN_DSN:
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]
    RAVEN_CONFIG = {
        'dsn': RAVEN_DSN,
    }

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
