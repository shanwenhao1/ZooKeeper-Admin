#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/03/15
# @Author  : Wenhao Shan
# @Dsec    : Wraps of raise ActionError, to handle the exception on the server running

import json
from functools import wraps
from django.http import HttpResponse
from utils.error import ActionError
from zktool.enum.web_enum import WebErr, WebReq, WebResp


def action_err(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except ActionError as e:
            res = {
                "status": WebResp.ActionErr,
                "errMsg": e.__str__(),
                "obj": {}
            }
            return HttpResponse(json.dumps(res))
    return wrapper
