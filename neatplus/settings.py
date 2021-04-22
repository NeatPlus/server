import os
from pathlib import Path

import sentry_sdk
from django.core.management.utils import get_random_secret_key
from environs import Env
from marshmallow.validate import OneOf
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

# Read .env file for environment variable
env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Server environment
SERVER_ENVIRONMENT = env.str(
    "SERVER_ENVIRONMENT",
    validate=OneOf(choices=["development", "testing", "staging", "production"]),
    error="SERVER_ENVIRONMENT can only be one of {choices}",
)

# Is server secure server?
IS_SERVER_SECURE = SERVER_ENVIRONMENT in ["staging", "production"]

# Secret key for server
if IS_SERVER_SECURE:
    SECRET_KEY = env.str("DJANGO_SECRET_KEY", validate=lambda n: len(n) > 49)
else:
    SECRET_KEY = env.str(
        "DJANGO_SECRET_KEY",
        validate=lambda n: len(n) > 49,
        default=get_random_secret_key(),
    )

# Debug
if IS_SERVER_SECURE:
    DEBUG = False
else:
    DEBUG = True

# List of allowed hosts
if IS_SERVER_SECURE:
    ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[], subcast=str)
else:
    ALLOWED_HOSTS = ["0.0.0.0", "localhost", "127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    "modeltranslation",
    "admin_interface",
    "colorfield",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Internal
    "summary",
    "survey",
    "user",
    # External
    "django_filters",
    "rest_framework",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "silk",
    "corsheaders",
    "simple_history",
    "ordered_model",
]

try:
    import django_extensions

    INSTALLED_APPS += ["django_extensions"]

except ModuleNotFoundError:
    pass

X_FRAME_OPTIONS = "SAMEORIGIN"

MIDDLEWARE = [
    "silk.middleware.SilkyMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "neatplus.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "neatplus.wsgi.application"


# Database

DATABASES = {"default": env.dj_db_url("DATABASE_URL", default="sqlite:///db.sqlite3")}

# CACHES
CACHE = {"default": env.dj_cache_url("CACHE_URL", default="locmem://")}

# Auth user model
AUTH_USER_MODEL = "user.User"

AUTHENTICATION_BACKENDS = ["neatplus.auth_backends.EmailOrUsernameModelBackend"]

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


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging
ENABLE_SYSLOG = env.bool("ENABLE_SYSLOG", default=False)

if ENABLE_SYSLOG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "()": "django.utils.log.ServerFormatter",
                "format": "[{server_time}] ({levelname}): {message}",
                "style": "{",
            },
        },
        "handlers": {
            "SysLog": {
                "level": "INFO",
                "formatter": "simple",
                "class": "logging.handlers.SysLogHandler",
                "address": (env.url("SYSLOG_URL"), env.int("SYSLOG_PORT")),
            },
        },
        "loggers": {
            "django": {
                "handlers": ["SysLog"],
                "level": "INFO",
            },
        },
    }


# Static file and media file settings
USE_S3_STORAGE = env.bool("USE_S3_STORAGE", default=False)
if USE_S3_STORAGE:
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
    CACHE_CONTROL_MAX_AGE = env.int("AWS_S3_CACHE_CONTROL_MAX_AGE", default=86400)
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": f"max-age={CACHE_CONTROL_MAX_AGE}"}
    AWS_S3_REGION_NAME = env.str("AWS_S3_REGION_NAME")
    USE_CLOUDFRONT_CDN = env.bool("USE_CLOUDFRONT_CDN", default=False)
    if USE_CLOUDFRONT_CDN:
        AWS_S3_CUSTOM_DOMAIN = env.str("CLOUDFRONT_CDN_URL")
    else:
        AWS_S3_CUSTOM_DOMAIN = (
            f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
        )
    UPLOAD_STATIC_TO_S3 = env.bool("UPLOAD_STATIC_TO_S3", default=True)
    # s3 static settings
    if UPLOAD_STATIC_TO_S3:
        STATIC_LOCATION = "static"
        STATIC_URL = f"{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
        STATICFILES_STORAGE = "neatplus.storage_backends.StaticStorage"
    else:
        STATIC_LOCATION = "static"
        STATIC_URL = "/static/"
        STATIC_ROOT = os.path.join(BASE_DIR, "static")
    # s3 media settings
    MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "neatplus.storage_backends.MediaStorage"
else:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Django rest framework settings

REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "neatplus.pagination.CustomLimitOffsetPagination",
    "PAGE_SIZE": 100,
}

if IS_SERVER_SECURE:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
    ]
else:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ]

# OTP settings
OTP_TOTP_ISSUER = env.str("OTP_TOTP_ISSUER", default="neatplus-server")

# SimpleJWT settings
SIMPLE_JWT = {
    "ALGORITHM": "HS512",
    "ISSUER": env.str("SIMPLE_JWT_ISSUER", default="neatplus-sever"),
}

# CORS settings
CORS_URLS_REGEX = r"^(/api/).*$"
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=[], subcast=str)

# SILK settings
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_META = True
SILKY_INTERCEPT_PERCENT = env.float("SILKY_INTERCEPT_PERCENT", default=1.0)


# Sentry
ENABLE_SENTRY = env.bool("ENABLE_SENTRY", default=False)
if ENABLE_SENTRY:
    sentry_sdk.init(
        dsn=env.url("SENTRY_DSN"),
        integrations=[DjangoIntegration(), CeleryIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        environment=SERVER_ENVIRONMENT,
    )


# CELERY
CELERY_BROKER_TYPE = env.str(
    "CELERY_BROKER_TYPE",
    default="filesystem",
    validate=OneOf(choices=["redis", "filesystem"]),
    error="CELERY_BROKER_TYPE can only be one of {choices}",
)

if CELERY_BROKER_TYPE == "redis":
    CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL

if CELERY_BROKER_TYPE == "filesystem":
    CELERY_BROKER_URL = "filesystem://"
    CELERY_RESULT_BACKEND = "file:///tmp"
    CELERY_BROKER_TRANSPORT_OPTIONS = {
        "data_folder_in": "/tmp",
        "data_folder_out": "/tmp",
        "data_folder_processed": "/tmp",
    }

CELERY_TIMEZONE = TIME_ZONE
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_WORKER_PREFETCH_MULTIPLIER = 1


# Default auto field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Model translation
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = ("en", "es", "fr")
MODELTRANSLATION_PREPOPULATE_LANGUAGE = "en"
MODELTRANSLATION_AUTO_POPULATE = True
