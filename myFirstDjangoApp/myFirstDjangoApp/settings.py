from pathlib import Path
import os

# ===========================
# --- Répertoires de base ---
# ===========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===========================
# --- Sécurité & Débogage ---
# ===========================
SECRET_KEY = 'django-insecure-i+#tm_aytosdy7pg2yvu69q7ty(u*vwwou5m)w3ex$d^-g66l_'
DEBUG = True
ALLOWED_HOSTS = ['*']

# ===========================
# --- Applications installées ---
# ===========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'myApp.apps.MyappConfig'
]

# ===========================
# --- Middleware ---
# ===========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # si tu utilises WhiteNoise pour le déploiement
]

ROOT_URLCONF = 'myFirstDjangoApp.urls'

# ===========================
# --- Templates ---
# ===========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # dossier de tes templates
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

WSGI_APPLICATION = 'myFirstDjangoApp.wsgi.application'

# ===========================
# --- Base de données ---
# ===========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===========================
# --- Validation des mots de passe ---
# ===========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===========================
# --- Internationalisation ---
# ===========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ===========================
# --- Fichiers statiques ---
# ===========================
STATIC_URL = '/static/'                           # URL pour accéder aux fichiers statiques
STATICFILES_DIRS = [BASE_DIR / "static"]          # dossier où se trouvent les CSS/JS du projet
STATIC_ROOT = BASE_DIR / 'productionfiles'        # dossier pour collectstatic (déploiement)

# ===========================
# --- Fichiers média ---
# ===========================
MEDIA_URL = '/media/'                              # URL pour accéder aux fichiers uploadés
MEDIA_ROOT = BASE_DIR / 'media'                    # dossier où sont stockés les fichiers uploadés

# ===========================
# --- Email (SMTP Gmail) ---
# ===========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bambaloahmadou@gmail.com'
EMAIL_HOST_PASSWORD = 'ECz6@5n%'  # prudence : à ne jamais mettre en clair pour la prod !

# ===========================
# --- Auto Field par défaut ---
# ===========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'espace_etudiant'
