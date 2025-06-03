[toc]
***

# Hadoop
## 问题解决：
+ mysql上的数据库在Linux上无法访问
  - 连接到Windows的mysql：mysql在windows和Linux上都有安装，属于两个不同的mysql实例，数据不互通。
  - 权限不足
+ 无法解析主机名
  - 修改/etc/hosts文件，添加主机名和IP的映射
  - 修改Windows的hosts文件，添加主机名和IP的映射，C:\Windows\System32\drivers\etc\hosts
## 常用命令
+ 脚本命令：
  - zk.sh start、stop：启动、关闭Zookeeper集群
  - kfk.sh start、stop：启动、关闭Kafka集群，需要zookeeper支持
  - myhadoop.sh start、stop：启动、关闭hadoop集群
  - xcall.sh ls:在所有节点上执行ls命令
  - xsync.sh path：分发文件
  - cluster.sh start、stop：一键启动、关闭kafka集群
  - mysql_to_hdfs_full.sh all 2023-01-07：将mysql中的数据全量导入到hdfs中
+ hdfs
  - hadoop fs -mkdir -p /origin_data/ad/db/product_full/test
  - hadoop fs -text path/file：查看文件内容
+ 其他
  - scp -r job hadoop103:/opt/module/flume/ ：将job文件夹分发到hadoop103上，单独分发一台。
## 入门 
+ Hadoop2.x组成（1.x中MapReduce负责计算和资源调度，无yarn）
   - MapReduce:计算
   - Yarn:资源调度
   - HDFS:存储
   - Common:辅助工具   
+ 核心组件的配合：yarn负责资源调度，MapReduce负责计算，HDFS负责存储
+ hadoop数据一般分散储存与集群的任意三个节点上。
+ [大数据生态图](!G:\Word-Markdown\Markdown-GitHub\图片\大数据技术生态图.png)
+ 集群常用端口

|端口名|hadoop2.x|hadoop3.x|
|:--|:--|:--|
|nameNode内部通信|8020、9000|**8020**、9000、9020|
|nameNode HTTP UI|**50070**|**9870**|
|MapReduce 查看执行任务端口|8088|8088|
|历史服务器通信|19888|19888|


### 模板机安装
+ 配置静态IP：sudo vim /etc/sysconfig/network-scripts/ifcfg-ens33
  ```
  TYPE="Ethernet"
  PROXY_METHOD="none"
  BROWSER_ONLY="no"
  BOOTPROTO="static"
  DEFROUTE="yes"
  IPV4_FAILURE_FATAL="no"
  IPV6INIT="yes"
  IPV6_AUTOCONF="yes"
  IPV6_DEFROUTE="yes"
  IPV6_FAILURE_FATAL="no"
  IPV6_ADDR_GEN_MODE="stable-privacy"
  NAME="ens33"
  UUID="5bddb733-eafd-4bd2-8867-3d88b0bded83"
  DEVICE="ens33"
  ONBOOT="yes"

  IPADDR=192.168.10.102
  GATEWAY=192.168.10.2
  DNS1=192.168.10.2
  ```
+ 关闭防火墙//systemctl disable firewalld.service
+ 设置主机名称(/etc/hostname)，设置IP映射(/etc/hosts)  
#### 克隆&脚本分发
+ 克隆虚拟机，修改hostname（vim /etc/hostname）、IP、hosts
+ 安装JDK、Hadoop
#### JDK和Hadoop
+ 安装对应的JDK、hadoop，配置Linux环境变量
  - #JAVA_HOME
    export JAVA_HOME=/opt/module/jdk1.8.0_212
    export PATH=$PATH:$JAVA_HOME/bin
  - #HADOOP_HOME
    export HADOOP_HOME=/opt/module/hadoop-3.1.3
    export PATH=$PATH:$HADOOP_HOME/bin
    export PATH=$PATH:$HADOOP_HOME/sbin
+ 配置datanode的免密登录
  - ssh-keygen -t rsa //三次回车，依次生成公钥、私钥、公私钥
  - ssh-copy-id hadoop103 //分发公钥给hadoop103，实现对hadoop103的免密登录
