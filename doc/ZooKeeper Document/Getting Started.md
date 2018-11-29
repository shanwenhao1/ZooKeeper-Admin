# Getting Started

- [Getting Started: Coordinating Distributed Applications with ZooKeeper](#Getting Started&middot;&middot;Coordinating Distributed Applications with ZooKeeper)
- [Pre-requisites](#Pre&middot;&middot;requisites)
- [下载](#下载)
- [Standalone Operation](#Standalone Operation)
    - [配置myid](#配置myid)
- [ZK编程](#ZK编程)
- [Running Replicated ZooKeeper](#Running Replicated ZooKeeper)

## Getting Started&middot;&middot;Coordinating Distributed Applications with ZooKeeper

该文档包含了一些信息帮助你快速使用ZooKeeper.它主要针对希望尝试它的开发人员,
并包含单个ZooKeeper服务器的简单安装说明,一些命令可以验证它是否正在运行,还有
一个简单的编程示例.最后,为了方便起见,有一些关于更复杂的安装部分,例如,运行
主从复制部署,并优化事务日志.然而,完整的商业部署说明,请参阅ZooKeeper管理员指南.

## Pre&middot;&middot;requisites

见管理指南中的[System Requirements](https://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_systemReq)

## 下载

To get a ZooKeeper distribution, download a recent [stable](http://zookeeper.apache.org/releases.html)
 release from one of the Apache Download Mirrors.

## Standalone Operation

在独立模式下设置ZooKeeper服务器非常简单, 服务包含在一个JAR文件中, 因此安装过程中
包含了创建配置. 安装步骤:
- 解压下载的稳定ZooKeeper版本, 解压并进入解压后的目录
```
tar -zxvf zookeeper-3.4.12.tar.gz
```

- 要启动ZooKeeper你需要一个配置文件. 创建conf/zoo.cfg, 文件内容示例如下
```
# ZooKeeper的心跳时钟时长, 单位milliseconds(毫秒), 会话超时时间最小为2倍tickTime
tickTime=2000
# 初始化的时间限制, initLimit * tickTime
initLimit=10
# 同步的超时时间限制, syncLimit * tickTime
syncLimit=5
# 快照的存储目录, 自定义
dataDir=/tmp/zookeeper
# 服务端口
clientPort=2181
# 最大客户端连接数
#maxClientCnxns=60
# 快照最大保存数量
#autopurge.snapRetainCount=3
# 日志存放目录
dataLogDir=/datalog
# ZooKeeper是否开启自动删除运行日志(ZooKeeper交互过程会产生大量日志, 但由于删除日志操作会
# 影响性能, 因此一般不开启)
#autopurge.purgeInterval=1
# 日志保留数量
# autopurge.snapRetainCount
# 集群模式, 有两个tcp port, 第一个用来主从连接交换数据的, 第二个用来进行选举(新leader)
#server.1=zoo1:2888:3888
#server.2=zoo2:2888:3888
#server.3=zoo3:2888:3888
```

- 启动服务
```
bin/zkServer.sh start
# 用bin/zkServer.sh status 查看启动状态, 如果报java not found, 则安装jdk: sudo apt-get install default-jdk
# 可用bin/zkCli.sh -server 127.0.0.1:2181本地连接zk服务进行测试.
```
这里是独立模式下运行ZooKeeper, 如果想要以主从模式运行ZooKeeper, 请[参考](https://zookeeper.apache.org/doc/current/zookeeperStarted.html#sc_RunningReplicatedZooKeeper)
各个zk服务server.X组成了zk集群, 当服务启动的时候, 它们依靠配置文件下的.X(*myid*) 知道彼此的存在.


### 配置myid

在dataDir内会放置一个myid文件, 里面就一个数字, 用来唯一标识这个服务.这个id是很重要的,
一定要保证整个集群中唯一.zookeeper会根据这个id来取出server.x上的配置.比如当前id为1,
则对应着zoo.cfg里的server.1的配置.


## ZK编程

ZooKeeper有Java、C监听.它们在功能上是等价的. C bindings存在两种类型: 单线程和多线程.它们
仅仅差别在Messaging loop完成的方式, [详情Programming Examples in the ZooKeeper
Programmer's Guide](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_programStructureWithExample).

## Running Replicated ZooKeeper

在生产环境中, ZooKeeper最好以Replicated Model方式部署. 要求至少三台
(两台server的服务稳定性不如一台server)以上的server组成叫做quorum的group.

如果想要测试, 在单个机器上运行多个server可以以如下方式进行配置
```
dataDir=/tmp/zookeeper_1
dataLogDir=/datalog_1
clientPort=2181
server.1=localhost:2888:3888
server.2=localhost:2889:3889
server.3=localhost:2890:3890

dataDir=/tmp/zookeeper_2
dataLogDir=/datalog_2
clientPort=2182
server.1=localhost:2888:3888
server.2=localhost:2889:3889
server.3=localhost:2890:3890

dataDir=/tmp/zookeeper_3
dataLogDir=/datalog_3
clientPort=2183
server.1=localhost:2888:3888
server.2=localhost:2889:3889
server.3=localhost:2890:3890
```
且每个server都需要拥有单独的dataDir(快照目录, 记得在其目录配置myid)和不通的clientPort, 这种测试的话单个
server挂掉的话会导致整个集群都挂掉.


## Supervisor脚本
```bash
[program:ZooKeeper1] ;
user=root ; 进程运行的用户身份　　　　　
directory=/home/swh/ZooKeeper/zookeeper-3.4.12/bin ; 程序所在路径
command=sudo ./zkServer.sh start-foreground zoo1.cfg ;
stderr_logfile=/home/swh/ZooKeeper/runlog/err.log ; 错误日志保存路径
stdout_logfile=/home/swh/ZooKeeper/runlog/zk.log ; 输出日志保存路径
stdout_logfile_maxbytes = 20MB
stdout_logfile_backups = 3
autostart=True
autorestart=False
startsecs=5 ; 启动时间5秒后无异常则表明成功启动
startretries=0 ; 启动失败重启次数, 默认为3
```