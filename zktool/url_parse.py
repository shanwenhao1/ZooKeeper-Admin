#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15
# @Author  : Wenhao Shan

import re
from urllib.parse import urlparse
import urllib.request


def parse_url_path(url: str):
    """
    解析url路径
    :param url: 示例: /admin/App/user/477a5c80-ce9b-11e8-a50e-b8975a37456b/change/
    :return:
    """
    url = url.strip()
    url = url.strip("/")
    path_dict = url.split("/")
    return path_dict
