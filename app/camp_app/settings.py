"""
Django settings for camp_app project.

Generated by 'django-admin startproject' using Django 3.1.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
def value_from_env(key, default=None):
    """
    Return a env variable, raising an exception if it is not defined
    """
    value = os.environ.get(key, default)
    if value is None:
        error_msg = (
            "No '%s' env variable found. This needs to be set in the Admin GUI deployment"
        )
        raise RuntimeError(error_msg % key)
    return value


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = value_from_env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = value_from_env("DEBUG", False) == "True"

ALLOWED_HOSTS = value_from_env("ALLOWED_HOSTS", [])

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    #'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'camper',
    'django.contrib.sites',
    'cms',
    'menus',
    'treebeard',
    'sekizai',
    'filer',
    'easy_thumbnails',
    'mptt',
    'djangocms_text_ckeditor',
    'djangocms_link',
    'djangocms_file',
    'djangocms_picture',
    'djangocms_video',
    'djangocms_googlemap',
    'djangocms_snippet',
    'djangocms_style',
    'djangocms_icon',
    'djangocms_bootstrap4',
    'djangocms_bootstrap4.contrib.bootstrap4_alerts',
    'djangocms_bootstrap4.contrib.bootstrap4_badge',
    'djangocms_bootstrap4.contrib.bootstrap4_card',
    'djangocms_bootstrap4.contrib.bootstrap4_carousel',
    'djangocms_bootstrap4.contrib.bootstrap4_collapse',
    'djangocms_bootstrap4.contrib.bootstrap4_content',
    'djangocms_bootstrap4.contrib.bootstrap4_grid',
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron',
    'djangocms_bootstrap4.contrib.bootstrap4_link',
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup',
    'djangocms_bootstrap4.contrib.bootstrap4_media',
    'djangocms_bootstrap4.contrib.bootstrap4_picture',
    'djangocms_bootstrap4.contrib.bootstrap4_tabs',
    'djangocms_bootstrap4.contrib.bootstrap4_utilities',
    'nested_inline',
    'gallery',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
]

ROOT_URLCONF = 'camp_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'camp_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config("DATABASE_ENGINE", default='django.db.backends.sqlite3'),
        "NAME": config("DATABASE_NAME", default=BASE_DIR / 'db.sqlite3'),
        "USER": config("DATABASE_USERNAME", default='user'),
        "PASSWORD": config("DATABASE_PASSWORD", default='password'),
        "HOST": config("DATABASE_HOST", default='localhost'),
        "PORT": config("DATABASE_PORT", default=5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'sk'

TIME_ZONE = 'Europe/Bratislava'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_DIR = os.path.join(BASE_DIR, 'staticfiles')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    STATIC_DIR,
)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "camper": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        }
    }
}

LANGUAGES = [
    ('sk', _('Slovak')),
    # ('en-us', _('English')),
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

CMS_TEMPLATES = [
    # ('home.html', 'Home page template'),
    # ('base.html', 'Base'),
    ('tabor.html', 'Home'),
    ('accounts/register_child.html', 'Register'),
    # ('menu.html', 'Menu'),
    # ('page.html', 'Page')

]

GALLERY_LOGO_PATH = ""
GALLERY_TITLE = "Galéria"
GALLERY_FOOTER_INFO = ""
GALLERY_FOOTER_EMAIL = ""
GALLERY_IMAGE_MARGIN = 20

EMAIL_HOST = config("EMAIL_HOST", default="secret")
EMAIL_PORT = config("EMAIL_PORT", default=25, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="secret")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="secret")
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=False, cast=bool)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_ENABLED = config("EMAIL_ENABLED", default=False, cast=bool)
PAGE_DOMAIN = config("PAGE_DOMAIN", default="https://test.farapd.sk")

THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)


TEXT_ADDITIONAL_ATTRIBUTES = ('onclick', )

VALID_REGISTRATION = config("VALID_REGISTRATION", default="tabor2022")
ADVANCE_PMT_DUE = config("ADVANCE_PMT_DUE", default=14, cast=int)
VALID_IBAN = config("VALID_IBAN", default="SK31 8330 0000 0024 0188 0167")
