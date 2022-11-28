# HDFS

参考 HDFS 实现一个简单地分布式文件系统

### 开发日志

----------------------------------- 2022/11/27 -------------------------------------

当前已支持 **创建目录、文件上传和文件下载**

**创建目录逻辑：**
- 直接在文件目录树上创建、添加对应节点

对应namenode接口：
- `mkdir` 使用方法：`c.mkdir("/test")`

**文件上传逻辑：**  [测试文件](https://github.com/onlyone2019/HDFS/blob/main/putFileTest.py)
- 向namenode查询文件分块大小
- 客户端本地将文件分块
- 向namenode请求创建文件，namenode节点生成文件节点，将其添加到目录树后告诉客户端每个块应送去的地址。默认备份是1个，所以每个块要存在两个地址上
- 客户端向各地址传文件块(当前文件传送使用FTP)

对应namendoe端接口：
- `getBlockSize` 使用方法：`c.getBlockSize()`
- `getLocation` 使用方法：`c.getLocation(filepath , blocknum)` 文件路径 和 文件块数

**文件下载逻辑：** [测试文件](https://github.com/onlyone2019/HDFS/blob/main/getFileTest.py)
- 向namenode查询文件各块存储位置，当前每个块存的地址有两个（一个是备份），随机选择一个
- 根据位置获得各个块
- 将各块拼接起来

对应namenode接口：
- `get` 使用方法：`c.get("/x.txt")`

注意：
当前只设置了一个datanode，所以所有文件块都存在一个datanode。之后 如何决定block应该存在哪 这个逻辑还需要完善。

----------------------------------- 2022/11/28 -------------------------------------

新增功能： **ls、文件目录树的固化。**

**ls逻辑：**
- 根据用户传过来的参数`path`，找到文件，返回用户这个文件夹下所有文件的名称

对应namenode接口：
- `ls` 使用方法：`c.ls("/test")`

**文件目录树固化 **
- **需求：** namenode文件目录树应该是保存在内存中的，服务器停止的时候需要将文件目录树固化下来，服务器重启后自动加载文件目录树

- **实现：** 文件目录树存储借助python `pickle` 模块将对象序列化。对象加载和保存分别为`load` 和 `dump`。

当前目录下的`dirTree.pkl`文件存储的目录树形式如下：`/test/xxxx` 即根目录下有`test`文件夹，其下又有`xxxx`文件夹

客户端测试代码：
```python
import zerorpc
c = zerorpc.Client()
c.connect("tcp://ip:4242")
print(c.ls("/"))  # ["test"]
print(c.ls("/test")) #["xxxx"]
```