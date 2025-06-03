[toc]

***
# Kafka:消息中间件
+ JMS: Java Message Service,定义了Java中间件的标准。
  - JMS Provider：JMS 消息的提供者,提供JMS服务的软件系统
  - JMS Producer：消息的生产者
  - JMS Consumer：消息的消费者
  - JMS Message：消息（data），包含消息头、属性、消息内容。
+ 可视化工具：kafka_tool,注意配置kafka主机有三个端口看配置文件
+ 查看有错的日志：cat /opt/module/kafka/logs/server.log | grep -i "error\|warn"
+ JMS消息模型
  - 点对点模型（P2P）：消息生产者生产消息发送到队列中，消息消费者从队列中取出消息进行消费，消息被消费后队列中不在保存。
  - 发布/订阅模型（Pub/Sub）：消息生产者（发布者）将消息发布到主题中，消息消费者（订阅者，允许多人同时订阅）从主题中订阅消息。Kafka采用的就是这种模型。
+ 通信
  - 线程通信：通过堆共享数据。
  - 进程通信：通过Socket网络通信，kafka底层为网络通信，kafka是一个进程
+ Java消息中间件
  
|特性|ActiveMQ|RabbitMQ|RocketMQ|Kafka|
|---|---|---|---|---|
|开发语言|Java|Erlang|Java|Scala,java|
|单机吞吐量|万级|万级|十万级|几十万级|
|topic数量对吞吐量的影响|topic越多，吞吐量越低|无|Topiic可达到几千量级|Topiic可达到几百量级，更多吞吐量下降|
|延迟|ms级|us级|ms级|ms级|
|可用性|高|高|非常高|非常高|
|消息可靠性|有较低的概率丢失数据|有较低的概率丢失数据|经过参数优化配置，可以做到0丢失|经过参数优化配置，可以做到0丢失|
|功能支持|MQ领域功能完备|高并发，延时最低|MQ完善，分布式，拓展性好|功能简单，支持简单的MQ功能|

+ Kafka特点
  - 文件后缀为.log，每个文件有一个offset偏移量，表示文件中消息的起始位置。
  - 修改server.properties配置文件中log.dirs=/tmp/kafka-logs，默认端口9092
  - Zookeeper：Kafka依赖Zookeeper，Kafka使用Zookeeper来保存集群的元数据，包括集群的broker列表，topic列表，partition列表，consumer列表等。

## 问题解决
+ 集群非正常关闭后，kafka无法启动（或多台机器仅一台成功）
  - 关闭集群，删除zeekoop中保存的kafka集群元数据、zookeeper、kafka日志，更正配置文件，重新启动zookeeper
  - 路径：/opt/module/zookeeper/Data/version-2

## KRaft模式
+ 在4.1.0版本之后，Kafka将Zookeeper替换为KRaft模式，KRaft模式是Kafka Raft协议的实现，KRaft模式将Zookeeper替换为Raft协议，Raft协议是一种分布式一致性协议，用于保证分布式系统中的数据一致性。基于Java8
+ 优点
  - 提高可扩展性——KRaft 的恢复时间比 ZooKeeper 快一个数量级。这使我们能够有效地扩展到单个集群中的数百万个分区。ZooKeeper 的有效限制是数万
  - 更有效的元数据传播——基于日志、事件驱动的元数据传播可以提高 Kafka 的许多核心功能的性能。另外它还支持元数据主题的快照。
  - 由于不依赖zookeeper，集群扩展时不再受到zookeeper读写能力限制；
  - controller不再动态选举，而是由配置文件规定。这样我们可以有针对性的加强controller节点的配置，而不是像以前一样对随机controller节点的高负载束手无策

### kraft模式配置
+ 修改config/kraft/server.properties配置文件
```
#kafka的角色（controller相当于主机、broker节点相当于从机，主机类似zk功能）
process.roles=broker, controller
#节点ID
node.id=1
#controller服务协议别名
controller.listener.names=CONTROLLER
#全Controller列表
controller.quorum.voters=1@kafka-broker1:9093,2@kafka-broker2:9093,3@kafka-broker3:9093
#不同服务器绑定的端口
listeners=PLAINTEXT://:9092,CONTROLLER://:9093
#broker服务协议别名
inter.broker.listener.name=PLAINTEXT
#broker对外暴露的地址
advertised.listeners=PLAINTEXT://kafka-broker1:9092
#协议别名到安全协议的映射
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
#kafka数据存储目录
log.dirs=/opt/module/kafka-kraft/datas
```  
+ 修改不同节点的配置  
  - 不同节点需要对node.id相应改变，值需要和controller.quorum.voters对应
  - 不同节点需要根据各自的主机名称，修改相应的advertised.listeners地址。
### 初始化集群数据目录
+ 首先在每个部署节点生成存储目录唯一ID
+ 进入kafka目录：cd /opt/module/kafka-kraft
+ 生产存储ID：bin/kafka-storage.sh random-uuid J7s9e8PPTKOO47PxzI39VA
  -	用生成的ID格式化每一个kafka数据存储目录
  bin/kafka-storage.sh format -t J7s9e8PPTKOO47PxzI39VA -c /opt/module/kafka-kraft/config/kraft/server.properties


## kafka项目架构
+ main-producer
  - 创建生产者对象：KafkaProducer<String, String> producer = new KafkaProducer<>(props);
  - 参数设置：Map<String,Object> configMap = new HashMap<>();
    - 设置配置参数：configMap.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    -  设置K、v序列化参数：configMap.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
       configMap.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
  - 创建消息： ProducerRecord<String, String> record = new ProducerRecord<>("test", key:a1,value: "hello kafka");
  - 通过生产者对象发送消息: producer.send(record);
  - 关闭生产者对象: producer.close();
+ main-consumer
  - 创建消费者对象：KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
  - 参数设置：Map<String,Object> configMap = new HashMap<>();
    - 设置配置参数：configMap.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    - 设置组id:configMap.put(ConsumerConfig.GROUP_ID_CONFIG, "group1");
    - 设置K、v反序列化参数：configMap.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
      configMap.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
  - 订阅主题：consumer.subscribe(Collections.singletonList("test"));
  - 拉取消息：ConsumerRecords<String, String> records = consumer.poll(100);
    - 遍历消息：for (ConsumerRecord<String, String> record : records) {
      - 处理消息：System.out.println("key: " + record.key() + ", value: " + record.value());
    }
  - 关闭消费者对象：consumer.close();
+ 相关知识点
  - 多个消费者组成消费者组，多个生产者组成生产者组。 
  - 为保证数据可靠性，仅有一个文件(leader)可提供读写操作，其他为副本(follower)。 
  - Broker:服务节点,可有备份,Partition:分区,副本:leader和follower
  - Broker通过网络连接所有分区。
  - Broker:服务节点挂掉后，由zookeper从备份中选举新的leader