+ 编写分发脚本xsync.sh，分发JDK、Hadoop、环境变量JAVA_HOME、HADOOP_HOME。
### Hadoop集群搭建**完全分布式模式**
+ **集群有一致性，不可单独将某台虚拟机恢复快照否则集群有崩溃可能，快照应是集群快照。**
+ 虚拟机挂起前应关闭虚拟机上的所有软件。
#### 集群规划
+ NameNode和SecondaryNameNode不要安装在同一台服务器
+	ResourceManager也很消耗内存，不要和NameNode、SecondaryNameNode配置在同一台机器上
+ 故NanmeNode在hadoop102,SecondaryNameNode在hadoop104，ResourceManager在hadoop103
#### 集群配置(需分发配置文件)
+ 根据集群规划配置core-site.xml、hdfs-site.xml、yarn-site.xml、mapred-site.xml、workers文件
+ 配置工作节点：vim /opt/module/hadoop-3.1.3/etc/hadoop/workers
  添加节点名单
##### 启动、关闭、查看集群
+ 第一次启动需格式化：hdfs namenode -format(再次格式化时需要先
  停止所有节点工作，并删除所有的$HDAOOP_HOME:data、logs文件夹)
+ 启动集群：start-all.sh(不推荐),
  **推荐：start-dfs.sh(配置了ResourceManager hadoop102节点)、start-yarn.sh(配置了YARM的hadoop103节点)**
+ 关闭集群：stop-all.sh
+ Web端查看HDFS的NameNode
  - 浏览器中输入：http://hadoop102:9870
		查看HDFS上存储的数据信息
  - Web端查看YARN的ResourceManager
    浏览器中输入：http://hadoop103:8088
    查看YARN上运行的Job信息
##### 集群日志聚集
+ 配置vim mapred-site.xml的历史服务器记录产生的日志，配置yarn-site.xml使得日志聚集与一个主机方便查看。配置见末尾。
##### 内网集群时间同步
+ 部署在外网的集群无需时间同步，可自行根据网络上时间同步
+ 选取一台主机作为时间服务器，其他主机与时间服务器同步
  - 时间主机设置：vim /etc/ntp.conf
  ```
  restrict 192.168.10.0 mask 255.255.255.0 nomodify notrap
  //设置可访问本时间服务器的网段，（10.0~10.125）
  #server 0.centos.pool.ntp.org iburst
  #server 1.centos.pool.ntp.org iburst
  #server 2.centos.pool.ntp.org iburst
  //注释掉默认时间服务器1.centos\centos2
  #server 3.centos.pool.ntp.org iburst

  server 127.127.1.0
  fudge 127.127.1.0 stratum 10 //设置本机为时间服务器

  ```
  - sudo vim /etc/sysconfig/ntpd 新增：SYNC_HWCLOCK=yes设置硬件时间也同步
  - 重启hadoop102上的ntp服务：systemctl restart ntpd.service，并设置开机自启动：systemctl enable ntpd.service
+ 其他主机配置
  - 关闭所有节点上ntp服务和自启动：systemctl stop ntpd.service,systemctl disable ntpd.service
  - 设置定时同步时间任务（以每分钟同步为例）：*/1 * * * * /usr/sbin/ntpdate hadoop102
### 常见错误解决
+ 集群崩溃处理
  - 停止所有进程->删除所有的data、logs目录->格式化NameNode(hdfs namenode -format)->启动集群
+ finallshell无法连接虚拟机：修改虚拟机网络模式为NAT、设置虚拟机IP固定、关闭防火墙、安装ssh服务、更换登录用户。

## HDFS
### 概述
+ 优缺点
  - 缺点：不适合低延时、大量小文件储存、不支持并发写入、**仅支持追加数据，不可修改**
  - 优点：高容错、适合大数据处理、高吞吐量、可构建在廉价的机器上
+ 文件分块处理，块带薪可通过设置dis.blocksize参数来设置，该参数hdfs.default中。（**大小设置：寻址时间为数据传输时间的1%为最佳，即Tc*Vc**，常见128/256）
+ namenode工作机制：文件修改操作追加到edits文件中，不修改硬盘上的元数据
  - 读取元数据时将元数据（FsImage文件）和edits文件合并
  - 但edits文件过大恢复元数据需要的时间过长。因此，需要定期进行FsImage和Edits的合并，如果这个操作由NameNode节点完成，又会效率过低。因此，引入一个新的节点SecondaryNamenode，专门用于FsImage和Edits的合并。
  - 查看edits文件：hdfs oev -i edits -o edits.xml（输出到edits.xml文件）
  - 修改hdfs-defualt.xml文件，设置edits和FsImage的合并时间间隔,dfs.namenode.checkpoint.period=3600//1小时合并一次,dfs.namenode.checkpoint.txns=1000000 dfs.namenode.checkpoint.check.period=60//每60分钟检查一次若操作数大于1000000则合并一次
