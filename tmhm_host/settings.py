"""
Django settings for OnlineLearning project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
#hello

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
'''
# By Vijay
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR=os.path.join(BASE_DIR,'templates')
STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
# endvijay
#AUTH_USER_EMAIL_UNIQUE = True
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5w^7@844)#j4!=w*8_sd_mr(0!q42n3@3@)gab91r!opc32t^9'

# SECURITY WARNING: don't run with debug turned on in production!

#production
# DEBUG = False
# ALLOWED_HOSTS = ['www.learnopad.com', 'learnopad.com', '68.183.81.120', '139.59.42.126', '127.0.0.1']

#Development
DEBUG = True
ALLOWED_HOSTS = ['128.199.219.129', '127.0.0.1','139.59.42.126']

# Application definition

INSTALLED_APPS = [
    # By vijay
    'admin_interface',
    'colorfield',
    # endVijay
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Admin',
    'LandingPage',
    'facilitators',
    'learners',
    'campus',
    'corporates',
    #'django.contrib.sites',
    # By vijay
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    'widget_tweaks',
    'myauth',
    'channels',
    'rest_framework',
    'payment_gateway',
    'mailing',
    # endVijay
    'chat',
    #amir
    'wkhtmltopdf',
]
# for go
# By vijay
# SITE_ID = 1
# LOGIN_REDIRECT_URL = '/'
X_FRAME_OPTIONS = 'SAMEORIGIN'

# endvijay

# REST_FRAMEWORK = {
#    'DEFAULT_AUTHENTICATION_CLASSES': (
#               'rest_framework.authentication.TokenAuthentication',
#    ),
#    'DEFAULT_PERMISSION_CLASSES':(
#                'rest_framework.permissions.IsAuthenticated',
#     ),

# }
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chat.middileware.RequestMiddleware'

    
]

ROOT_URLCONF = 'tmhm_host.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'LandingPage.context_processors.base',
            ],
        },
    },
]

WSGI_APPLICATION = 'tmhm_host.wsgi.application'
ASGI_APPLICATION = "tmhm_host.routing.application"

# By vijay
''' for google authentication integration '''
# AUTHENTICATION_BACKENDS = [
    
#     # Needed to login by username in Django admin, regardless of `allauth`
#     'django.contrib.auth.backends.ModelBackend',

#     # `allauth` specific authentication methods, such as login by e-mail
#     'allauth.account.auth_backends.AuthenticationBackend',

# ]
# endVijay


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases



DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
  }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': 'learnopad',
#             'USER': 'learnopad_admin',
#             'PASSWORD': 'learnopad@tmhmdocean#2020adv',
#             'HOST': 'localhost',
#             'PORT': '',
#         }
#     }



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'asgi_redis.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [('localhost', 6379)],
#         }
#     }
# }
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
   }
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'myauth.CustomUser'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATIC_TMP = os.path.join(BASE_DIR, 'static')
#STATIC_URL = '/static/'
#STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# managing media files
#MEDIA_URL = '/media/'

#os.makedirs(STATIC_TMP, exist_ok=True)
#os.makedirs(STATIC_ROOT, exist_ok=True)



# By Vijay
#STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media/')
#MEDIA_URL = '/media/'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR, 'static'),]
#MEDIA_URL='/img/'
#MEDIA_ROOT = os.path.join(BASE_DIR,'media')
#django_heroku.settings(locals())


#By vijay
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'learnopad@gmail.com'
EMAIL_HOST_PASSWORD = 'learnOpad@2020'