## kafka底层知识
### 框架
+ Zookeeper中有多个node，kafka的Broker通过监听这些node的变化来获取集群信息
+ kafka的多个Broker谁先选举上谁获得集群控制权，选举上后创建/controller 
#### Zookeeper
  - /controller:保存当前集群的controller信息
  - /brokers/ids:保存当前集群的broker_id信息
  - /brokers/topics:保存当前集群的topic信息，每个主题创建需要名字、分区数量、副本数量
  - /brokers/topics/{topic_name}/partitions:保存当前集群的topic的partition信息
  - /brokers/topics/{topic_name}/partitions/{partition_id}/state:保存当前集群的topic的partition的leader和follower信息
  - /consumers:保存当前集群的消费者组信息
  - /consumers/{group_id}/offsets:保存当前集群的消费者组消费的topic的partition的offset信息
  - /consumers/{group_id}/ids:保存当前集群的消费者组消费的topic的partition的consumer_id信息
  - /admin/config:保存当前集群的配置信息
#### 集群启动流程
  - 第一个broker:注册Broker节点、监听/controller节点变化(当前节点变化)、
    注册/controller节点、选举成为/controller节点、
    监听/brokers/ids节点(子节点变化)
  - 第二个broker:注册Broker节点、监听/controller节点变化(当前节点变化)、
    注册/controller节点、通知集群变化
    连接brokers，发送集群相关数据
  - 第三个broker:注册Broker节点、监听/controller节点变化(当前节点变化)、
    注册/controller节点、通知集群变化
    连接brokers，发送集群相关数据
+ /controller节点的删除
  - 通知节点删除、zookeeper选举、注册/controller节点、
    增加监听器、连接所有brokers发送集群相关数据
+ 通信
  - broker与zookeeper通信：通过zookeeper的client
  - controller与broker通信：通过JDK1.4 NIO : Channel、Buffer、Selector、SelectionKey
+ kafkaserver：提供服务接口，kafkaapis：提供接口实现。
+ broker组件
  - LogManager：日志管理器，负责读写数据
  - Controller：控制器，负责集群的元数据管理、副本的选举等操作
  - ZKClient：zookeeper客户端，负责与zookeeper通信
  - SocketServer：网络通信服务器，端口9092
  - replicaManager：副本管理器，负责副本的创建、删除、选举等操作
  - NetworkClient：网络通信客户端，端口9092
  - Apis：提供接口服务
  
+ 工作流程：生产者生成数据，经过拦截器interceptor、序列化器、分区器，发送到broker，broker将数据写入到磁盘，
  消费者从broker拉取数据，经过拦截器、反序列化器、消费者组协调器，消费数据。 
  [kafka工作流图](G:\Word-Markdown\Markdown-GitHub\图片\kafka工作流.png)

+ 数据生产者（KafkaProducer）：生产者对象，用于对我们的数据进行必要的转换和处理，将处理后的数据放入到数据收集器中，类似于生产者消费者模式下的生产者。这里我们简单介绍一下内部的数据转换处理：
  - 如果配置拦截器栈（interceptor.classes），那么将数据进行拦截处理。某一个拦截器出现异常并不会影响后续的拦截器处理。
  - 因为发送的数据为KV数据，所以需要根据配置信息中的序列化对象对数据中Key和Value分别进行序列化处理。
  - 计算数据所发送的分区位置，**若以partition指定了会不被校验直接使用分区号。**
  - 将数据追加到数据收集器中。

+	数据收集器（RecordAccumulator）：用于收集，转换我们产生的数据，类似于生产者消费者模式下的缓冲区。为了优化数据的传输，Kafka并不是生产一条数据就向Broker发送一条数据，而是通过合并单条消息，进行批量（批次）发送，提高吞吐量，减少带宽消耗。
  - 默认情况下，一个发送批次的数据容量为16K，这个可以通过参数batch.size进行改善。
  - 批次是和分区进行绑定的。也就是说发往同一个分区的数据会进行合并，形成一个批次。
  - 如果当前批次能容纳数据，那么直接将数据追加到批次中即可，如果不能容纳数据，那么会产生新的批次放入到当前分区的批次队列中，这个队列使用的是Java的双端队列Deque。旧的批次关闭不再接收新的数据，等待发送

+ 数据发送器（Sender）：线程对象，用于从收集器对象中获取数据，向服务节点发送。类似于生产者消费者模式下的消费者。因为是线程对象，所以启动后会不断轮询获取数据收集器中已经关闭的批次数据。对批次进行整合后再发送到Broker节点中
  - 因为数据真正发送的地方是Broker节点，不是分区。所以需要将从数据收集器中收集到的批次数据按照可用Broker节点重新组合成List集合。
  - 将组合后的<节点，List<批次>>的数据封装成客户端请求（请求键为：Produce）发送到网络客户端对象的缓冲区，由网络客户端对象通过网络发送给Broker节点。
  - Broker节点获取客户端请求，并根据请求键进行后续的数据处理：向分区中增加数据。

#### 数据校验级别：
  - ACKS = 0:无需等待服务端响应，只管发送数据即可，吞吐量最高，可靠性最低，效率最高。
  - **ACKS = 1**:等待服务端响应，只要服务端响应成功，就认为数据发送成功，吞吐量较高，可靠性中等，效率中等，中庸之策。
  - ACKS = -1:等待服务端响应，只要服务端响应成功，就认为数据发送成功，吞吐量最低，可靠性最高，效率最低。
+ 重试次数可调节：retries

+ 数据传输语义
  - at most once:最多一次，数据可能会丢失，但不会重复。
  - at least once:最少一次，数据不会丢失，但可能会重复。
  - exactly once:精确一次，数据不会丢失，也不会重复。（幂等+事务+ACK）

#### 事务：保证幂等性，保证数据一致性
+ 需通过修改scanlan源码。
+ 事务流程：producer查找事务管理器所在的节点、事务初始、
  初始化生产者id、将数据所在分区信息传回事务管理器、生产数据、
  leader提交保存成功的数据分区信息、事务提交
  修改事务状态、写入事务标记、修改事务状态为完成。

#### 数据存储基础流程
+ ReplicaManager(kafka启动创建) : 副本管理器组件，用于提供主题副本的相关功能，
  在数据的存储前进行ACK校验和事务检查,并提供数据请求的响应处理
+ Partition : 分区对象，主要包含分区状态变换的监控,分区上下线的处理等功能，
  在数据存储是主要用于对分区副本数量的相关校验，并提供追加数据的功能
+ UnifiedLog : 同一日志管理组件，用于管理数据日志文件的新增，
  删除等功能，并提供数据日志文件偏移量的相关处理。
+ LocalLog : 本地日志组件，管理整个分区副本的数据日志文件。
  假设当前主题分区中有3个日志文件,那么3个文件都会在组件中进行管理和操作。
+ LogSegment : 文件段组件，对应具体的某一个数据日志文件，
  假设当前主题分区中有3个日志文件,
  那么3个文件每一个都会对应一个LogSegment组件,
  并打开文件的数据管道FileChannel。数据存储时,
  就是采用组件中的FileChannel实现日志数据的追加
