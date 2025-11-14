[toc]

---

# Doris

+ 架构：
  - FE(原数据管理)：leader、follower保证高可用。Observer拓展查询节点备份元数据
  - BE(数据管理、查询计划执行)
+ 采用mysql协议，兼容mysql客户端
+ Broker：可选进程，用于支持Doris读写远端存储上的文件和目录，如 HDFS、BOS和AFS等。
+ [FE Web页面](：http://hadoop102:7030/login)，用户：root ，密码：无

## doris表的设计
+ 支持分区、hash分桶，Tablet之间的数据是没有交集的，独立存储的
+ 数据模型：数仓采用聚合中的幂等模型，存放dwd层数据
  - Aggregate：聚合模型，将数据按时间分区，分区内数据按key聚合。
  - Unique：唯一明细模型，将数据按时间分区，分区内数据按key存储。
  - Duplicate：明细模型，将数据按时间分区，分区内数据按key存储，不进行去重。
+ 引擎：olap|mysql|broker|hive
  - Olap：默认引擎，管理数据和元数据
  - 其他：仅管理元数据
+ 分区：Partition
  - 支持 Range和List的划分方式
  - 可指定一到多列，写分区值时需要加双引号，不指定时系统自动生成用户不可见的全值范围同表名的分区
  - rang分区：按范围划分，通过 VALUES [...) 同时指定上下界，eg：p201701: [MIN_VALUE,  2017-02-01)
  - list分区：按值划分，通过 VALUES IN (...) 同时指定多个值，eg：p_cn: ("Beijing", "Shanghai", "Hong Kong")
+ 分桶：Bucket
  - 仅支持Hash的划分方式，支持多列
  - DISTRIBUTED BY HASH(`user_id`) BUCKETS 16
+ **动态分区：动态添加分区及动态删除分区的功能。动态分区只支持 Range 分区。**
## 物化视图（Doris自动维护）：
+ 物化视图：将查询结果存储在表中，查询时直接查询物化视图
+ 适用场景：
  - 分析需求覆盖明细数据查询以及固定维度查询两方面。
  - 查询仅涉及表中的很小一部分列或行。
  - 查询包含一些耗时处理操作，比如：时间很久的聚合操作等
+ **doris现在对物化视图仅支持单表查询，不支持join操作**
+ 物化视图的创建：
  - 从查询语句中抽象出，多个查询共有的分组和聚合方式作为物化视图的定义
  - 不需要给所有维度组合都创建物化视图
  - 查看相关语法：help CREATE MATERIALIZED VIEW
+ 删除：DROP MATERIALIZED VIEW 物化视图名 on Base 表名;
+ 聚合函数：
  - 支持：sum、min、max、count
  - 限制（因物化视图损失了部分维度数据）：
    - 聚合函数中仅支持单列，不支持sum(a+b)
    - 表的物化视图 key 中不包含删除语句中的条件列，则删除语句不能执行
    - 单表上过多的物化视图会影响导入的效率：导入数据时，物化视图和 base 表数据是同步更新（<10）
    - 相同列，不同聚合函数，不能同时出现在一张物化视图中，比如：select sum(a),min(a) from table 不支持
    - 只能改变列顺序，不能起到聚合的作用
## 修改表：
+ alter table：partition 、rollup、schema change、rename 和 index 





















## Linux部署
+ 依赖java1.8、gcc4.8.2、cetos 7.1
+ FE、BE很消耗磁盘资源需要分开部署
+ 注意实现：
  - FE的磁盘空间主要用于存储元数据，包括日志和image
  - BE的磁盘空间主要用于存放用户数据，总磁盘空间按用户总数据量* 3（3副本）*1.4（预留空间）
  - 多个FE所在服务器的时钟必须保持一致（允许最多5秒的时钟偏差）
  - 高可用：1FE + 1observer时读高可用，1FE + 3Follower 时写高可用
  - **Follower的数量必须为奇数，Observer 数量随意**
  - Broker是用于访问外部数据源（如HDFS）的进程。通常，在每台机器上部署一个 broker实例即可。
+ 常用端口：
  
|实例名|端口名|默认端口|通信方向|说明|
|---|---|---|---|---|
|FE|**http_port**|8030|FE<-->FE,用户<--> FE|**FE上的http_server端口**|
|BE|**webserver_port**|8040|BE<-->FE|**BE上的http server端口**|
|BE	|be_prot|9060|FE-->BE|BE上thrift server的端口用于接收来自FE 的请求|
|BE|heartbeat_service_port|9050|FE-->BE|BE上心跳服务端口,用于接收来自FE的心跳|
|BE|brpc_prot*|8060|FE<-->BE,BE<-->BE|BE上brpc端口,用于BE之间通信|
|FE|rpc_port|9020|BE-->FE,FE<-->FE|FE上thirt server端口号|
|FE|query_port|9030|用户<--> FE|FE上的mysqlserver端口|
|FE|edit_log_port|9010|FE<-->FE|FE上bdbje之间通信用的端口|
|Broker|broker_ipc_port|8000|FE-->BROKER,BE-->BROKER|Broker上的thrift server用于接收请求|

### 部署
+ 操作系统安装要求
    1. 设置系统最大打开文件句柄数（注意这里的*不要去掉）。
    ```
    sudo vim /etc/security/limits.conf
    * soft nofile 65536
    * hard nofile 65536
    * soft nproc 65536
    * hard nproc 65536
    ```
    1. 设置最大虚拟块的大小。sudo vim /etc/sysctl.conf
    vm.max_map_count=2000000
+ 上传安装包，并解压
    ```
    mkdir -p /opt/module/doris

    tar -xvf apache-doris-fe-1.2.4.1-bin-arm.tar.xz -C /opt/module/doris

    mv /opt/module/doris/apache-doris-fe-1.2.4.1-bin-arm /opt/module/doris/fe
    #安装be
    tar -xvf apache-doris-be-1.2.4.1-bin-arm.tar.xz -C /opt/module/doris

    mv /opt/module/doris/apache-doris-be-1.2.4.1-bin-arm /opt/module/doris/be
    ```
+ 安装java依赖
    ```
    tar -xvf apache-doris-dependencies-1.2.4.1-bin-arm.tar.xz -C /opt/module/doris

    mv /opt/module/doris/apache-doris-dependencies-1.2.4.1-bin-arm /opt/module/doris/dependencies

    cp /opt/module/doris/dependencies/java-udf-jar-with-dependencies.jar /opt/module/doris/be/lib
    ```
+ 配置FE
    ```
    vim /opt/module/doris/fe/conf/fe.conf
    # web 页面访问端口
    http_port = 7030
    # 配置文件中指定元数据路径：默认在 fe 的根目录下，可以不配
    # meta_dir = /opt/module/doris/fe/doris-meta
    # 修改绑定 ip
    priority_networks = 192.168.9.102/24
    ```
    - 	生产环境强烈建议单独指定目录不要放在Doris安装目录下，最好是单独的磁盘
    - 	如果机器有多个IP，比如内网外网, 虚拟机docker等，需要进行IP绑定，才能正确识别。
    - JAVA_OPTS 默认Java 最大堆内存为 4GB，建议生产环境调整至 8G 以上
    - 启动FE：/opt/module/doris/fe/bin/start_fe.sh --daemon
+ 配置BE
    ```
    vim /opt/module/doris/be/conf/be.conf

    webserver_port = 7040
    # 不配置存储目录， 则会使用默认的存储目录
    storage_root_path = /opt/module/doris/doris-storage1;/opt/module/doris/doris-storage2.SSD,10
    priority_networks = 192.168.9.102/24
    mem_limit=40%
    ```
    - 同理IP需要绑定
    - storage_root_path默认在be/storage下，需要手动创建该目录。多个路径之间使用英文状态的分号;分隔（最后一个目录后不要加）
    - 可以通过路径区别存储目录的介质，HDD或SSD。可以添加容量限制在每个路径的末尾，通过英文状态逗号，隔开，如：storage_root_path=/home/disk1/doris.HDD,50;/home/disk2/doris.SSD,10;/home/disk2/doris：/home/disk1/doris.HDD,50，表示存储限制为50GB，HDD
  + 添加BE（BE需要先在FE中添加，才可加入集群）
    - 使用mysql-client连接到FE：mysql -hhadoop102 -P9030 -uroot
    - FE 默认没有密码，设置密码：SET PASSWORD FOR 'root' = PASSWORD('root');
    - 添加BE（102~104）：ALTER SYSTEM ADD BACKEND "hadoop102:9050";
    - 启动be：/opt/module/doris/be/bin/start_be.sh --daemon
    - 查看BE状态：SHOW BACKENDS：mysql -h hadoop102 -P 9030 -uroot -proot ， show proc '/backends';

### 扩容和缩容
+ FE 扩容和缩容：可以通过将FE扩容至3个以上节点（必须是奇数）来实现FE的高可用
  - 查看 FE 状态：show proc '/frontends';
+ 增加FE：
  - ALTER SYSTEM ADD OBSERVER "hadoop103:9010";
  - 分发FE相应节点，**注意需要删除元数据：rm -rf /opt/module/doris/fe/doris-meta/**
  - 启动FE（第一次需要启动命令需要添加参 --helper leader主机，edit_log_port）：/opt/module/doris/fe/bin/start_fe.sh --daemon --helper hadoop102:9010
+ 减少FE
    - ALTER SYSTEM DROP FOLLOWER[OBSERVER] "fe_host:edit_log_port";
+ BE 扩容和缩容：只需要在FE中添加或删除BE节点即可
  - 安全删除BE： ALTER SYSTEM DECOMMISSION BACKEND "be_host:be_heartbeat_service_port";
  - 当磁盘空间不足删除失败，取消删除：CANCEL DECOMMISSION BACKEND "be_host:be_heartbeat_service_port";
  - 增加BE：在MySQL客户端，通过 ALTER SYSTEM ADD BACKEND 命令增加BE