+ datanode工作机制：
   - 一个数据块在DataNode上以文件形式存储在磁盘上，包括两个文件，一个是数据本身，一个是元数据包括数据块的长度，块数据的校验和，以及时间戳。
   - DataNode启动后向NameNode注册，通过后，周期性（6小时）的向NameNode上报所有的块信息。
   - DN向NN上报数据块信息的时间间隔，3s心跳一次，心跳返回NN个DN的命令，若无心疼则NN认为DN已失效。

### HDFS架构
+ NameNode(nn):储存元数据（数据之数据）
  - 管理HDFS的命名空间
  - 配置副本策略，管理数据块映射信息
  - 处理客户端读写请求
+ DataNode:数据库及其校验和 
  - 存储实际的数据块
  - 执行数据的读写操作
+ Client:客户端
  - 获取文件系统元数据位置，进行数据读写操作。
  - 管理HDFS
+ SecondaryNameNode:NameNode的备份节点（定时自动备份，2nn）
  - 辅助NameNode工作，分担其工作量，并推送给NameNode
  - 可用于辅助恢复NameNode
### HDFS的shell操作
+ HDFS上传，hadoop fs [opt/put] src dst
  - -moveFromLocal:从本地剪切粘贴到HDFS，
  - -copyFromLocal:等效与put，从本地复制粘贴到HDFS
  - -appendToFile:追加到已经存在的文件末尾
+ HDFS下载，hadoop fs [opt/get] dst src
  - -getToLocal:复制文件到本地
  - -copyToLocal:等效于get，从HDFS复制粘贴到本地
+ 命令格式：hadoop fs -参数
+ hadoop fs -help//查看命令帮助
+ hadoop fs -mkdir -p //创建多级目录
+ hadoop jar $JAVA_HOME xx.jar /input /output//运行jar包,input为输入目录，output为输出目录
+ hadoop fs -tail 1kb.txt//查看文件最后1kb内容
+ -ls、-cat、-makdir、-chgrp、chmod、chown、cp、mv、tail、rm
+ -du：统计文件大小
+ -setrep：设置副本数量
+ hdfs dfsadmin -refreshNodes //刷新NameNode节点配置
+  hdfs --daemon start namenode //启动namenode，--daemon表示后台启动
### HDFS客户端操作
### HDFS读写流程
+ 文件上传流程：
  - 客户端通过DistributedFileSystem向NameNode请求上传文件，NameNode检查目标文件是否已存在，父目录是否存在。
  - NameNode返回是否可以上传。
  - 客户端请求第一个Block上传到哪几个DataNode服务器上。
  - NameNode返回3个DataNode的地址，**选择距离最近的节点**
  - 客户端通过FSDataOutputStream请求第一个DataNode上传数据，DataNode收到请求会继续调用第二个DataNode，第三个DataNode。 
  - 三个DataNode逐级返回是否可以上传。  
  - 客户端开始往第一个DataNode上传数据，datenode1会将数据写入本地磁盘中，同时会传输给datenode2，datenode2会传给datenode3。
  - 重复步骤，直到数据全部上传完成。 


## MapReduce
### MapReduce框架
+ map阶段：读取数据，处理数据，输出数据 
+ reduce阶段：读取数据，处理数据，输出数据
+ 输入数据：HDFS
+ 输出数据：HDFS
+ 作业提交：yarn
### MapReduce优化
+ map阶段：进行部分reduce操作，减少数据传输量和减轻reduce端压力
+ 可通过mapreduce.job.reduces设置reduce数量