+ LogConfig: 日志配置对象，常用的数据存储配置

+ 索引文件：Kafka的索引文件中的索引信息是不连续的，而且为了效率，
  kafka默认情况下，4kb的日志数据才会记录一次索引，
  但是这个是可以进行配置修改的，参数为log.index.interval.bytes，
  默认值为4096。所以我们有的时候会将kafka的不连续索引数据称之为稀疏索引。
#### 数据刷写
+ 在Linux系统中，当我们把数据写入文件系统之后，
  其实数据在操作系统的PageCache（页缓冲）里面，并没有刷到磁盘上。
  如果操作系统挂了，数据就丢失了。
  一方面，应用程序可以调用fsync这个系统调用来强制刷盘，
  另一方面，操作系统有后台线程，定时刷盘。
  频繁调用fsync会影响性能，需要在性能和可靠性之间进行权衡。
  实际上，Kafka提供了参数进行数据的刷写
+ 参数
  - log.flush.interval.messages ：达到消息数量时，会将数据flush到日志文件中
  - log.flush.interval.ms ：间隔多少时间(ms)，执行一次强制的flush操作。
  - flush.scheduler.interval.ms：所有日志刷新到磁盘的频率
  - log.flush.interval.messages和log.flush.interval.ms无论哪个达到，都会flush。官方不建议通过上述的三个参数来强制写盘，数据的可靠性应该通过replica来保证，而强制flush数据到磁盘会对整体性能产生影响。

#### 副本数据同步流程
+ 副本(Follower)节点中FetcherThread线程会不断的从Leader节点中拉取数据，
  并追加到本地日志文件中。
+ 消费者可以从Leader节点中拉取数据，也可以从Follower节点中拉取数据，到能获取的数据必须是所有副本共有的数据。

#### 日志清理策略
+ Kafka软件的目的本质是用于传输数据，而不是存储数据，但是为了均衡生产数据速率和消费者的消费速率，所以可以将数据保存到日志文件中进行存储。默认的数据日志保存时间为7天，可以通过调整如下参数修改保存时间：
  -	log.retention.hours：小时（默认：7天，最低优先级）
  -	log.retention.minutes，分钟
  -	log.retention.ms，毫秒（最高优先级）
  -	log.retention.check.interval.ms，负责设置检查周期，默认5分钟。
  日志一旦超过了设置的时间，Kafka中提供了两种日志清理策略：delete和compact。
  -	delete：将过期数据删除
  -	log.cleanup.policy = delete（所有数据启用删除策略）
+ **基于时间：默认打开**。以segment中所有记录中的最大时间戳作为该文件时间戳。
+ 基于大小：默认关闭。超过设置的所有日志总大小，删除最早的segment。log.retention.bytes，默认等于-1，表示无穷大

#### 消费数据
+ 建Map类型的配置对象，根据场景增加相应的配置属性
+ 创建消费者对象：根据配置创建消费者对象KafkaConsumer，
  向Kafka订阅（subscribe）主题消息，并向Kafka发送请求（poll）获取数据。
+ 获取数据：Kafka会根据消费者发送的参数，返回数据对象ConsumerRecord。
  返回的数据对象中包括指定的数据。
+ 关闭消费者：KafkaConsumer.close()方法关闭消费者，释放资源。

+ 消费者组
  - 同组消费者中对于同一个分区的数据仅有一个消费者可消费。
  - 组员数量多于分区数量，则部分消费者无法消费数据，作为备用消费者存在。
  - 消费者具体消费那个分区数据，由组中leader分配，遵循粘性分配

+ 偏移量offset：偏移量offset是消费者消费数据的一个非常重要的属性。
  默认情况下，消费者如果不指定消费主题数据的偏移量，那么消费者启动消费时，
  无论当前主题之前存储了多少历史数据，消费者只能从连接成功后当前主题
  最新的数据偏移位置读取，而无法读取之前的任何数据，
  如果想要获取之前的数据，就需要设定配置参数或指定数据偏移量。

+ 起始偏移量：在消费者的配置中，我们可以增加偏移量相关参数
  auto.offset.reset，用于从最开始获取主题数据，
  - latest：对于同一个消费者组，消费者只能消费到连接topic后，
    新产生的数据（未提交偏移量的场合）。
  - earliest：对于同一个消费者组，从头开始消费。

+ 偏移量提交
  - 自动提交：默认情况下，消费者会定期自动提交偏移量。
  - 手动提交：需要禁用自动提交auto.offset.reset=false，才能开启手动提交
  - 异步提交：向Kafka发送偏移量offset提交请求后，就可以直接消费下一批数据，
    因为无需等待kafka的提交确认，所以无法知道当前的偏移量一定提交成功，
    所以安全性比较低，但相对，消费性能会提高

+ 事务(支持不同的事务隔离级别)
  - 已提交读：read_committed
  - 未提交读：read_uncommitted


#### Controller选举
+ 先在Zookeeper上创建临时节点/controller成功的Broker就是Controller。
  Controller重度依赖Zookeeper，依赖zookeepr保存元数据，依赖zookeeper进行
  服务发现。Controller大量使用Watch功能实现对集群的协调管理。如果此时，
  作为Controller的Broker节点宕掉了。那么zookeeper的临时节点/controller
  就会因为会话超时而自动删除。而监控这个节点的Broker就会收到通知而
  向ZooKeeper发出创建/controller节点的申请，一旦创建成功，那么创建
  成功的Broker节点就成为了新的Controller
+ 脑裂现象：网络的抖动，不稳定，导致和ZooKeeper之间的会话超时，集群放弃当前
  leader选举出新leader，然后网络恢复，老的leader重新连接上ZooKeeper，
  ZooKeeper会再次发起leader选举，导致集群中存在两个leader，这就是脑裂现象。
  - Kafka通过一个任期（epoch:纪元）的概念来解决，也就是说，
    每一个Broker当选Controller时，会告诉当前Broker是第几任Controller，
    一旦重新选举时，这个任期会自动增1，那么不同任期的Controller的epoch值
    是不同的，那么旧的controller一旦发现集群中有新任controller的时候，
    那么它就会完成退出操作（清空缓存，中断和broker的连接，并重新加载最新
    的缓存），让自己重新变成一个普通的Broker。

####  Broker上线下线
+ Controller 在初始化时，会利用 ZK 的 watch 机制注册很多不同类型的监听器，
  当监听的事件被触发时，Controller 就会触发相应的操作。
  Controller 在初始化时，会注册多种类型的监听器，主要有以下几种：
  -	监听 /admin/reassign_partitions 节点，用于分区副本迁移的监听
  -	监听 /isr_change_notification 节点，用于 Partition ISR 变动的监听
  -	监听 /admin/preferred_replica_election 节点，用于需要进行 Partition 最优 leader 选举的监听
  -	监听 /brokers/topics 节点，用于 Topic 新建的监听
  -	监听 /brokers/topics/TOPIC_NAME 节点，用于 Topic Partition 扩容的监听
  -	监听 /admin/delete_topics 节点，用于 Topic 删除的监听
  -	监听 /brokers/ids 节点，用于 Broker 上下线的监听。
