# Zookeeper Security Started

@TOC
- [创建Kerberos服务](#首先创建Kerberos服务器(ubuntu下))
- [Zookeeper with kerberos security](#Zookeeper加入kerberos验证机制)
    - [创建Zookeeper kerberos principal](#创建Zookeeper kerberos principal)
    - [配置Zookeeper](#配置Zookeeper)


## 首先创建Kerberos服务器(ubuntu下)

官方文档:
- [1](https://github.com/ekoontz/zookeeper/wiki)
- [2](https://cwiki.apache.org/confluence/display/ZOOKEEPER/ZooKeeper+and+SASL)

Kerberos原理:
- [1](https://blog.csdn.net/wulantian/article/details/42418231)

他人博客:
- [1](https://blog.csdn.net/bugzeroman/article/details/82457832)
- [2](https://www.jianshu.com/p/fc2d2dbd510b)
- [3](https://blog.csdn.net/tonyhuang_google_com/article/details/40861179)

具体步骤: 
- 下载并安装ntp(时间服务器)
    ```bash
    sudo apt-get install ntp
    sudo /etc/init.d/ntp restart
    ```
    - 如果需要配置客户机同步时间的话, 更改配置/etc/ntp.conf

- 下载安装kerberos server
    ```bash
    sudo apt-get install krb5-kdc krb5-admin-server
    ```
    - 查看config files, 可根据自己的需求编辑
        - reconfigure realm(自动创建示例配置文件)
        ```bash
        sudo dpkg-reconfigure krb5-kdc
        ```
        - 检查/etc/krb5kdc/kdc.conf
        - 修改/etc/krb5.conf
            ```bash
                [logging]
                 default = FILE:/home/swh/Kerberos/log/krb5libs.log
                 kdc = FILE:/home/swh/Kerberos/log/krb5kdc.log
                 admin_server = FILE:/home/swh/Kerberos/log/kadmind.log
                
                [libdefaults]
                 default_realm = EXAMPLE.COM
                 dns_lookup_realm = false
                 dns_lookup_kdc = false
                 ticket_lifetime = 24h
                 renew_lifetime = 7d
                 forwardable = true
                
                [realms]
                 EXAMPLE.COM = {
                  kdc = localhost
                  admin_server = localhost
                 }
                
                [domain_realm]
                 .example.com = EXAMPLE.COM
                 example.com = EXAMPLE.COM
            ```
    - 创建new realm
        ```bash
        sudo krb5_newrealm
        ```
    - 通过admin创建用户, 根据自己需求创建. (默认有root用户)
        - 进入kdc server的命令, quit/exit退出
            ```bash
            sudo kadmin.local
            # 创建test用户并输入密码
            addprinc test/admin
            # 添加加密密钥至/etc/krb5.keytab
            ktadd -k /etc/krb5.keytab test/admin
            ```
        - 验证用户和加密密钥是否创建成功
            ```bash
            sudo kinit -k -t /etc/krb5.keytab test/admin
            ```
    - 编写Kerberos访问控制列表ACL文件/etc/krb5kdc/kadm5.acl, 加入以下配置
        ```bash
        test/admin@EXAMPLE.COM  *
        ```
    - 常用命令, [各文件意义](https://docs.oracle.com/cd/E24847_01/html/819-7061/setup-9.html)
        - 重启krb服务
        ```bash
        sudo /etc/init.d/krb5-admin-server restart
        ```
        - klist 命令查看kinit 向kdc服务获取TGT的状态
        
- kerberos认证流程嵌入至其他项目中, 一般使用GSSAPI或者SASL等更通用的一些标准接口


## Zookeeper加入kerberos验证机制


### 创建Zookeeper kerberos principal

在kerberos服务器上创建Zookeeper的server 和client principal(Zookeepr集群的话则最好是
每个zk节点创建一个server principal, client可以选择只创建一份)
- bash 命令
    ```bash
    #　单个节点的server pricipal创建(这边偷懒没有每个节点创建一个)
    addprinc -randkey zookeeper/192.168.1.89
    ktadd -k /home/swh/ZooKeeper/zookeeper-3.4.12/zookeeper.keytab zookeeper/192.168.1.89
    
    # 客户端pricipal创建
    addprinc -randkey zkClient
    ktadd -k /home/swh/ZooKeeper/zookeeper-3.4.12/zkClient.keytab zkClient
    ```
    使用scp命令将keytab文件拷贝至每个zk节点对应的zk目录下
    ```bash
    # swh@192.168.1.89: 虚拟机192.168.1.89的用户swh登录
    sudo scp zookeeper.keytab swh@192.168.1.89:/home/swh/ZooKeeper/zookeeper-3.4.12/
    ```
    ![](picture/zk%20sasl/1.png)
    
- klist 命令查看kinit 向kdc服务获取TGT的状态
    ```bash
    sudo kinit -k -t /home/swh/ZooKeeper/zookeeper-3.4.12/zookeeper.keytab zookeeper/192.168.1.89
    sudo klist
    ```

### 配置Zookeeper

- 修改zoo.cfg
    ```bash
    # ZooKeeper的心跳时钟时长, 单位milliseconds(毫秒), 会话超时时间最小为2倍tickTime
    tickTime=2000
    # 初始化的时间限制, initLimit * tickTime
    initLimit=10
    # 同步的超时时间限制, syncLimit * tickTime
    syncLimit=5
    # 快照的存储目录, 自定义
    dataDir=/home/swh/ZooKeeper/zkPurge/zkPurge1
    # 服务端口
    clientPort=2181
    # 最大客户端连接数
    #maxClientCnxns=60
    # 快照最大保存数量
    #autopurge.snapRetainCount=3
    # 日志存放目录
    dataLogDir=/home/swh/ZooKeeper/log/log1
    # ZooKeeper是否开启自动删除运行日志(ZooKeeper交互过程会产生大量日志, 但由于删除日志操作会
    # 影响性能, 因此一般不开启)
    #autopurge.purgeInterval=1
    # 日志保留数量
    # autopurge.snapRetainCount
    # 集群模式, 有两个tcp port, 第一个用来主从连接交换数据的, 第二个用来进行选举(新leader)
    server.1=192.168.1.89:2888:3888
    server.2=192.168.1.89:2889:3889
    server.3=192.168.1.89:2890:3890
    
    # 开启client之间的验证
    authProvider.1=org.apache.zookeeper.server.auth.SASLAuthenticationProvider
    jaasLoginRenew=3600000
    ```
- 在zk conf目录下创建java.env文件
```bash
export JVMFLAGS="-Djava.security.auth.login.config=/home/swh/ZooKeeper/zookeeper-3.4.12/conf/zk_jaas.conf"
```
- 在zk conf目录下创建java.env配置中的zk_jaas.conf文件
    ```bash
    Server {
           com.sun.security.auth.module.Krb5LoginModule required
           useKeyTab=true
           keyTab="/home/swh/ZooKeeper/zookeeper-3.4.12/zookeeper.keytab"
           storeKey=true
           useTicketCache=false
           principal="zookeeper/192.168.1.89";
    };
    Client {
           com.sun.security.auth.module.Krb5LoginModule required
           useKeyTab=true
           keyTab="/home/swh/ZooKeeper/zookeeper-3.4.12/zkClient.keytab"
           principal="myzkclient"
           useTicketCache=false
           debug=true;
    };
    ```
- 重启zk服务器, 因为我们是用supervisor管理的, 因此只需要, [supervisor脚本](ZooKeeper%20Document/Getting%20Started.md)
```bash
sudo supervisorctl reload
```
