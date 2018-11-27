# Kazoo文档笔记

[官方文档](https://kazoo.readthedocs.io/en/latest/index.html)

## 基本用法

### 新建一个连接
```python
from kazoo.client import KazooClient

# KazooClient 会尽量保持连接
zk = KazooClient(hosts='127.0.0.1:2181') 
# zk = KazooClient(hosts='127.0.0.1:2181', read_only=True) read only model
zk.start()
# 终止连接
zk.stop()
```

由于Kazoo是保持连接的, 因此尽量使用KazooState监听连接状态, 共有三种状态
```python
from kazoo.client import KazooState

# 当一个KazooClient是第一次创建时, 初始状态是LOST. 随后建立连接后状态变为CONNECTED, 
# 如果连接出现问题或者连接到一个不通的zk节点会报SUSPEND状态, 连接命令不成功
def my_listener(state):
    """
    Listening for Connection Events
    :param state:
    """
    if state == KazooState.LOST:
        pass
    elif state == KazooState.SUSPENDED:
        pass
    else:
        pass
```

### 创建节点

- ensure_path(): 递归的创建节点及路径, 但是不能初始化数据
- create(): 创建节点且初始化数据, 要求节点路径事先存在
```
# Ensure a path, create if necessary
zk.ensure_path("/my/favorite")

# Create a node with data
zk.create("/my/favorite/node", b"a value")
```

### 读取数据

- exists(): 查看节点是否存在, 如果存在返回ZnodeStat, 不存在返回None
- get(): 获取znode数据以ZnodeStat的格式
- get_children(): 获取指定节点的children列表
```
# Determine if a node exists
if zk.exists("/my/favorite"):
    # Do something

# Print the version of a node and its data
data, stat = zk.get("/my/favorite")
print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

# List the children
children = zk.get_children("/my/favorite")
print("There are %s children with names %s" % (len(children), children))
```

### 更新数据

```
zk.set("/my/favorite", b"some data")
# zk.set("/my/favorite", b"some data", version=1) 也可使用version控制, 更新时, 如果版本号不比之前的
# 版本号大的话则会报BadVersionError
```

### 删除节点

```
zk.delete("/my/favorite/node", recursive=True)  # 删除节点, recursive=True会递归删除children, 默认为false
```

### 重试命令

Kazoo默认不支持与zookeeper的失败重连, 而是直接将失败的信息raise出来. 但他提供了retry方法进行
重连
```
result = zk.retry(zk.get, "/path/to/node")
```

### 自定义重试

```python
from kazoo.retry import KazooRetry
from kazoo.client import KazooClient

client = KazooClient
# 一下code会重试client.get最多三次
kr = KazooRetry(max_tries=3, ignore_expire=False)
result = kr(client.get, "/some/path")
```

### Watchers

Kazoo可以在节点上设置监视函数(watch functions), 当节点值或者该节点Children值改变时触发.

Watchers可以设置成两种方式:
- one-time watch events: 只会被call一次, 且不接受session events.此种方式的watch必须由以下
方法传递
    - get()
    - get_children()
    - exists()
    ```
      def my_func(event):
          # check to see what the children are now

      # Call my_func when the children change
      children = zk.get_children("/my/favorite/node", watch=my_func)
    ```
- native Zookeeper watchers:

Kazoo提供了更高级的API去监视data和children, 而不必为每一此触发的事件去新建一个watch, 如下:
- [ChildrenWatch](https://kazoo.readthedocs.io/en/latest/api/recipe/watchers.html#kazoo.recipe.watchers.ChildrenWatch)
- [DataWatch](https://kazoo.readthedocs.io/en/latest/api/recipe/watchers.html#kazoo.recipe.watchers.DataWatch)
```
@zk.ChildrenWatch("/my/favorite/node")
def watch_children(children):
    print("Children are now: %s" % children)
# Above function called immediately, and from then on

@zk.DataWatch("/my/favorite")
def watch_node(data, stat):
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
```

### Transactions(事务)

ZooKeeper3.4以上版本都支持事务
```
transaction = zk.transaction()
transaction.check('/node/a', version=3)
transaction.create('/node/b', b"a value")
results = transaction.commit()
```

## async用法

### Connection Handling

创建一个async 连接
```python
from kazoo.client import KazooClient
from kazoo.handlers.gevent import SequentialGeventHandler

zk = KazooClient(handler=SequentialGeventHandler())

# returns immediately
event = zk.start_async()

# Wait for 30 seconds and see if we're connected
event.wait(timeout=30)

if not zk.connected:
    # Not connected, stop trying to connect
    zk.stop()
    raise Exception("Unable to connect.")
```

### Asynchronous Callbacks

所有的kazoo_async方法中除了start_async()之外都返回了一个[IAsyncResult](https://kazoo.readthedocs.io/en/latest/api/interfaces.html#kazoo.interfaces.IAsyncResult)
实例.这些实例允许设置回调函数, 当实例调用完成时(a result, or chain one or more callback functions)会
触发这些回调函数

```
import sys

from kazoo.exceptions import ConnectionLossException
from kazoo.exceptions import NoAuthException

def my_callback(async_obj):
    try:
        children = async_obj.get()
        do_something(children)
    except (ConnectionLossException, NoAuthException):
        sys.exit(1)

# Both these statements return immediately, the second sets a callback
# that will be run when get_children_async has its return value
async_obj = zk.get_children_async("/some/node")
async_obj.rawlink(my_callback)
```

### Zookeeper CRUD

以下这些CRUD方法都是async方法, 且都返回IAsyncResult

- Creating Method:
    - create_async()
- Reading Methods:
    - exists_async()
    - get_async()
    - get_children_async()
- Updating Methods:
    - set_async()
- Deleting Methods:
    - delete_async()
    
ensure_path()没有async的用法, 且delete_async()不支持recursive(递归删除).