+ 每台 Broker 在上线时，都会与ZK建立一个建立一个session，
  并在 /brokers/ids下注册一个节点，节点名字就是broker id，这个节点是临时
  节点，该节点内部会有这个 Broker 的详细节点信息。Controller会监听
  /brokers/ids这个路径下的所有子节点，如果有新的节点出现，那么就代表有新的
  Broker上线，如果有节点消失，就代表有broker下线，Controller会进行相应的
  处理，Kafka就是利用ZK的这种watch机制及临时节点的特性来完成集群 Broker的
  上下线。无论Controller监听到的哪一种节点的变化，都会进行相应的处理，
  同步整个集群元数据

### 零拷贝
+ 零拷贝技术，在Kafka中，零拷贝技术被大量使用，零拷贝技术可以减少数据
  在内核空间和用户空间之间的拷贝次数，从而减少CPU的上下文切换次数，
  提高数据传输的效率。
+ 零拷贝实现：数据发送给消费者时间不经过kafka的broker，而是OS通过特权指令
  直接从文件系统发送给消费者

### 顺写日志
+ Kafka的日志文件是顺序写入的，顺序写入的效率比随机写入的效率高很多。
+ kafka文件是保存在内存中的数组内，每次将数据追加到文件末尾即可，无需查找位置

 
## Linux集群部署
+ 集群规划：3台机器，每台机器上部署1个Zookeeper，1个Kafka Broker
+ Zookeeper客户端工具安装
  - 我们可以通过ZooKeeper软件自带命令行客户端对保存的信息进行访问，也可以采用一些工具软件进行访问，prettyZoo-win.msi安装包默认安装即可。
  - 通过主机名和端口号进行连接
+ 查看有错的日志：cat /opt/module/kafka/logs/server.log | grep -i "error\|warn"

### Linux集群部署问题解决
+ 集群非正常关闭后，kafka无法启动（或多台机器仅一台成功）
  - 关闭集群，删除zeekoop中保存的kafka集群元数据、zookeeper、kafka日志，更正配置文件，重新启动zookeeper
  - 路径：/opt/module/zookeeper/Data/version-2
+ 混合模式启动导致kafka某一台无法启动
  - 在kafka2.4后支持与zookeeper解耦合，同时也支持依赖zookeeper运行的模式。
  - 当配置文件中同时选了两个即为混合模式，导致kafka无法启动



### zookeeper服务操作    
+ 启动ZooKeeper
  + 在每个节点下执行如下操作
  + 进入zookeeper目录: cd /opt/module/zookeeper
  + 启动ZK服务: bin/zkServer.sh start
+ 关闭ZooKeeper
  + 在每个节点下执行如下操作
  + 进入zookeeper目录: cd /opt/module/zookeeper
  + 关闭ZK服务: bin/zkServer.sh stop
+ 查看ZooKeeper状态
  + 在每个节点下执行如下操作
  + 进入zookeeper目录: cd /opt/module/zookeeper
  + 查看ZK服务状态: bin/zkServer.sh status


### 配置Zookeeper
+ 配置服务器编号
 -	在/opt/module/zookeeper/目录下创建zkData
 - 在zkData目录下创建myid文件，文件内容为1
+ 修改配置文件
  - 重命名/opt/module/zookeeper/conf目录下的zoo_sample.cfg文件为zoo.cfg文件
  - 修改zoo.cfg文件，新增：
    ```
    # 以下内容为修改内容
    dataDir=/opt/module/zookeeper/zkData

    # 以下内容为新增内容
    ####################### cluster ##########################
    # server.A=B:C:D
    #
    # A是一个数字，表示这个是第几号服务器
    # B是A服务器的主机名
    # C是A服务器与集群中的主服务器（Leader）交换信息的端口
    # D是A服务器用于主服务器（Leader）选举的端口
    #########################################################
    server.1=hadoop102:2888:3888
    server.2=hadoop103:2888:3888
    server.3=hadoop104:2888:3888
    ```
+ 修改日志文件保存位置：vim /opt/module/zookeeper/conf/log4j.properties
  - log.dirs=/opt/module/zookeeper/logs
+ 分别将不同虚拟机/opt/module/zookeeper/zkData目录下myid文件进行修改
  - vim /opt/module/zookeeper/zkData/myid
  - hadoop102:1
  - hadoop103:2
  - hadoop104:3

### 配置kafka
+ 进入cd /opt/module/kafka/config文件目录
+ 修改配置文件：vim server.properties
```
#broker的全局唯一编号，每个服务节点不能重复，只能是数字。
node.id=1
#broker对外暴露的IP和端口 （每个节点单独配置）
advertised.listeners=PLAINTEXT://hadoop102:9092
#处理网络请求的线程数量
num.network.threads=3
#用来处理磁盘IO的线程数量
num.io.threads=8：
#发送套接字的缓冲区大小
socket.send.buffer.bytes=102400
#接收套接字的缓冲区大小
socket.receive.buffer.bytes=102400
#请求套接字的缓冲区大小
socket.request.max.bytes=104857600
#kafka运行日志(数据)存放的路径，路径不需要提前创建，kafka自动帮你创建，可以配置多个磁盘路径，路径与路径之间可以用"，"分隔
log.dirs=/opt/module/kafka/logs
#topic在当前broker上的分区个数
num.partitions=1
#用来恢复和清理data下数据的线程数量
num.recovery.threads.per.data.dir=1
# 每个topic创建时的副本数，默认时1个副本
offsets.topic.replication.factor=1
#segment文件保留的最长时间，超时将被删除
log.retention.hours=168
#每个segment文件的大小，默认最大1G
log.segment.bytes=1073741824
# 检查过期数据的时间，默认5分钟检查一次是否数据过期
log.retention.check.interval.ms=300000
#配置连接Zookeeper集群地址（在zk根目录下创建/kafka，方便管理）
zookeeper.connect=hadoop102:2181,hadoop103:2181,hadoop104:2181/kafka
```
+ 分发kafka，并修改配置文件，中broker.id、listeners=PLAINTEXT://kafka-broker1:9092
+ 配置kafka环境变量：vim /etc/profile.d/my_env.sh
```
#KAFKA_HOME
export KAFKA_HOME=/opt/module/kafka
export PATH=$PATH:$KAFKA_HOME/bin
```
+ source /etc/profile

### 集群启停

+ 启动前请先启动ZooKeeper服务:zk start
+ 进入/opt/module/kafka目录
  - 执行启动指令
  bin/kafka-server-start.sh -daemon config/server.properties
  3.10.5.7关闭Kafka
+  进入/opt/module/kafka目录
   - 执行关闭指令
   bin/kafka-server-stop.sh

