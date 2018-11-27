#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10
# @Author  : Wenhao Shan

import log
from zktool.enum.log_enum import KazooStatus
from kazoo.client import KazooClient, KazooState

Zk_Address = '192.168.1.89:2181'


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


ZK = KazooClient(hosts=Zk_Address)


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
