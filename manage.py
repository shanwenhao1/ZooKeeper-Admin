#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10
# @Author  : Wenhao Shan
# Desc     : The ZK Admin main function

import os
import sys

HOST = "localhost:8081"


def run():
    """
    web main run
    :return:
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zkWeb.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHON PATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    default_cfg = ["manage.py", "runserver", HOST]
    # 如果是命令行启动未输入启动参数, 则使用默认参数
    execute_from_command_line(sys.argv if len(sys.argv) > 1 else default_cfg)      # sys.argv


if __name__ == '__main__':
    run()