+ 联合脚本
  - 因为Kafka启动前，需要先启动ZooKeeper，关闭时，又需要将所有Kafka全部关闭后，才能关闭ZooKeeper，这样，操作起来感觉比较麻烦，所以可以将之前的2个脚本再做一次封装,联合kfk、zk
  - 创建xcall.sh文件，用于调用指令，xcall 后面跟着linux指令操作，可以同时对多个服务器节点同时执行相同指令，eg：xcall jps
  - 创建cluster.sh文件，用于集群启动。
  - 通过：cluster.sh start、stop来启动、关闭Kafka集群。


### Kafka-Eagle监控
+ Kafka-Eagle框架可以监控Kafka集群的整体运行情况，在生产环境中经常使用。
+ kafka-eagle安装依赖mysql，所以需要先安装mysql。
  - 安装后修改改Kafka集群配置
  ```
  修改/opt/module/kafka/bin/kafka-server-start.sh脚本文件中的内容
  if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
      export KAFKA_HEAP_OPTS="-server -Xms2G -Xmx2G -XX:PermSize=128m -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:ParallelGCThreads=8 -XX:ConcGCThreads=5 -XX:InitiatingHeapOccupancyPercent=70"
      export JMX_PORT="9999"
      #export KAFKA_HEAP_OPTS="-Xmx1G -Xms1G"
  fi
  ```
+ 安装
  - 将kafka-eagle-bin-3.0.1.tar.gz上传到虚拟机/opt/software目录下，并解压缩
  - 修改配置文件，/opt/module/efak/conf/system-config.properties
  ```
  ######################################
  # multi zookeeper & kafka cluster list
  # Settings prefixed with 'kafka.eagle.' will be deprecated, use 'efak.' instead
  ######################################
  efak.zk.cluster.alias=cluster1
  cluster1.zk.list=kafka-broker1:2181,kafka-broker2:2181,kafka-broker3:2181/kafka

  ######################################
  # zookeeper enable acl
  ######################################
  cluster1.zk.acl.enable=false
  cluster1.zk.acl.schema=digest
  cluster1.zk.acl.username=test
  cluster1.zk.acl.password=test

  ######################################
  # broker size online list
  ######################################
  cluster1.efak.broker.size=20

  ######################################
  # zk client thread limit
  ######################################
  kafka.zk.limit.size=32
  ######################################
  # EFAK webui port
  ######################################
  efak.webui.port=8048

  ######################################
  # kafka jmx acl and ssl authenticate
  ######################################
  cluster1.efak.jmx.acl=false
  cluster1.efak.jmx.user=keadmin
  cluster1.efak.jmx.password=keadmin123
  cluster1.efak.jmx.ssl=false
  cluster1.efak.jmx.truststore.location=/data/ssl/certificates/kafka.truststore
  cluster1.efak.jmx.truststore.password=ke123456

  ######################################
  # kafka offset storage
  ######################################
  cluster1.efak.offset.storage=kafka


  ######################################
  # kafka jmx uri
  ######################################
  cluster1.efak.jmx.uri=service:jmx:rmi:///jndi/rmi://%s/jmxrmi

  ######################################
  # kafka metrics, 15 days by default
  ######################################
  efak.metrics.charts=true
  efak.metrics.retain=15

  ######################################
  # kafka sql topic records max
  ######################################
  efak.sql.topic.records.max=5000
  efak.sql.topic.preview.records.max=10

  ######################################
  # delete kafka topic token
  ######################################
  efak.topic.token=keadmin

  ######################################
  # kafka sasl authenticate
  ######################################
  cluster1.efak.sasl.enable=false
  cluster1.efak.sasl.protocol=SASL_PLAINTEXT
  cluster1.efak.sasl.mechanism=SCRAM-SHA-256
  cluster1.efak.sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username="kafka" password="kafka-eagle";
  cluster1.efak.sasl.client.id=
  cluster1.efak.blacklist.topics=
  cluster1.efak.sasl.cgroup.enable=false
  cluster1.efak.sasl.cgroup.topics=
  cluster2.efak.sasl.enable=false
  cluster2.efak.sasl.protocol=SASL_PLAINTEXT
  cluster2.efak.sasl.mechanism=PLAIN
  cluster2.efak.sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="kafka" password="kafka-eagle";
  cluster2.efak.sasl.client.id=
  cluster2.efak.blacklist.topics=
  cluster2.efak.sasl.cgroup.enable=false
  cluster2.efak.sasl.cgroup.topics=

  ######################################
  # kafka ssl authenticate
  ######################################
  cluster3.efak.ssl.enable=false
  cluster3.efak.ssl.protocol=SSL
  cluster3.efak.ssl.truststore.location=
  cluster3.efak.ssl.truststore.password=
  cluster3.efak.ssl.keystore.location=
  cluster3.efak.ssl.keystore.password=
  cluster3.efak.ssl.key.password=
  cluster3.efak.ssl.endpoint.identification.algorithm=https
  cluster3.efak.blacklist.topics=
  cluster3.efak.ssl.cgroup.enable=false
  cluster3.efak.ssl.cgroup.topics=
  ######################################
  # kafka sqlite jdbc driver address
  ######################################
  # 配置mysql连接
  efak.driver=com.mysql.jdbc.Driver
  efak.url=jdbc:mysql://kafka-broker1:3306/ke?useUnicode=true&characterEncoding=UTF-8&zeroDateTimeBehavior=convertToNull
  efak.username=root
  efak.password=000000
  ######################################
  # kafka mysql jdbc driver address
  ######################################
  #efak.driver=com.mysql.cj.jdbc.Driver
  #efak.url=jdbc:mysql://kafka-broker1:3306/ke?useUnicode=true&characterEncoding=UTF-8&zeroDateTimeBehavior=convertToNull
  #efak.username=root
  #efak.password=123456

  ```
  - 添加环境变量: 创建/etc/profile.d/my_env.sh脚本文件
    - kafkaEFAK
    export KE_HOME=/opt/module/efak
    export PATH=$PATH:$KE_HOME/bin
    - 刷新环境变量
    source /etc/profile.d/my_env.sh
#### 使用
+ 启动eagle：进入efak文件目录cd /opt/module/efak
  - 启动eagle：bin/efak-server.sh start
  - 停止eagle：bin/efak-server.sh stop
+ 登录页面查看监控数据：http://kafka-broker1:8048/
  - 默认用户名：admin，密码：123456

## kafka集成到flume
+ **flume是日志采集器**，采集日志数据发送到kafka，然后将数据写入HDFS
### 安装部署
+ 将压缩包apache-flume-1.10.1-bin.tar.gz上传到linux系统的/opt/software目录下
+ 将软件压缩包解压缩到/opt/module目录中，并修改名称
  - 解压缩文件
  tar -zxf /opt/software/apache-flume-1.10.1-bin.tar.gz -C /opt/module/
  - 修改名称
  mv /opt/module/apache-flume-1.10.1-bin /opt/module/flume
+	生产环境中，可以设置flume的堆内存为4G或以上。
  + 修改/opt/module/flume/conf/flume-env.sh文件，配置如下参数（虚拟机环境暂不配置）
