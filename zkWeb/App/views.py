#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15
# @Author  : Wenhao Shan
# Desc     : App application handle function

import log
import json
from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as DUser
from utils.error import ActionError
from utils.word_check import pass_word_check
from utils.md5 import md5_check_in_time
from zktool.err_handle import action_err
from zktool.enum.log_enum import DjangoStatus, DbStatus
from zktool.enum.web_enum import WebErr, WebReq, WebResp
from zkWeb.App.models import User
from zkWeb.App.form.contact_form import ContactForm
from zkWeb.settings import EMAIL_HOST_USER
from zkWeb.App.app_tool.node_tool import get_person_all_node, modify_node, delete_node, verify_node_by_path, get_node_by_path

# 只有templates文件夹配置在settings.py中, get_template才能获取到相应的html.


def home(request):
    """
    Home页面处理函数
    :param request:
    :return:
    """
    return render(request, "home.html")


def about(request):
    """
    about us 页面处理函数
    :param request:
    :return:
    """
    return render(request, "about.html")


def contact(request):
    """
    联系我们处理函数
    :param request:
    :return:
    """
    title = "Contact Us"
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        '''for Key,value in form.cleaned_data.iteritems():
            print(Key,value)'''
        for Key in form.cleaned_data:  # 输出所有在form中的数据
            print(Key, ":", form.cleaned_data.get(Key))
        # 注册时发送邮件同时在settings那有设置邮箱
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        subject = 'Site contact form'
        from_email = EMAIL_HOST_USER
        to_email = [form_email, 'swh-email@qq.com ']
        contact_message = "User: %s, Message: %s. \n Email: via %s" % (
            form_full_name,
            form_message,
            form_email)
        some_html_message = "<h1>Hello, %s</h1>" % contact_message
        mail_error = send_mail(subject,
                               contact_message,
                               from_email,
                               to_email,
                               html_message=some_html_message,
                               fail_silently=True)  # 设置是否可以发送邮件
        if mail_error != 1:
            log.tag_error("Mail Error", "Contact Send Mail Error, user: %s, email: %s, message: %s!!!" %
                          (form_full_name, form_email, form_message))
    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }
    return render(request, "contact.html", context)


def doc(request):
    """
    文档
    :param request:
    :return:
    """
    context = dict()
    return render(request, "doc.html", context)


def login_zk(request):
    """
    登录
    :param request:
    :return:
    """
    context = dict()
    context["Check"] = ""
    if request.method == "GET":
        return render(request, "login.html", context)
    if request.method != "POST":
        raise Http404(WebErr.PostErr)

    user_name = request.POST.get("user_name")
    password = request.POST.get("password")
    user = authenticate(username=user_name, password=password)
    if user is not None and user.is_active:
        context["Check"] = "Login success"
        login(request, user)
    else:
        context["Check"] = "Password Error!!"
    response = render(request, "login.html", context)
    # response.set_cookie('cookie', new_uuid())
    return response


def logout_zk(request):
    """
    登出
    :param request:
    :return:
    """
    logout(request)
    return render(request, "home.html")


@transaction.atomic
def register(request):
    """
    注册模块
    :param request:
    :return:
    """
    context = dict()
    if request.method == "GET":
        return render(request, "register.html", context)
    if request.method != "POST":
        raise Http404(WebErr.PostErr)

    user_name = request.POST.get("user_name")
    password = request.POST.get("password")
    email = request.POST.get("email")
    sex = request.POST.get("sex")

    # 查询记录是否存在, 不存在则返回None
    already_user = User.objects.filter(user_name=user_name).first()
    if already_user:
        information = "该用户已注册"
        context["errMsg"] = information
        return render(request, "register.html", context)

    # 校验密码格式
    if not pass_word_check(password):
        information = "密码格式错误!!!"
        context["errMsg"] = information
        return render(request, "register.html", context)

    # 新建用户
    try:
        # 我的表注册
        user = User.objects.create(user_name=user_name, password=password, email=email, sex=sex)
        information = "注册成功, 欢迎: " + user_name
        context["errMsg"] = information
    except Exception:
        log.tag_error(DjangoStatus.Register, "%s Register Failed, Create User error" % user_name)
        information = "注册失败"
        context["errMsg"] = information
        return render(request, "register.html", context)
    # Django注册
    register_add = DUser.objects.create_user(username=user_name, password=password, email=email)
    if not register_add:
        information = "注册失败"
        context["errMsg"] = information
        log.tag_error(DjangoStatus.Register, "%s Register Failed, delete data" % user_name)
        # 删除我的表数据
        User.objects.delelet(user_id=user.user_id)
    # 注册成功则登录
    auth_user = authenticate(username=user_name, password=password)
    login(request, auth_user)
    log.tag_info(DjangoStatus.Register, "%s Register succeed!" % user_name)

    return render(request, "register.html", context)


@transaction.atomic
def zk(request):
    """
    zk控制台
    :param request:
    :return:
    """
    context = dict()
    if not request.user.is_authenticated:
        raise Http404("Please Login in first")
    if request.method == "GET":
        user_name = request.user
        try:
            all_node_info = get_person_all_node(user_name)
            context["nodeInfo"] = all_node_info
        except ActionError as e:
            context["errMsg"] = e.__str__()
        return render(request, "zk.html", context)
    if request.method != "POST":
        raise Http404(WebErr.PostErr)
    data = json.loads(request.body.decode())
    # 修改节点
    user_name = request.user
    if data['action'] == WebReq.ModifyAct:
        modify_node(user_name, data["nodeId"], data["nodeData"])
    elif data['action'] == WebReq.DeleteAct:
        delete_node(user_name, data["nodeId"])
    context["status"] = WebResp.ActionSuccess
    context["errMsg"] = ""
    # context["nodeInfo"] = new_node_info
    # 返回采用http返回格式, 方便js解析(判断请求是否成功)
    return HttpResponse(json.dumps(context))


# TODO 将zkAdmin 与查询zk服务分离, zkAdmin只允许内网访问(或者设置白名单)
@action_err
def zk_info(request):
    """
    获取zk节点信息
    :param request:
    :return:
    """
    context = dict()
    try:
        user_name = request.POST.get('username')
        # password + timestamp 生成的md5校验
        md5 = request.POST.get('md5')
        timestamp = request.POST.get("timestamp")
        zk_name = request.POST.get('zkName')
    except:
        raise ActionError("parameter error")
    if type(timestamp) is not str and type(timestamp) is not float:
        raise ActionError("parameter error")

    user = User.objects.filter(user_name=user_name).first()
    if not user:
        log.tag_info(DbStatus.Inquire, "User: %s not Exist In table user" % user_name)
        raise ActionError("User not exist")
    if type(timestamp) is str:
        timestamp = float(timestamp)
    if not md5_check_in_time(md5, user.password, int(timestamp)):
        raise ActionError("MD5校验失败")
    # 验证node是否属于该用户
    zk_path = verify_node_by_path(user, zk_name)
    # 获取zk节点信息
    zk_node = get_node_by_path(zk_path)
    context["obj"] = zk_node
    context["status"] = WebResp.ActionSuccess
    context["errMsg"] = ""
    return HttpResponse(json.dumps(context))
