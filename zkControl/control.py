#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10
# @Author  : Wenhao Shan

import log
from functools import wraps
from kazoo.exceptions import NodeExistsError, NoNodeError
from zkControl.KazooClient.connect import ZK
from zktool.enum.log_enum import ZkControlStatus
from zktool.enum.msg_enum import KazooMsg
from utils.error import ActionError


def handle(func):
    """
    wrap function of zk handle function
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not ZK.connected:
            ZK.start()
        return func(*args, **kwargs)
    ZK.stop()
    return wrapper


def any_callback(result):
    try:
        return result.get()
    except NodeExistsError:
        return True


@handle
def create_node(node_path: str, node_data: b""=b""):
    """
    创建新节点并set data, 目前只支持json格式的data
    :param node_path: 节点路径
    :param node_data: 节点值
    :return:
    """
    with ZK.transaction():
        try:
            ZK.create(node_path, node_data)
        except Exception as e:
            if type(e) == NodeExistsError:
                log.tag_error(ZkControlStatus.Create, "Node exist")
                raise ActionError(KazooMsg.Node_Exist)
            else:
                log.tag_error(ZkControlStatus.Create, "create node with error: " + str(e))
                raise ActionError(KazooMsg.Create_Failed)
        # 返回创建后的数据
        data = get_node(node_path)
    return data


@handle
def get_node(node_path: str):
    """
    获取节点信息
    :param node_path:
    :return:
    """
    try:
        data, _ = ZK.get(node_path)
    except Exception as e:
        if type(e) == NoNodeError:
            log.tag_error(ZkControlStatus.Get, "Node not exist")
            raise ActionError(KazooMsg.Node_Not_Exist)
        else:
            log.tag_error(ZkControlStatus.Get, "get node with error: " + str(e))
            raise ActionError(KazooMsg.Get_Failed)
    return data


@handle
def update_node(node_path: str, new_node_data: b""):
    """
    更新节点
    :param node_path:
    :param new_node_data:
    :return:
    """
    with ZK.transaction():
        try:
            ZK.set(node_path, new_node_data)
        except Exception as e:
            if type(e) is NoNodeError:
                log.tag_error(ZkControlStatus.Update, "Node not exist")
                raise ActionError(KazooMsg.Node_Not_Exist)
            else:
                log.tag_error(ZkControlStatus.Update, "update node with error: " + str(e))
                raise ActionError(KazooMsg.Update_Failed)
        # 返回更新后的数据
        data = get_node(node_path)
    return data


# TODO 修复zk.DataWatch的bug
# @ZK.DataWatch("/")
@handle
def delete_node(node_path: str):
    """
    删除节点
    :param node_path:
    :return:
    """
    try:
        ZK.delete(node_path, recursive=True)
    except Exception as e:
        log.tag_error(ZkControlStatus.Delete, "delete node with error: " + str(e))
        raise ActionError(KazooMsg.Delete_Failed)


@handle
def get_children(node_path: str):
    """
    get a list of child nodes of a path
    :param node_path:
    :return:
    """
    try:
        children_list = ZK.get_children(node_path)
    except Exception as e:
        if type(e) is NoNodeError:
            log.tag_error(ZkControlStatus.Get, "Node not exist")
            raise ActionError(KazooMsg.Node_Not_Exist)
        else:
            log.tag_error(ZkControlStatus.Get, "inquire children list with error: " + str(e))
            raise ActionError(KazooMsg.Delete_Failed.Get_Children_Failed)
    return children_list


if __name__ == '__main__':
    pass
    # from zktool.code_tool.encode import en_json
    # from zktool.code_tool.decode import de_json
    # nod_path = "/test/create"
    # json_data = {
    #     "test": "test_node_update",
    #     "child": {
    #         "child_test": "child_node"
    #         }
    #     }
    # b_json = en_json(json_data)
    # # print(de_json(create_node(nod_path, b_json)))
    # print(de_json(create_node("/test/another_create", b_json)))
    # # delete_node(nod_path)
    # # print(de_json(get_node("/test/another_create")))
    # delete_node("/test/another_create")
    # print(get_children("/"))