+ 修改JVM配置
  export JAVA_OPTS="-Xms4096m -Xmx4096m -Dcom.sun.management.jmxremote"
#### 增加集成配置
##### flume采集数据到Kafka的配置
+ 在linux系统解压缩后的flume软件目录中，创建job目录
  - 进入flume软件目录：cd /opt/module/flume
  - 创建job目录：mkdir job 
+ 创建配置文件：file_to_kafka.conf
  - 进入job目录 ：cd /opt/module/flume/job
  - 创建文件：vim file_to_kafka.conf
  - 增加文件内容
    ```
    # 定义组件
    a1.sources = r1
    a1.channels = c1

    # 配置source
    a1.sources.r1.type = TAILDIR
    a1.sources.r1.filegroups = f1
    # 日志（数据）文件
    a1.sources.r1.filegroups.f1 = /opt/module/data/test.log
    a1.sources.r1.positionFile = /opt/module/flume/taildir_position.json

    # 配置channel
    # 采用Kafka Channel，省去了Sink，提高了效率
    a1.channels.c1.type = org.apache.flume.channel.kafka.KafkaChannel
    a1.channels.c1.kafka.bootstrap.servers = kafka-broker1:9092,kafka-broker2:9092,kafka-broker3:9092
    a1.channels.c1.kafka.topic = test
    a1.channels.c1.parseAsFlumeEvent = false

    # 组装 
    a1.sources.r1.channels = c1
    ```
##### 执行flume操作采集数据到Kafka
+ 进入flume
  cd /opt/module/flume
+ 执行
  bin/flume-ng agent -n a1 -c conf/ -f job/file_to_kafka.conf

## kafka优化
+ Linux部署可享受零拷贝带来的性能提升。
+ 顺序读写可机械硬盘性能与SSD性能相当，可选择机械硬盘降低成本，数据保存
  留出10%的空间，同时需要考虑是否启动压缩
+ 网络带宽高于万兆，则无带宽性能瓶颈，**网络带宽通常需预留2/3或3/4作为预留资源**
+ 内存配置
  Kafka运行过程中设计到的内存主要为JVM的堆内存和操作系统的页缓存，每个Broker节点的堆内存建议10-15G内存，而数据文件（默认为1G）的25%在内存就可以了。综合上述，Kafka在大数据场景下能够流畅稳定运行至少需要11G，建议安装Kafka的服务器节点的内存至少大于等于16G。
+ CPU选择
  在生产环境中，建议CPU核数最少为16核，建议32核以上，方可保证大数据环境中的Kafka集群正常处理与运行
+ 副本分配策略
  Kafka采用分区机制对数据进行管理和存储，每个Topic可以有多个分区，每个分区可以有多个副本。应根据业务需求合理配置副本，一般建议设置至少2个副本以保证高可用性。
+ 故障转移方案
  当Kafka集群中的某个Broker节点发生故障时，其负责的分区副本将会被重新分配到其他存活的Broker节点上，并且会自动选择一个备份分区作为新的主分区来处理消息的读写请求。
+ 数据备份与恢复
  Kafka采用基于日志文件的存储方式，每个Broker节点上都有副本数据的本地备份。在数据备份方面，可以通过配置Kafka的数据保留策略和数据分区调整策略来保证数据的持久性和安全性；在数据恢复方面，可以通过查找备份数据并进行相应的分区副本替换来恢复数据。
+ 参数配置优化

|参数名|	默认参数值|	位置|	优化场景|	备注|
|---|---|---|---|---|
|num.network.threads|	3|	服务端|	低延迟|	
|num.io.threads|8|服务端|低延迟|
|socket.send.buffer.bytes|102400(100K)|服务端|高吞吐|
|socket.receive.buffer.bytes|65536(64K)|服务端|高吞吐场景|
|max.in.flight.requests.per.connection|5|生产端|幂等|
|buffer.memory|33554432（32M）|生产端|高吞吐|
|batch.size|16384(16K)|生产端|提高性能|
|linger.ms|0|生产端|提高性能|
|fetch.min.bytes|1|消费端|提高性能|网络交互次数|
|max.poll.records|500|消费端|批量处理|控制批量获取消息数量|
|fetch.max.bytes|57671680 (55M)|消费端|批量处理|控制批量获取消息字节大小|
+ 数据压缩和批量发送
  - 通过压缩和批量发送可以优化Kafka的性能表现。Kafka支持多种数据压缩算法，包括Gzip、Snappy、LZ4和zstd。在不同场景下，需要选择合适的压缩算法，以确保性能最优。 

  |压缩算法|压缩比率|压缩效率|解压缩效率|
  |---|---|---|---|
  |snappy|2.073|580m/s|2020m/s|
  |lz4|2.101|800m/s|4220m/s|
  |zstd|2.884|520m/s|1600m/s|
  - 从表格数据可以直观看出，zstd有着最高得压缩比，而LZ4算法，在吞吐量上表现得非常高效。对于Kafka而言，在吞吐量上比较：lz4 > snappy>zstd>gzip。而在压缩比上：zstd>lz4>gzip>snappy
  - Kafka支持两种批处理方式：异步批处理和同步批处理。在不同场景下，需要选择合适的批处理方式，进行性能优化。同时需要合理设置批处理参数，如batch.size、linger.ms等。
 


## kafka集成到spark
+ 特点
  - spark仅仅作为消费者使用，从kafka中消费数据，利用mevent集成。
+ 修改pom.xml文件，增加依赖
```
<dependency>
	<groupId>org.apache.spark</groupId>
	<artifactId>spark-core_2.12</artifactId>
	<version>3.3.1</version>
</dependency>
<dependency>
	<groupId>org.apache.spark</groupId>
	<artifactId>spark-streaming_2.12</artifactId>
	<version>3.3.1</version>
</dependency>
<dependency>
	<groupId>org.apache.spark</groupId>
	<artifactId>spark-streaming-kafka-0-10_2.12</artifactId>
	<version>3.3.1</version>
</dependency>

```
+ 创建SparkStreamingKafka.scala文件，编写代码
```
package com.atguigu.kafka.test;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.storage.StorageLevel;
import org.apache.spark.streaming.Duration;
import org.apache.spark.streaming.api.java.JavaInputDStream;
import org.apache.spark.streaming.api.java.JavaPairDStream;
import org.apache.spark.streaming.api.java.JavaReceiverInputDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.apache.spark.streaming.kafka010.ConsumerStrategies;
import org.apache.spark.streaming.kafka010.KafkaUtils;
import org.apache.spark.streaming.kafka010.LocationStrategies;
import scala.Tuple2;

import java.util.*;

public class Kafka4SparkStreamingTest {
    public static void main(String[] args) throws Exception {

        // TODO 创建配置对象
        SparkConf conf = new SparkConf();
        conf.setMaster("local[*]");
        conf.setAppName("SparkStreaming");

        // TODO 创建环境对象
        JavaStreamingContext ssc = new JavaStreamingContext(conf, new Duration(3 * 1000));

        // TODO 使用kafka作为数据源

        // 创建配置参数
        HashMap<String, Object> map = new HashMap<>();
        map.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,"localhost:9092");
        map.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        map.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        map.put(ConsumerConfig.GROUP_ID_CONFIG,"atguigu");
        map.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG,"latest");

        // 需要消费的主题
        ArrayList<String> strings = new ArrayList<>();
        strings.add("test");

        JavaInputDStream<ConsumerRecord<String, String>> directStream =
                KafkaUtils.createDirectStream(
                        ssc,
                        LocationStrategies.PreferBrokers(),
                        ConsumerStrategies.<String, String>Subscribe(strings,map));

        directStream.map(new Function<ConsumerRecord<String, String>, String>() {
            @Override
            public String call(ConsumerRecord<String, String> v1) throws Exception {
                return v1.value();
            }
        }).print(100);

        ssc.start();
        ssc.awaitTermination();
    }
}

```

