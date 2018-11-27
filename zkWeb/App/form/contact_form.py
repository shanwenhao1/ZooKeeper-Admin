#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/12
# @Author  : Wenhao Shan
# DESC: Form模块并未使用

from django import forms
from zkWeb.App.models import Contact


class ContactForm(forms.Form):
    full_name = forms.CharField(required=False)  # 表明full_name不是必须要填写的
    email = forms.EmailField()
    message = forms.CharField()


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        '''email_base,provider=email.split("@")
        domain,extension=provider.split('.')
        if not extension=="USC":#如果email中没有.edu则提示邮件地址输入错误
            raise forms.ValidationError("Please make sure you use your USC email.")
        if not extension=="edu":#如果email中没有.edu则提示邮件地址输入错误
            raise forms.ValidationError("Please use a valid .EDU email address!!")'''
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        return full_name
