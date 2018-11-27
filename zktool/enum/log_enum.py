#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10
# @Author  : Wenhao Shan

from utils.enum import Enum

# zk连接状态标签
KazooStatus = Enum(
    Lost="Kazoo Session Lost",
    Suspended="Kazoo Not Connected",
    Conn="Kazoo Connected",
    ConnFailed="Kazoo Connected Failed"
)

# zk操作日志标签
ZkControlStatus = Enum(
    Create="Create Node",
    Get="Inquire Node",
    Update="Update Node",
    Delete="Delete Node",
)


Code = Enum(
    EnCode="En_Code Error",
    DeCode="De_Code Error",
)


# Django User Register
DjangoStatus = Enum(
    Register="Zk Register",
    Login="Zk Login",
)

DbStatus = Enum(
    Inquire="DB Inquire Error",
    Create="DB Create Error",
    Update="DB Update Error",
    Delete="DB Delete Error"
)
