"""
Django settings for core project.

Gerado por 'django-admin startproject' usando Django 5.2.7.
Ajustado para funcionar em DEV e PRODUÇÃO (Railway/Nixpacks ou Docker),
com variáveis de ambiente via python-decouple e WhiteNoise para estáticos.
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url
from django.contrib.messages import constants as message_constants

# =========================
# Paths / Base
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Segurança / Debug
# =========================
# Em produção, defina SECRET_KEY nas variáveis do Railway.
SECRET_KEY = config("SECRET_KEY", default="dev-insecure-key-change-me")

# Se não houver DEBUG definido nas envs, assume False (produção).
DEBUG = config("DEBUG", default=False, cast=bool)

# ALLOWED_HOSTS via env (se vazio, usa localhost/127.0.0.1)
ALLOWED_HOSTS = [h for h in config("ALLOWED_HOSTS", default="").split(",") if h] or [
    "localhost",
    "127.0.0.1",
]

# CSRF_TRUSTED_ORIGINS (aceita múltiplos separados por vírgula)
CSRF_TRUSTED_ORIGINS = [
    o for o in config("CSRF_TRUSTED_ORIGINS", default="https://*.railway.app").split(",") if o
]

# Cabeçalhos de segurança recomendados em produção
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Estes podem ser ajustados conforme seu domínio:
    # CSRF_COOKIE_DOMAIN = config("CSRF_COOKIE_DOMAIN", default=None)
    # SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN", default=None)
else:
    SECURE_SSL_REDIRECT = False

# =========================
# Apps
# =========================
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps do projeto
    "usuarios",
    "consultas",

    # Tarefas assíncronas
    "django_q",
]

# Em DEV, evita servir estáticos duplicados
if DEBUG:
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")

# =========================
# Middleware
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise deve vir logo após SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =========================
# URLs / WSGI
# =========================
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

# =========================
# Templates
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# =========================
# Banco de Dados
# =========================
# Usa DATABASE_URL se existir (ex.: Postgres do Railway),
# caso contrário, cai para SQLite local.
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=False,  # Ajuste para True se o Postgres exigir SSL
    )
}

# =========================
# Validação de Senhas
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# I18N / TZ
# =========================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True  # Mantém datetimes como aware (UTC internamente)

# =========================
# Arquivos Estáticos & Mídia
# =========================
# WhiteNoise: coleta para staticfiles e serve em produção
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Se você tem estáticos dentro de templates/static, mantenha:
STATICFILES_DIRS = (
    BASE_DIR / "templates" / "static",
)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise: arquivos estáticos comprimidos e com manifest
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# =========================
# Mensagens (Bootstrap/Tailwind)
# =========================
MESSAGE_TAGS = {
    message_constants.SUCCESS: "bg-green-50 text-green-700",
    message_constants.ERROR: "bg-red-50 text-red-700",
}

# =========================
# Django-Q (fila com ORM)
# =========================
Q_CLUSTER = {
    "name": "pythonando",
    "workers": 1,
    "retry": 200,
    "timeout": 180,
    "queue_limit": 50,
    "orm": "default",  # usa o banco default (funciona em sqlite/postgres)
}

# =========================
# Logging básico (útil no Railway)
# =========================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO" if not DEBUG else "DEBUG",
    },
}

# =========================
# Integrações / APIs
# =========================
OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
