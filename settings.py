import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

MEDIA_URL = "/media/"  # Add leading slash
MEDIA_ROOT = os.path.join(BASE_DIR, "media/", "img")

# Initialize environment variables
env = environ.Env()

# Read Docker env file first, then fallback to .env
docker_env_file = BASE_DIR / ".env.docker"
regular_env_file = BASE_DIR / ".env"

is_local = os.getenv("LOCAL", "").lower() == "true"

if is_local:
    # Force use of regular .env file
    if regular_env_file.exists():
        env.read_env(regular_env_file)  # Use env.read_env(), not environ.Env.read_env()
        print(f"Loading LOCAL environment from: {regular_env_file}")
    else:
        print(f"Warning: Local env file {regular_env_file} not found!")
else:
    if docker_env_file.exists():
        env.read_env(docker_env_file)  # Use env.read_env()
        print(f"Loading environment from: {docker_env_file}")
    elif regular_env_file.exists():
        env.read_env(regular_env_file)  # Use env.read_env()
        print(f"Loading fallback environment from: {regular_env_file}")
    else:
        print("Warning: No .env file found")

# Quick Access to env vars - all values must be in .env
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])

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

# Database - Simplified approach
postgres_host = env("POSTGRES_HOST", default=None)

if postgres_host:
    # PostgreSQL configuration
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("POSTGRES_DB"),
            "USER": env("POSTGRES_USER"),
            "PASSWORD": env("POSTGRES_PASSWORD"),
            "HOST": postgres_host,
            "PORT": env.int("POSTGRES_PORT", default=5432),
        }
    }
    print(f"Using PostgreSQL at: {postgres_host}")
else:
    # SQLite fallback
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    print("Using SQLite for development")

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# Tell Django to use your custom User model instead of the default one
AUTH_USER_MODEL = "user_app.User"
# Custom authentication backend
# AUTHENTICATION_BACKENDS = [
#     'user_app.backends.EmailBackend',  # Your custom email backend
#     'django.contrib.auth.backends.ModelBackend',  # Keep as fallback
# ]

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/admin/"  # Where to redirect after successful login
LOGOUT_REDIRECT_URL = "/login/"

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
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

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# GMAIL CONFIG
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
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
