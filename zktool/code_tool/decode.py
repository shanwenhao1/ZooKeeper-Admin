#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/11
# @Author  : Wenhao Shan

import json
import log
from utils.error import ActionError
from zktool.enum.log_enum import Code


def de_json(data: b""):
    """
    将b""型数据解码成json(dict)
    :param data:
    :return:
    """
    if data == b"":
        return dict()
    decode_data = data.decode("utf-8")
    try:
        data_json = json.loads(decode_data)
    except Exception as e:
        log.tag_error(Code.DeCode, str(e))
        raise ActionError("node data is not json type")
    return data_json
