#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/27
# @Author  : Wenhao Shan

import json
from django.http import request
from django.test import TestCase
from utils.md5 import md5_check
from utils.time_utils import get_now_time_timestamp
from zkControl.control import create_node, delete_node
from zktool.code_tool.encode import en_json
from zkWeb.App.models import User, UserNode, Node
from zkWeb.App.views import zk_info as zookeeper


def mock_data():
    """
    模拟创建节点及测试用户数据
    :return:
    """
    username = "test999"
    password = "test999_password"
    zk_path = "test/test999"
    json_data = {
        "test": 123,
        "zk_test": {
            "hello": "hello"
        }
    }
    # 创建节点
    create_node(zk_path, en_json(json_data))
    node = Node.objects.create(node_path=zk_path, node_name="test_node")
    user = User.objects.create(user_name=username, password=password)
    UserNode.objects.create(node_id=node.node_id, user_id=user.user_id)
    return username, password, "test_node", node.node_id


def delete_mock_data(username: str, zk_path: str, node_id: str):
    """
    删除模拟节点数据
    :return:
    """
    # 删除节点
    delete_node(zk_path)
    # 数据库测试数据可以不用删除, 因为测试完成后, django自动将测试数据库删除掉了
    # Node.objects.get(node_path=zk_name).delete()
    # User.objects.get(user_name=username).delete()


class ZkTest(TestCase):
    """
    zk test, 有两种方式配置数据库:
        一种是django默认的创建test数据库方式: 运行命令为python manage.py test --keepdb ZkTest(--keepdb不删除测试数据库,
        默认为每次测试都会新建完成后删除数据库)(会新建一个test开头的数据库, 数据库编码格式要设置成utf8)
        另一种是采用sqlite3, 配置在settings.py内, 命令为: python manage.py test test.zk_test.ZkTest
    https://docs.djangoproject.com/en/dev/topics/testing/overview/
    """

    def setUp(self):
        self.url = "http://localhost:8081/zk_node/"
        self.username, self.password, self.zk_name, self.node_id = mock_data()

    def tearDown(self):
        delete_mock_data(self.username, self.zk_name, self.node_id)

    def test_zk_info(self):
        """
        测试获取zk信息
        :return:
        """
        timestamp = get_now_time_timestamp(utc=True)
        md5 = md5_check(self.password, timestamp)
        req_data = {
            "username": self.username,
            "md5": md5,
            "timestamp": timestamp,
            "zkPath": self.zk_name
        }
        # 手动构建request
        req = request.HttpRequest()
        req.method = 'POST'
        for key, value in req_data.items():
            req.POST.setdefault(key, value)
        resp = zookeeper(req)
        zk_info = json.loads(resp.content)
        self.assertEqual(zk_info["status"], 0), "测试获取zk信息失败!!!"
        self.assertEqual(zk_info["obj"]["test"], 123), "测试获取zk失败, zk数据错误!!!"
