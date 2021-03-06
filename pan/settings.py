"""
Django settings for pan project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
from django.urls import reverse_lazy, reverse
from django.shortcuts import HttpResponseRedirect
import pymysql

pymysql.install_as_MySQLdb()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g#wk6asv0nngjph%400x(tmdsha(f@gx$*!u=i^^#7843(l57j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',
                 '120.24.161.98']

# Application definition

INSTALLED_APPS = [
    'users',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'livingcost',
    'asset',
    'article',
    'money',
    'guardian',
    'document',
    'chartit',  # 图表功能
    'sorl.thumbnail',  # 缩略图功能
    'django_forms_bootstrap',  # 表单bootstrap美化
    'taggit',  # tag功能
    'markdownx',  # markdown 实时预览图
]

AUTH_USER_MODEL = 'users.UserProfile'

AUTHENTICATION_BACKENDS = (
    'users.views.CustomAuthBackend',
    'guardian.backends.ObjectPermissionBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'pan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pan.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         }
#     }
# else:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')},
    # 'mysql': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'USER': 'pan',
    #     'PASSWORD': 'qqq456777',
    #     'NAME': 'test',
    #     'HOST': '120.24.161.98',
    #     'PORT': '3306',
    # }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = reverse_lazy('index')

'''
第三方库的设置
'''
THUMBNAIL_DEBUG = True

TAGGIT_CASE_INSENSITIVE = True
TAGGIT_FORCE_LOWERCASE = True
