#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/23
# @Author  : Wenhao Shan

from utils.enum import Enum

WebErr = Enum(
    PostErr="Only POST Request allowed",
)


WebResp = Enum(
    ActionErr=1,
    ActionSuccess=0,
)

WebReq = Enum(
    ModifyAct="Modify",
    DeleteAct="Delete",
)
