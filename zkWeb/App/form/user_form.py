#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/12
# @Author  : Wenhao Shan
# DESC: Form模块并未使用

from django import forms
from zkWeb.App.models import User, UserNode


class NodeAdminForm(forms.Form):
    """
    """


class AddUserForm(forms.ModelForm):
    """
    添加zk新用户
    """
    class Meta:
        user_model = User
        user_node_model = UserNode
        fields = ("user_name", "password", "email", "node_path", "node_name")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': ' form-control'}),
            'node_path': forms.TextInput(attrs={'class': 'form-control'}),
            'node_name': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields["user_name"].label = "user_name"
        self.fields["user_name"].error_messages = {"required": u"请输入用户名"}
        self.fields["password"].label = "password"
        self.fields["password"].error_messages = {"required": u"请输入密码"}
        self.fields["email"].label = u"email"
        self.fields["email"].error_messages = {"required": u"请输入邮箱"}
        self.fields["node_path"].label = u"node_path"
        self.fields["node_path"].error_messages = {"required": u"请输入初始ZK分配节点"}
        self.fields["node_name"].label = u"node_name"
        self.fields["node_name"].error_messages = {"required": u"请输入节点名称"}

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6:
            raise forms.ValidationError(u"密码必须大于6位")
        return password
