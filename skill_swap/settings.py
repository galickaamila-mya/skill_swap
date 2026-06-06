import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-skillswap-dev-key-change-in-production"
)
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "channels",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "core.apps.CoreConfig",
    "user.apps.UserConfig",
    "skills.apps.SkillsConfig",
    "matching.apps.MatchingConfig",
    "chat.apps.ChatConfig",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]
ROOT_URLCONF = "skill_swap.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
WSGI_APPLICATION = "skill_swap.wsgi.application"
ASGI_APPLICATION = "skill_swap.asgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "skill_swap_db"),
        "USER": os.environ.get("DB_USER", "shop"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "12345678"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static_dev"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = 1
LOGIN_URL = "/user/login/"
LOGIN_REDIRECT_URL = "/user/profile/"
LOGOUT_REDIRECT_URL = "/"
SESSION_ENGINE = "django.contrib.sessions.backends.db"
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@skillswap.local")
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {"SCOPE": ["profile", "email"], "AUTH_PARAMS": {"access_type": "online"}}
}
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
SPECTACULAR_SETTINGS = {
    "TITLE": "Skill Swap API",
    "DESCRIPTION": "API платформы бартерного обмена навыками",
    "VERSION": "1.0.0",
}
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_CACHE_DB = os.environ.get("REDIS_CACHE_DB", "1")
REDIS_CHANNEL_DB = os.environ.get("REDIS_CHANNEL_DB", "0")
REDIS_CACHE_URL = os.environ.get(
    "REDIS_CACHE_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}"
)
REDIS_CHANNEL_URL = os.environ.get(
    "REDIS_CHANNEL_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CHANNEL_DB}"
)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "IGNORE_EXCEPTIONS": True,
        },
    }
}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_CHANNEL_URL], "capacity": 1500, "expiry": 60},
    }
}
