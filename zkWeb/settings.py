#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10
# @Author  : Wenhao Shan

"""
Django settings for zkWeb project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
import platform

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vunfukbfdor=ivuth93fr*m#-vg-xj%ftft!ql(4=#b5wpi6s_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["192.168.1.89", "localhost"]

# 设置邮箱地址
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'test@gmail.com'
# EMAIL_HOST_PASSWORD = '******'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.qq.com'
EMAIL_HOST_USER = 'swh-email@qq.com '
EMAIL_HOST_PASSWORD = 'ufjvyzgaatgzbahe'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',                                             # 此为我添加的third party apps
    # 'django.contrib.sites',                                     # django登录相关, https://stackoverflow.com/questions/9736975/django-admin-doesnotexist-at-admin
    # 'zkWeb.template_app.Templates.registration',              # 注册登录相关的html文件
    'zkWeb.App',
    'zkWeb.template_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',            # 添加该项设置浏览器语言, 该项必须在SessionMiddleware之后
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# session设置
SESSION_COOKIE_AGE = 60 * 30    # 30分钟
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览, 则cookie失效


ROOT_URLCONF = 'zkWeb.urls'

# HTML模板绝对路径
tem_path = os.path.join(BASE_DIR, "zkWeb", "template_app", "Templates")
tem_path_sys = os.path.join(tem_path, "registration")

tem_path_c = tem_path.replace("/", "\\") if platform.architecture()[1].rfind("Windows") == 0 else tem_path
tem_path_sys_c = tem_path_sys.replace("/", "\\") if platform.architecture()[1].rfind("Windows") == 0 else tem_path_sys

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [tem_path_c, tem_path_sys_c],
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

WSGI_APPLICATION = 'zkWeb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kw_zk',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.1.89',
        'PORT': '3306',
        # 测试数据库默认编码格式为utf8
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    }
}

# 测试所用
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "zkWeb", "template_app", "Templates", "statics_env", "static_root")
STATICFILES_DIRS = [
    # statics下的my_static为自己的css目录, static_root为第三方模板css(内包含video js等)
    # os.path.join(BASE_DIR, "zkWeb", "template_app", "Templates", "statics", "my_static"),
    # os.path.join(BASE_DIR, "zkWeb", "template_app", "Templates", "statics_env", "static_root"),
    os.path.join(BASE_DIR, "zkWeb", "template_app", "Templates", "statics")
]
STATIC_PATH = '/static/'
