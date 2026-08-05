from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR.parent / ".env"

load_dotenv(ENV_FILE)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.tenants',
    'core',
    'apps.inspecoes',
    'apps.produtos',
    'apps.configuracao',
    'apps.ia',
    ]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.tenants.middleware.TenantMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.tenant',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {

    "default": {

        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),

    },
    "vector": {

    "ENGINE": "django.db.backends.postgresql",

    "NAME": os.getenv("VECTOR_DB"),

    "USER": os.getenv("VECTOR_USER"),

    "PASSWORD": os.getenv("VECTOR_PASSWORD"),

    "HOST": os.getenv("VECTOR_HOST"),

    "PORT": os.getenv("VECTOR_PORT"),

}}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / "media"

# ----------------------- Inferência de IA -----------------------
# O backend executa a inferência chamando o Python do projeto "ia"
# (fora do container). Configure via env quando necessário.

IA_DIR = Path(os.getenv("IA_DIR", str(BASE_DIR.parent / "ia")))

IA_PYTHON = os.getenv(
    "IA_PYTHON",
    str(Path(IA_DIR) / ".venv" / "Scripts" / "python.exe"),
)

IA_MODELO_PADRAO = os.getenv(
    "IA_MODELO_PADRAO",
    "runs/detect/abacaxi_tomate/weights/best.pt",
)

IA_SAMPLES = Path(
    os.getenv("IA_SAMPLES", str(BASE_DIR / "static" / "ia" / "samples"))
)

# ----------------------- Jazzmin (Admin) -----------------------

JAZZMIN_SETTINGS = {
    "site_title": "Iron | Inspeção Industrial",
    "site_header": "Iron Sistema de Inspeção",
    "site_brand": "IRON",
    "welcome_sign": "Bem-vindo ao Iron Sistema de Inspeção",
    "copyright": "Iron Sistemas",
    "search_model": ["auth.User", "tenants.Empresa", "produtos.Produto"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "tenants.Empresa": "fas fa-building",
        "tenants.MembroEmpresa": "fas fa-user-tag",
        "produtos": "fas fa-boxes",
        "produtos.Produto": "fas fa-box",
        "configuracao": "fas fa-cogs",
        "configuracao.Linha": "fas fa-industry",
        "configuracao.Camera": "fas fa-video",
        "configuracao.Workflow": "fas fa-project-diagram",
        "configuracao.Etapa": "fas fa-list-ol",
        "ia": "fas fa-brain",
        "ia.ModeloIA": "fas fa-robot",
        "inspecoes": "fas fa-search",
        "inspecoes.Inspecao": "fas fa-search-plus",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-cube",
    "topmenu_links": [
        {"name": "Início", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Abrir o Sistema", "url": "/", "new_window": False},
        {"app": "produtos"},
        {"app": "configuracao"},
        {"app": "ia"},
        {"app": "inspecoes"},
        {"app": "tenants"},
    ],
    "custom_css": "admin/css/iron.css",
    "custom_js": "admin/js/iron.js",
    "show_ui_builder": False,
    "related_modal_active": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "superhero",
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-secondary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "default_theme_mode": "dark",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
}

CACHES = {
    "default": {

        "BACKEND": "django_redis.cache.RedisCache",

        "LOCATION": f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/1",

        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },

    }

}

DATABASE_ROUTERS = [
    "core.routers.TenantRouter"
]