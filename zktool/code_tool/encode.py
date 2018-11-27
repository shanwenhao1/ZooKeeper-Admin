#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/11
# @Author  : Wenhao Shan

import json


def en_json(data: dict):
    """
    将json(dict)型数据, 编码成b""
    :param data:
    :return:
    """
    str_json = json.dumps(data)
    return str_json.encode("utf-8")
