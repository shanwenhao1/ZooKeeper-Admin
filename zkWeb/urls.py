#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10
# @Author  : Wenhao Shan
# Desc     : The ZK Admin App Route Register Position
"""zkWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from zkWeb.App.views import home, register, about, contact, login_zk, logout_zk, zk, zk_info, doc
from zkWeb.App.admin import admin

admin.autodiscover()


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'login/', login_zk, name='auth_login'),
    path(r'logout/', logout_zk, name='auth_logout'),
    path(r'register/', register, name='auth_register'),

    path(r'', home, name='/'),
    path(r'home/', home, name='home'),
    path(r'about/', about, name='about'),
    path(r'contact/', contact, name='contact'),
    path(r'doc/', doc, name='doc'),
    path(r'zk/', zk, name="zk"),
    # post请求获取节点信息, 目前使用明文密码, 后续考虑使用md5加密
    path(r'zk_node/', zk_info, name="zk_node"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
