#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/11
# @Author  : Wenhao Shan

from utils.enum import Enum

KazooMsg = Enum(
    Node_Exist="Node Exist",
    Node_Not_Exist="Node Not Exist",
    Create_Failed="Create Node Failed",
    Get_Failed="Inquire Node Failed",
    Update_Failed="Update Node Failed",
    Delete_Failed="Delete Node Failed",
    Get_Children_Failed="Get Children List Of Given Node Failed",
)
