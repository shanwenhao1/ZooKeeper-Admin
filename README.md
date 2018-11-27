# ZooKeeper管理后台

<img align="right" width="59px" src="https://raw.githubusercontent.com/gin-gonic/logo/master/color.png">

[![Build Status](https://travis-ci.org/gin-gonic/gin.svg)](https://travis-ci.org/gin-gonic/gin)
[![Join the chat at https://gitter.im/gin-gonic/gin](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/gin-gonic/gin?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## [Kafka(包含zk)详解](doc/Kafka.md)


## [Django项目新建步骤](doc/web%20base.md)

[Django Book](http://djangobook.py3k.cn/2.0/)

启动方法: 
- 数据库
    - 新建数据库, 并更改settings.py内的数据库连接属性.
    - 运行bash命令, 在数据库创建model对应的表
    ```bash
          // App下对应的model
          python manage.py makemigrations App
          python manage.py makemigrations App2
          ...
          python manage.py migrate
    ```

## ZooKeeper

账户: root
密码: *******
本项目使用Python3 + Django实现

ZooKeeper方面使用Kazoo连接管理zookeeper, [Kazoo笔记](doc/Kazoo.md)

