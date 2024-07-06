"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.0.33', '*']
INTERNAL_IPS = [    #for django toolbar
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'social_django',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'mptt',
    'myauth',
    'main',
    'taggit',
    # 'django_ckeditor_5',
    'ckeditor',
    'ckeditor_uploader',
    'django_cleanup.apps.CleanupConfig',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'blog.urls'

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

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog',
        'USER': 'igor',
        'PASSWORD': 'igor',
        'HOST': '127.0.0.1',
        'PORT': '5433',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
# STATIC_ROOT = (BASE_DIR / 'static')

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'myauth.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# social auth configs for google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = str(os.getenv('GOOGLE_KEY'))
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = str(os.getenv('GOOGLE_SECRET'))


# Конфигурация сервера электронной почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kampaiski@gmail.com'
EMAIL_HOST_PASSWORD = 'quvy bmmy vxff obde '
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SITE_ID = 1

customColorPalette = [

    {

        'color': 'hsl(4, 90%, 58%)',

        'label': 'Red'

    },

    {

        'color': 'hsl(340, 82%, 52%)',

        'label': 'Pink'

    },

    {

        'color': 'hsl(291, 64%, 42%)',

        'label': 'Purple'

    },

    {

        'color': 'hsl(262, 52%, 47%)',

        'label': 'Deep Purple'

    },

    {

        'color': 'hsl(231, 48%, 48%)',

        'label': 'Indigo'

    },

    {

        'color': 'hsl(207, 90%, 54%)',

        'label': 'Blue'

    },

]

# CKEDITOR_5_CUSTOM_CSS = 'path_to.css'  # optional

# CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage"  # optional
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'min': {
        'toolbar': [
            ['Undo', 'Redo',
             '-', 'Bold', 'Italic', 'Underline',
             '-', 'Link', 'Unlink', 'Anchor',
             '-', 'Format',
             '-', 'Maximize',
             '-', 'Table',
             '-', 'Image',
             '-', 'Source',
             '-', 'NumberedList', 'BulletedList'
            ],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
             '-', 'Font', 'FontSize', 'TextColor',
             '-', 'Outdent', 'Indent',
             '-', 'HorizontalRule',
             '-', 'Blockquote'
            ]
        ],
        'height': 500,
        'width': '100%',
        'toolbarCanCollapse': False,
        'forcePasteAsPlainText': True
    }
}
CKEDITOR_5_CONFIGS = {

    'default': {

        'toolbar': ['heading', '|', 'bold', 'italic', 'link',

                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

    },
    'awesome_ckeditor': {
        'toolbar': 'full',
        'height': 300,
    },

    'extends': {

        'blockToolbar': [

            'paragraph', 'heading1', 'heading2', 'heading3',

            '|',

            'bulletedList', 'numberedList',

            '|',

            'blockQuote',

        ],

        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',

                    'code', 'subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',

                    'bulletedList', 'numberedList', 'todoList', '|', 'blockQuote', 'imageUpload', '|',

                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',

                    'insertTable', ],

        'image': {

            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',

                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side', '|'],

            'styles': [

                'full',

                'side',

                'alignLeft',

                'alignRight',

                'alignCenter',

            ]

        },

        'table': {

            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells',

                               'tableProperties', 'tableCellProperties'],

            'tableProperties': {

                'borderColors': customColorPalette,

                'backgroundColors': customColorPalette

            },

            'tableCellProperties': {

                'borderColors': customColorPalette,

                'backgroundColors': customColorPalette

            }

        },

        'heading': {

            'options': [

                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},

                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},

                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},

                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}

            ]

        }

    },

    'list': {

        'properties': {

            'styles': 'true',

            'startIndex': 'true',

            'reversed': 'true',

        }

    }

}
