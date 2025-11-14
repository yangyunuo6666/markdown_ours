[toc]

***

# Zookpeeper
+ Zookeeper是一个开源的分布式的，为分布式应用提供协调服务：通知机制 + 文件系统 
+ zk特点：
  - **半数存活，当集群中半数以上机器可用，集群可用。**
  - 集群有一个leader，多个follower，数据全局一致，每个server保存一份相同的数据副本，更新请求时，leader将更新同步到follower。数据更新采用原子广播方式，保证数据一致性
  - 数据结构是树形
+ Zookeeper启动时读取myid文件中编号，拿到里面的数据与zoo.cfg里面的配置信息比较从而判断到底是哪个server
+ 端口：
  - 监听客户端连接的端口：2181
  - 监听leader选举的端口：3888
  - 选举端口：2888
+ 选举机制：过半选举，故部署奇数台机器
+ 监听原理：
  - main线程创建两个线程，一个负责监听listerer，一个负责网络连接通信connect。
  - 通过connect将注册的监听事件发送给ZK，ZK将监听事件放到监听列表中，zk监听到数据、路径变化，就会通知listener，listener收到通知后，回调业务逻辑process()方法

+ 常用命令
  - stat：查看服务器状态
  - help：显示所有操作命令

## 集群部署
+ 解压安装包为zookeeper
+ 在/zookeeper/目录下创建zkData文件夹，在/zookeeper/zkData目录下创建myid文件，myid文件中写入一个编号
    ```
    mkdir /opt/modules/zookeeper/zkData
    echo 1 > /opt/modules/zookeeper/zkData/myid
    ```
+ 修改配置文件
```
mv zookeeper/conf/zoo_sample.cfg zookeeper/conf/zoo.cfg

vim zoo.cfg
    dataDir=/opt/module/zookeeper-3.4.10/zkData
    #第2台服务器，与leader通信的端口是2888，选举的端口是3888
    server.2=hadoop102:2888:3888 
    server.3=hadoop103:2888:3888
    server.4=hadoop104:2888:3888
```









