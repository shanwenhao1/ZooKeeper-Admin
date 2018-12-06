#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/20
# @Author  : Wenhao Shan

import log
from copy import deepcopy
from utils.error import ActionError
from zkWeb.App.models import User, UserNode, Node
from zkControl.control import get_node, update_node
from zktool.code_tool.decode import de_json
from zktool.code_tool.encode import en_json
from zktool.enum.log_enum import DbStatus


def get_node_by_path(node_path: str):
    """
    根据node_path获取节点存储信息
    :param node_path:
    :return:
    """
    try:
        node_info = de_json(get_node(node_path))
    except:
        # # TODO 解决不识别bool类型
        # node_info = {
        #     "Error": "没有该节点信息",
        #     "test": "test",
        #     "num": 1111,
        #     "another": {
        #         "test1": "11222",
        #         "other": {
        #             "szg": 13434
        #         }
        #     }
        # }
        raise ActionError("Get node info error")
    return node_info


def get_person_all_node(username: str):
    """
    获取个人所有节点信息
    :param username:
    :return:
    """
    all_node_info = list()
    # 获取唯一的user_id
    user = User.objects.filter(user_name=username).first()
    if not user:
        log.tag_error(DbStatus.Inquire, "User: %s not Exist In table user" % username)
        raise ActionError("User error")
    user_id = user.user_id
    all_node = UserNode.objects.filter(user_id=user_id).all()
    # 没有数据
    if len(all_node) == 0:
        return all_node_info
    node_id_list = [node.node_id for node in all_node]
    node_info = Node.objects.filter(node_id__in=node_id_list).all()
    node_single = dict()
    for node in node_info:
        node_single["nodeId"] = node.node_id
        node_single["nodeName"] = node.node_name
        node_single["nodePath"] = node.node_path
        node_single["nodeInfo"] = get_node_by_path(node.node_path)
        all_node_info.append(deepcopy(node_single))
    return all_node_info


def verify_node(user_name: str, node_id: str):
    """
    验证节点归属并返回节点记录
    :param user_name:
    :param node_id:
    :return:
    """
    # 验证node归属
    user = User.objects.filter(user_name=user_name).first()
    if not user:
        log.tag_error(DbStatus.Inquire, "User: %s not Exist In table user" % user_name)
        raise ActionError("User error")
    user_id = user.user_id
    all_node = UserNode.objects.filter(user_id=user_id).all()
    node_id_list = [node.node_id for node in all_node]
    if node_id not in node_id_list:
        raise ActionError("The node: %s is not belongs to user: %s" % (node_id, user_name))
    # 获取node_path
    node_record = Node.objects.get(node_id=node_id)
    return node_record


def verify_node_by_path(user_name: str, password: str, node_path: str):
    """
    根据user_name和node_path判断用户是否具有对应节点权限
    :param user_name:
    :param password:
    :param node_path:
    :return:
    """
    user = User.objects.filter(user_name=user_name).first()
    if not user:
        log.tag_info(DbStatus.Inquire, "User: %s not Exist In table user" % user_name)
        raise ActionError("User not exist")
    if user.password != password:
        raise ActionError("password error")
    user_id = user.user_id
    node = Node.objects.filter(node_path=node_path).first()
    if not node:
        raise ActionError("Node Path Not Exist")
    node_id = node.node_id
    all_user_node = UserNode.objects.filter(user_id=user_id).all()
    all_node_id = [user_node.node_id for user_node in all_user_node]
    if node_id not in all_node_id:
        raise ActionError("Node not belongs to user")
    return True


def modify_node(user_name: str, node_id: str, node_info: dict):
    """
    修改节点信息
    :param user_name:
    :param node_id:
    :param node_info:
    :return:
    """
    # 获取node_path
    node_record = verify_node(user_name, node_id)
    node_path = node_record.node_path
    # 更新node
    new_node_info = de_json(update_node(node_path, en_json(node_info)))
    return new_node_info


def delete_node(user_name: str, node_id: str):
    """
    删除节点(只是删除节点数据, 节点并不删除, 需要找zk管理员删除)
    :param user_name:
    :param node_id:
    :return:
    """
    node_record = verify_node(user_name, node_id)
    node_path = node_record.node_path
    # 删除节点
    update_node(node_path, b"")
    return dict()
