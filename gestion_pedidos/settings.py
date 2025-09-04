import os
from pathlib import Path

# Carga del .env
from dotenv import load_dotenv
load_dotenv()  # lee .env desde la raíz del proyecto

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Básico ---
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-override-this")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Hosts
# Lee ALLOWED_HOSTS desde .env (coma-separado), añade defaults útiles
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()]
RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOST and RENDER_HOST not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_HOST)
# Para evitar 400 en pruebas locales
for h in ("localhost", "127.0.0.1","192.168.80.41"):
    if h not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(h)
# Render usa onrender.com
if ".onrender.com" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(".onrender.com")

# CSRF (necesario en Render)
CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]

# Zona horaria Colombia
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# --- Apps / Middleware ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # tus apps:
    "pedidos",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise justo después de SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gestion_pedidos.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "gestion_pedidos.wsgi.application"
ASGI_APPLICATION = "gestion_pedidos.asgi.application"

# --- Base de datos (Postgres via DATABASE_URL) ---
# Si no defines DATABASE_URL, caerá a SQLite (útil para un quick start offline)
default_db_url = os.environ.get("DATABASE_URL", "")
if default_db_url:
    DATABASES = {
        "default": dj_database_url.config(
            default=default_db_url,
            conn_max_age=600,
            ssl_require=True,  # fuerza SSL si tu URL no trae ?sslmode=require
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --- Archivos estáticos y media ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise: compresión + manifest (cache busting)
if os.environ.get("DEBUG", "True").lower() == "true":
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", str(BASE_DIR / "media"))

# --- Seguridad recomendable en prod ---
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 60  # puedes subirlo gradualmente
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# --- Logging mínimo (útil en Render) ---
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