## kafka集成到flink、
+ 特点
  - flink仅仅作为消费者使用，从kafka中消费数据，利用mevent集成。
+ 修改pom.xml文件，增加相关依赖
```
<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-java</artifactId>
	<version>1.17.0</version>
</dependency>
<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-streaming-java</artifactId>
	<version>1.17.0</version>
</dependency>
<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-clients</artifactId>
	<version>1.17.0</version>
</dependency>
<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-connector-kafka</artifactId>
	<version>1.17.0</version>
</dependency>
```
+ 编写代码
```
package com.atguigu.kafka;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class Kafka4FlinkTest {
    public static void main(String[] args) throws Exception {

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        KafkaSource<String> kafkaSource = KafkaSource.<String>builder()
                .setBootstrapServers("localhost:9092")
                .setTopics("test")
                .setGroupId("atguigu")
                .setStartingOffsets(OffsetsInitializer.latest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

        DataStreamSource<String> stream = env.fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "kafka-source");

        stream.print("Kafka");

        env.execute();
    }
}
```

## kafka集成到springboot
+ 特点
  - springboot即可生产数据，也可以消费数据，故配置时需要同时配置生产者和消费者配置。
+ 修改pom.xml文件，增加相关依赖
```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.0.5</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.atguigu</groupId>
    <artifactId>springboot-kafka</artifactId>
    <version>0.0.1</version>
    <name>springboot-kafka</name>
    <description>Kafka project for Spring Boot</description>
    <properties>
        <java.version>17</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <exclusions>
                <exclusion>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter-logging</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.kafka</groupId>
            <artifactId>spring-kafka</artifactId>
        </dependency>
        <dependency>
            <groupId>org.apache.kafka</groupId>
            <artifactId>kafka-clients</artifactId>
            <version>3.6.1</version>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
            <version>1.2.83</version>
        </dependency>
        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-json</artifactId>
            <version>5.8.11</version>
        </dependency>
        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-db</artifactId>
            <version>5.8.11</version>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```
+ 在resources中增加application.yml文件
```
spring:
  kafka:
    bootstrap-servers: localhost:9092
    producer:
      acks: all
      batch-size: 16384
      buffer-memory: 33554432
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.apache.kafka.common.serialization.StringSerializer
      retries: 0
    consumer:
      group-id: test#消费者组
      #消费方式: 在有提交记录的时候，earliest与latest是一样的，从提交记录的下一条开始消费
      # earliest：无提交记录，从头开始消费
      #latest：无提交记录，从最新的消息的下一条开始消费
      auto-offset-reset: earliest
      enable-auto-commit: true #是否自动提交偏移量offset
      auto-commit-interval: 1s #前提是 enable-auto-commit=true。自动提交的频率
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      max-poll-records: 2
      properties:
        #如果在这个时间内没有收到心跳，该消费者会被踢出组并触发{组再平衡 rebalance}
        session.timeout.ms: 120000
        #最大消费时间。此决定了获取消息后提交偏移量的最大时间，超过设定的时间（默认5分钟），服务端也会认为该消费者失效。踢出并再平衡
        max.poll.interval.ms: 300000
        #配置控制客户端等待请求响应的最长时间。
        #如果在超时之前没有收到响应，客户端将在必要时重新发送请求，
        #或者如果重试次数用尽，则请求失败。
        request.timeout.ms: 60000
        #订阅或分配主题时，允许自动创建主题。0.11之前，必须设置false
        allow.auto.create.topics: true
        #poll方法向协调器发送心跳的频率，为session.timeout.ms的三分之一
        heartbeat.interval.ms: 40000
        #每个分区里返回的记录最多不超max.partitions.fetch.bytes 指定的字节
        #0.10.1版本后 如果 fetch 的第一个非空分区中的第一条消息大于这个限制
        #仍然会返回该消息，以确保消费者可以进行
        #max.partition.fetch.bytes=1048576  #1M
    listener:
      #当enable.auto.commit的值设置为false时，该值会生效；为true时不会生效
      #manual_immediate:需要手动调用Acknowledgment.acknowledge()后立即提交
      #ack-mode: manual_immediate
      missing-topics-fatal: true #如果至少有一个topic不存在，true启动失败。false忽略
      #type: single #单条消费？批量消费？ #批量消费需要配合 consumer.max-poll-records
      type: batch
      concurrency: 2 #配置多少，就为为每个消费者实例创建多少个线程。多出分区的线程空闲
    template:
      default-topic: "test"
server:
  port: 9999
```
### 编写功能代码
+ 建配置类：SpringBootKafkaConfig
```
package com.atguigu.springkafka.config;

public class SpringBootKafkaConfig {
    public static final String TOPIC_TEST = "test";
    public static final String GROUP_ID = "test";
}
```
+ 创建生产者控制器：KafkaProducerController
```
package com.atguigu.springkafka.controller;

import com.atguigu.springkafka.config.SpringBootKafkaConfig;
import lombok.extern.slf4j.Slf4j;
import cn.hutool.json.JSONUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.web.bind.annotation.*;

import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.util.concurrent.ListenableFutureCallback;

@RestController
@RequestMapping("/kafka")
@Slf4j
public class KafkaProducerController {


    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @ResponseBody
    @PostMapping(value = "/produce", produces = "application/json")
    public String produce(@RequestBody Object obj) {

        try {
            String obj2String = JSONUtil.toJsonStr(obj);
            kafkaTemplate.send(SpringBootKafkaConfig.TOPIC_TEST, obj2String);
            return "success";
        } catch (Exception e) {
            e.getMessage();
        }
        return "success";
    }
}
```
+ 创建消费者控制器：KafkaConsumerController
```
package com.atguigu.springkafka.component;

import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import lombok.extern.slf4j.Slf4j;
import com.atguigu.springkafka.config.SpringBootKafkaConfig;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Optional;


@Component
@Slf4j
public class KafkaDataConsumer {
    @KafkaListener(topics = SpringBootKafkaConfig.TOPIC_TEST, groupId = SpringBootKafkaConfig.GROUP_ID)
    public void topic_test(List<String> messages, @Header(KafkaHeaders.RECEIVED_TOPIC) String topic) {
        for (String message : messages) {
            final JSONObject entries = JSONUtil.parseObj(message);
            System.out.println(SpringBootKafkaConfig.GROUP_ID + " 消费了： Topic:" + topic + ",Message:" + entries.getStr("data"));
            //ack.acknowledge();
        }
    }
}
```
## 面试
+ Kafka都有哪些组件？
+ Kafka的LSO、LEO、 HW 的含义？
  LSO，LEO，HW其实都是kafka中的偏移量。只不过它们代表的含义是不相同的。
  这里的LSO有两层含义：
  一个是Log Start Offset， 一个是Log Stable Offset，第一个表示数据文件的起始偏移量，同学们还记的，咱们的log文件的文件名吗，文件名中的那个数字就是当前文件的LSO, 第二个表示的位移值是用来判断事务型消费者的可见性，就是所谓的事务隔离级别，一个叫read_commited, 一个叫read_uncommited。当然了，如果你的生产者或消费者没有使用事务，那么这个偏移量没有任何的意义。
  LEO 表示 Log End Offset，就是下一个要写入的数据偏移量，所以这个偏移量的数据是不存在的
  HW表示高水位线偏移量的意思。是kafka为了数据的一致性所增加的一种数据隔离方式。简单的理解，就是消费者只能消费到，小于高水位线偏移量的数据。
