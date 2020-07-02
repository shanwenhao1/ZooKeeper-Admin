#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/03/15
# @Author  : Wenhao Shan

import hashlib
from utils.time_utils import get_now_time_timestamp


def generate_md5(text: str):
    """
    generate md5
    :param text: str that you want to generate md5
    :return:
    """
    str_md5 = hashlib.md5()
    str_md5.update(text.encode("utf-8"))
    return str_md5.hexdigest()


def md5_check(secret_key: str, timestamp: float):
    """
    generate md5 according to timestamp and SecretKey
    :param secret_key:
    :param timestamp:
    :return:
    """
    return generate_md5(secret_key + str(timestamp))


def md5_check_in_time(md5: str, secret_key: str, timestamp: int):
    """
    check md5 with timestamp in limit time
    :param md5:
    :param secret_key:
    :param timestamp:
    :return:
    """
    # server timestamp(UTC)
    now_timestamp = get_now_time_timestamp(utc=True)
    diff_time = now_timestamp - timestamp
    if diff_time > 600 or diff_time < -600:
        return False
    if md5 != md5_check(secret_key, timestamp):
        return False
    return True
