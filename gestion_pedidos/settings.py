import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Carga .env desde la raíz del proyecto (mismo nivel que manage.py)
load_dotenv(BASE_DIR / ".env")

def env_list(name, default=""):
    raw = os.getenv(name, default)
    return [x.strip() for x in raw.split(",") if x.strip()]

# --- Modo/seguridad ---
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-inseguro")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", "http://localhost:8000")

# --- Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pedidos",
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/login/"

ROOT_URLCONF = "gestion_pedidos.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # si tienes una carpeta 'templates' en la raíz del proyecto, se añade:
        "DIRS": [BASE_DIR / "templates"] if (BASE_DIR / "templates").exists() else [],
        "APP_DIRS": True,  # carga templates dentro de cada app (p.ej., pedidos/templates)
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

# --- Base de datos ---
# Por defecto (local) SQLite; si defines MYSQL_* en .env, usa MySQL (ideal en PA)
if os.getenv("MYSQL_DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MYSQL_DB_NAME"),
            "USER": os.getenv("MYSQL_DB_USER"),
            "PASSWORD": os.getenv("MYSQL_DB_PASSWORD"),
            "HOST": os.getenv("MYSQL_DB_HOST", "localhost"),
            "PORT": os.getenv("MYSQL_DB_PORT", "3306"),
            "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --- i18n ---
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# --- Static & Media ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"   # necesario para collectstatic en PA
# Solo si además tienes una carpeta 'static/' en la raíz:
if (BASE_DIR / "static").exists():
    STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Seguridad extra en prod ---
if not DEBUG:
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_SSL_REDIRECT = False  # En PA (free) el HTTPS lo maneja *.pythonanywhere.com
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
