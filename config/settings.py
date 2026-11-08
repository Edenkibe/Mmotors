
"""
Django settings for config project.
Mmotors - Development and Production configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# =====================================================
# BASE CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env file (not committed to GitHub)
load_dotenv(BASE_DIR / ".env")

# =====================================================
# SECURITY SETTINGS
# =====================================================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be configured in environment variables.")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        ""
    ).split(",")
    if origin.strip()
]

# =====================================================
# APPLICATION DEFINITION
# =====================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'apps.core',
    'apps.accounts',
    'django_recaptcha',
    'widget_tweaks',
    'apps.voiture',
    'apps.promotion',
    'django_celery_beat',
    'apps.dossiers',
    'apps.contact',
    'apps.location',
    'apps.integration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# =====================================================
# DATABASE - MYSQL
# =====================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "Mmotors"),
        "USER": os.getenv("DB_USER", "root"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3308"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
        "CONN_MAX_AGE": 60,
    }
}

# =====================================================
# PASSWORD VALIDATION
# =====================================================

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

# =====================================================
# INTERNATIONALIZATION
# =====================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Paris'

USE_I18N = True
USE_TZ = True

# =====================================================
# STATIC FILES
# =====================================================

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = (
    [BASE_DIR / 'static']
    if (BASE_DIR / 'static').exists()
    else []
)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# =====================================================
# MEDIA FILES
# =====================================================

MEDIA_URL = '/voitures/'
MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", BASE_DIR / "voitures"))

# =====================================================
# AUTHENTICATION
# =====================================================

AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = "/"

PASSWORD_RESET_TIMEOUT = 14400

# =====================================================
# RECAPTCHA
# =====================================================

RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY", "")
RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY", "")

# =====================================================
# EMAIL CONFIGURATION
# =====================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '').strip()
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '').replace(' ', '')

DEFAULT_FROM_EMAIL = os.getenv(
    'DEFAULT_FROM_EMAIL',
    EMAIL_HOST_USER
)

EMAIL_TIMEOUT = 20

# =====================================================
# STRIPE
# =====================================================

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# =====================================================
# YOUSIGN
# =====================================================

YOUSIGN_API_KEY = os.getenv("YOUSIGN_API_KEY", "")
YOUSIGN_BASE_URL = os.getenv("YOUSIGN_BASE_URL", "")
YOUSIGN_WEBHOOK_SECRET = os.getenv(
    "YOUSIGN_WEBHOOK_SECRET",
    ""
)

# =====================================================
# CELERY / REDIS
# =====================================================

CELERY_BROKER_URL = os.getenv(
    "REDIS_URL",
    "redis://127.0.0.1:6380/0"
)

CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'Europe/Paris'
CELERY_ENABLE_UTC = True

CELERY_BEAT_SCHEDULE = {
    'update-promotions-every-minute': {
        'task': 'promotion.tasks.update_promotions',
        'schedule': 60.0,
    },

    'update-location-every-minute': {
        'task': 'location.tasks.update_locations',
        'schedule': 60.0,
    },
}

# =====================================================
# PRODUCTION SECURITY
# =====================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https"
)

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# =====================================================
# DEFAULT PRIMARY KEY
# =====================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
