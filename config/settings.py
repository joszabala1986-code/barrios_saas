import os
from dotenv import load_dotenv
from pathlib import Path

# =========================
# LOAD ENV
# =========================
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# ENTORNO
# =========================
ENV = os.environ.get('ENV', 'dev')
DEBUG = ENV == 'dev'

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

# =========================
# HOSTS
# =========================
if DEBUG:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]
else:
    ALLOWED_HOSTS = [
        "barrios.plantadigital.com.ar",
        "www.barrios.plantadigital.com.ar",
        "barrios-saas.onrender.com",
    ]

    CSRF_TRUSTED_ORIGINS = [
        "https://barrios.plantadigital.com.ar",
        "https://www.barrios.plantadigital.com.ar",
        "https://barrios-saas.onrender.com",
    ]

# =========================
# SEGURIDAD
# =========================
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    # 🔥 FIX CSRF
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_HTTPONLY = False

    SESSION_COOKIE_HTTPONLY = True

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'SAMEORIGIN'

    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"

    SECURE_CROSS_ORIGIN_OPENER_POLICY = None
    SECURE_CROSS_ORIGIN_RESOURCE_POLICY = None
else:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False

    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'

# =========================
# APPS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core.apps.CoreConfig',
    'axes',
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

   
    'axes.middleware.AxesMiddleware',
    'core.middleware.BarrioMiddleware',
]

# =========================
# URLS / WSGI
# =========================
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# =========================
# TEMPLATES
# =========================
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

# =========================
# BASE DE DATOS
# =========================
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'postgres'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),

            # 🔥 USAR HOST DIRECTO DE SUPABASE (NO pooler)
            'HOST': os.environ.get('DB_HOST'),

            'PORT': os.environ.get('DB_PORT', '6543'),

            'OPTIONS': {
                'sslmode': 'require',
            },

            # 🔥 evita errores 502
            'CONN_MAX_AGE': 60,
        }
    }

# =========================
# PASSWORDS
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# LOCALIZACIÓN
# =========================
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Mendoza'

USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES
# =========================
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================
# MEDIA
# =========================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =========================
# USER
# =========================
AUTH_USER_MODEL = 'core.Usuario'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'

# =========================
# EMAIL
# =========================
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.mail.yahoo.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_USER')

# =========================
# LOGGING
# =========================
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}


# =========================
# SESIONES
# =========================
SESSION_COOKIE_AGE = 2592000
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# =========================
# SUPABASE
# =========================
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# =========================
# INTENTOS DE ACCESOS
# =========================
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 10
AXES_COOLOFF_TIME = 1  # horas
AXES_RESET_ON_SUCCESS = True

# 🔥 CLAVE PARA RENDER (PROXY)
AXES_BEHIND_REVERSE_PROXY = False

# 🔥 IDENTIFICAR IP REAL
