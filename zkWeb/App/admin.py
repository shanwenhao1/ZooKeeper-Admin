#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10
# @Author  : Wenhao Shan
# Desc     : The ZK Admin Part, Handle The User And zkNode distribution, 详细:
#            http://djangobook.py3k.cn/2.0/chapter10/

from django.contrib import admin
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User as DUser
from zkWeb.App.models import User, UserNode, Node
from zkControl.control import create_node, delete_node

admin.site.site_header = "ZooKeeper管理后台"
admin.site.site_title = "ZK管理"


class UserNodeInline(admin.TabularInline):
    """
    根据用户管理节点信息记录(要求删除用户时, 所有与该用户相关的UserNode表记录都要删除掉)
    """
    model = UserNode
    # search_fields = ("user", )
    list_display = ("node", )
    list_filter = ("user", )

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     url_path_dict = parse_url_path(request.path)
    #     if db_field.name == "user":
    #         kwargs['queryset'] = UserNode.objects.select_related("user").filter(user_id=url_path_dict[-2])
    #         return super(UserNodeInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    #     else:
    #         return db_field.formfield(**kwargs)


class UserAdmin(admin.ModelAdmin):
    """
    用户注册信息表
    """
    inlines = [UserNodeInline]
    list_display = ("user_id", "user_name", "password", "email")        # 需要显示的字段
    search_fields = ("user_id", "user_name")                            # 页面添加查询栏
    # list_filter = ()                                                  # 过滤

    # exclude = ("user_id", )                                           # 排除掉哪些字段可以编辑, 与fields功能相反
    fields = ("user_name", "password", "email", "sex")

    # 重载create, 添加注册django user表数据
    def save_model(self, request, obj, form, change):
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        obj.save()
        # Django新建用户
        user = DUser.objects.filter(username=user_name)
        if not user:
            DUser.objects.create_user(username=user_name, password=password, email=email)
        else:
            user = user[0]
            if not check_password(password, user.password) or user.email != email:
                # 密码存入的是hash加密后的
                user.password = make_password(password)
                user.email = email
                user.save()

    # 重载delete, 添加删除django user表数据
    def delete_model(self, request, obj):
        user_name = obj.user_name
        obj.delete()
        if DUser.objects.filter(username=user_name):
            DUser.objects.get(username=user_name).delete()


class NodeUserInline(admin.TabularInline):
    """
    根据节点管理节点信息记录(要求删除节点时, 所有与该节点相关的UserNode表记录都要删除掉)
    """
    model = UserNode
    search_fields = ("node", )
    list_display = ("user",)


class NodeAdmin(admin.ModelAdmin):
    # 将UserNode内嵌至Node管理
    inlines = [NodeUserInline]
    list_display = ("node_id", "node_path", "node_name", )
    search_fields = ("node_id", "node_name")
    fields = ("node_path", "node_name",)

    # 重载save, 添加创建zk_node
    def save_model(self, request, obj, form, change):
        node_path = request.POST.get("node_path")
        is_create = True if not Node.objects.filter(node_path=node_path) else False
        obj.save()
        if is_create:
            create_node(node_path)

    # 重载delete, 添加删除zk_node
    def delete_model(self, request, obj):
        node_path = obj.node_path
        obj.delete()
        delete_node(node_path)


admin.site.register(User, UserAdmin)
admin.site.register(Node, NodeAdmin)
