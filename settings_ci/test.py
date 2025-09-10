"""
Test settings for ITVDN Django Study Project
"""

import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

MEDIA_URL = "/media/"  # Add leading slash
MEDIA_ROOT = os.path.join(BASE_DIR, "media/", "img")

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
    POSTGRES_PORT=(int, 5432),
)

# Read .env file from root directory
environ.Env.read_env(BASE_DIR / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="test-secret-key-for-ci-only")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "itvdn_shop",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "user_app",  # Your custom app
    "phone_field",
    "django_premailer",
    "send_email",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "urls"
AUTH_USER_MODEL = "user_app.User"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "wsgi.application"

# Test database using environment variables from .env file
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="django_study_test"),
        "USER": env("POSTGRES_USER", default="django_user"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="django_password"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default=5432),
    }
}

# Password validation - simplified for tests
AUTH_PASSWORD_VALIDATORS = []

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/admin/"  # Where to redirect after successful login
LOGOUT_REDIRECT_URL = "/login/"

# Internationalization
LANGUAGE_CODE = env("LANGUAGE_CODE", default="en-us")
TIME_ZONE = env("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"  # Add leading slash
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # For collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Your custom static files
]
# Static files finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Use in-memory cache for tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Fast password hashing for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable logging during tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "handlers": ["console"],
    },
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = env("EMAIL_USER")
EMAIL_RECIPIENT = env("EMAIL_RECIPIENT")
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "TestSite Team <noreply@example.com>"

MAILCHIMP_API_KEY = env("MLCHMP_KEY")
MAILCHIMP_DATA_CENTER = env("MLCHMP_DATA_CENTER")
MAILCHIMP_EMAIL_LIST_ID = env("MLCHMP_EMAIL_LIST_ID")
