#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10
# @Author  : Wenhao Shan

import log
from zktool.enum.log_enum import KazooStatus
from kazoo.client import KazooClient, KazooState
from kazoo.security import Permissions, ACL, AUTH_IDS, make_digest_acl

Zk_Address = '192.168.1.89:2181'
ACL_MY = make_digest_acl(username="kongwang", password="kw_zk_node_acl_3345", read=True, write=True,
                         create=True, delete=True, admin=True, all=True)


class ZKClientAsync(KazooClient):
    """
    该类继承自KazooClient
    """

    def __init__(self, hosts='127.0.0.1:2181',
                 timeout=10.0, client_id=None, handler=None,
                 default_acl=None, auth_data=None, read_only=None,
                 randomize_hosts=True, connection_retry=None,
                 command_retry=None, logger=None, **kwargs):
        super(ZKClientAsync, self).__init__(hosts, timeout, client_id, handler, default_acl, auth_data,
                                            read_only, randomize_hosts, connection_retry, command_retry,
                                            logger, **kwargs)


# 由于ZooKeeper的权限控制是节点级别的, 且不继承. 在创建节点时使用acl参数添加权限控制
# 相应的加权限后, 访问节点都需要认证
ZK = KazooClient(hosts=Zk_Address, default_acl=[ACL_MY], auth_data=[("digest", "kongwang:kw_zk_node_acl_3345")])


@ZK.add_listener
def my_listener(state):
    """
    Listening for Connection Events
    :param state:
    """
    if state == KazooState.LOST:
        log.tag_error(KazooStatus.Lost, "Register somewhere that session was lost, "
                                        "Please check session status")
    elif state == KazooState.SUSPENDED:
        log.tag_error(KazooStatus.Suspended, "Handle being disconnected from zookeeper")
    else:
        log.tag_info(KazooStatus.Conn, "Handle being connected/reconnected to zookeeper")