## yarn
### 基础知识
#### yarn工作机制
+ 节点提交任务（application）给RM申请资源，RM返回资源提交路径及applicationID。
+ 节点以job.submit()生成Job.split（任务切片，需要几个containe就有几个切片）、Job.xml、Job.jar，提交给NM，NM提交资源完毕申请运行。
+ RM生成任务(Task)并加入FIFO调度队列，调度到该Task后，选择一个NM负责运行生成一个容器在容器内运行MARppmaster成为AM，
+ 去申请任务的节点得到job.split，得到需要多少容器。
+ AM去申请容器运行MapTask，map结束后MR向RM申请容器运行ReduceTask，ReduceTask结束后AM向RM申请释放容器资源。
#### yarn框架
+ ResourceManager(RM)：集群资源调度，处理NM请求管理AM和资源。
+ NodeManager(NM)：节点资源管理,处理RM、AM的命令
+ ApplicationMaster(AM)：任务运行管理
+ Container：容器（封装了任务需要的资源，相当于一台独立服务器，一节点可有多个容器）
+ Application：应用程序（任务程序）

### yarn的scheduler和调度算法
+ hadoop3.1.3版本默认是CapacityScheduler（容量调度器），CDH框架默认调度器是FairScheduler（公平调度器），在yarn-default.xml中配置。
  - FIFO:先进先出调度，单队列。
  - Fair：公平调度，所有任务平分队列资源。**高并发集群**
  - DRF：不同资源按不同算法分配。
  - CapacityScheduler：容量调度器，多队列（每个队列采用FIFO），队列有优先级，容量，队列资源（有低保有上限，可借用其他队列空闲资源但别人一要立刻归还）,用户可配置，多用户（同一用户资源限额）。
  - FairScheduler：公平调度器，多队列（单队列调度算法可设置），队列没有优先级，队列资源均分（有低保有上限，可借用其他队列空闲资源但别人一要立刻归还），用户可配置，多用户（同一用户资源限额）
### yarn常用命令
+ yarn application -list [opt-active] 查看所有任务,可指定查询任务的类型。
  - ALL:所有任务,NEW、FINISHED、NEW_SAVING、FAILED、KILLED、SUBMITTED、ACCEPTED、RUNNING
+ yarn application -kill 任务ID ，删除任务
+ yarn logs -applicationId 任务ID ，查看任务日志
+ yarn applicationtempt -list ，查看所有尝试提交的任务
+ yarn container -list ，查看所有容器
+ yarn container -status 容器ID ，查看容器状态
+ yarn node -list -all，查看所有节点
+ yarn rmadmin -refreshQueues，**刷新队列配置**
+ yarn queue：查看队列
   - status queue_name：查看队列状态，defualt默认队列
### yarn生产核心参数（yarn-site.xml）
+ ResourceManager相关： 
  - yarn.resourcemanager.scheduler.client.thread-count：ResourceManager处理调度器请求的线程数量，默认50，生产可调大。
  - yarn.resourcemanager.scheduler.class：指定使用的调度器，默认CapacityScheduler，高并发建议使用FairScheduler。
+ NodeManager相关：
  - yarn.nodemanager.resource.detect-hardware-capabilities：是否让yarn集群对硬件资源进行检测，默认false，生产建议开启。
  - yarn.nodemanager.resource.count-logical-processors-as-cores：是否将虚拟核数当作CPU核数，默认false。
  - yarn.nodemanager.resource.pcores-vcores-multiplier：CPU核数与虚拟核数乘数，默认1
  - yarn.nodemanager.resource.memory-mb：NodeManager总的可用内存，默认8G
  - yarn.nodemanager.resource.system-reserved-memory-mb：NodeManager为系统保留的内存
  - yarn.nodemanager.resource.cpu-vcores：NodeManager总的可用CPU核数，默认8个
+ container相关：
  - yarn.scheduler.minimum-allocation-mb：单个container可申请的最小内存，默认1024MB
  - yarn.scheduler.maximum-allocation-mb：单个container可申请的最大内存，默认8192MB
  - yarn.scheduler.minimum-allocation-vcores：单个container可申请的最小CPU核数，默认1个
  - yarn.scheduler.maximum-allocation-vcores：单个container可申请的最大CPU核数，默认4个
### 容量调度器配置
+ vim capacity-scheduler.xml，多队列调度
  - 添加队列：yarn.scheduler.capacity.root.queues > default,hive
  - 添加队列属性：yarn.scheduler.capacity.root.default.capacity > 50,yarn.scheduler.capacity.root.hive.capacity > 50
  - 添加队列最大资源：yarn.scheduler.capacity.root.default.maximum-capacity > 100,yarn.scheduler.capacity.root.hive.maximum-capacity > 100
