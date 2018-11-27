#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/16
# @Author  : Wenhao Shan
# Desc     : tag and filter handle, 使用方法是在模板中写入 {% load poll_extras %}

import re
from django import template
from utils.time_utils import get_now_time

register = template.Library()


@register.tag(name="current_time")
def do_current_time(parser, token):
    """
    register使用示例函数
    :param parser:
    :param token:
    :return:
    """
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        msg = '%r tag requires arguments' % token.contents[0]
        raise template.TemplateSyntaxError(msg)

    m = re.search(r'(.*?) as (\w+)', arg)
    if m:
        fmt, var_name = m.groups()
    else:
        msg = '%r tag had invalid arguments' % tag_name
        raise template.TemplateSyntaxError(msg)

    if not (fmt[0] == fmt[-1] and fmt[0] in ('"', "'")):
        msg = "%r tag's argument should be in quotes" % tag_name
        raise template.TemplateSyntaxError(msg)

    return CurrentTimeNode3(fmt[1:-1], var_name)


class CurrentTimeNode3(template.Node):
    def __init__(self, format_string, var_name):
        self.format_string = str(format_string)
        self.var_name = var_name

    def render(self, context):
        now = get_now_time()
        context[self.var_name] = now.strftime(self.format_string)
        return ''
