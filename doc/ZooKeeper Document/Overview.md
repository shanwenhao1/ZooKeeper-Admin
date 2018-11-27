# Overview

- [ZooKeeper](#ZooKeeper&middot;&middot;A Distributed Coordination Service for Distributed Applications)
- [Design Goals](#Design Goals)
- [Data model and the hierarchical namespace(数据模型与分层命名的空间)](#Data model and the hierarchical namespace(数据模型与分层命名的空间))
- [Nodes and ephemeral nodes](#Nodes and ephemeral nodes)
- [Conditional updates and watches](#Conditional updates and watches)
- [Guarantees](#Guarantees)
- [Simple API](#Simple API)
- [Implementation(实现)](#Implementation(实现))
- [Uses](#Uses)
- [Performance(性能)](#Performance(性能))

## ZooKeeper&middot;&middot;A Distributed Coordination Service for Distributed Applications

ZooKeeper是一种针对分布式服务的高性能协调服务. 它对外只暴露一些简单的服务, 提供简单的接口,
比如naming、配置管理、synchronization、Group services.

ZooKeeper运行在Java中并对Java和C都有绑定.

众所周知, 协调服务很难得到正确的结果, 他们特别容易出现诸如条件竞争和死锁等错误.
ZooKeeper致力于解除分布式应用实现协调服务的痛点.

## Design Goals

**ZooKeeper is simple.** ZooKeeper允许分布式进程通过共享层次命名空间(组织成一个标准的文件系统)
相互协调工作. 这些name space由data registers(数据寄存器)组成, 称为znodes, 以ZooKeeper说法来看, 这些
znodes类似于文件和目录.ZooKeeper数据保存在内存中, 因此有高吞吐、低延迟的特性

ZooKeeper实现了高性能、高可用、严格有序存储. 这意味着ZooKeeper可以应用于大型、分布式系统中.
可靠性方面, ZooKeeper解决了单点障碍, 而严格排序意味着可以在客户端实现复杂的同步函数.

**ZooKeeper is replicated.** 似于分布式进程协调,ZooKeeper 自身可被复制副本到一组主机上作为一个整体..

![ZooKeeper Service](../picture/ZooKeeper%20picture/zkservice.jpg)
ZooKeeper服务集群的服务端相互知道彼此的存在. 它们维护了一个内存镜像的状态镜像, 连同事务日志和
快照集一起持久化存储.只要大部分服务器可用, 那么ZooKeeper服务就能保持稳定.

**ZooKeeper is ordered.** ZooKeeper 为每个更新标记了序号,它反应了ZooKeeper 事务的顺序.并发操作可以
用这个序号来实现更高层次的抽象,例如同步服务

**ZooKeeper is fast.** 它在以读为主的场景下非常快.ZooKeeper 应用运行在数千台机器上,在读写比为
10:1 的时候表现最佳.

## Data model and the hierarchical namespace(数据模型与分层命名的空间)

ZooKeeper 提供的命名空间非常像标准的文件系统.名字是路径元素通过斜杠(/)分割的序列. ZooKeeper 命名空间
中的每个节点都是一个唯一的路径

![ZooKeeper namespace](../picture/ZooKeeper%20picture/zknamespace.jpg)

## Nodes and ephemeral nodes

与标准的文件系统不同,ZooKeeper 命名空间中的每个节点都存有与子节点相关的数据.它就像一个文件系统允许
文件变成一个目录.(ZooKeeper 为存储协调数据而设计:状态信息、配置信息、路径信息等,因此每个节点存储的
数据通常都很小,量级在B到KB之间.)我们用术语znode 来指ZooKeeper 数据节点.

Znodes 的数据结构中包括:数据变更的版本号、ACL 变更以及时间戳,以便缓存验证和协调更新.每次znode数据
改变,版本号递增.例如,每当客户端收到数据,它将同时收到数据的版本.

命名空间中znode存储的数据是被原子性读写的.读操作可以获得Znode相关的全部数据,写操作将覆盖全部数据.
每个node有一个权限控制列表( Access Control List ,ACL)来限制什么人可以干什么事.

ZooKeeper 也有临时节点的概念. 这些节点存在时间与会话一致,会话创建时znode生效.当会话结束时Znode
被删除.临时节点对你实现功能非常有用,请参考[tbd].

## Conditional updates and watches

ZooKeeper 支持watches 的概念. 客户端可以在Znodes上设一个watch .znode 改变时会触发或删除watch.
当watch 被触发时,客户端会收到一个说“znode已被改变”的包.并且,如果客户端和一个Zookeeper服务器
之间的连接中断时,客户端会收到一个本地通知.对于如何使用,请参考[tbd].

## Guarantees

ZooKeeper 非常简单、迅速,这源自于它的设计目标.因此它为构建更复杂的服务提供了基础.
例如同步服务, 它提供了一套保障:
- Sequential Consistency(顺序一致性) - 按照客户端的发送顺序进行更新
- Atomicity(原子性)- 更新或成功或失败.不会有中间态的部分结果
- Single System Image(单一系统镜像) - 无论客户端或服务器,连接到服务端后都能看到同样的视图
- Reliability(可靠性) - 一旦应用一个更新,它将留存到客户端覆盖本次更新为止
- Timeliness(时效性) - 在一段时间内保证系统的客户端视图是最新的

## Simple API

ZooKeeper的一个设计目标是提供简单的接口. 因此它只支持以下操作:
- create: creates a node at a location in the tree
- delete: deletes a node
- exists: tests if a node exists at a location
- get data: reads the data from a node
- set data: writes data to a node
- get children: retrieves a list of children of a node
- sync: waits for data to be propagated

## Implementation(实现)

ZooKeeper 组件展示了ZooKeeper服务的高级组件.除请求处理器以外,构成ZooKeeper
服务的每个服务端的副本集都拷贝自它的每个组件.

![ZooKeeper components](../picture/ZooKeeper%20picture/zkcomponents.jpg)

副本数据库是一个内存数据库,包含了整个数据树.更新日志序列化后记录在磁盘上,用来恢复数据.

每个Zookeeper服务器服务客户端.客户端连接到一个服务端后提交请求.读
请求从每个服务器数据库的本地副本中响应.服务状态变更请求、写请求按照约定的协议执行.

协议的一部分,客户端的全部写请求被转到叫领导者(leader)的一个独立的服务端.其余的Zookeeper服务端,
称为从服务(followers) ,从领导者(leader)那边接收消息并确认消息已收到.消息层负责在领导者发生故
障时更换领导者并同步数据到从服务.

ZooKeeper 采用了一个自定义的原子消息协议.由于消息层是原子的,Zookeeper 可以保证本地副本没有偏差.
当领导者收到一个写请求时,它会计算出系统何时做了写操作,并在事务中更新最新状态.

## Uses

ZooKeeper的程序接口非常简单

## Performance(性能)

ZooKeeper是为高性能而设计的, 下图就是ZooKeeper在Yahoo的性能展示. (ZooKeeper在读大于写的
时候表现尤为出色, 因为写操作还涉及到所有服务端的同步操作)
![ZooKeeper Performance](../picture/ZooKeeper%20picture/zkperfRW-3.2.jpg)

                            不同读写比率下的吞吐量