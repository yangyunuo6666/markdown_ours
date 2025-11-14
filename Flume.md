[toc]

***

# Flume
+ 分布式的海量日志采集、聚合和传输的系统,基于流式架构,**实时监控flume软件：Ganglia**
+ (flume配置模板查询网站)：[http://flume.apache.org/FlumeUserGuide.html],找到对应的组件，点击进去，找到Configuration Options，即可查看配置模板
+ [flume文档查看地址](http://flume.apache.org/FlumeUserGuide.html)
+ 数据读取与传输：
  - 事务机制：保存在data、checkpoint文件夹中
  - 读取偏移量：以一个json文件保存偏移量，数据文件单独保存。
+ Event:传输单元，Flume数据传输的基本单元，以事件的形式将数据从源头送至目的地。
+ 架构
  - Flume 的基本部署单元是 Agent，每个 Agent 由三个核心组件构成：Source、Channel(缓冲) 和 Sink，数据流通过它们形成单向管道（Source → Channel → Sink）
  - Web Server -> Agent -> HDFS
+ Agent(JVM进程，以事件组织数据)组件
  - Source是负责接收数据到Flume Agent的组件。Source组件可以处理各种类型、各种格式的日志数据，包括avro、thrift、exec、jms、spooling directory、netcat、sequence generator、syslog、http、legacy。
  - Channel是位于Source和Sink之间的缓冲区。Flume自带两种Channel：Memory Channel和File Channel。Memory Channel内存型，性能高，但可靠性低；File Channel磁盘型可靠性高，但性能低。
  - Sink不断地轮询Channel中的事件且批量地移除它们，并将这些事件批量写入到存储或索引系统、或者被发送到另一个Flume Agent。Sink是完全事务性的。
+ Channel slectors：
  - Replicating：将source过来的events复制到所有的channel中
  - Multiplexing：根据event的属性，将event路由到不同的channel中
+ source自定义：实现Source接口，并实现相应方法

## flume调优&事务机制
### 调优
+ Source：
  - 增加Source个（使用Tair Dir Source时可增加FileGroups个数）可以增大Source的读取数据的能力。
  - eg：当某一个目录产生的文件过多时需要将这个文件目录拆分成多个文件目录，同时配置好多个Source
  - batchSize参数决定Source一次批量运输到Channel的event条数，适当调大这个参数可以提高Source搬运Event到Channel时的性能
+ Channel：
  - type选择memory时Channel的性能最好，但是如果Flume进程意外挂掉可能会丢失数据。
  - type选择file时Channel的容错性更好，但是性能上会比memory channel差
  - Capacity 参数决定Channel可容纳最大的event条数。transactionCapacity 参数决定每次Source往channel里面写的最大event条数和每次Sink从channel里面读的最大event条数。transactionCapacity需要大于Source和Sink的batchSize参数。
+ sink：
  - 增加Sink的个数可以增加Sink消费event的能力。Sink也不是越多越好够用就行，过多的Sink会占用系统资源，造成系统资源不必要的浪费
  - batchSize参数决定Sink一次批量从Channel读取的event条数，适当调大这个参数可以提高Sink从Channel读取event的性能。
### 事务机制
+ Flume使用两个独立的事务分别负责从Soucrce到Channel，以及从Channel到Sink的事件传递。

## flume部署
+ 将apache-flume-1.7.0-bin.tar.gz上传到linux的/opt/software目录下
+ 解压apache-flume-1.7.0-bin.tar.gz到/opt/module/目录下
  ```
  [atguigu@hadoop102 software]$ tar -zxf apache-flume-1.7.0-bin.tar.gz -C /opt/module/
  ```
+ 修改apache-flume-1.7.0-bin的名称为flume
  ```
  [atguigu@hadoop102 module]$ mv apache-flume-1.7.0-bin flume
  ```
+ 删除./lib/guava-11.0.2.jar，因为hadoop的classpath中已经有了guava.jar，**避免冲突,兼容hadoop3.1.3**
+ 将flume/conf下的flume-env.sh.template文件修改为flume-env.sh，并配置flume-env.sh文件
  ```
  [atguigu@hadoop102 conf]$ mv flume-env.sh.template flume-env.sh
  [atguigu@hadoop102 conf]$ vi flume-env.sh
  export JAVA_HOME=/opt/module/jdk1.8.0_144
  ```
+ 修改日志文件保存位置：vim log4j.properties
  - `<Property name="LOG_DIR">/opt/module/flume/log</Property>`
+ 生产配置：
  - 在flume目录下创建jobs文件夹并进入，创建一个配置文件netcat-flume-logger.conf(端口-flume-控制台.配置)
  - flume-telnet-logger.conf内容如下：
    ```
    # Name the components on this agent，命名组件
    a1.sources = r1
    a1.sinks = k1
    a1.channels = c1

    # Describe/configure the source,source类型配置
    a1.sources.r1.type = netcat #输入源为netcat端口类型
    a1.sources.r1.bind = localhost
    a1.sources.r1.port = 44444

    # Describe the sink，输出类型配置
    a1.sinks.k1.type = logger #输出源为控制台类型

    # Use a channel which buffers events in memory#缓冲区类型配置
    a1.channels.c1.type = memory #总是内存缓冲区
    a1.channels.c1.capacity = 1000 #channel中可存储的最大事件数
    a1.channels.c1.transactionCapacity = 100 #一次最大事务数量

    # Bind the source and sink to the channel，绑定source和sink到channel
    a1.sources.r1.channels = c1
    a1.sinks.k1.channel = c1
    ```

## flume读取hdfs的hive日志案例
+ 1．Flume要想将数据输出到HDFS，必须持有Hadoop相关jar包，拷贝到flume的lib目录下
  ```
  commons-configuration-1.6.jar、
  hadoop-auth-2.7.2.jar、
  hadoop-common-2.7.2.jar、
  hadoop-hdfs-2.7.2.jar、
  commons-io-2.4.jar、
  htrace-core-3.1.0-incubating.jar
  ```
+ 2．创建flume配置文件flume-flie-hdfs.conf
  - 要想读取Linux系统中的文件（即本地文件），就得按照Linux命令的规则执行命令。由于Hive日志在Linux系统中所以读取文件的类型选择：exec即execute执行的意思。表示执行Linux命令来读取文件。
  ```
  # Name the components on this agent
  a2.sources = r2
  a2.sinks = k2
  a2.channels = c2
  
  # Describe/configure the source
  a2.sources.r2.type = exec
  a2.sources.r2.command = tail -F /opt/module/hive/logs/hive.log
  a2.sources.r2.shell = /bin/bash -c

  # Describe the sink
  a2.sinks.k2.type = hdfs
  a2.sinks.k2.hdfs.path = hdfs://hadoop102:9000/flume/%Y%m%d/%H
  #上传文件的前缀
  a2.sinks.k2.hdfs.filePrefix = logs-
  #是否按照时间滚动文件夹
  a2.sinks.k2.hdfs.round = true
  #多少时间单位创建一个新的文件夹
  a2.sinks.k2.hdfs.roundValue = 1
  #重新定义时间单位
  a2.sinks.k2.hdfs.roundUnit = hour
  #是否使用本地时间戳
  a2.sinks.k2.hdfs.useLocalTimeStamp = true
  #积攒多少个Event才flush到HDFS一次
  a2.sinks.k2.hdfs.batchSize = 1000
  #设置文件类型，可支持压缩
  a2.sinks.k2.hdfs.fileType = DataStream
  #多久生成一个新的文件
  a2.sinks.k2.hdfs.rollInterval = 600
  #设置每个文件的滚动大小
  a2.sinks.k2.hdfs.rollSize = 134217700
  #文件的滚动与Event数量无关
  a2.sinks.k2.hdfs.rollCount = 0
  #最小冗余数
  a2.sinks.k2.hdfs.minBlockReplicas = 1

  # Use a channel which buffers events in memory
  a2.channels.c2.type = memory
  a2.channels.c2.capacity = 1000
  a2.channels.c2.transactionCapacity = 100

  # Bind the source and sink to the channel
  a2.sources.r2.channels = c2
  a2.sinks.k2.channel = c2
  ```
+ 执行监控配置
  ```
  bin/flume-ng agent --conf conf/ --name a2 --conf-file job/flume-file-hdfs.conf
  ```
  - --conf conf/  ：表示配置文件存储在conf/目录
	- --name a1	：表示给agent起名为a1
	- --conf-file job/flume-telnet.conf ：flume本次启动读取的配置文件是在job文件夹下的flume-telnet.conf文件。
	- -Dflume.root.logger==INFO,console ：-D表示flume运行时动态修改flume.root.logger参数属性值，并将控制台日志打印级别设置为INFO级别。日志级别包括:log、info、warn、error。


## 问题解决：
+ flume零点漂移问题：
  - 问题描述：flume读取hdfs日志，发现日志时间与当前时间相差8小时
  - 解决方案：在flume配置文件中添加hdfs.useLocalTimeStamp = true