+ vim yarn-site.xml 设置优先级调度
  - yarn.cluster.max-application-priority：集群最大优先级，默认1000
  - 修改优先级命令：yarn application -appID -updatePriority  优先级

## 生产调优(企业经验)
### 核心参数
#### NameNode、datanode内存生产配置
+ vim hadoop-env.sh
  - (原则每增加10**6个数据块,namenode增加1GB运行内存,Xmx1024m)
  - DataNode同理,且namenode最小1G，datanode最小4G
  - export HDFS_NAMENODE_OPTS="-Dhadoop.security.logger=INFO,RFAS -Xmx1024m"
  - export HDFS_DATANODE_OPTS="-Dhadoop.security.logger=ERROR,RFAS -Xmx1024m"

#### NameNode心跳并发配置
+ vim hdfs-site.xml
  - 原则上线程数=ln(num_DataNode)
  - dfs.namenode.handler.count>21
  - //设置用于处理并发心跳和元数据的线程池线程数为21
    
#### 开启回收站配置
+ vim core-site.xml
  - s.trash.interval>1 //回收保存时间为1分钟
+ 回收站路径：/user/atguigu/.Trash/
+ **通过网页和程序删除的文件会被彻底删除**
### 集群压力测试
+ 通过虚拟机的网络适配器修改网络限速，向hadoop写入数据，通过yarn查看性能。

### 多目录配置
#### NameNode多目录配置（需要格式化集群，新增目录是副本）
+ vim hdfs-site.xml
  -  <name>dfs.namenode.name.dir</name>
     <value>file://${hadoop.tmp.dir}/dfs/name1,
     file://${hadoop.tmp.dir}/dfs/name2</value>

#### DataNode多目录配置（每个目录内容不一致）
+ vim hdfs-site.xml
  -  <name>dfs.datanode.data.dir</name>
     <value>file://${hadoop.tmp.dir}/dfs/data1,
     file://${hadoop.tmp.dir}/dfs/data2</value>

### 磁盘数据均衡
+ 新增空白磁盘时使用
  - 生成均衡计划（我们只有一块磁盘，不会生成计划）
  - hdfs diskbalancer -plan hadoop103
  - 执行均衡计划：
  - hdfs diskbalancer -execute hadoop103.plan.json
  - 查看当前均衡任务的执行情况
  - hdfs diskbalancer -query hadoop103
  - 取消均衡任务
  - hdfs diskbalancer -cancel hadoop103.plan.json