+ Controller选举是怎么实现的？
  这里的controller选举主要指的还是Kafka依赖于ZK实现的controller选举机制，也就是说，kafka的所有broker节点会监听ZK中的一个controller临时节点，如果这个节点没有创建，那么broker就会申请创建，一旦创建成功，那么创建成功的broker就会当选为集群的管理者controller，一旦失去了和ZK的通信，那么临时节点就会消失，此时就会再次进行controller的选举，选举的规则是完全一样的，一旦新的controller选举，那么controller纪元会被更新。
+ 分区副本AR, ISR, OSR的含义？
  这里的AR可以理解为分区的所有副本集合。而ISR表示的就是正在同步数据的副本列表，列表的第一个就是分区的Leader副本，其他的副本就是Follower副本。OSR就是没有处于同步数据的副本列表。一旦副本拉取数据满足了特点的条件，那么会从OSR中移除并增加到ISR中。同样，如果副本没有拉取数据满足了特定的条件，就会从ISR中移除，放入到OSR中。这就是所谓的ISR列表的收缩和扩张。kafka使用这种ISR的方式有效的权衡了数据可靠性和性能之间的关系
+ Producer生产消息是如何实现的？
  这里所谓的生产消息。指的就是生产者客户端的生产数据的基本流程。咱们之前的图形中，就把这个流程已经画出来了。我相信图形比文字应该更容易记忆，所以请大家参考前面的生产者组件。
+ Producer ACK应答策略？
  ACK应答机制其实就是生产者发送数据后kafka接收确认方式。Kafka确认的方式有3种:
  第一种是当生产者数据发送到网络客户端的缓冲区后，Kafka就认为数据收到了，那么就会进行响应，也就是应答。但是这种方式，数据可靠性是非常低的，因为不能保证数据一定会写入日志文件。但是发送效率影响不大。
  第二种是当主题分区的Leader副本将数据写入日志后，Kafka才认为数据收到了，然后再对生产者进行响应。这种方式，发送数据的效率会降低，但是可靠性会高一些。而可靠性最高的就是第三种方式，
  第三种方式就是主题分区的ISR副本列表种所有的副本都已经将数据写入日志后。Kafka才认为数据收到了，然后再对生产者进行响应。这种方式，发送数据的效率会非常低。生产者对象可以根据生产环境和业务要求对应答机制进行配置。
  三种方式分别对应0，1和-1(all)。另外，生产者数据幂等性操作要求ACK应答处理机制必须为-1，而ACK的参数默认值也是-1
+ Producer 消息重复或消息丢失的原因？
  Producer消息重复和消息丢失的原因，主要就是kafka为了提高数据可靠性所提供的重试机制，如果禁用重试机制，那么一旦数据发送失败，数据就丢失了。而数据重复，恰恰是因为开启重试机制后，如果因为网络阻塞或不稳定，导致数据重新发送。那么数据就有可能是重复的。所以kafka提供了幂等性操作解决数据重复，并且幂等性操作要求必须开启重试功能和ACK取值为-1，这样，数据就不会丢失了。
  kafka提供的幂等性操作只能保证同一个生产者会话中同一个分区中的数据不会重复，一旦数据发送过程中，生产者对象重启，那么幂等性操作就会失效。那么此时就需要使用Kafka的事务功能来解决跨会话的幂等性操作。但是跨分区的幂等性操作是无法实现的。
+ Follower拉取Leader消息是如何实现的？
  这个问题说的是数据拉取流程，请大家参考数据拉取流程
+ Consumer拉取消息是如何实现的？
  这个问题说的是数据拉取流程，请大家参考数据拉取流程
+ Consumer消息重复或消息丢失的原因？
  这里主要说的是消费者提交偏移量的问题。消费者为了防止意外情况下，重启后不知道从哪里消费，所以会每5s时间自动保存偏移量。但是这种自动保存偏移量的操作是基于时间的，一旦未达到时间，消费者重启了，那么消费者就可能重复消费数据。
  Kafka提供自动保存偏移量的功能的同时，也提供了手动保存偏移量的2种方式，一个是同步提交，一个是异步提交。本质上都是提交一批数据的最后一个偏移量的值，但是可能会出现，偏移量提交完毕，但是拉取的数据未处理完毕，消费者重启了。那么此时有的数据就消费不到了，也就是所谓的数据丢失。
+ Kafka数据如何保证有序？
  这里的有序我们要考虑的点比较多，但是总结起来就是生产有序，存储有序，消费有序。
  所谓的生产有序就是生产者对象需要给数据增加序列号用于标记数据的顺序，然后再服务端进行缓存数据的比对，一旦发现数据是乱序的，那么就需要让生产者客户端进行数据的排序，然后重新发送数据，保证数据的有序。不过这里的缓存数据的比对，最多只能有5条数据比对，所以生产者客户端需要配置参数，将在途请求缓冲区的请求队列数据设置为5，否则数据依然可能乱序。因为服务端的缓存数据是以分区为单位的，所以这就要求生产者客户端需要将数据发送到一个分区中，如果数据发送到多个分区，是无法保证顺序的。这就是生产有序的意思。那存储有序指的是kafka的服务端获取数据后会将数据顺序写入日志文件，这样就保证了存储有序，当然也只能是保证一个分区的数据有序。接下来就是消费有序。所谓的消费有序其实就是kafka在存储数据时会给数据增加一个访问的偏移量值，那消费者只能按照偏移量的方式顺序访问，并且一个分区的数据只能被消费者组中的一个消费者消费，那么按照偏移量方式的读取就不会出现乱序的情况。所以综合以上的描述。Kafka就能够实现数据的有序。