### 集群扩容、缩容
#### 添加白、黑名单
+ 生成白名单：vim whitelist
+ vim hdfs-site.xml
+ dfs.hosts > path_to_whitelist//允许访问的名单
+ dfs.hosts.exclude > path_to_blacklist//不允许访问的名单
+ 第一次需重启集群，非第一次刷新NameNode即可：hdfs dfsadmin -refreshNodes 
#### 新增服务器hadoop105
+ 克隆模板机，修改IP、hostname，安装ssh服务
+ 复制hadoop102的/opt/module/*、/etc/profile.d/my_env.sh
+ 删除hadoop105上的hadoop历史数据，data和logs目录
+ 配置ssh免密登录，启动DataNode
  - 启动：hdfs --daemon start datanode、yarn --daemon start nodemanager
+ 若有白名单需加入白名单，加入后续刷新：hdfs dfsadmin -refreshNodes
#### 退役服务器
+ 加入黑名单，即可。
+ 第一次需重启集群，非第一次刷新NameNode即可：hdfs dfsadmin -refreshNodes
#### 服务器之间的数据均衡（空闲datanode机器执行）
+ sbin/start-balancer.sh -threshold 10//开启服务器数据均衡，误差10%
+ sbin/stop-balancer.sh//关闭服务器数据均衡
### 储存优化
#### 纠删码（至少5台机器,datasize>2Mb）
+ 原理：通过算法将上传数据生成3块数据块、2块效验单元,5个存在3个其他2个可计算得出。
+ 查看可用纠删码策略：hdfs ec -listPolicies
+ 开启对RS-3-2-1024k策略的支持:hdfs ec -enablePolicy  -policy RS-3-2-1024k
+ 设置/input目录使用:hdfs ec -setPolicy -path /input -policy RS-3-2-1024k
#### 异构存储（冷热数据分离，热存放在RAM）
+ 查看可用异构策略：hdfs storagepolicies -listPolicies
+ 为指定路径（数据存储目录）设置指定的存储策略
  - hdfs storagepolicies -setStoragePolicy -path xxx -policy xxx
+ 获取指定路径（数据存储目录或文件）的存储策略
  - hdfs storagepolicies -getStoragePolicy -path xxx
+ 取消存储策略；执行改命令之后该目录或者文件，以其上级的目录为准，如果是根目录，那么就是HOT
  - hdfs storagepolicies -unsetStoragePolicy -path xxx
+ 查看文件块的分布
  - bin/hdfs fsck xxx -files -blocks -locations
+ 查看集群节点
  - hadoop dfsadmin -report
+ 也可通过修改hdfs-site.xml文件，配置冷热数据分离

### 集群迁移
#### Apache和Apache之间的数据迁移
+ scp -r hello.c root@hadoop105:/user/markdown //push hello.c
+ scp -r root@hadoop105:/user/markdown/hello.c .//pull hello.c
#### Apache和CDH之间的数据迁移
####

### 故障排除
#### NameNode故障处理
+ 拷贝SecondaryNameNode中数据到原NameNode存储数据目录
  - scp -r atguigu@hadoop104:/opt/module/hadoop-3.1.3/data/dfs/namesecondary/* ./name/
+ 重新启动NameNode
  - hdfs --daemon start namenode
#### 集群安全模式&磁盘修复
+ 安全模式：数据不可写，
+ 数据块损坏，hadoop进入了安全模式，导致数据不可用。
  - 分别进入集群的每个datanode节点，删除损坏的block文件
  - 离开安全模式：hdfs dfsadmin -safemode leave(进入leave换enter)
  - 删除元数据。
#### 慢磁盘监控
+ 通过心跳时间间隔大于3s
+ fio命令测试磁盘读写性能（fio -filename=/path）
  - rw=randwrite//随机写,randread随机读,rw=witer顺序写，randomrw随机混合读写
  - -size=1G//测试文件大小，-bs=4k//每次读写的块大小
  - runtime=60//测试时间，-name=test//测试文件名
#### 小文件归档
+ 解决hadoop小文件过多导致namenode内存溢出问题
+ 归档：将多个小文件打包成一个tar文件整体，需要使用其中一个文件时使用cp命令复制即可

# 配置文件
## core-site.xml
```xml
<configuration>

    <!-- 指定NameNode的地址 -->
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://hadoop102:8020</value>
    </property>
    <!-- 指定hadoop数据的存储目录 -->
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/opt/module/hadoop-3.1.3/data</value>
    </property>
    <!-- 配置HDFS网页登录使用的静态用户为atguigu -->
    <property>
        <name>hadoop.http.staticuser.user</name>
        <value>atguigu</value>
    </property>


</configuration>
```
## hdfs-site.xml
```xml
<configuration>
	<!-- nn web端访问地址-->
	<property>
        <name>dfs.namenode.http-address</name>
        <value>hadoop102:9870</value>
    </property>
	<!-- 2nn web端访问地址-->
    <property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>hadoop104:9868</value>
    </property>
</configuration>
```
## yarn-site.xml
```xml
<configuration>
    <!-- 指定MR走shuffle -->
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <!-- 指定ResourceManager的地址-->
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>hadoop103</value>
    </property>
    <!-- 环境变量的继承 -->
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    </property>

    <!-- 开启日志聚集功能 -->
    <property>
        <name>yarn.log-aggregation-enable</name>
        <value>true</value>
    </property>
    <!-- 设置日志聚集服务器地址 -->
    <property>  
        <name>yarn.log.server.url</name>  
        <value>http://hadoop102:19888/jobhistory/logs</value>
    </property>
    <!-- 设置日志保留时间为7天 -->
    <property>
        <name>yarn.log-aggregation.retain-seconds</name>
        <value>604800</value>
    </property>

</configuration> 
```
## mapred-site.xml
```xml
<configuration>
	<!-- 指定MapReduce程序运行在Yarn上 -->
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>

<!-- 历史服务器端地址，10020为端口 -->
<property>
    <name>mapreduce.jobhistory.address</name>
    <value>hadoop102:10020</value>
</property>
<!-- 历史服务器web端地址 -->
<property>
    <name>mapreduce.jobhistory.webapp.address</name>
    <value>hadoop102:19888</value>
</property>

```