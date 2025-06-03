[toc]
***

# Flink 1.13.0
+ Flink是一个分布式流处理和批处理框架,用于实时数据(不断在产生的数据)的处理。
+ **幂等性**：数据重复处理而结果不变，如统计种类
+ 应用场景
  - 电商和市场营销(实时推荐、广告投放、实时风控、实时大屏)
  - 物联网(IoT)和工业互联网(实时监控、实时报警、实时数据分析和决策)
  - 金融服务(实时交易处理、实时风险控制、实时数据分析)
  - 互联网和社交媒体(实时数据分析、实时推荐、实时监控)
+ 流处理和批处理
  - 流处理:实时处理数据流,低延时、高吞吐、容错高、精确性、可扩展性、易用性
  - 批处理:先收集大量数据再处理
+ 流处理过程
  - 数据不写入硬盘，而在保存在内存中，以数据管道的形式对数据进行不断的处理
+ 流处理演变
  - 原始版本，结合分布式系统后数据顺无法保证。 
  - lambda架构保证数据顺序：数据流同时以流处理、和批处理两种方式进行处理，
    最后进行汇总。（同时兼有低延时、高准确）
  - flink架构：一套系统实现流处理和批处理，通过不同时间语义保证数据顺序
+ 数据处理架构：
  - 事件驱动型：当一件事发生后处理一件事。（事件->触发器->处理）
  - 数据分析型：提取数据、分析数据、生成数据报告。（数据->数据仓库->数据报告）
+ api分层(越底层与具体越灵活，越顶层越简明使用越方便)
  - SQL:最高层语言
  - table api:声明领域专用语言
  - DataStream api(DataSet api):核心api
  - CEP(有状态流处理):底层api
+ Flink&spark
  - spark streaming：微批处理，足够小的批看为流，底层为批处理RDD模型
  - flink：批为有界流，流为无界流，底层为流处理DAG模型

## Flink项目示例
+ maven依赖配置 
```xml
<!--此处声明变量依赖会覆盖dependencies后相同的版本号 -->
<properties>
    <flink.version>1.13.0</flink.version>
    <java.version>1.8</java.version>
    <!--scala因flink底层用到其组件故需要Scala -->
    <scala.binary.version>2.12</scala.binary.version>
    <slf4j.version>1.7.30</slf4j.version>
</properties>

<dependencies>
    <!-- Flink 核心依赖 -->
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-java</artifactId>
        <version>${flink.version}</version>
    </dependency>

    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-streaming-java_${scala.binary.version}</artifactId>
        <version>${flink.version}</version>
    </dependency>

    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-clients_${scala.binary.version}</artifactId>
        <version>${flink.version}</version>
    </dependency>

    <!-- 日志依赖 -->
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-api</artifactId>
        <version>${slf4j.version}</version>
    </dependency>

    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-log4j12</artifactId>
        <version>${slf4j.version}</version>
    </dependency>

    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-to-slf4j</artifactId>
        <version>2.14.0</version>
    </dependency>
</dependencies>
```
+ 词频统计
```java
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.java.operators.AggregateOperator;
import org.apache.flink.api.java.operators.DataSource;
import org.apache.flink.api.java.operators.FlatMapOperator;
import org.apache.flink.api.java.operators.UnsortedGrouping;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.util.Collector;

public class BatchWordCount {
    public static void main(String[] args) throws Exception {
        // 1. 创建执行环境
        ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
        
        // 2. 从文件读取数据，按行读取（存储的元素就是每行的文本）
        DataSource<String> lineDS = env.readTextFile("input/words.txt");
        
        // 3. 转换数据格式
        FlatMapOperator<String, Tuple2<String, Long>> wordAndOne = lineDS
            .flatMap((String line, Collector<Tuple2<String, Long>> out) -> {
                String[] words = line.split(" ");
                for (String word : words) {
                    out.collect(Tuple2.of(word, 1L));
                }
            })
            .returns(Types.TUPLE(Types.STRING, Types.LONG)); // 显式声明类型信息
        
        // 4. 按照 word 进行分组
        UnsortedGrouping<Tuple2<String, Long>> wordAndOneUG = wordAndOne.groupBy(0);
        
        // 5. 分组内聚合统计
        AggregateOperator<Tuple2<String, Long>> sum = wordAndOneUG.sum(1);
        
        // 6. 打印结果
        sum.print();
    }
}
```  
## flink框架
+ [系统架构图](G:\Word-Markdown\Markdown-GitHub\图片\flink系统架构图.png)
  - 作业管理器（JobManger）和任务管理器（TaskManager）。对于一个提交执行的作业，JobManager 是真正意义上的“管理者”（Master），负责管理调度，所以在不考虑高可用的情况下只能有一个；而 TaskManager 是“工作者”（Worker、Slave），负责执行任务处理数据，所以可以有一个或多个。
  - 这里首先要说明一下“客户端”。其实客户端并不是处理系统的一部分，它只负责作业的提交。具体来说，就是调用程序的 main 方法，将代码转换成“数据流图”（Dataflow Graph），并最终生成作业图（JobGraph），一并发送给 JobManager。提交之后，任务的执行其实就跟客户端没有关系了；我们可以在客户端选择断开与 JobManager 的连接, 也可以继续保持连接。之前我们在命令提交作业时，加上的-d 参数，就是表示分离模式（detached mode)，也就是断开连接。当然，客户端可以随时连接到 JobManager，获取当前作业的状态和执行结果，也可以发送请求取消作业。我们在上一章中不论通过 Web UI 还是命令行执行“flink run”的相关操作，都是通过客户端实现的。
  - JobManager 和 TaskManagers 可以以不同的方式启动：
    - 作为独立（Standalone）集群的进程，直接在机器上启动
    - 在容器中启动
    - 由资源管理平台调度启动，比如 YARN、K8S
  - 这其实就对应着不同的部署方式。TaskManager 启动之后，JobManager 会与它建立连接，并将作业图（JobGraph）转换成可执行的“执行图”（ExecutionGraph）分发给可用的 TaskManager，然后就由 TaskManager 具体执行任务。接下来，我们就具体介绍一下 JobManger 和 TaskManager 在整个过程中扮演的角色。
#### flink作业提交流程
+ [作业提交流程](G:\Word-Markdown\Markdown-GitHub\图片\flink作业工作流程.png)
  - [standalone模式](G:\Word-Markdown\Markdown-GitHub\图片\flink独立模式.png)
  - [yarn 会话模式](G:\Word-Markdown\Markdown-GitHub\图片\flink-yarn会话.png)
  - [yarn 单作业模式](G:\Word-Markdown\Markdown-GitHub\图片\flink-yarn单作业.png)
### JobManager
+ JobManager 是一个 Flink 集群中任务管理和调度的核心，是控制应用执行的主进程
+ JobMaster组件​  
  - JobMaster 是 JobManager 中最核心的组件，负责处理单独的作业（Job），与具体 Job 一一对应。多个 Job 可同时在 Flink 集群中运行，每个 Job 拥有独立 JobMaster。早期版本 Flink 中无 JobMaster 概念，当时较小的 JobManager 实际指向现 JobMaster 功能。  
  - 作业提交时，JobMaster 接收客户端提交的应用（包含 Jar 包、数据流图 dataflow graph 和作业图 JobGraph）。JobMaster 将 JobGraph 转换为物理执行图 ExecutionGraph（含所有可并发执行的任务），并向 ResourceManager 申请必要资源。资源就绪后，分发执行图至 TaskManager。运行期间，JobMaster 负责 checkpoint 协调等中央操作。   
+ 资源管理器（ResourceManager）组件​  
  - **集群唯一** ResourceManager 负责资源分配与管理，核心对象为 TaskManager 的任务槽（task slots）。任务槽是 CPU/内存资源的计算单元，每个 Task 需分配至 slot 执行。需区分 Flink 内置 ResourceManager 与外部平台（如 YARN）的 ResourceManager。  
  - Flink ResourceManager 针对不同环境有不同实现：  
  - Standalone 部署下（无 Per-Job 模式），仅分发可用 TaskManager 的 slots，无法启动新 TaskManager  
  - 外部资源管理平台环境下，可动态分配空闲 slot 对应的 TaskManager，资源不足时向平台申请容器启动 TaskManager，并回收空闲 TaskManager 释放资源  
+ 分发器（Dispatcher）​组件
  - 提供 REST 接口用于作业提交，为每个新作业启动 JobMaster 并维护 Web UI 展示监控信息。非必需组件，部分部署模式中可省略。


### TaskManager任务管理器
+ TaskManager 是 Flink 中的工作进程，数据流的具体计算就是它来做的，所以也被称为“Worker”。Flink 集群中必须至少有一个 TaskManager；当然由于分布式计算的考虑，通常会有多个 TaskManager 运行，每一个 TaskManager 都包含了一定数量的任务槽（task slots）。Slot(插槽)是资源调度的最小单位，slot 的数量限制了 TaskManager 能够并行处理的任务数量。
+ 启动之后，TaskManager 会向资源管理器注册它的 slots；收到资源管理器的指令后，TaskManager 就会将一个或者多个槽位提供给 JobMaster 调用，JobMaster 就可以分配任务来执行了。
+ 在执行过程中，TaskManager 可以缓冲数据，还可以跟其他**运行同一应用的 TaskManager交换数据**。

### 程序与数据流(Dataflow)
+ 程序
  - Source：读取数据源
  - Transformation：利用各种算子(eg:.sum())进行数据加工
  - Sink：数据输出
+ Dataflow逻辑数据流
  - flink程序都会被映射为dataflow图，每个dataflow以一到多个source开始，并以一到多个sink结束,类似于有向无环图DAG。
  - 大部分情况下，程序中的Transformation与算子一一对应。

### 任务Task和任务槽Task Slots
+ Flink 中每一个 worker(也就是 TaskManager)都是一个 JVM 进程，它可以
  启动多个独立的线程，来并行执行多个子任务（subtask）
+ 每个任务槽（task slot）其实表示了 TaskManager 拥有计算资源的一个固定大小
  的子集。这些资源就是用来独立执行一个子任务的，描述了集群并发能力
+ 默认情况下，flink允许子任务共享slot，一个slot可保存作业的整个管道，
  即**当并行度最大为2时，2个slot即可满足需要**
+ 当我们将资源密集型和非密集型的算子放在同一个slot中时，它可自动
  分配对资源占用比例，保证了最重的任务平均分配给所有的taskmanager

### 并行度：实际使用到的并发能力
+ 任务并行、数据并行
  - 任务并行：前后发生的不同任务同时处理数据。
  - 数据并行：同一个算子拆分为多份同时处理数据。
+ 并行计算：一个算子任务就被拆分成了多个并行的“子任务”（subtasks），再将它们分发到不同节点，就真正实现了并行计算。
+ 并行度：**针对一个特定算子**的子任务（subtask）的个数被称之为其并行度（parallelism）。这样，包含并行子任务的数据流，就是并行数据流，它需要多个分区（stream partition）来分配并行任务。一般情况下，一个流程序的并行度，可以认为就是其所有算子中最大的并行度。一个程序中，不同的算子可能具有不同的并行度。
+ 一个特定算子的子任务（subtask）的个数被称之为其并行度（parallelism）。这样，包含并行子任务的数据流，就是并行数据流，它需要多个分区（stream partition）来分配并行任务。一般情况下，一个流程序的并行度，可以认为就是其所有算子中最大的并行度。一个程序中，不同的算子可能具有不同的并行度。
+ **并行度设置方法：算子>代码环境>提交设置**
  - .setParallelism(3)//设置算子并行度3,设置为1时可仅写入一个文件
  - setParallelism(3)方法,全局设定并行度3
  - 提交应用时设置，通过-p参数。
  - 配置文件 flink-conf.yaml 中直接更改默认并行度:parallelism.default: 2

#### 数据传输形式
+ one-to-one(forwarding)：直传，在本地一个分区中传输数据。
  数据流维护着分区以及元素的顺序。比如图中的 source 和 map 算子，
  source算子读取数据之后，可以直接发送给 map 算子做处理，它们之间不需要
  重新分区，也不需要调整数据的顺序。这就意味着 map 算子的子任务，看到的元素
  个数和顺序跟 source 算子的子任务产生的完全
+ Redistribution：重新分配，数据需要传输到不同分区、不同节点（用网络）。
  数据流的分区会发生改变。比图中的 map 和后面的 keyBy/window 算子之
  间（这里的 keyBy 是数据传输算子，后面的 window、apply 方法共同构成了
   window 算子）,以及 keyBy/window 算子和 Sink 算子之间，都是这样的关系。
#### 算子合并： 
+ 合并算子链
  在 Flink 中，并行度相同的一对一（one to one）算子操作，
  可以直接链接在一起形成一个“大”的任务（task），
  这样原来的算子就成为了真正任务里的一部分  
+ 意义：将算子链接成 task 是非常有效的优化：可以减少线程之间的切换和
  基于缓存区的数据交换，在减少时延的同时提升吞吐量。
+ Flink 默认会按照算子链的原则进行链接合并，如果我们想要禁止合并或者自行定义，也
  可以在代码中对算子做一些特定的设置：
  // 禁用算子链
  .map(word -> Tuple2.of(word, 1L)).disableChaining();
  // 从当前算子开始新链
  .map(word -> Tuple2.of(word, 1L)).startNewChain()
+ 共享组：同组算子才可共享slot
  - .slotSharingGroup("1")//设置共享组1,此句后不设置共享组皆为1组
  - 默认组：default
### 执行图ExecutionGraph
+ 执行图分层
  - streamGraph：最初数据流图，根据用户代码生成。
  - jobGraph：streamGraph经过优化后生成了jobGraph，主要优化：合并符合条件的节点
  - executionGraph：jobGraph的并行化版本，是调度层的最核心的数据结构。
  - 物理执行图：jobmanage根据executionGraph度job进行调度后，在各个taskmanage
               上部署形task形成的“图”，不是具体的数据结构。

## DataStream API
### 基本框架：
+ 获取执行环境:StreamExecutionEnvironment
  - StreamExecutionEnvironment.getExecutionEnvironment();
    获取当前上下文环境,此为流环境,之前通常需要设置主机、端口、并行度等
  - StreamExecutionEnvironment.createLocalEnvironment();
  - StreamExecutionEnvironment.createRemoteEnvironment("host", port, "path")
+ 读取数据源:source
+ 定义基于数据的转换操作: transform
+ 定义结果输出位置:sink
+ 触发程序执行: execute
  - env.execute("job name");，job name可为空。

+ 执行模式 execute mode
  由于 Flink 程序默认是 STREAMING 模式，我们这里重点介绍一下 BATCH 模式的配置。
  主要有两种方式：
  - 流执行模式（STREAMING）：
    这是 DataStream API 最经典的模式，一般用于需要持续实时处理的无界数据流。
    默认情况下，程序使用的就是 STREAMING 执行模式。
  - 批执行模式（BATCH）, 意义在于统计结果
    专门用于批处理的执行模式, 这种模式下，Flink 处理作业的方式类似于 
    MapReduce框架。对于不会持续计算的有界数据，我们用这种模式处理会更方便。
  - 自动模式（AUTOMATIC）
    在这种模式下，将由程序根据输入数据源是否有界，来自动选择执行模式。
  - 配置执行模式
    - 通过命令行配置
      bin/flink run -Dexecution.runtime-mode=BATCH ...
      在提交作业时，增加 execution.runtime-mode 参数，指定值为 BATCH。
    - 通过代码配置
      StreamExecutionEnvironment env =
      StreamExecutionEnvironment.getExecutionEnvironment();
      env.setRuntimeMode(RuntimeExecutionMode.BATCH);
      在代码中，直接基于执行环境调用 setRuntimeMode 方法，传入 BATCH 模式。
    - 建议: 不要在代码中配置，而是使用命令行。这同设置并行度是类似的：在提交作业时指
      定参数可以更加灵活，同一段应用程序写好之后，既可以用于批处理也可以用于流处理。而在
      代码中硬编码（hard code）的方式可扩展性比较差，一般都不推荐。

### 源算子Source:读取数据的算子
+ 读取数据预处理
  - 定义一个数据类Event，包含需要的多个字段，方便处理。
    (**必需提供无参构造方法、所有属性必须为public、所有属性必须可序列化**)
+ Flink 代码中通用的添加 source 的方式，是调用执行环境的 addSource()方法：
  DataStream<String> stream = env.addSource(...);
  方法传入一个实现SourceFunction接口了对象参数，返回 DataStreamSource。
  这里的DataStreamSource 类继承自 SingleOutputStreamOperator 类，
  又进一步继承自 DataStream。所以很明显，读取数据的 source 操作是一个算子，
  得到的是一个数据流（DataStream）。
  - SourceFunction接口：run方法：循环读取数据方法、cancel方法：停止读取数据方法
    对于 SourceFunction接口，已有多个实现类可供调用
+ 文件source
  - env.readTextFile("input/file");
    - 参数可以是目录，也可以是文件；
    - 路径可以是相对路径，也可以是绝对路径；
    - 相对路径是从系统属性 user.dir 获取路径: idea 下是 project 的根目录, standalone 模式
    下是集群节点根目录；
    - 也可以从 hdfs 目录下读取, 使用路径 hdfs://..., 由于 Flink 没有提供 hadoop 相关依赖,
    需要 pom 中添加相关依赖:
    ```java
    <dependency>
     <groupId>org.apache.hadoop</groupId>
     <artifactId>hadoop-client</artifactId>
     <version>2.7.5</version>
     <scope>provided</scope>
    </dependency>
    ```
  - env.socketTextStream("host", port);

+ 测试读取
  - 定义一个集合，包含多个数据对象，用于测试，此处对象可用Event类。
    DataStream<Event> stream = env.fromCollection(clicks);
  - 从元素读取数据：env.fromElements(new 1，new 2),**测试最常用**。
  - users[random.nextInt(users.length)]//从测试数据集合中随机选择一个元素。
+ 从 Kafka 读取数据
  - 以 Kafka 作为数据源获取数据，我们只需要引入 Kafka 连接器的依赖
    ```xml
    <dependency>
      <groupId>org.apache.flink</groupId>
        <artifactId>flink-connector-kafka_${scala.binary.version}</artifactId>
      <version>${flink.version}</version>
    </dependency>
    ```
  - 然后调用 env.addSource()，传入 FlinkKafkaConsumer 的对象实例即可。
    ```java
    DataStreamSource<String> stream = env.addSource(new FlinkKafkaConsumer<String>
    ("clicks",new SimpleStringSchema(),properties));
    ```
  - 创建 FlinkKafkaConsumer 时需要传入三个参数：
    - 第一个参数 topic，定义了从哪些主题中读取数据。可以是一个 topic，也可以
      是 topic列表，还可以是匹配所有想要读取的 topic 的正则表达式。当从多个
      topic 中读取数据时，Kafka 连接器将会处理所有 topic 的分区，将这些分区
      的数据放到一条流中去。
    - 第二个参数是一个 DeserializationSchema 或者 KeyedDeserializationSchema。
      Kafka 消息被存储为原始的字节数据，所以需要反序列化成 Java 或者 Scala
      对象。上面代码中使用的 SimpleStringSchema，是一个内置的 DeserializationSchema，
      它只是将字节数组简单地反序列化成字符串。DeserializationSchema 和 
      KeyedDeserializationSchema 是公共接口，所以我们也可以自定义反序列化逻辑。
    - 第三个参数是一个 Properties 对象，设置了 Kafka 客户端的一些属性。

+ 自定义source
  + 重写两个关键方法：
    - run()方法：使用运行时上下文对象（SourceContext）向下游发送数据。
      ctx.collect(new Event(...));//发送数据
    - cancel()方法：通过标识位控制退出循环，来达到中断数据源的效果
      //在run方法中while(flag)循环来不断发送数据，当cancel方法被调用时，flag=false，循环退出，run方法结束。
### Flink支持数据类型
+ 基本类型类：所有 Java 基本类型及其包装类，再加上 Void、String、Date、BigDecimal 和 BigInteger
+ 数组类型：包括基本类型数组（PRIMITIVE_ARRAY）和对象数组(OBJECT_ARRAY)
+ 复合类型：
  - Java 元组类型（TUPLE）：这是 Flink 内置的元组类型，是 Java API 的一部分。最多25 个字段，也就是从 Tuple0~Tuple25，不支持空字段
  - Scala 样例类及 Scala 元组：不支持空字段
  - 行类型（ROW）：可以认为是具有任意个字段的元组,并支持空字段
  - POJO：Flink 自定义的类似于 Java bean 模式的类
+ 辅助类型：Option、Either、List、Map 等
+ 泛型类型（GENERIC）
  - Flink 支持所有的 Java 类和 Scala 类。不过如果没有按照上面 POJO 类型的要求来定义，就会被 Flink 当作泛型类来处理。Flink 会把泛型类型当作黑盒，无法获取它们内部的属性；它们也不是由 Flink 本身序列化的，而是由 Kryo 序列化的。在这些类型中，元组类型和 POJO 类型最为灵活，因为它们支持创建复杂类型。而相比之下，POJO 还支持在键（key）的定义中直接使用字段名，这会让我们的代码可读性大大增加。所以，在项目实践中，往往会将流处理程序中的元素类型定为 Flink 的 POJO 类型。
  - Flink 对 POJO 类型(即自定义的Event类)的要求如下：
    - 类是公共的（public）和独立的（standalone，也就是说没有非静态的内部类）；
    - 类有一个公共的无参构造方法；
    - 类中的所有字段是 public 且非 final 的；或者有一个公共的 getter 和 setter 方法，这些方法需要符合 Java bean 的命名规范。
#### 类型提示
+ flink有一个类型提取系统，可以分析函数的输入和返回类型，自动获取类型信息，
  从而获得对应的序列化器和反序列化器。但是，由于 Java 中泛型擦除的存在，
  导致序列化和反序列化难以进行，这时就需要显式地提供类型信息，才能使应用程序正常工作或提高其性能。
+ 类型提示：显式地提供类型信息
  - 通过调用.returns()方法，可以显式地指定返回类型，eg：.returns(Types.TUPLE(Types.INT,Types.LONG))
  - **使用TypeHint类**：TypeHint类可捕获泛型类型信息并记录，为运行时提供足够的信息。eg：returns(new TypeHint<Tuple2<Integer, Long>>() {})//适合嵌套的复杂类型。

### 转换算子Transformation
#### map映射：
+ 一一映射，输入一个元素，输出一个元素，基于DataStrema调用map()方法就可以进行转换处理。方法需要传入的参数是接口 MapFunction 的实现类；返回值类型还是 DataStream，不过泛型（流中的元素类型）可能改变了。
+ 实现 MapFunction 接口的时候，需要指定两个泛型，分别是输入事件和输出事件的类型，还需要重写一个 map()方法，定义从一个输入事件转换为另一个输出事件的具体逻辑。
+ 使用自定义类实现mapfunction接口
  ```java
  stream.map(new  UserExtractor());// 传入 MapFunction 的实现类
  public static class UserExtractor implements MapFunction<Event,String> {

    @Override
    public String map(Event e) throws Exception {
      return e.user;
    }

  }
  ```
+ 使用匿名内部类实现mapfunction接口
  ```java
  stream.map(new MapFunction<Event, String>() {
    @Override
    public String map(Event e) throws Exception {
      return e.user;
    }
  })
  ```
+ 使用lambda表达式实现mapfunction接口，需注意类型擦除，需使用TypeHint类
  ```java
  stream.map(e -> e.user);
  ```
#### 过滤filter
+ 对数据源中的数据进行过滤。进行 filter 转换之后的新数据流的数据类型与原数据流是相同的。filter 转换需要传入的参数需要实现 FilterFunction 接口，而 FilterFunction 内要实现 filter()方法，就相当于一个返回布尔类型的条件表达式。
+ 自定义类实现FilterFunction
  ```java
  public static class UserFilter implements FilterFunction<Event> {
    @Override
    public boolean filter(Event e) throws Exception {
      return e.user.equals("Mary");
    }
  }
  ```
+ 匿名内部类实现FilterFunction
  ```java
  stream.filter(new FilterFunction<Event>() {
    @Override
    public boolean filter(Event e) throws Exception {
      return e.user.equals("Mary");
    }
  })
  ```
+ lambda表达式实现FilterFunction
  ```java
  stream.filter(e -> e.user.equals("Mary"))
  ```
#### flatMap扁平映射
+ 将数据拆分为多条数据，再对拆分后的数据进行map操作。flatMap 的输入和输出数据流的数据类型可以不一样。flatMap 需要传入的参数是 FlatMapFunction 接口的实现类，而 FlatMapFunction 接口需要实现 flatMap()方法。
+ flatmap()方法中的参数是一个输入元素(value.xx访问一个值)，输出通过调用out.collect()方法将数据发送到下游，故可同时实现map和filter功能。
+ 自定义类实现FlatMapFunction
  ```java
  public static class MyFlatMap implements FlatMapFunction<Event, String> {
    @Override
    public void flatMap(Event value, Collector<String> out) throws Exception
    {
      if (value.user.equals("Mary")) {
        out.collect(value.user);
      } else if (value.user.equals("Bob")) {
        out.collect(value.user);//collect收集器，具有泛型可搜集多种类型
        out.collect(value.url);//flatmap通过调用out.collect()方法将数据发送到下游
      }
    }
  }
  ```
+ 匿名内部类实现FlatMapFunction
  ```java
  stream.flatMap(new FlatMapFunction<Event, String>() {
    @Override
    public void flatMap(Event value, Collector<String> out) throws Exception {
      if (value.user.equals("Mary")) {
        out.collect(value.user);
      } else if (value.user.equals("Bob")) {
        out.collect(value.user);
        out.collect(value.url);
      }
    }
  })
  ```
+ lambda表达式实现FlatMapFunction
  ```java
  stream.flatMap((Event e, Collector<String> out) -> {
    if (e.user.equals("Mary")) {
      out.collect(e.user);}
    else if (e.user.equals("Bob")) {
      out.collect(e.user);
      out.collect(e.url);
    }
  }).returns(new TypeHint<String>() {});//解决泛型擦除的问题
  ```
### 聚合算子
+ 逻辑分区方法
  + 按键分区keyBy：基于不同的 key，流中的数据将被分配到不同的分区中去，这样一来，所有具有相同的 key 的数据，都将被发往同一个分区，那么下一步算子操作就将会在同一个 slot中进行处理了。
  + 在内部，是通过计算 key 的哈希值（hash code），对分区数进行取模运算来实现的。所以这里 key 如果是 POJO 的话，必须要重写 hashCode()方法。
  + keyBy()方法需要传入一个参数，这个参数指定了一个或一组 key。有很多不同的方法来指定 key：比如对于 Tuple 数据类型，可以指定字段的位置或者多个位置的组合；对于 POJO 类型，可以指定字段的名称（String）；另外，还可以传入 Lambda 表达式或者实现一个键选择器（KeySelector），用于说明从数据中提取 key 的逻辑。
  + keyBy 得到的结果将不再是 DataStream，而是会将 DataStream 转换为KeyedStream。KeyedStream 可以认为是“分区流”或者“键控流”，它是对 DataStream 按照key 的一个逻辑分区，所以泛型有两个类型：除去当前流中的元素类型外，还需要指定 key 的类型。
  + KeyedStream 也继承自 DataStream，所以基于它的操作也都归属于 DataStream API。但它跟之前的转换操作得到的 SingleOutputStreamOperator 不同，只是一个流的分区操作，并不是一个转换算子。KeyedStream 是一个非常重要的数据结构，只有基于它才可以做后续的聚合操作（比如 sum，reduce）；而且它可以将当前算子任务的状态（state）也按照 key 进行划分、限定为仅对当前 key 有效。
  + 分组求极值实例
    ```java
    stream.keyBy(new keySelector<Event, String>() {
      @Override
      public String getKey(Event value) throws Exception {
        return value.user;
      }
    }).max("timestamp");


    stream.keyBy(value -> value.user).max("timestamp");//lambda表达式写法
    ```
#### 简单聚合
+ 简单聚合算子返回的，同样是一个 SingleOutputStreamOperator，也就是从 KeyedStream 又转换成了常规的 DataStream。所以可以这样理解：keyBy 和聚合是成对出现的，先分区、后聚合，得到的依然是一个 DataStream。而且经过简单聚合之后的数据流，元素的数据类型保持不变。
+ 一个聚合算子，会为每一个key保存一个聚合的值，在Flink中我们把它叫作“状态”（state）。所以每当有一个新的数据输入，算子就会更新保存的聚合结果，并发送一个带有更新后聚合值的事件到下游算子。对于无界流来说，这些状态是永远不会被清除的，所以我们使用聚合算子，应该只用在含有有限个 key 的数据流上。
+ sum()：在输入流上，对指定的字段做叠加求和的操作,**可接受int、string型参数，分别指定第N个字段、名为string的字段**
+ min()：在输入流上，对指定的字段求最小值。
+ max()：在输入流上，对指定的字段求最大值。
+ minBy()：与 min()类似，在输入流上针对指定字段求最小值。不同的是，min()只计算指定字段的最小值，其他字段会保留最初第一个数据的值；而 minBy()则会返回整条记录。
+ maxBy()：与 max()类似，在输入流上针对指定字段求最大值。两者区别与min()/minBy()完全一致。

#### 归约聚合
+ 简单聚合是对一些特定统计需求的实现，那么 reduce 算子就是一个一般化的聚合统计操作了。它可以对已有的数据进行归约处理，把每一个新输入的数据和当前已经归约出来的值，再做一个聚合计算。与简单聚合类似，reduce 操作也会将 KeyedStream 转换为 DataStream。它不会改变流的元素数据类型，所以输出类型和输入类型是一样的。
+ 调用 KeyedStream 的 reduce 方法时，需要传入一个参数，实现 ReduceFunction 接口,需要重写reduce方法(reduce中递归进行归约操作，归约的中间结果称为状态，归约操作可定义大小比较等)，接口在源码中的定义如下：
  ```java
  public interface ReduceFunction<T> extends Function, Serializable {
  T reduce(T value1, T value2) throws Exception;
  }
  ```
+ 实例:记录所有用户中访问频次最高的那个
  ```java
  import org.apache.flink.api.common.functions.MapFunction;
  import org.apache.flink.api.common.functions.ReduceFunction;
  import org.apache.flink.api.java.tuple.Tuple2;
  import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

  public class TransReduceTest {
      public static void main(String[] args) throws Exception {
          // 创建流处理执行环境
          StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
          env.setParallelism(1);

          env.addSource(new ClickSource()) // 使用自定义数据源 ClickSource
              // 转换数据：将 Event 转换为 (用户, 1L) 元组
              .map((MapFunction<Event, Tuple2<String, Long>>) event -> 
                  Tuple2.of(event.user, 1L)
              )
              // 按键分区：按用户名分组
              .keyBy(tuple -> tuple.f0)
              // 局部聚合：按用户统计 PV
              .reduce((ReduceFunction<Tuple2<String, Long>>) (current, next) -> 
                  Tuple2.of(current.f0, current.f1 + next.f1)
              )
              // 全局分区：将所有数据分配到同一分区
              .keyBy(tuple -> true)
              // 全局聚合：找出最大的 PV 值
              .reduce((ReduceFunction<Tuple2<String, Long>>) (maxPv, currentPv) -> 
                  currentPv.f1 > maxPv.f1 ? currentPv : maxPv
              )
              .print(); // 输出结果

          env.execute("User PV Statistics Job");
      }
  }
  ```
### 用户自定义函数UDF 
+ Flink 的 DataStream API 编程风格其实是一致的：基本上都是基于 DataStream 调用一个方法，表示要做一个转换操作；方法需要传入一个参数，这个参数都是需要实现一个接口。仅可以通过自定义函数类或者匿名类来实现接口，也可以直接传入 Lambda 表达式。这就是所谓的用户自定义函数（user-defined function，UDF）。
#### 函数类（Function Classes）
+ 通过定义一个类，实现 Function 接口，并重写接口中的方法，就可以实现自定义的函数。
#### 匿名函数（Lambda）**使用时注意返回值的类型擦除问题**
+ 直接传入一个 Lambda 表达式，作为方法参数。Lambda 表达式会被隐式地转换为一个实现了 Function 接口的类。
#### 富函数类（Rich Function Classes）
+ “富函数类”也是 DataStream API 提供的一个函数类的接口，所有的 Flink 函数类都有其Rich 版本。富函数类一般是以抽象类的形式出现的。**例如：RichMapFunction、RichFilterFunction、RichReduceFunction 等,可继承RichMapFunction实现更加灵活的函数使用。**
+ 富函数类提供了 getRuntimeContext()方法（我们在本节的第一个例子中使用了一下），可以获取到运行时上下文的一些信息，例如程序执行的并行度，任务名称，以及状态（state）。这使得我们可以大大扩展程序的功能，特别是对于状态的操作，使得 Flink中的算子具备了处理复杂业务的能力。
+ Rich Function 有生命周期的概念。典型的生命周期方法有：
  - open()方法，是 Rich Function 的初始化方法，也就是会开启一个算子的生命周期。当一个算子的实际工作方法例如 map()或者 filter()方法被调用之前，open()会首先被调用。所以像文件 IO 的创建，数据库连接的创建，配置文件的读取等等这样一次性的工作，都适合在 open()方法中完成。。
  - close()方法，是生命周期中的最后一个调用的方法，类似于解构方法。一般用来做一些清理工作。需要注意的是，这里的生命周期方法，对于一个并行子任务来说只会调用一次；
- 继承富函数类，实现从数据库读取数据
  ```java
  public class MyFlatMap<IN, OUT> extends RichFlatMapFunction<IN, OUT> {

      @Override
      public void open(Configuration parameters) throws Exception {
          super.open(parameters);
          // 进行一些初始化工作
          // 例如，建立一个和 MySQL 的连接
      }

      @Override
      public void flatMap(IN value, Collector<OUT> out) throws Exception {
          // 对数据库进行读写操作
          // 处理输入值并可能输出结果
      }

      @Override
      public void close() throws Exception {
          super.close();
          // 进行清理工作，关闭和 MySQL 数据库的连接
      }
  }
  ```
### 物理分区
+ 当发生数据倾斜的时候，系统无法自动调整，这时就需要我们重新进行负载均衡，将数据流较为平均地发送到下游任务操作分区中去。Flink 对于经过转换操作之后的 DataStream，提供了一系列的底层操作接口，能够帮我们实现数据流的手动重分区。为了同 keyBy 相区别，我们把这些操作统称为“物理分区”操作。物理分区与 keyBy 另一大区别在于，keyBy 之后得到的是一个 KeyedStream，而物理分区之后结果仍是 DataStream，且流中元素数据类型保持不变。从这一点也可以看出，分区算子并不对数据进行转换处理，只是定义了数据的传输方式。

#### 有随机分配（Random）
+ 通过调用 DataStream 的.shuffle()方法，将数据随机地分配到下游算子的并行任务中去。随机分区服从均匀分布（uniform distribution），所以可以把流中的数据随机打乱，均匀地传递到下游任务分区，因为是完全随机的，所以对于同样的输入数据, 每次执行得到的结果也不会相同。
+ eg：
  ```java
  stream.shuffle().print("shuffle").setParallelism(4);
  ```

#### 轮询分配（Round-Robin）
+ 按照先后顺序将数据做依次分发，通过调用 DataStream 的.rebalance()方法，就可以实现轮询重分区。rebalance使用的是 Round-Robin 负载均衡算法，可以将输入流数据平均分配到下游的并行任务中去。
+ eg：
  ```java
  stream.rebalance().print("rebalance").setParallelism(4);
  ```
#### 重缩放（Rescale）
+ 重缩放分区和轮询分区非常相似。当调用 rescale()方法时，其实底层也是使用 Round-Robin算法进行轮询，但是只会将数据轮询发送到下游并行任务的一部分中，如图 也就是说，“发牌人”如果有多个，那么 rebalance 的方式是每个发牌人都面向所有人发牌；而 rescale的做法是分成小团体，发牌人只给自己团体内的所有人轮流发牌。
+ 由于 rebalance 是所有分区数据的“重新平衡”，当 TaskManager 数据量较多时，这种跨节点的网络传输必然影响效率；而如果我们配置的 task slot 数量合适，用 rescale 的方式进行“部重缩放”，就可以让数据只在当前 TaskManager 的多个 slot 之间重新分配，从而避免了网络传输带来的损耗。
+ 从底层实现上看，rebalance 和 rescale 的根本区别在于任务之间的连接机制不同。rebalance将会针对所有上游任务（发送数据方）和所有下游任务（接收数据方）之间建立通信通道，这是一个笛卡尔积的关系；而 rescale 仅仅针对每一个任务和下游对应的部分任务之间建立通信通道，节省了很多资源。
+ eg：
  ```java
  public class RescaleTest {
      public static void main(String[] args) throws Exception {
          // 创建执行环境并设置全局并行度为1
          StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
          env.setParallelism(1);

          env.addSource(new RichParallelSourceFunction<Integer>() {
              @Override
              public void run(SourceContext<Integer> sourceContext) throws Exception {
                  for (int i = 0; i < 8; i++) {
                      // 将奇数发送到索引为1的并行子任务，偶数发送到索引为0的并行子任务
                      if (((i + 1) % 2) == getRuntimeContext().getIndexOfThisSubtask()) {
                          sourceContext.collect(i + 1);
                      }
                  }
              }

              @Override
              public void cancel() {
                  // 取消逻辑（如果需要）
              }
          })
          .setParallelism(2)          // 设置数据源的并行度为2
          .rescale()                  // 执行重新缩放操作
          .print()                    // 打印输出结果
          .setParallelism(4);         // 设置打印操作的并行度为4

          // 执行Flink作业
          env.execute("Rescale Test Job");
      }
  }
  ```
#### 广播（Broadcast）
+ 这种方式其实不应该叫做“重分区”，因为经过广播之后，数据会在不同的分区都保留一份，可能进行重复处理。可以通过调用 DataStream 的 broadcast()方法，将输入数据复制并发送到下游算子的所有并行任务中去。
+ eg：
  ```java
  stream. broadcast().print("broadcast").setParallelism(4);
  ```

#### 全局分区（Global）
+ 全局分区也是一种特殊的分区方式。这种做法非常极端，通过调用.global()方法，会将所有的输入流数据都发送到下游算子的第一个并行子任务中去。这就相当于强行让下游任务并行度变成了 1，所以使用这个操作需要非常谨慎，可能对程序造成很大的压力。

#### 自定义分区（Custom）
+ 当Flink提供的所有分区策略都不能满足用户的需求时，我们可以通过使用partitionCustom()方法来自定义分区策略。在调用时，方法需要传入两个参数，第一个是自定义分区器（Partitioner）对象，第二个是应用分区器的字段，它的指定方式与keyBy指定key基本一样：可以通过字段名称指定，也可以通过字段位置索引来指定，还可以实现一个KeySelector。
+ eg:我们可以对一组自然数按照奇偶性进行重分区。代码如下：
  ```java
  public class CustomPartitionTest {
      public static void main(String[] args) throws Exception {
          // 创建执行环境并设置全局并行度为1
          StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
          env.setParallelism(1);

          // 从元素创建数据流，并按照奇偶进行自定义分区
          env.fromElements(1, 2, 3, 4, 5, 6, 7, 8)
              .partitionCustom(
                  new Partitioner<Integer>() {
                      @Override
                      public int partition(Integer key, int numPartitions) {
                          // 根据键的奇偶性进行分区
                          return key % 2;
                      }
                  },
                  new KeySelector<Integer, Integer>() {
                      @Override
                      public Integer getKey(Integer value) throws Exception {
                          // 选择键作为分区的依据
                          return value;
                      }
                  }
              )
              .print() // 打印输出结果
              .setParallelism(2); // 设置打印操作的并行度为2

          // 执行Flink作业
          env.execute("Custom Partition Test Job");
      }
  }
  ```

### 输出算子（Sink）
+ 与Source 算子非常类似，除去一些Flink预实现的Sink，一般情况下Sink算子的创建是
  通过调用DataStream的.addSink()方法实现的。 stream.addSink(new 
  SinkFunction(…)); addSource 的参数需要实现一个SourceFunction接口；
  类似地，addSink方法同样需要传入一个参数，实现的是SinkFunction接口。
  在这个接口中只需要重写一个方法invoke(),用来将指定的值写入到外部系统中。
  这个方法在每条数据记录到来时都会调用： default void invoke(IN value, 
  Context context) throws Exception 当然，SinkFuntion 多数情况下同样并
  不需要我们自己实现。Flink官方提供了一部分的框架的Sink连接器。
  - Kafka(source、sink)
  - Cassandra(sink)
  - Kinesis(sink)
  - RabbitMQ(sink)
  - Nifi(sink)
  - Elasticsearch(sink)
  - JDBC(sink)  
  - HDFS(sink)
  - 文件系统(sink)
  - Twitter Streaming API(source)
  - Google PubSub(source/sink)
+  第三方连接器
  - Apache Bahir 作为给Spark和Flink提供扩展支持的项目，也实现了一些其他第三方系统与Flink的连接器
  - Apache ActiveMQ(source/sink)
  - Apache Flume (sink)
  - Akka (sink)
  - Netty (sink)
#### 输出到文件
+ Flink 为此专门提供了一个流式文件系统的连接器：StreamingFileSink，它继承自
  抽象类RichSinkFunction，而且集成了 Flink 的检查点（checkpoint）机制，
  用来保证精确一次（exactly once）的一致性语义。
+ StreamingFileSink 为批处理和流处理提供了一个统一的Sink，它可以将分区文件写入
  Flink支持的文件系统。它可以保证精确一次的状态一致性，大大改进了之前流式文件
  Sink的方式。它的主要操作是将数据写入桶（buckets），每个桶中的数据都可以分割
  成一个个大小有限的分区文件，这样一来就实现真正意义上的分布式文件存储。我们可以
  通过各种配置来控制“分桶”的操作；默认的分桶方式是基于时间的，我们每小时写入
  一个新的桶。换句话说，每个桶内保存的文件，记录的都是1小时的输出数据。 
+ StreamingFileSink 支持行编码（Row-encoded）和批量编码（Bulk-encoded，比如
  Parquet）格式。这两种不同的方式都有各自的构建器（builder），调用方法也非常
  简单，可以直接调用StreamingFileSink 的静态方法： 
  - 行编码：StreamingFileSink.forRowFormat（basePath，rowEncoder）。 
  - 批量编码：StreamingFileSink.forBulkFormat（basePath，bulkWriterFactory）。 
  - 在创建行或批量编码 Sink 时，我们需要传入两个参数，用来指定存储桶的基本路径
    （basePath）和数据的编码逻辑（rowEncoder或bulkWriterFactory）
+ eg：测试数据直接写入文件： 
  ```java
  import org.apache.flink.api.common.serialization.SimpleStringEncoder; 
  import org.apache.flink.core.fs.Path; 
  import org.apache.flink.streaming.api.datastream.DataStreamSource; 
  import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment; 
  import 
  org.apache.flink.streaming.api.functions.sink.filesystem.StreamingFileSink; 
  import 
  org.apache.flink.streaming.api.functions.sink.filesystem.rollingpolicies.Defa
  ultRollingPolicy; 
  import java.util.concurrent.TimeUnit; 
  public class SinkToFileTest { 
  public static void main(String[] args) throws Exception{ 
  StreamExecutionEnvironment 
  env 
  StreamExecutionEnvironment.getExecutionEnvironment(); 
  
          env.setParallelism(4); 
  
          DataStreamSource<Event> stream = env.fromElements(new Event("Mary", 
  "./home", 1000L), 
                  new Event("Bob", "./cart", 2000L), 
                  new Event("Alice", "./prod?id=100", 3000L), 
                  new Event("Alice", "./prod?id=200", 3500L), 
                  new Event("Bob", "./prod?id=2", 2500L), 
                  new Event("Alice", "./prod?id=300", 3600L), 
                  new Event("Bob", "./home", 3000L), 
                  new Event("Bob", "./prod?id=1", 2300L), 
                  new Event("Bob", "./prod?id=3", 3300L)); 
  
          StreamingFileSink<String> fileSink = StreamingFileSink 
                  .<String>forRowFormat(new Path("./output"), 
                          new SimpleStringEncoder<>("UTF-8")) 
                  .withRollingPolicy( 
                          DefaultRollingPolicy.builder() 
                                  .withRolloverInterval(TimeUnit.MINUTES.toMillis(15)
  ) 
                                  .withInactivityInterval(TimeUnit.MINUTES.toMillis(5
  )) 
                                  .withMaxPartSize(1024 * 1024 * 1024) 
                                  .build()) 
                  .build(); 
  
          // 将Event转换成String写入文件 
          stream.map(Event::toString).addSink(fileSink); 
  
          env.execute(); 
      } 
  }
  ```
  - 滚动”的概念在日志文件的写入中经常遇到：因为文件会有内容持续不断地写入，
    所以我们应该给一个标准，到什么时候就开启新的文件，将之前的内容归档保存。
#### 输出到kafka
+ Flink与Kafka的连接器提供了端到端的精确一次（exactly once）语义保证，这在
  实际项目中是最高级别的一致性保证。
+ eg：
  ```java
  import org.apache.flink.api.common.serialization.SimpleStringSchema;
  import org.apache.flink.streaming.api.datastream.DataStreamSource;
  import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
  import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;

  import java.util.Properties;

  public class SinkToKafkaTest {
      public static void main(String[] args) throws Exception {
          // 创建执行环境
          StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
          env.setParallelism(1);

          // 配置Kafka属性
          Properties properties = new Properties();
          properties.put("bootstrap.servers", "hadoop102:9092");

          // 读取输入文件
          DataStreamSource<String> stream = env.readTextFile("input/clicks.csv");

          // 配置并添加Kafka Sink
          stream.addSink(new FlinkKafkaProducer<>(
                  "clicks", // Kafka主题
                  new SimpleStringSchema(), // 序列化/反序列化模式
                  properties // Kafka配置属性
          ));

          // 执行任务
          env.execute("Sink to Kafka Test");
      }
  }
  ```
  - 这里我们可以看到，addSink传入的参数是一个FlinkKafkaProducer。这也很好理解
    因为需要向 Kafka 写入数据，自然应该创建一个生产者。FlinkKafkaProducer
    继承了抽象类TwoPhaseCommitSinkFunction，这是一个实现了“两阶段提交”的 
    RichSinkFunction。两阶段提交提供了Flink向Kafka写入数据的事务性保证，
    能够真正做到精确一次（exactly once）的状态一致性。
#### 输出到Redis
+ Redis：它一个开源的内存式的数据存储，提供了像字符串（string）、哈希表（hash）
  、列表（list）、集合（set）、排序集合（sorted set）、位图（bitmap）、
  地理索引和流（stream）等一系列常用的数据结构。因为它运行速度快、支持的数据类型
  丰富，在实际项目中已经成为了架构优化必不可少的一员，一般用作数据库、缓存，
  也可以作为消息代理。 
+ Flink 没有直接提供官方的Redis连接器，不过Bahir项目还是担任了合格的辅助角色，
  为我们提供了 Flink-Redis 的连接工具。但版本升级略显滞后，目前连接器
  版本为 1.0，支持的Scala 版本最新到2.11。由于我们的测试不涉及到Scala的相关
  版本变化，所以并不影响使用。在实际项目应用中，应该以匹配的组件版本运行。 
+ 具体测试步骤如下： 
  - 导入的Redis连接器依赖 
  ```xml
  <dependency> 
    <groupId>org.apache.bahir</groupId> 
    <artifactId>flink-connector-redis_2.11</artifactId> 
    <version>1.0</version> 
  </dependency> 
  ```
  - 启动Redis集群 :这里我们为方便测试，只启动了单节点Redis。 
  - 编写输出到Redis的示例代码 连接器为我们提供了一个RedisSink，它继承了抽象类RichSinkFunction，这就是已经实现
  好的向Redis写入数据的SinkFunction。我们可以直接将Event数据输出到Redis：
```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.redis.RedisSink;
import org.apache.flink.streaming.connectors.redis.common.config.FlinkJedisPoolConfig;
import org.apache.flink.streaming.connectors.redis.common.mapper.RedisCommand;
import org.apache.flink.streaming.connectors.redis.common.mapper.RedisCommandDescription;
import org.apache.flink.streaming.connectors.redis.common.mapper.RedisMapper;

// 假设 Event 类和 ClickSource 类已经定义在其他地方
// 如果没有定义，请确保添加相应的导入或类定义

public class SinkToRedisTest {
    public static void main(String[] args) throws Exception {
        // 创建执行环境
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);

        // 创建一个到Redis连接的配置
        FlinkJedisPoolConfig conf = new FlinkJedisPoolConfig.Builder()
                .setHost("hadoop102")
                .setPort(6379) // 根据实际情况设置Redis端口，默认是6379
                .build();

        // 添加数据源并配置Redis Sink
        env.addSource(new ClickSource())
                .addSink(new RedisSink<>(conf, new MyRedisMapper()));

        // 执行任务
        env.execute("Sink to Redis Test");
    }

    /**
     * 自定义RedisMapper，用于定义如何将Event对象写入Redis
     */
    public static class MyRedisMapper implements RedisMapper<Event> {

        @Override
        public RedisCommandDescription getCommandDescription() {
            // 指定使用HSET命令，并指定Redis中的哈希键名为"clicks"
            return new RedisCommandDescription(RedisCommand.HSET, "clicks");
        }

        @Override
        public String getKeyFromData(Event e) {
            // 定义Redis的键，这里使用Event的用户字段作为键
            return e.user;
        }

        @Override
        public String getValueFromData(Event e) {
            // 对于HSET命令，getValue通常返回null，因为字段和值通过其他方法提供
            return null;
        }

        @Override
        public String getHashFieldFromData(Event e) {
            // 定义哈希字段，这里使用Event的URL字段作为哈希字段
            return e.url;
        }

        // 如果需要存储更多字段，可以实现额外的逻辑
        // 例如，使用其他Redis命令或将多个字段组合在一起
    }
}

/**
 * 假设的Event类定义
 */
class Event {
    public String user;
    public String url;
    // 其他字段...

    // 构造方法
    public Event(String user, String url /*, 其他参数... */) {
        this.user = user;
        this.url = url;
        // 初始化其他字段...
    }

    // Getter 和 Setter 方法（如果需要）
}

/**
 * 假设的ClickSource类定义
 */
class ClickSource implements SourceFunction<Event> { // 需要导入相应的SourceFunction
    // 实现数据源逻辑，例如生成Event对象
}
```
#### 输出到Elasticsearch
+ ElasticSearch是一个分布式的开源搜索和分析引擎，适用于所有类型的数据。
  ElasticSearch有着简洁的REST风格的API，以良好的分布式特性、速度和可扩展性而
  闻名，在大数据领域应用非常广泛。Flink为ElasticSearch专门提供了官方的
  Sink 连接器，Flink 1.13支持当前最新版本的ElasticSearch。
+ 添加Elasticsearch 连接器依赖 ：
```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-elasticsearch7_2.12</artifactId>
    <version>${flink.version}</version>
</dependency>
```
+ 代码：
  ```java
  import org.apache.flink.api.common.functions.RuntimeContext;
  import org.apache.flink.streaming.api.datastream.DataStreamSource;
  import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
  import org.apache.flink.streaming.connectors.elasticsearch.ElasticsearchSinkFunction;
  import org.apache.flink.streaming.connectors.elasticsearch.RequestIndexer;
  import org.apache.flink.streaming.connectors.elasticsearch7.ElasticsearchSink;
  import org.apache.http.HttpHost;

  import java.util.ArrayList;
  import java.util.HashMap;
  import java.util.Map;

  // 假设 Event 类定义如下
  class Event {
      public String user;
      public String url;
      public Long timestamp;

      public Event(String user, String url, Long timestamp) {
          this.user = user;
          this.url = url;
          this.timestamp = timestamp;
      }

      // 可选：添加 getters 和 setters
  }

  public class SinkToEsTest {
      public static void main(String[] args) throws Exception {
          // 创建 Flink 执行环境
          StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
          env.setParallelism(1);

          // 创建数据源
          DataStreamSource<Event> stream = env.fromElements(
                  new Event("Mary", "./home", 1000L),
                  new Event("Bob", "./cart", 2000L),
                  new Event("Alice", "./prod?id=100", 3000L),
                  new Event("Alice", "./prod?id=200", 3500L),
                  new Event("Bob", "./prod?id=2", 2500L),
                  new Event("Alice", "./prod?id=300", 3600L),
                  new Event("Bob", "./home", 3000L),
                  new Event("Bob", "./prod?id=1", 2300L),
                  new Event("Bob", "./prod?id=3", 3300L)
          );

          // 配置 Elasticsearch 的 HTTP 主机
          ArrayList<HttpHost> httpHosts = new ArrayList<>();
          httpHosts.add(new HttpHost("hadoop102", 9200, "http"));

          // 创建 ElasticsearchSink.Builder
          ElasticsearchSink.Builder<Event> esSinkBuilder = new ElasticsearchSink.Builder<>(
                  httpHosts,
                  new ElasticsearchSinkFunction<Event>() {
                      @Override
                      public void process(Event element, RuntimeContext ctx, RequestIndexer indexer) {
                          // 构建要索引的数据
                          Map<String, Object> json = new HashMap<>();
                          json.put("user", element.user);
                          json.put("url", element.url);
                          json.put("timestamp", element.timestamp);

                          // 创建 IndexRequest
                          indexer.add(Requests.indexRequest()
                                  .index("clicks") // 索引名称
                                  .type("_doc")     // 对于 ES 7.x，使用默认类型 "_doc"
                                  .source(json));   // 数据源
                      }
                  }
          );

          // 可选：配置批量写入参数
          esSinkBuilder.setBulkFlushMaxActions(1); // 每个批次最多写入一个事件，便于调试

          // 添加 Sink 到数据流
          stream.addSink(esSinkBuilder.build());

          // 执行 Flink 作业
          env.execute("Sink to Elasticsearch Test");
      }
  }
  ```
#### 输出到MySQL
+ 引入依赖
```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-jdbc_${scala.binary.version}</artifactId>
    <version>${flink.version}</version>
</dependency>
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.47</version>
</dependency>
```
+ 启动MySQL，在database库下建表clicks
+ 代码:
```java
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
import org.apache.flink.connector.jdbc.JdbcExecutionOptions;
import org.apache.flink.connector.jdbc.JdbcSink;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class SinkToMySQL {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);

        DataStreamSource<Event> stream = env.fromElements(
            new Event("Mary", "./home", 1000L),
            new Event("Bob", "./cart", 2000L),
            new Event("Alice", "./prod?id=100", 3000L),
            new Event("Alice", "./prod?id=200", 3500L),
            new Event("Bob", "./prod?id=2", 2500L),
            new Event("Alice", "./prod?id=300", 3600L),
            new Event("Bob", "./home", 3000L),
            new Event("Bob", "./prod?id=1", 2300L),
            new Event("Bob", "./prod?id=3", 3300L)
        );

        stream.addSink(
            JdbcSink.sink(
                "INSERT INTO clicks (user, url) VALUES (?, ?)",
                (statement, r) -> {
                    statement.setString(1, r.user);
                    statement.setString(2, r.url);
                },
                JdbcExecutionOptions.builder()
                    .withBatchSize(1000)
                    .withBatchIntervalMs(200)
                    .withMaxRetries(5)
                    .build(),
                new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
                    .withUrl("jdbc:mysql://localhost:3306/userbehavior")
                    .withDriverName("com.mysql.cj.jdbc.Driver")
                    .withUsername("username")
                    .withPassword("password")
                    .build()
            )
        );

        env.execute();
    }
}
```
##### 自定义sink
+ Flink为我们提供了通用的SinkFunction接口和对应的RichSinkDunction抽象类，
  只要实现它，通过简单地调用DataStream的.addSink()方法就可以自定义写入任何
  外部存储。
+ 在实现SinkFunction的时候，需要重写的一个关键方法invoke()，在这个方法中我们
  就可以实现将流里的数据发送出去的逻辑。 
+ 我们这里使用了SinkFunction的富函数版本，因为这里我们又使用到了生命周期的概念，
  创建HBase的连接以及关闭HBase的连接需要分别放在open()方法和close()方法中。 
  ```xml
  <dependency> 
      <groupId>org.apache.hbase</groupId> 
      <artifactId>hbase-client</artifactId> 
      <version>${hbase.version}</version> 
  </dependency> 
  ```
  ```java
  import org.apache.flink.configuration.Configuration;
  import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
  import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;
  import org.apache.hadoop.hbase.HBaseConfiguration;
  import org.apache.hadoop.hbase.TableName;
  import org.apache.hadoop.hbase.client.Connection;
  import org.apache.hadoop.hbase.client.ConnectionFactory;
  import org.apache.hadoop.hbase.client.Put;
  import org.apache.hadoop.hbase.client.Table;

  import java.nio.charset.StandardCharsets;

  public class SinkCustomtoHBase {
      public static void main(String[] args) throws Exception {
          StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
          env.setParallelism(1);

          env.fromElements("hello", "world")
              .addSink(new RichSinkFunction<String>() {
                  public org.apache.hadoop.conf.Configuration configuration; // 管理HBase的配置信息
                  public Connection connection; // 管理HBase连接

                  @Override
                  public void open(Configuration parameters) throws Exception {
                      super.open(parameters);
                      configuration = HBaseConfiguration.create();
                      configuration.set("hbase.zookeeper.quorum", "hadoop102:2181");
                      connection = ConnectionFactory.createConnection(configuration);
                  }

                  @Override
                  public void invoke(String value, Context context) throws Exception {
                      Table table = connection.getTable(TableName.valueOf("test")); // 表名为test
                      Put put = new Put("rowkey".getBytes(StandardCharsets.UTF_8)); // 指定rowkey

                      put.addColumn(
                          "info".getBytes(StandardCharsets.UTF_8), // 指定列族
                          value.getBytes(StandardCharsets.UTF_8), // 写入的数据
                          "1".getBytes(StandardCharsets.UTF_8) // 写入的数据（时间戳或版本）
                      );
                      table.put(put); // 执行put操作
                      table.close(); // 关闭表
                  }

                  @Override
                  public void close() throws Exception {
                      super.close();
                      if (connection != null && !connection.isClosed()) {
                          connection.close(); // 关闭连接
                      }
                  }
              });

          env.execute();
      }
  }
  ```


## Flink 时间和窗口

### 时间语义
+ 处理时间
  - 每一条数据的处理时间，数据被处理时所在机器的系统时间
+ 事件时间（flink采用）
  - 事件发生的的时间，即数据产生的时间以时间戳的形式包含在数据本身中。
#### **逻辑时钟**：
+ 这个时钟的时间不会自动流逝；它的时间进展，就是靠着新到数据的时间戳来推动的。
#### 水位线（watermark）
+ 水位线作用
  - ​全局时钟同步：每个并行任务拥有独立的逻辑时钟，通过水位线广播机制，所有下游任务可同步推进时钟，确保窗口计算等操作在全局一致的时空维度下执行。
  - ​处理乱序与延迟数据：水位线标记时间进展，允许系统识别迟到数据​（时间戳早于当前水位线的事件），即当收到13秒时间戳的数据时10的窗口才关闭进行计算。配置allowedLateness可定义窗口关闭后如何处理迟到数据（如丢弃或输出至侧流）。
  ​- 保障时效性：即使下游任务处理速度不一致或存在背压，水位线仍按预定时间推进，避免因数据阻塞导致计算延迟。
+ 特性
  - 水位线是插入到数据流中的一个标记，可以认为是一个特殊的数据 
  - 水位线主要的内容是一个时间戳，用来表示当前事件时间的进展 
  - 水位线是基于数据的时间戳生成的 
  - 水位线的时间戳必须单调递增，以确保任务的事件时间时钟一直向前推进 
  - 水位线可以通过设置延迟，来保证正确处理乱序数据 
  - 一个水位线Watermark(t)，表示在当前流中事件时间已经达到了时间戳t, 这代表t之前的所有数据都到齐了，之后流中不会出现时间戳t’ ≤ t的数据 
+ 生成策略
  - 基于事件时间：从数据中提取时间戳，并生成对应的水位线。例如，使用当前事件时间减去最大延迟时间（maxOutOfOrderness）来生成水位线。
  - 周期生成：若数据流稀疏，可定期发射水位线，如每秒生成一次，无需等待数据到达。
##### 水位线生成策略（Watermark Strategies）
+ 核心方法：`.assignTimestampsAndWatermarks()`
  ```java
  DataStream<Event> withTimestampsAndWatermarks = 
      stream.assignTimestampsAndWatermarks(<watermark Strategy>);
  ```
  - 必要性说明：
    - 原始时间戳需显式分配，Flink无法自动识别事件时间
    - 例外情况：Kafka等源可直接获取时间戳

+ WatermarkStrategy结构：
  ```java
  public interface WatermarkStrategy<T> 
      extends TimestampAssignerSupplier<T>, WatermarkGeneratorSupplier<T> {
      @Override
      TimestampAssigner<T> createTimestampAssigner(Context context);
      
      @Override
      WatermarkGenerator<T> createWatermarkGenerator(Context context);
  }
  ```
  - TimestampAssigner：主要负责从流中数据元素的某个字段中提取时间戳，并分配给元素。时间戳的分配是生成水位线的基础。 
  - WatermarkGenerator：主要负责按照既定的方式，基于时间戳生成水位线。在WatermarkGenerator 接口中，主要又有两个方法：onEvent()和onPeriodicEmit()。 
  - onEvent：每个事件（数据）到来都会调用的方法，它的参数有当前事件、时间戳，以及允许发出水位线的一个WatermarkOutput，可以基于事件做各种操作 
  - onPeriodicEmit：周期性调用的方法，可以由WatermarkOutput发出水位线。周期时间为处理时间，可以调用环境配置的.setAutoWatermarkInterval()方法来设置，默认为200ms。 

##### Flink内置水位线生成器
+ 有序流水位线（Monotonous Timestamps）,时间戳单调递增，用于生成周期水位线
  ```java
  WatermarkStrategy.<Event>forMonotonousTimestamps()
      .withTimestampAssigner(new SerializableTimestampAssigner<Event>() {
          @Override
          public long extractTimestamp(Event element, long recordTimestamp) {
              return element.timestamp; // 必须返回毫秒时间戳
          }
      });
  ```

+ 乱序流水位线（Bounded Out-of-Orderness），允许一定范围内的乱序事件，通过设置延时
  - code：
  ```java 
  public class WatermarkTest {
      public static void main(String[] args) throws Exception {
          StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
          env.setParallelism(1);

          env.addSource(new ClickSource())
              // 插入水位线的逻辑
              .assignTimestampsAndWatermarks(
                  // 针对乱序流插入水位线，延迟时间设置为5秒
                  WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                      .withTimestampAssigner(new SerializableTimestampAssigner<Event>() {
                          // 抽取时间戳的逻辑
                          @Override
                          public long extractTimestamp(Event element, long recordTimestamp) {
                              return element.timestamp;
                          }
                      })
              )
              .print();

          env.execute();
      }
  }
  ```
+ 重要实现细节：
  - 水位线计算公式：`maxTimestamp - outOfOrdernessMillis - 1`
  - 源码示例：
  ```java
  public void onPeriodicEmit(WatermarkOutput output) {
      output.emitWatermark(new Watermark(maxTimestamp - outOfOrdernessMillis - 1));
  }
  ```

##### 自定义水位线策略
+ WatermarkGenerator接口实现：
  - 周期性生成器（Periodic Generator）
    ```java
    public static class CustomWatermarkStrategy implements WatermarkStrategy<Event> {
        @Override
        public TimestampAssigner<Event> createTimestampAssigner(Context context) {
            return new SerializableTimestampAssigner<Event>() {
                @Override
                public long extractTimestamp(Event element, long recordTimestamp) {
                    return element.timestamp; // 显式指定时间戳字段
                }
            };
        }

        @Override
        public WatermarkGenerator<Event> createWatermarkGenerator(Context context) {
            return new WatermarkGenerator<Event>() {
                private final long delay = 5000L;
                private long maxTs = Long.MIN_VALUE + delay + 1L;

                @Override
                public void onEvent(Event event, long eventTs, WatermarkOutput output) {
                    maxTs = Math.max(eventTs, maxTs);
                }

                @Override
                public void onPeriodicEmit(WatermarkOutput output) {
                    output.emitWatermark(new Watermark(maxTs - delay - 1L));
                }
            };
        }
    }
    ```

  -  断点式生成器（Punctuated Generator）
    ```java
    public class CustomPunctuatedGenerator implements WatermarkGenerator<Event> {

        @Override
        public void onEvent(Event r, long eventTimestamp, WatermarkOutput output) {
            // 只有在遇到特定的itemId时，才发出水位线
            if (r.user.equals("Mary")) {
                output.emitWatermark(new Watermark(r.timestamp - 1));
            }
        }

        @Override
        public void onPeriodicEmit(WatermarkOutput output) {
            // 不需要做任何事情，因为我们在onEvent方法中发射了水位线
        }
    }
    ```

+ 5. 自定义数据源水位线
  - 关键限制：
    - 与`assignTimestampsAndWatermarks()`方法互斥
    - 必须使用`collectWithTimestamp`明确时间戳
  - 完整实现示例：
    ```java
    import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
    import org.apache.flink.streaming.api.functions.source.SourceFunction;
    import org.apache.flink.streaming.api.watermark.Watermark;

    import java.util.Calendar;
    import java.util.Random;

    public class EmitWatermarkInSourceFunction {
        public static void main(String[] args) throws Exception {
            StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
            env.setParallelism(1);

            env.addSource(new ClickSourceWithWatermark()).print();

            env.execute();
        }

        // 泛型是数据源中的类型
        public static class ClickSourceWithWatermark implements SourceFunction<Event> {
            private boolean running = true;

            @Override
            public void run(SourceContext<Event> sourceContext) throws Exception {
                Random random = new Random();
                String[] userArr = {"Mary", "Bob", "Alice"};
                String[] urlArr  = {"./home", "./cart", "./prod?id=1"};

                while (running) {
                    long currTs = Calendar.getInstance().getTimeInMillis(); // 毫秒时间戳
                    String username = userArr[random.nextInt(userArr.length)];
                    String url      = urlArr[random.nextInt(urlArr.length)];
                    Event event = new Event(username, url, currTs);

                    // 使用collectWithTimestamp方法将数据发送出去，并指明数据中的时间戳字段
                    sourceContext.collectWithTimestamp(event, event.timestamp);

                    // 发送水位线
                    sourceContext.emitWatermark(new Watermark(event.timestamp - 1L));

                    Thread.sleep(1000L);
                }
            }

            @Override
            public void cancel() {
                running = false;
            }
        }
    }
    ```


+ 注意事项（补充）
  - 时间单位必须统一为毫秒
  - 默认水位线间隔：200ms，可通过`env.getConfig().setAutoWatermarkInterval()`修改
  - 乱序流延迟设置原则：`maxOutOfOrderness >= 实际最大网络延迟`
  - 水位线传播机制：取分区最小水位线作为整体水位线

#### 水位线传递
+ 水位线传递机制
  - 水位线作为事件时间进展标记，随数据在任务间传递
  - 每个任务维护独立时钟（无全局统一时钟）
  - 时钟更新触发条件：收到所有上游分区的"数据已到齐"保证

+ 并行任务处理规则：
    1. 上游多分区发送水位线时，下游任务为每个分区维护分区水位线
    2. 任务时钟 = 所有分区水位线的最小值（木桶原理）
      ``` 
      上游分区水位线：[5s, 7s, 3s, 6s] → 任务时钟 = 3s
      ```

+ 关键处理流程：
    - 步骤1：接收上游分区水位线
      - 更新对应分区水位线值
    - 步骤2：计算全局时钟
      - 新时钟 = min(所有分区水位线)
    - 步骤3：时钟推进判断
      - 若新时钟 > 当前时钟 → 触发广播
      - 若新时钟 ≤ 当前时钟 → 维持不变



### 窗口
+ 窗口是处理无限流的核心，窗口将流切割成有限大小的多个批次，这样就可以对每个批次进行计算。常见的有一天、一月、一小时、一分钟等时间窗口。
  - flink的时间语义下，窗口的关闭时间实际上是延时关闭的。
  - 数据来的时候自带时间戳，根据时间戳判断属于哪个窗口，然后放入对应的窗口中，若窗口没有则自动创建。（可将窗口看做桶来处理）

#### 窗口类型
+ 驱动类型分类
  - 时间驱动：固定时间段为一个窗口，TimeWindow类，以[Long start,Long end)表示一段时间，单位ms。
  - 事件驱动：当事件数量达到某个值时触发，计算窗口。
+ 分配数据规则分类：
  - 滚动窗口：固定大小，不重叠，单参数表示窗口大小
  - 滑动窗口：固定大小，可重叠，一参表示窗口大小，一参表示滑动步长(上一个窗口开始多久后此窗口开始)
  - 会话窗口：无固定大小，当固定时间间隔内无数据到来，该窗口关闭
  - 全局窗口：所有数据都进入一个窗口，相当与没有开窗，需要手动触发计算（自定义触发器）
#### 窗口API
+ 分区窗口Keyed Windows
  ```java
  stream.keyBy(<key selector>) 
  .window(<window assigner>) 
  .aggregate(<window function>)
  ```
+ 全局窗口All Windows
```java
streamallWindow(<WindowAssigner>)
.aggregate(<window function>)
```
#### 窗口构建
##### 窗口分配器
+ 构建：调用.window(<WindowAssigner>)方法。返回 WindowedStream。如果是非按键分区窗口，那么直接调用.windowAll(WindowAssigner)方法，同，返回的是AllWindowedStream。
+ 滚动时间窗口构建：
  ```java
  stream.keyBy(...) 
    .window(TumblingProcessingTimeWindows.of(Time.seconds(5))) 
    .aggregate(...)
  ```
  - of()方法中传入一个Time类型的参数，表示窗口的大小
  - of重载方法：of.of(Time.days(1), Time.hours(-8))，第一个参数表示窗口大小，第二个参数表示滑动步长，因其默认为零时区，加上-8偏移正好为北京时间。
+ 时间滑动窗口
  ```java
  stream.keyBy(...) 
    .window(SlidingProcessingTimeWindows.of(Time.seconds(10), Time.seconds(5))) 
    .aggregate(...) 
  ``` 
  - 第一个参数表示窗口大小，第二个参数表示滑动步长,类似滚动窗口也可使用重载的of方法。
+ 时间会话窗口
  ```java
  stream.keyBy(...) 
    .window(ProcessingTimeSessionWindows.withGap(Time.seconds(10))) 
    .aggregate(...) 
  ```
  - .withGap(Time.seconds(10)):设置会话超时时间10s
+ 滚动事件时间窗口 
  - 窗口分配器由类TumblingEventTimeWindows提供，用法与滚动处理事件窗口完全一致。
  ```java 
  stream.keyBy(...) 
  .window(TumblingEventTimeWindows.of(Time.seconds(5))) 
  .aggregate(...)
  ``` 
这里.of()方法也可以传入第二个参数offset，用于设置窗口起始点的偏移量。 
+ 滑动事件时间窗口 
  - 窗口分配器由类SlidingEventTimeWindows 提供，用法与滑动处理事件窗口完全一致。 
  ```java
  stream.keyBy(...) 
  .window(SlidingEventTimeWindows.of(Time.seconds(10), Time.seconds(5))) 
  .aggregate(...)
  ``` 
+ 事件时间会话窗口 
  - 窗口分配器由类EventTimeSessionWindows 提供，用法与处理事件会话窗口完全一致。
  ```java 
  stream.keyBy(...) 
  .window(EventTimeSessionWindows.withGap(Time.seconds(10))) 
  .aggregate(...) 
  ```
+ 滚动计数窗口 
  - 滚动计数窗口只需要传入一个长整型的参数size，表示窗口的大小。 
  ```java
  stream.keyBy(...) 
  .countWindow(10)
  ``` 
  - 我们定义了一个长度为10的滚动计数窗口，当窗口中元素数量达到10的时候，就会触发计算执行并关闭窗口。 
+ 滑动计数窗口 
  - 与滚动计数窗口类似，不过需要在.countWindow()调用时传入两个参数：size和slide，前者表示窗口大小，后者表示滑动步长。 
  ```java
  stream.keyBy(...) 
  .countWindow(10，3) 
  ```
  - 我们定义了一个长度为10、滑动步长为3的滑动计数窗口。每个窗口统计10个数据，每隔3个数据就统计输出一次结果。
+ 全局窗口：
  - 全局窗口是计数窗口的底层实现，一般在需要自定义窗口时使用。它的定义同样是直接调用.window()，分配器由GlobalWindows 类提供。 
  ```java
  stream.keyBy(...) 
  .window(GlobalWindows.create()); 
  ```
  - 需要注意使用全局窗口，必须自行定义触发器才能实现窗口计算，否则起不到任何作用。
##### 窗口函数(数据处理主体)
+ 增量聚合函数：AggregateFunction
  - 来了就计算，将中间结果保存，当窗口关闭时返回最终结果。
  - 常用：ReduceFunction、AggregateFunction
+ 约归函数：ReduceFunction
  - 来了一个数据，就和之前的状态做约归，返回新的状态。
  - **聚合状态类型、输出、入结果类型必须一致**
+ 聚合函数：AggregateFunction
  - 解决ReduceFunction聚合状态类型、输出、入结果类型不一致时如何处理的问题。
  - 需要实现AggregateFunction类
  ```java
  public interface AggregateFunction<IN, ACC, OUT> extends Function, Serializable 
  { 
    ACC createAccumulator(); 
    ACC add(IN value, ACC accumulator); 
    OUT getResult(ACC accumulator); 
    
    ACC merge(ACC a, ACC b); 
  }
  ```
  -  createAccumulator()：创建一个累加器，这就是为聚合创建了一个初始状态，每个聚合任务只会调用一次。 **配合hashset可创建保存多个数据的累加器**
  -  add()：将输入的元素添加到累加器中。这就是基于聚合状态，对新来的数据进行进一步聚合的过程。方法传入两个参数：当前新到的数据 value，和当前的累加器accumulator；返回一个新的累加器值，也就是对聚合状态进行更新。每条数据到来之后都会调用这个方法。 
  -  getResult()：从累加器中提取聚合的输出结果。也就是说，我们可以定义多个状态，然后再基于这些聚合的状态计算出一个结果进行输出。比如之前我们提到的计算平均值，就可以把sum和count作为状态放入累加器，而在调用这个方法时相除得到最终结果。这个方法只在窗口要输出结果时调用。 
  -  merge()：合并两个累加器，并将合并后的状态作为一个累加器返回。这个方法只在需要合并窗口的场景下才会被调用；最常见的合并窗口（Merging Window）的场景就是会话窗口（Session Windows）。 
 

 + 全局窗口函数：必须先收集所有的数据再进行计算是使用
 + 全窗口函数：WindowFunction(老版本，易弃用)
  - WindowFunction 字面上就是“窗口函数”，它其实是老版本的通用窗口函数接口。我们可以基于WindowedStream调用.apply()方法，传入一个WindowFunction的实现类。 
  ```java
  stream 
    .keyBy(<key selector>) 
    .window(<window assigner>) 
    .apply(new MyWindowFunction()); 
  ```
  - 这个类中可以获取到包含窗口所有数据的可迭代集合（Iterable），还可以拿到窗口（Window）本身的信息。WindowFunction接口在源码中实现如下： 
  ```java
  public interface WindowFunction<IN, OUT, KEY, W extends Window> extends Function, 
  Serializable { 
    void apply(KEY key, W window, Iterable<IN> input, Collector<OUT> out) throws 
    Exception; 
  } 
  ```
+ 全-处理窗口函数（ProcessWindowFunction） 
  - ProcessWindowFunction 是 Window API 中最底层的通用窗口函数接口。之所以说它“最底层”，是因为除了可以拿到窗口中的所有数据之外，ProcessWindowFunction还可以获取到一个“上下文对象”（Context）。这个上下文对象非常强大，不仅能够获取窗口信息，还可以访问当前的时间和状态信息。这里的时间就包括了处理时间（processing time）和事件时间水位线（event time watermark）。这就使得ProcessWindowFunction更加灵活、功能更加丰富。事实上，ProcessWindowFunction是Flink底层API——处理函数（process function）中的一员
  - 这些好处是以牺牲性能和资源为代价的。作为一个全窗口函数，ProcessWindowFunction同样需要将所有数据缓存下来、等到窗口触发计算时才使用。它其实就是一个增强版的WindowFunction。通过传入一个ProcessWindowFunction的实现类使用
  - 电商统计每小时uv例子
  ```java
  public class UvCountByWindowExample {
      public static void main(String[] args) throws Exception {
          StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
          env.setParallelism(1);

          SingleOutputStreamOperator<Event> stream = env.addSource(new ClickSource())
                  .assignTimestampsAndWatermarks(
                          WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ZERO)
                                  .withTimestampAssigner(new SerializableTimestampAssigner<Event>() {
                                      @Override
                                      public long extractTimestamp(Event element, long recordTimestamp) {
                                          return element.timestamp;
                                      }
                                  })
                  );

          // 将数据全部发往同一分区，按窗口统计UV
          stream.keyBy(data -> true)
                  .window(TumblingEventTimeWindows.of(Time.seconds(10)))
                  .process(new UvCountByWindow())
                  .print();

          env.execute();
      }

      // 自定义窗口处理函数
      public static class UvCountByWindow extends ProcessWindowFunction<Event, String, Boolean, TimeWindow> {
          @Override
          public void process(Boolean aBoolean, Context context, Iterable<Event> elements, Collector<String> out) throws Exception {
              HashSet<String> userSet = new HashSet<>();
              // 遍历所有数据，放到Set里去重
              for (Event event : elements) {
                  userSet.add(event.user);
              }
              // 结合窗口信息，包装输出内容
              Long start = context.window().getStart();
              Long end = context.window().getEnd();
              out.collect("窗口: " + new Timestamp(start) + " ~ " + new Timestamp(end)
                      + " 的独立访客数量是：" + userSet.size());
          }
      }
  }
  ```
+ **增量聚合和全窗口函数的结合使用(实战)**
  - 在使用增量聚合时多传入一个全窗口函数，全窗口函数提供更多信息，聚合函数负责实时处理。
  ```java
  // ReduceFunction 与 WindowFunction 结合 
  public <R> SingleOutputStreamOperator<R> reduce( 
      ReduceFunction<T> reduceFunction, 
      WindowFunction<T, R, K, W> function)  

  // ReduceFunction 与 ProcessWindowFunction 结合 
  public <R> SingleOutputStreamOperator<R> reduce( 
      ReduceFunction<T> reduceFunction, 
      ProcessWindowFunction<T, R, K, W> function) 

  // AggregateFunction 与 WindowFunction 结合 
  public <ACC, V, R> SingleOutputStreamOperator<R> aggregate( 
      AggregateFunction<T, ACC, V> aggFunction, 
      WindowFunction<V, R, K, W> windowFunction) 

  // AggregateFunction 与 ProcessWindowFunction 结合 
  public <ACC, V, R> SingleOutputStreamOperator<R> aggregate( 
      AggregateFunction<T, ACC, V> aggFunction, 
      ProcessWindowFunction<V, R, K, W> windowFunction) 
  ``` 
  - 统计10秒钟的url浏览量，每5秒钟更新一次:
  ```java
  public class UrlViewCountExample { 
      public static void main(String[] args) throws Exception { 
          StreamExecutionEnvironment env = 
              StreamExecutionEnvironment.getExecutionEnvironment(); 
          env.setParallelism(1); 
  
          SingleOutputStreamOperator<Event> stream = env.addSource(new 
              ClickSource()) 
              .assignTimestampsAndWatermarks(
                  WatermarkStrategy.<Event>forMonotonousTimestamps() 
                      .withTimestampAssigner(new SerializableTimestampAssigner<Event>() { 
                          @Override 
                          public long extractTimestamp(Event element, long recordTimestamp) { 
                              return element.timestamp; 
                          } 
                      })
              ); 
  
          // 需要按照url分组，开滑动窗口统计 
          stream.keyBy(data -> data.url) 
              .window(SlidingEventTimeWindows.of(Time.seconds(10), Time.seconds(5))) 
              // 同时传入增量聚合函数和全窗口函数 
              .aggregate(new UrlViewCountAgg(), new UrlViewCountResult()) 
              .print(); 
  
          env.execute(); 
      } 
  
      // 自定义增量聚合函数，来一条数据就加一 
      public static class UrlViewCountAgg implements AggregateFunction<Event, Long, Long> { 
          @Override 
          public Long createAccumulator() { 
              return 0L; 
          } 
  
          @Override 
          public Long add(Event value, Long accumulator) { 
              return accumulator + 1; 
          } 
  
          @Override 
          public Long getResult(Long accumulator) { 
              return accumulator; 
          } 
  
          @Override 
          public Long merge(Long a, Long b) { 
              return null; 
          } 
      } 
  
      // 自定义窗口处理函数，只需要包装窗口信息 
      public static class UrlViewCountResult extends ProcessWindowFunction<Long, UrlViewCount, String, TimeWindow> { 
  
          @Override 
          public void process(String url, Context context, Iterable<Long> elements, 
                              Collector<UrlViewCount> out) throws Exception { 
              // 结合窗口信息，包装输出内容 
              Long start = context.window().getStart(); 
              Long end = context.window().getEnd(); 
              // 迭代器中只有一个元素，就是增量聚合函数的计算结果 
              out.collect(new UrlViewCount(url, elements.iterator().next(), start, end)); 
          } 
      } 
  }
  ```
#### 触发器trigger
+ 使用
  ```java
  stream.keyBy(...) 
    .window(...) 
    .trigger(new MyTrigger()) 
  ```
+ tringger:需要实现Trigger接口，并重写里面的方法
  - onElement()：窗口中每到来一个元素，都会调用这个方法。 
  - onEventTime()：当注册的事件时间定时器触发时，将调用这个方法。 
  - onProcessingTime ()：当注册的处理时间定时器触发时，将调用这个方法。 
  - clear()：当窗口关闭销毁时，调用这个方法。一般用来清除自定义的状态。
+ on方法都可以响应事件，返回值是一个枚举TriggerResult，包括CONTINUE继续、FIRE触发、PURGE清除、FIRE_AND_PURGE触发并清除，eg：return TriggerResult.FIRE;
#### 清理器
+ 基于WindowedStream调用.evictor()方法，就可以传入一个自定义的移除器（Evictor）
  ```java
  stream.keyBy(...) 
    .window(...) 
    .evictor(new MyEvictor()) 
  ```
+ Evictor:需要实现Evictor接口，并重写里面的方法
  - evictBefore()：定义执行窗口函数之前的移除数据操作 
  - evictAfter()：定义执行窗口函数之后的以处数据操作 默认情况下，预实现的移除器都是在执行窗口函数（window fucntions）之前移除数据的。
#### 迟到数据处理
##### 允许延时（网络大几百ms延时的有限等待）
+ 基于WindowedStream 调用.allowedLateness()方法，传入一个 Time类型的延迟时间，就可以表示允许这段时间内的延迟数据。 
  ```java
  stream.keyBy(...) 
    .window(TumblingEventTimeWindows.of(Time.hours(1))) 
    .allowedLateness(Time.minutes(1))
  ```
  - 定义了1小时的滚动窗口，并设置了允许1分钟的延迟数据
##### 侧输出流（兜底）
+ 基于WindowedStream 调用.sideOutputLateData()方法，传入一个 OutputTag，用于标记延迟数据。
  ```java
  DataStream<Event> stream = env.addSource(...); 

  OutputTag<Event> outputTag = new OutputTag<Event>("late") {}; 
  stream.keyBy(...) 
    .window(TumblingEventTimeWindows.of(Time.hours(1))) 
    .sideOutputLateData(outputTag) 
  ```
+ 侧输出流的使用:将迟到数据放入侧输出流之后，还应该可以将它提取出来。基于窗口处理完成之后的DataStream，调用.getSideOutput()方法，传入对应的输出标签，就可以获取到迟到数据所在的流了。
  ```java
  SingleOutputStreamOperator<AggResult> winAggStream = stream.keyBy(...) 
    .window(TumblingEventTimeWindows.of(Time.hours(1))) 
    .sideOutputLateData(outputTag) 
    .aggregate(new MyAggregateFunction()) 
  DataStream<Event> lateStream = winAggStream.getSideOutput(outputTag); 
  ```
  - 这里注意，getSideOutput()是 SingleOutputStreamOperator 的方法，获取到的侧输出流数据类型应该和OutputTag指定的类型一致，与窗口聚合之后流中的数据类型可以不同。
 
## 处理函数Process function(底层api)
+ **stream.process(new MyProcessFunction())** 
+ 基于 DataStream 调用.process()方法就可以了。方法需要传入一个ProcessFunction作为参数，用来定义处理逻辑。
  - 这里 ProcessFunction 不是接口，而是一个抽象类，继承了 AbstractRichFunction；MyProcessFunction 是它的一个具体实现。所以所有的处理函数，都是富函（RichFunction），富函数可以调用的东西这里同样都可以调用。 
### **process function 方法**
```java
public abstract class ProcessFunction<I, O> extends AbstractRichFunction # I:输入类型，O:输出类型
{ 
 
public abstract void processElement(I value, Context ctx, Collector<O> out) throws Exception; 

public void onTimer(long timestamp, OnTimerContext ctx, Collector<O> out) throws Exception {} 
 
} 
```
#### processElement(I value，Context ctx，Collector<O> out)
+ 抽象方法，用于处理流中的每一个元素。
+ value：输入元素
+ ctx：上下文，可以获取到当前处理事件的 timestamp 和对应的时间戳、侧输出流、定时器。
+ ctx抽象类定义
  ```java
  public abstract class Context { 
    public abstract Long timestamp(); 
    public abstract TimerService timerService(); 
    public abstract <X> void output(OutputTag<X> outputTag, X value); 
  } 
  ```
  - timerService()：获取当前时间服务，可以用来注册定时器。
  - output()：向侧输出流中输出一个元素。
  - timestamp()：获取当前处理事件的 timestamp。
+ out：收集器，用来输出数据。
  - “收集器”（类型为Collector），用于返回输出数据。使用方式与flatMap算子中的收集器完全一样，直接调用 out.collect()方法就可以向下游发出一个数据。这个方法可以多次调用，也可以不调用。
#### onTimer(Long timestamp，OnTimerContext ctx，Collector<O> out)
+ 非抽象方法，当定时器触发时被调用，故可用其实现窗口。
+ timestamp：设置好的触发时间。
+ ctx：上下文，可以获取到当前处理事件的 timestamp 和对应的时间戳、侧输出流。
+ out：收集器，用来输出数据。

### 按键分区处理函数KeyedProcessFunction
+ 先分区再进行计算，可充分利用并行计算优势，普通processFunction无法使用定时器，仅有分区后才注册、删除定时器。
#### Timer && TimerService
+ TimerService对象，通过ctx.timerService()获取
  ```java 
  // 获取当前的处理时间 
  long currentProcessingTime(); 
  // 注册处理时间定时器，当处理时间超过time时触发 
  void registerProcessingTimeTimer(long time); 
  // 删除触发时间为time的处理时间定时器 
  void deleteProcessingTimeTimer(long time);

  // 获取当前的水位线（事件时间） 
  long currentWatermark(); 
  // 注册事件时间定时器，当水位线超过time时触发 
  void registerEventTimeTimer(long time);  
  // 删除触发时间为time的处理时间定时器 
  void deleteEventTimeTimer(long time); 
  ```
  - 处理事件时间与处理时间的定时器，timeService内部以优先队列保存其时间戳。
  - 在keyedStream中，对于每个key和时间戳，最多只有一个定时器，如果注册了多次，onTimer()方法也将只被调用一次。
  - 基于KeyedStream 注册定时器时，会传入一个定时器触发的时间戳，这个时间戳的定时器对于每个key都是有效的。这样，我们的代码并不需要做额外的处理，底层就可以直接对不同key 进行独立的处理操作了。利用这个特性，有时我们可以故意降低时间戳的精度，来减少定时器的数量，从而提高处理性能。比如我们可以在设置定时器时只保留整秒数，那么定时器的触发频率就是最多1秒一次。
  - 时间戳在定时器中精度是毫秒级，同时支持检查点。
#### KeyedProcessFunction使用
+ stream.keyBy( t -> t.f0 ).process(new MyKeyedProcessFunction()) 
+ keyedProcess抽象类定义，使用同processFunction
```java
public abstract class KeyedProcessFunction<K, I, O> extends AbstractRichFunction # K:分区key,I:输入类型，O:输出类型
{  

  public abstract void processElement(I value, Context ctx,Collector<O> out) throws Exception; 
  public void onTimer(long timestamp, OnTimerContext ctx, Collector<O> out) throws Exception {} 
  public abstract class Context {...} 

} 
```
+ 示例：
  -  ctx.timerService().registerProcessingTimeTimer(currTs + 10 
* 1000L); //注册一个10秒后的定时器
  - onTimer()方法会在定时器触发时被调用，在此方法中进行触发处理，timestamp为定时器触发时间，ctx为上下文，out为收集器。
  - code
  ```java
  import org.apache.flink.streaming.api.datastream SingleOutputStreamOperator; 
  import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment; 
  import org.apache.flink.streaming.api.functions.KeyedProcessFunction; 
  import org.apache.flink.util.Collector; 
   
  import java.sql.Timestamp; 
   
  public class ProcessingTimeTimerTest { 
      public static void main(String[] args) throws Exception { 
          StreamExecutionEnvironment env = 
  StreamExecutionEnvironment.getExecutionEnvironment(); 
          env.setParallelism(1); 
   
          // 处理时间语义，不需要分配时间戳和watermark 
          SingleOutputStreamOperator<Event> stream = env.addSource(new 
  ClickSource()); 
   
          // 要用定时器，必须基于KeyedStream 
          stream.keyBy(data -> true) 
                  .process(new KeyedProcessFunction<Boolean, Event, String>() { 
                      @Override 
                      public void processElement(Event value, Context ctx, 
  Collector<String> out) throws Exception { 
                          Long currTs = ctx.timerService().currentProcessingTime(); 
                          out.collect("数据到达，到达时间：" + new Timestamp(currTs)); 
                          // 注册一个10秒后的定时器 
                          ctx.timerService().registerProcessingTimeTimer(currTs + 10 
  * 1000L); 
                      } 
                      @Override 
                      public void onTimer(long timestamp, OnTimerContext ctx, 
  Collector<String> out) throws Exception { 
                          out.collect("定时器触发，触发时间：" + new Timestamp(timestamp)); 
                      } 
                  }) 
                  .print(); 
   
          env.execute(); 
      } 
  } 
  ```
### 窗口处理函数
```java
public abstract class ProcessWindowFunction<IN, OUT, KEY, W extends Window>// IN:输入类型，OUT:输出类型，KEY:分区key，W:窗口类型
        extends AbstractRichFunction {

    public abstract void process(
            KEY key, // 分区key
            Context context,//窗口上下文
            Iterable<IN> elements,
            Collector<OUT> out //收集器
    ) throws Exception;

    public void clear(Context context) throws Exception {
       //清理窗口状态
    }

    public abstract class Context implements java.io.Serializable {
        // Class implementation remains unchanged
    }
}
```
#### 窗口上下文
```java
public abstract class Context implements java.io.Serializable { 
  //获取窗口状态
  public abstract W window(); 
  //获取当前时间戳
  public abstract long currentProcessingTime(); 
  public abstract long currentWatermark(); 

  // 获取窗口状态
  public abstract KeyedStateStore windowState(); 
  // 获取全局状态
  public abstract KeyedStateStore globalState(); 
  public abstract <X> void output(OutputTag<X> outputTag, X value); 
} 
```
### 侧输出流
+ 定义输出标签：OutputTag<T> outputTag = new OutputTag<T>("side-output"){};
+ 实例
  ```java
  DataStream<Integer> stream = env.addSource(...);

  SingleOutputStreamOperator<Long> longStream = stream.process(
      new ProcessFunction<Integer, Long>() {
          @Override
          public void processElement(Integer value, Context ctx, Collector<Integer> out) throws Exception {
              // 转换成Long，输出到主流中
              out.collect(Long.valueOf(value));
              
              // 转换成String，输出到侧输出流中
              ctx.output(outputTag, "side-output: " + String.valueOf(value));
          }
      }
  );
  ```
+  获取侧输出流：DataStream<string> StringStream = longStream.getSideOutput(outputTag);

## 多流转换
### 分流：直接使用侧输出流
### 合流Union
+ 合并两个或者多个相同类型的流，合并后类型为原类型，时间以最早的流为准（保证水位线的本质含义，是“之前的所有数据已经到齐了”）
+ eg
```java
stream1.union(stream2)
    .process(new ProcessFunction<Event, String>() {
        @Override
        public void processElement(Event value, Context ctx, Collector<String> out) throws Exception {
            // 输出当前事件的时间戳和当前水位线
            out.collect("时间戳: " + value.getTimestamp() + ", 水位线: " + ctx.timerService().currentWatermark());
        }
    })
    .print(); // 打印结果
```
### 连接：connect
+ 连接操作允许流的数据类型不同,连接后形式上统一了，但在流内部还是保持原来的类型不变，需要分别各定义一个processfunction。
+ **实现：**分两步，先基于一条DataStream调用.connect()方法，再调用同处理方法.Map/.flatMap/.process()方法得到datastream。
+ eg：
  - .map1()就是对第一条流中数据的map操作，.map2()则是针对第二条流。
  - ConnectedStreams 也可以直接调用.keyBy()进行按键分区的操作，得到的还是一个ConnectedStreams，connectedStreams.keyBy(keySelector1, keySelector2); 这里传入两个参数keySelector1 和 keySelector2，是两条流中各自的键选择器
  ```java
  import org.apache.flink.streaming.api.datastream.ConnectedStreams;
  import org.apache.flink.streaming.api.datastream.DataStream;
  import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
  import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
  import org.apache.flink.streaming.api.functions.co.CoMapFunction;

  public class CoMapExample {
      public static void main(String[] args) throws Exception {
          StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
          env.setParallelism(1);

          DataStream<Integer> stream1 = env.fromElements(1, 2, 3);
          DataStream<Long> stream2 = env.fromElements(1L, 2L, 3L);

          ConnectedStreams<Integer, Long> connectedStreams = stream1.connect(stream2);
          SingleOutputStreamOperator<String> result = connectedStreams.map(new CoMapFunction<Integer, Long, String>() {
              @Override
              public String map1(Integer value) {
                  return "Integer: " + value;
              }

              @Override
              public String map2(Long value) {
                  return "Long: " + value;
              }
          });

          result.print();
          env.execute();
      }
  }
  ```
#### 连接流processfunction
+ 连接流的处理，需要在接口中分别定义两条流的处理方法，此接口称为协同处理函数CoProcessFunction
+ 与CoMapFunction类似，如果是调用.flatMap()就需要传入一个CoFlatMapFunction，需要实现flatMap1()、flatMap2()两个方法；而调用.process()时，传入的则是一个CoProcessFunction。
+ 抽象类CoProcessFunction
  ```java
  public abstract class CoProcessFunction<IN1, IN2, OUT> extends AbstractRichFunction {
      ...
      public abstract void processElement1(IN1 value, Context ctx, Collector<OUT> out) throws Exception;
      public abstract void processElement2(IN2 value, Context ctx, Collector<OUT> out) throws Exception;
      public void onTimer(long timestamp, OnTimerContext ctx, Collector<OUT> out) throws Exception {}
      public abstract class Context {...}//收集器
      ...
  } 
  ```
#### 广播连接流
+ ：DataStream调用.connect()方法时，传入的参数也可以不是一个DataStream，而是一个“广播流”（BroadcastStream），这时合并两条流得到的就变成了一个“广播连接流”（BroadcastConnectedStream）。
+ 应用场景：动态定义规则、动态更新配置，规则是全局生效的，所以需要广播出去，下游子任务收到广播规则后将其保存为一个状态，称为“广播状态”。
+ **广播流的生成**：DataStream调用.broadcast()方法，传入一个映射状态描述器(MapStateDescriptor)，得到一个BroadcastStream。
  ```java
  MapStateDescriptor<String, Rule> ruleStateDescriptor = new 
  MapStateDescriptor<>(...); 
  BroadcastStream<Rule> ruleBroadcastStream = ruleStream 
    .broadcast(ruleStateDescriptor); 
  ```
+ 广播流连接：一条流处理数据，一条流处理规则，对应BroadcasProcessFunction。
  ```java
  public abstract class BroadcastProcessFunction<IN1, IN2, OUT> extends BaseBroadcastProcessFunction {
      ...
      public abstract void processElement(IN1 value, ReadOnlyContext ctx, Collector<OUT> out) throws Exception;
      public abstract void processBroadcastElement(IN2 value, Context ctx, Collector<OUT> out) throws Exception;
      ...
  }    
  ```
### 联接 Join
#### 窗口连接：Window Join（此处为笛卡尔积）
+ 调用DataStream的.join()方法来合并两条流，得到一个 JoinedStreams；接着通过.where()和.equalTo()方法指定两条流中联结的 key；然后通过.window()开窗口，并调用.apply()传入联结窗口函数进行处理计算。
  ```java
  stream1.join(stream2)
      .where(<KeySelector>)
      .equalTo(<KeySelector>)
      .window(<WindowAssigner>)
      .apply(<JoinFunction>)
  ```
  - 此处传入的WindowsAssigner是窗口分配器，三种窗口都可用。
  - apply为特殊的窗口函数，此处仅可调用apply()方法，不能调用reduce()、aggregate()、process()等方法。
  - JoinFunction函数类接口，需要实现join()方法，传入两个参数，分别对应两条流中联结的元素。
#### 间隔联结 Interval Join(仅支持事件时间语义)
+ 针对一条流的每个数据，开辟出其时间戳前后的一段时间间隔，看这期间是否有来自另一条流的数据匹配。
+ 间隔连接是一直内连接，但窗口连接基于数据进行，interval join基于时间进行。
+ interval join调用：间隔联结在代码中，是基于KeyedStream的联结（join）操作。DataStream在keyBy得到KeyedStream 之后，可以调用.intervalJoin()来合并两条流，传入的参数同样是一个KeyedStream，两者的key类型应该一致；得到的是一个IntervalJoin 类型。后续的操作同样是完全固定的：先通过.between()方法指定间隔的上下界，再调用.process()方法，定义对匹配数据对的处理操作。调用.process()需要传入一个处理函数，这是处理函数家族的最后一员：“处理联结函数”ProcessJoinFunction。 
  ```java
  stream1
      .keyBy(<KeySelector>)
      .intervalJoin(stream2.keyBy(<KeySelector>))
      .between(Time.milliseconds(-2), Time.milliseconds(1))
      .process(new ProcessJoinFunction<Integer, Integer, String>() {
          @Override
          public void processElement(Integer left, Integer right, Context ctx, Collector<String> out) {
              out.collect(left + "," + right);
          }
      });
  ```
#### 窗口同组连接 Window CoGroup
+ 窗口同组连接：基于窗口的联结，但联结的 key 不再是数据本身的 key，而是数据所属的窗口。
+ Window coGroup调用：
  ```java
  stream1.coGroup(stream2) 
      .where(<KeySelector>) 
      .equalTo(<KeySelector>) 
      .window(TumblingEventTimeWindows.of(Time.hours(1))) 
      .apply(<CoGroupFunction>) 
  ```
+ apply方法：可通过自定义配对方式实现left、right连接
  - 传入可遍历数据集和，而不是计算笛卡尔积，配对方法需要自定义，out为收集器。
  ```java
  public interface CoGroupFunction<IN1, IN2, O> extends Function, Serializable { 
    void coGroup(Iterable<IN1> first, Iterable<IN2> second, 
    Collector<O> out) 
    throws Exception; 
  } 
  ```

## **状态**
+ 状态：Flink中的状态是用于保存计算过程中的中间结果，以便在后续的计算中可以访问这些中间结果,保存在内存中。
+ 幂等性：数据重复处理而结果不变，如统计种类
+ flink状态管理：
  - 状态访问权限：访问本地状态时的权限控制。
  - 容错性：状态持久化，故障恢复  
  - 拓展性：分布式应用的横向扩展性。比如处理的数据量增大时，我们应该相应地对计算资源扩容，调大并行度。这时就涉及到了状态的重组调整。
+ **使用流程：**外部声明状态、open方法中注册状态描述器并通过ctx获取状态、具体方法中更新状态、使用完毕clear清空状态
+ 状态的访问需要通过RuntimeContext来获取，RuntimeContext是Flink运行时上下文，它提供了很多有用的信息，比如当前子任务的状态句柄、当前子任务的并行度、当前子任务的索引等。**通过getXXXState(状态描述器)方法获取状态**
+ 实例
```java
public static class MyFlatMapFunction extends RichFlatMapFunction<Long, String> {
    // 声明状态，声明在外面保证其作用域覆盖到flatMap方法
    private transient ValueState<Long> state;

    @Override
    public void open(Configuration config) {
        // 在open生命周期方法中获取状态
        ValueStateDescriptor<Long> descriptor = new ValueStateDescriptor<>(
            "my state", // 状态名称
            Types.LONG // 状态类型
        );
        state = getRuntimeContext().getState(descriptor);
    }

    @Override
    public void flatMap(Long input, Collector<String> out) throws Exception {
        // 访问状态
        Long currentState = state.value();
        currentState += 1; // 状态数值加1
        // 更新状态
        state.update(currentState);
        if (currentState >= 100) {
            out.collect("state: " + currentState);
            state.clear(); // 清空状态
        }
    }
}
    
```
### 状态一致性
+ 最多一次(At-most-once)：数据最多会被处理一次，数据可能丢失
+ 至少一次(At-least-once)：数据至少会被处理一次，数据可能重复处理，当数据具有幂等性时相当于精确一次
+ 精确一次(Exactly-once)：数据只会被处理一次，既不丢失也不重复处理，检查点实现了精确一次。

### 状态分类
+ 托管状态（Managed State）和原始状态（Raw State）
  - Managed State：Flink 内部自行进行状态管理，状态是受 Flink 管理的，由 Flink 框架自动进行状态的 checkpoint 和恢复。
  - Raw State：用户自行管理状态，需要自己序列化状态，Flink 不知道状态的具体内容，只负责在 checkpoint 时将状态持久化到外部存储，并在恢复时再将状态从外部存储加载回来。一般不用
+ 算子状态（Operator State）和按键分区状态（Keyed State） 
  - 算子状态：算子并行实例上定义的状态，作用范围被限定为当前算子任务。算子状态跟数据的key无关，所以不同key的数据只要被分发到同一个并行子任务，就会访问到同一个Operator State。
  - 按键分区状态：，是任务按照键（key）来访问和维护的状态。它的特点非常鲜明，就是以key为作用范围进行隔离，必须在KeyBy之后才能使用，
    - 可通过富函数类对转换算子进行扩展、实现自定义功能，比如 RichMapFunction、RichFilterFunction。在富函数中，我们可以调用.getRuntimeContext()获取当前的运行时上下文（RuntimeContext），进而获取到访问状态的句柄；这种富函数中自定义的状态也是Keyed State。
    - ，在应用的并行度改变时，状态也需要随之进行重组。不同key对应的Keyed State可以进一步组成所谓的键组（key groups），每一组都对应着一个并行子任务。键组是Flink重新分配Keyed State 的单元，键组的数量就等于定义的最大并行度。当算子并行度发生改变时，Keyed State 就会按照当前的并行度重新平均分配，保证运行时各个子任务的负载相同。
### Keyed状态支持类型
+ 值状态（ValueState）：保存一个值
  - 通过value()方法获取，update()方法更新。
  - 使用需要创建状态描述器(StateDescriptor)：
  ```java
  stateDescriptor = new ValueStateDescriptor<>("count", BasicTypeInfo.INT_TYPE_INFO);//传入状态名称和类型信息
  ```

+ 列表状态（ListState）：保存一个列表
  - Iterable<T> get()：获取当前的列表状态，返回的是一个可迭代类型Iterable<T>； 
  - update(List<T> values)：传入一个列表values，直接对状态进行覆盖； 
  - add(T value)：在状态列表中添加一个元素value； 
  - addAll(List<T> values)：向列表中添加多个元素，以列表values形式传入。 
  - 使用需要创建状态描述器(StateDescriptor)：
  ```java
  stateDescriptor = new ListStateDescriptor<>("list", BasicTypeInfo.INT_TYPE_INFO);
  ```

+ 映射状态（MapState）：保存一个映射，UK:保存Key类型 UV:value类型
  - UV get(UK key)：传入一个key作为参数，查询对应的value值； 
  - put(UK key, UV value)：传入一个键值对，更新key对应的value值； 
  - putAll(Map<UK, UV> map)：将传入的映射map中所有的键值对，全部添加到映射状
态中； 
  - remove(UK key)：将指定key对应的键值对删除； 
  - boolean contains(UK key)：判断是否存在指定的key，返回一个boolean值。 
另外，MapState也提供了获取整个映射相关信息的方法： 
  - Iterable<Map.Entry<UK, UV>> entries()：获取映射状态中所有的键值对； 
  - Iterable<UK> keys()：获取映射状态中所有的键（key），返回一个可迭代Iterable类型； 
  - Iterable<UV> values()：获取映射状态中所有的值（value），返回一个可迭代 Iterable
类型； 
  - boolean isEmpty()：判断映射是否为空，返回一个boolean值。 
  - 使用需要创建状态描述器(StateDescriptor)：
  ```java
  stateDescriptor = new MapStateDescriptor<>("map", BasicTypeInfo.INT_TYPE_INFO, BasicTypeInfo.STRING_TYPE_INFO);
  ```

+ 规约状态（ReducingState）：保存一个值，支持规约操作
  - 规约：新加入数据与状态进行规约，得到新的状态，并更新状态。(eg:max()实现)
  - ReducintState<T>这个接口调用的方法类似于 ListState，只不过它保存的只是一个聚合值，所以调用.add()方法时，不是在状态列表里添加元素，而是直接把新数据和之前的状态进行归约，并用得到的结果更新状态
  - **归约逻辑的定义**，是在归约状态描述器（ReducingStateDescriptor）中，通过传入一个归约函数（ReduceFunction）来实现的。这里的归约函数就是ReduceFunction，所以状态类型跟输入的数据类型是一样的。
  ```java 
  //归约状态描述器（ReducingStateDescriptor）
  public ReducingStateDescriptor( 
  String name, ReduceFunction<T> reduceFunction, Class<T> typeClass) 
  //其中第二个参数就是定义了归约聚合逻辑的ReduceFunction，另外两个参数则是状态的名称和类型。
  {...}
  ```

+ 聚合状态(AggregatingState):
  - 与归约状态非常类似，聚合状态也是一个值，用来保存添加进来的所有数据的聚合结果。**与 ReducingState 不同的是**，它的聚合逻辑是由在描述器中传入一个更加一般化的聚合函数（AggregateFunction）来定义的；这也就是之前我们讲过的 AggregateFunction，里面通过一个累加器（Accumulator）来表示状态，**所以聚合的状态类型可以跟添加进来的数据类型完全不同**，使用更加灵活
  - AggregatingState 接口调用方法也与ReducingState 相同，调用.add()方法添加元素时，会直接使用指定的AggregateFunction进行聚合并更新状态。

### 状态生存时间TTL(flink默认关闭)
+ TTL(time-to-live)：当状态在内存中存在的时间超出这个值时，就将它清除,flink采用的是惰性清理即当访问到状态时，才会判断其是否过期，过期则清除。
  - 惰性清理：访问一个会话，而该会话状态已过期，返回NULL，并清理状态。
+ TTL配置：创建SateConfig配置对象，调用enableTimeToLive()方法启动TTL
```java
StateTtlConfig ttlConfig = StateTtlConfig
    .newBuilder(Time.seconds(10))
    .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
    .setStateVisibility(StateTtlConfig.StateVisibility.NeverReturnExpired)
    .build();
ValueStateDescriptor<String> stateDescriptor = new ValueStateDescriptor<>("my state", String.class);
stateDescriptor.enableTimeToLive(ttlConfig);
```
  - .newBuilder() :TTL配置的构造器方法，必须调用，返回一个Builder之后再调用.build()方法就可以得到StateTtlConfig 了。方法需要传入一个Time作为参数，这就是设定的状态生存时间。 
  - .setUpdateType() ：设置更新类型
    - 更新类型指定了什么时候更新状态失效时间，默认OnCreateAndWrite表示只有创建状态和更改状态（写操作）时更新失效时间。
    - 另一种类型OnReadAndWrite则表示无论读写操作都会更新失效时间，也就是只要对状态进行了访问，就表明它是活跃的，从而延长生存时间。 
  - .setStateVisibility()：设置状态的可见性。
    - 所谓的“状态可见性”，是指因为清除操作并不是实时的，所以当状态过期之后还有可能基于存在，这时如果对它进行访问，能否正常读取到就是一个问题了。这里设置的NeverReturnExpired 是默认行为，表示从不返回过期值，也就是只要过期就认为它已经被清除了，应用不能继续读取；这在处理会话或者隐私数据时比较重要。
    - 对应的另一种配置是ReturnExpireDefNotCleanedUp，就是如果过期状态还存在，就返回它的值。 除此之外，TTL配置还可以设置在保存检查点（checkpoint）时触发清除操作，或者配置增量的清理（incremental cleanup），还可以针对RocksDB 状态后端使用压缩过滤器（compaction filter）进行后台清理。关于检查点和状态后端的内容，我们会在后续章节继续讲解。 
  - 目前的 TTL 设置只支持处理时间。**所有集合类型的状态（例如ListState、MapState）在设置 TTL 时，都是针对每一项（per-entry）元素的**。也就是说，一个列表状态中的每一个元素，都会以自己的失效时间来进行清理，而不是整个列表一起清理。

### 算子状态(Operator State)
+ 是一个算子并行实例上定义的状态，作用范围被限定为当前算子任务。算子状态跟数据的key无关，所以不同key的数据只要被分发到同一个并行子任务，就会访问到同一个Operator State。
+ 算子状态的实际应用场景不如Keyed State多，一般用在Source或Sink等与外部系统连接的算子上，或者完全没有key定义的场景。比如Flink的Kafka连接器中，就用到了算子状态。在我们给 Source 算子设置并行度后，Kafka 消费者的每一个并行实例，都会为对应的主题（topic）分区维护一个偏移量， 作为算子状态保存起来。这在保证 Flink 应用“精确一次”（exactly-once）状态一致性时非常有用。关于状态一致性的内容，
+ 当算子的并行度发生变化时，算子状态也支持在并行的算子任务实例之间做重组分配。根据状态的类型不同，重组分配的方案也会不同。
+ 使用：类似Keyed state使用
  ```java
  ListStateDescriptor<String> descriptor = new ListStateDescriptor<>(
      "buffered-elements",
      Types.of(String)
  );
  ListState<String> checkpointedState = context.getOperatorStateStore().getListState(descriptor); 
  ```

#### 算子状态分类
+ 列表状态（ListState） 
  - 状态表示为一组数据的列表。 与Keyed State 中的列表状态的区别是：在算子状态的上下文中，不会按键（key）分别处理状态，所以每一个并行子任务上只会保留一个“列表”（list），也就是当前并行子任务上所有状态项的集合。
  - 列表中的状态项就是可以重新分配的最细粒度，彼此之间完全独立。 
  - 当算子并行度进行缩放调整时，算子的列表状态中的所有元素项会被统一收集起来，相当于把多个分区的列表合并成了一个“大列表”，然后再均匀地分配给所有并行任务。这种“均匀分配”的具体方法就是“轮询”（round-robin），是通过逐一“发牌”的方式将状态项平均分配的。这种方式也叫作“平均分割重组”（even-split redistribution）。 
  - 算子状态中不会存在“键组”（key group）这样的结构，所以为了方便重组分配，就把它直接定义成了“列表”（list）。这也就解释了，为什么算子状态中没有最简单的值状态（ValueState）。 
+ 联合列表状态（UnionListState） 
  - 状态表示为一个列表。
  - 特别的：算子并行度进行缩放调整时联合列表状态的算子则会直接广播状态的完整列表，可以自行选择要使用的状态项和要丢弃的状态项。这种分配也叫作“联合重组”（union redistribution）。
  - 如果列表中状态项数量太多，为资源和效率考虑一般不建议使用联合重组的方式。
+ 广播状态（BroadcastState） 
  - 有时我们希望算子并行子任务都保持同一份“全局”状态，用来做统一的配置和规则设定。这时所有分区的所有数据都会访问到同一个状态，状态就像被“广播”到所有分区一样，这种特殊的算子状态，就叫作广播状态（BroadcastState）。 
  - 因为广播状态在每个并行子任务上的实例都一样，所以在并行度调整的时候就比较简单，只要复制一份到新的并行任务就可以实现扩展；而对于并行度缩小的情况，可以将多余的并行子任务连同状态直接砍掉——因为状态都是复制出来的，并不会丢失。 
  - 在底层，广播状态是以类似映射结构（map）的键值对（key-value）来保存的，必须基于一个“广播流”（BroadcastStream）来创建。

#### 算子状态恢复-Checkpoint
+ keyed State的回复有flink自动完成，Operator State需要手动恢复。
+ 默认情况下，检查点是被禁用的，需要在代码中手动开启。直接调用执行环境的.enableCheckpointing()方法就可以开启检查点。 
  ```java
  StreamExecutionEnvironment env = StreamExecutionEnvironment.getEnvironment(); 
  env.enableCheckpointing(1000); //设置检查点间隔为1秒
  ```
+ CheckpointedFunction 接口：状态持久化保存机制
  ```java
  public interface CheckpointedFunction {
      // 保存状态快照到检查点时，调用这个方法
      void snapshotState(FunctionSnapshotContext context) throws Exception;
      // 初始化状态时调用这个方法，也会在恢复状态时调用
      void initializeState(FunctionInitializationContext context) throws Exception;
  }   
  ```
  - 初始化状态方法调用，全局初始化时调用状态设置为defualt，重启是从检查点或保存点中读取状态快照。
  - **两个context不同：**snapshotState()方法中获得是快照上下文可提供检查点的相关信息，init方法的是运行上下文可获得状态。

### 广播状态(Broadcast State)
+ 广播状态：算子并行子任务都保持同一份“全局”状态，用来做统一的配置和规则设定。
  ```java
  //这里我们定义了一个“规则流”ruleStream，里面的数据表示了数据流stream处理的规则，规则的数据类型定义为Rule。于是需要先定义一个MapStateDescriptor来描述广播状态，然后传入ruleStream.broadcast()得到广播流，接着用stream和广播流进行连接。这里状态描述器中的key类型为String，就是为了区分不同的状态值而给定的key的名称。对于广播连接流调用.process()方法，可以传入“广播处理函数"KeyedBroadcastProcessFunction或者BroadcastProcessFunction来进行处理计算。广播处理函数里面有两个方法.processElement()和.processBroadcastElement()，源码中定义如下：
  MapStateDescriptor<String, Rule> ruleStateDescriptor = new MapStateDescriptor<>(...);
  BroadcastStream<Rule> ruleBroadcastStream = ruleStream
      .broadcast(ruleStateDescriptor);
  DataStream<String> output = stream
      .connect(ruleBroadcastStream)
      .process(new BroadcastProcessFunction<>() {...});

  //这里的.processElement()方法，处理的是正常数据流，第一个参数value就是当前到来的流数据；而.processBroadcastElement()方法就相当于是用来处理广播流的，它的第一个参数value就是广播流中的规则或者配置数据。两个方法第二个参数都是一个上下文ctx，都可以通过调 用.getBroadcastState()方法获取到当前的广播状态；区别在于，.processElement()方法里的上下文是“只读”的（ReadOnly），因此获取到的广播状态也只能读取不能更改；而.processBroadcastElement()方法里的Context则没有限制，可以根据当前广播流中的数据更状态。 
  public abstract class BroadcastProcessFunction<IN1, IN2, OUT> extends BaseBroadcastProcessFunction {
      ...
      public abstract void processElement(IN1 value, ReadOnlyContext ctx, Collector<OUT> out) throws Exception;
      public abstract void processBroadcastElement(IN2 value, Context ctx, Collector<OUT> out) throws Exception;
      ...
  }

  Rule rule = ctx.getBroadcastState(new MapStateDescriptor<>("rules", Types.String, Types.POJO(Rule.class))).get("my rule");    
  //通过调用ctx.getBroadcastState()方法，传入一个MapStateDescriptor，就可以得到当前的叫作“rules”的广播状态；调用它的.get()方法，就可以取出其中“my rule”对应的值进行计算处理。
  ```
### 状态的持久化CheckPoit与后端state backend
#### 状态持久化
+ Checkpoint：默认情况下，检查点是被禁用的，需要在代码中手动开启。直接调用执行环境的.enableCheckpointing()方法就可以开启检查点。 
  ```java
  StreamExecutionEnvironment env = StreamExecutionEnvironment.getEnvironment(); 
  env.enableCheckpointing(1000); //设置检查点间隔为1秒
  ```
+ savepoint：保存点在原理和形式上跟检查点完全一样，也是状态持久化保存的一个快照；区别在于，保存点是自定义的镜像保存，所以不会由Flink自动创建，而需要用户手动触发。这在有计划地停止、重启应用时非常有用。 
#### 状态后端
+ state backend：在Flink 中，状态的存储、访问以及维护，都是由其**可插拔的组件决定的**，默认后端HashMapStateBackend
+ 检查点的保存离不开JobManager 和 TaskManager，以及外部存储系统的协调。在应用进行检查点保存时，首先会由 JobManager 向所有 TaskManager 发出触发检查点的命令；TaskManger 收到之后，将当前任务的所有状态进行快照保存，持久化到远程的存储介质中；完成之后向 JobManager 返回确认信息。这个过程是分布式的，当 JobManger 收到所有TaskManager 的返回信息后，就会确认当前检查点成功保存。[检查点保存流程]("F:\Word-Markdown\Markdown-GitHub\图片\flink_state保存流程.png")

##### 状态后端分类：
+ 哈希表状态后端HashMapStateBackend：
  - **状态存放在内存里，哈希表状态后端在内部会直接把状态当作对象（objects）**，保存在Taskmanager的JVM堆（heap）上。
  - 普通的状态，以及窗口中收集的数据和触发器（triggers），都会以键值对（key-value）的形式存储起来，所以底层是一个哈希表（HashMap），这种状态后端也因此得名。 
  - 对于检查点的保存，一般是放在持久化的分布式文件系统（file system）中，也可以通过配置“检查点存储”（CheckpointStorage）来另外指定。HashMapStateBackend 是将本地状态全部放入内存的，这样可以获得最快的读写速度，使计算性能达到最佳；代价则是内存的占用。它适用于具有大状态、长窗口、大键值状态的作业，对所有高可用性设置也是有效的。
+ 内嵌RocksDB状态后端（EmbeddedRocksDBStateBackend） 
 - RocksDB 是一种内嵌的 key-value 存储介质，可以把数据持久化到本地硬盘。配置EmbeddedRocksDBStateBackend 后，会将处理中的数据全部放入RocksDB数据库中，RocksDB默认存储在TaskManager的本地数据目录里。
 -  与 HashMapStateBackend 直接在堆内存中存储对象不同，这种**方式下状态主要是放在RocksDB 中的。数据被存储为序列化的字节数组（Byte Arrays）**，读写操作需要序列化/反序列化，因此状态的访问性能要差一些。
 -  另外，因为做了序列化，key的比较也会按照字节进行，而不是直接调用.hashCode()和.equals()方法。对于检查点，同样会写入到远程的持久化文件系统中。 EmbeddedRocksDBStateBackend 始终执行的是异步快照，也就是不会因为保存检查点而阻塞数据的处理；而且它还提供了增量式保存检查点的机制，这在很多情况下可以大大提升保存效率。由于它会把状态数据落盘，而且支持增量化的检查点，所以在状态非常大、窗口非常长、键/值状态很大的应用场景中是一个好选择，同样对所有高可用性设置有效。

##### 状态后端的选择
+ HashMapStateBackend 是内存计算，读写速度非常快；但是，状态的大小会受到集群可用内存的限制，如果应用的状态随着时间不停地增长，就会耗尽内存资源。
+ RocksDB 是硬盘存储，所以可以根据可用的磁盘空间进行扩展，而且是唯一支持增量检查点的状态后端，所以它非常适合于超级海量状态的存储。不过由于每个状态的读写都需要做序列化/反序列化，而且可能需要直接从磁盘读取数据，这就会导致性能的降低，平均读写性能要比HashMapStateBackend 慢一个数量级。

##### 状态后端的配置
+ 配置默认的状态后端 flink-conf.yaml
  - 在flink-conf.yaml 中，可以使用 state.backend 来配置默认状态后端。 配置项的可能值为hashmap，这样配置的就是HashMapStateBackend；也可以是rocksdb，这样配置的就是 EmbeddedRocksDBStateBackend。另外，也可以是一个实现了状态后端工厂StateBackendFactory 的类的完全限定类名。 下面是一个配置HashMapStateBackend的例子：  
  ```java
  # 默认状态后端 
  state.backend: hashmap 
  # 存放检查点的文件路径 
  state.checkpoints.dir: hdfs://namenode:40010/flink/checkpoints 
  这里的state.checkpoints.dir 配置项，定义了状态后端将检查点和元数据写入的目录。 
  ```
+ 为每个作业（Per-job）单独配置状态后端 每个作业独立的状态后端，可以在代码中，基于作业的执行环境直接设置。代码如下：
  ```java
  StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(); 

  env.setStateBackend(new HashMapStateBackend()); 
  ```
  - 上面代码设置的是HashMapStateBackend，如果想要设置EmbeddedRocksDBStateBackend，可以用下面的配置方式： 
    ```java
    StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(); 

    env.setStateBackend(new EmbeddedRocksDBStateBackend())
    ```
  - 在IDE中使用EmbeddedRocksDBStateBackend，需要为Flink项目添加依赖：
    ```xml
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-statebackend-rocksdb_${scala.binary.version}</artifactId>
        <version>1.13.0</version>
    </dependency>
    ```


## 容错机制

### Checkpoint：一致性检查点
+ checkpoint的保存：
  - 周期性的触发保存，，当每隔一段时间检查点保存操作被触发时，就把每个任务当前的状态复制一份，按照一定的逻辑结构放在一起持久化保存起来，就构成了检查点。 
  - 保存时间点：：**当所有任务都恰好处理完一个相同的输入数据的时候，将它们的状态保存下来。**(首先，这样避免了除状态之外其他额外信息的存储，提高了检查点保存的效率。其次，一个数据要么就是被所有任务完整地处理完，状态得到了保存；要么就是没处理完，状态全部没保存：这就相当于构建了一个“事务”（transaction）。如果出现故障，我们恢复到之前保存的状态，故障时正在处理的所有数据都需要重新处理；所以我们只需要让源（source）任务向数据源重新提交偏移量、请求重放数据就可以了。这需要源任务可以把偏移量作为算子状态保存下来，而且外部数据源能够重置偏移量)
+ checkpoint保存流程：
  - 从最后一个所有算子都处理好的数据截止，把当前的状态保存成一个检查点，写入外部存储中。
  - 至于具体保存到哪里，这是由状态后端的配置项“检查点存储”（CheckpointStorage）来决定的，可以有作业管理器的堆内存（JobManagerCheckpointStorage）和文件系统（FileSystemCheckpointStorage）两种选择。一般情况下，我们会将检查点写入持久化的分布式文件系统。
+ 从检查点恢复状态:
  - 重启应用，重启后任务状态会被清空。
  - 读取检查点，恢复状态。
  - 数据重放，为了不丢数据，我们应该从保存检查点后开始重新读取数据，这可以通过Source任务向外部数据源重新提交偏移量（offset）来实现
+ checkpoint算法：检测所有任务都处理完同一个输入数据的时刻
  - **检查点分界线（Barrier）**：在数据流中插入一个特殊的数据结构，专门用来表示触发检查点保存的时间点。收到保存检查点的指令后，Source 任务可以在当前数据流中插入这个结构；之后的所有任务只要遇到它就开始对状态做持久化快照保存。由于数据流是保持顺序依次处理的，因此遇到这个标识就代表之前的数据都处理完了，可以保存一个检查点；而在它之后的数据，引起的状态改变就不会体现在这个检查点中，而需要保存到下一个检查点。 这种特殊的数据形式，把一条流上的数据按照不同的检查点分隔开，所以就叫作检查点的“分界线”（Checkpoint Barrier）。
    - 在JobManager 中有一个“检查点协调器”（checkpoint coordinator），专门用来协调处理检查点的相关工作。检查点协调器会定期向TaskManager发出指令，要求保存检查点（带着检查点ID）； TaskManager 会让所有的Source任务把自己的偏移量（算子状态）保存起来，并将带有检查点ID的分界线（barrier）插入到当前的数据流中，然后像正常的数据一样像下游传递；之后Source任务就可以继续读入新的数据了。每个算子任务只要处理到这个barrier，就把当前的状态进行快照；在收到 barrier 之前，还是正常地处理之前的数据，完全不受影响。
    - 具体实现上，Flink 使用了 Chandy-Lamport 算法的一种变体，被称为“异步分界线快照”（asynchronous barrier snapshotting）算法。算法的核心就是两个原则：当上游任务向多个并行下游任务发送barrier时，需要广播出去；而当多个上游任务向同一个下游任务传递barrier时，需要在下游任务执行“分界线对齐”（barrier alignment）操作，也就是需要等到所有并行分区的barrier 都到齐，才可以开始状态的保存。
+ 检查点配置：
  -  Checkpoint：默认情况下，检查点是被禁用的，需要在代码中手动开启。直接调用执行环境的.enableCheckpointing()方法就可以开启检查点。 
    ```java
    StreamExecutionEnvironment env = StreamExecutionEnvironment.getEnvironment(); 
    env.enableCheckpointing(1000); //设置检查点间隔为1秒
    ```
+ 检查点储存：默认情况下，检查点存储在JobManager的堆（heap）内存中。而对于大状态的持久化保存，Flink也提供了在其他存储位置进行保存的接口，这就是CheckpointStorage。
  - 具体可以通过调用检查点配置的.setCheckpointStorage()来配置，需要传入一个CheckpointStorage 的实现类。Flink 主要提供了两种 CheckpointStorage：作业管理器的堆内存（JobManagerCheckpointStorage）和文件系统（FileSystemCheckpointStorage）。
    ```java
    // 配置存储检查点到JobManager堆内存 
    env.getCheckpointConfig().setCheckpointStorage(new 
    JobManagerCheckpointStorage()); 
    // 配置存储检查点到文件系统 ,常用高可以的HDFS
    env.getCheckpointConfig().setCheckpointStorage(new 
    FileSystemCheckpointStorage("hdfs://namenode:40010/flink/checkpoints")); 
    ```
#### checkpoint的高级配置
+ 检查点模式（CheckpointingMode）
  设置检查点一致性的保证级别，有“精确一次”（exactly - once）和“至少一次”（at - least - once）两个选项。默认级别为exactly - once，而对于大多数低延迟的流处理程序，at - least - once就够用了，而且处理效率会更高。关于一致性级别，我们会在10.2节继续展开。
+ 超时时间（checkpointTimeout）
  用于指定检查点保存的超时时间，超时没完成就会被丢弃掉。传入一个长整型毫秒数作为参数，表示超时时间。
+ 最小间隔时间（minPauseBetweenCheckpoints）
  用于指定在上一个检查点完成之后，检查点协调器（checkpoint coordinator）最快等多久可以触发保存下一个检查点的指令。这就意味着即使已经达到了周期触发的时间点，只要距离上一个检查点完成的间隔不够，就依然不能开启下一次检查点的保存。这就为正常处理数据留下了充足的间隙。当指定这个参数时，maxConcurrentCheckpoints的值强制为1。
+ 最大并发检查点数量（maxConcurrentCheckpoints）
  用于指定运行中的检查点最多可以有多少个。由于每个任务的处理进度不同，完全可能出现后面的任务还没完成前一个检查点的保存、前面任务已经开始保存下一个检查点了。这个参数就是限制同时进行的最大数量。
  如果前面设置了minPauseBetweenCheckpoints，则maxConcurrentCheckpoints这个参数就不起作用了。
+ 开启外部持久化存储（enableExternalizedCheckpoints）
  用于开启检查点的外部持久化，而且默认在作业失败的时候不会自动清理，如果想释放空间需要自己手工清理。里面传入的参数ExternalizedCheckpointCleanup指定了当作业取消的时候外部的检查点该如何清理。
      - DELETE_ON_CANCELLATION：在作业取消的时候会自动删除外部检查点，但是如果是作业失败退出，则会保留检查点。
      - RETAIN_ON_CANCELLATION：作业取消的时候也会保留外部检查点。
+ 检查点异常时是否让整个任务失败（failOnCheckpointingErrors）
  用于指定在检查点发生异常的时候，是否应该让任务直接失败退出。默认为true，如果设置为false，则任务会丢弃掉检查点然后继续运行。

+ 不对齐检查点（enableUnalignedCheckpoints）
  不再执行检查点的分界线对齐操作，启用之后可以大大减少产生背压时的检查点保存时间。这个设置要求检查点模式（CheckpointingMode）必须为exactly - once，并且并发的检查点个数为1。代码中具体设置如下： 
  ```java
  StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
  // 启用检查点，间隔时间1秒
  env.enableCheckpointing(1000);
  CheckpointConfig checkpointConfig = env.getCheckpointConfig();
  // 设置精确一次模式
  checkpointConfig.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
  // 最小间隔时间500毫秒
  checkpointConfig.setMinPauseBetweenCheckpoints(500);
  // 超时时间1分钟
  checkpointConfig.setCheckpointTimeout(60000);
  // 同时只能有一个检查点
  checkpointConfig.setMaxConcurrentCheckpoints(1);
  // 开启检查点的外部持久化保存，作业取消后依然保留
  checkpointConfig.enableExternalizedCheckpoints(ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);
  // 启用不对齐的检查点保存方式
  checkpointConfig.enableUnalignedCheckpoints();
  // 设置检查点存储，可以直接传入一个String，指定文件系统的路径
  checkpointConfig.setCheckpointStorage("hdfs://my/checkpoint/dir");   
  ```
#### savapoint：保存点
+ 一个存盘的备份，它的原理和算法与检查点完全相同，只是多了一些额外的元数据。事实上，保存点就是通过检查点的机制来创建流式作业状态的一致性镜像（consistent image）的。 保存点中的状态快照，是以算子ID和状态名称组织起来的，相当于一个键值对。从保存点启动应用程序时，Flink会将保存点的状态数据重新分配给相应的算子任务。 
+ 用途
  - 版本管理和归档存储 
  - 更新Flink版本 
  - 更新应用程序 ：注意程序必须是兼容的，也就是说更改之后的程序，状态的拓扑结构和数据类型都是不变的，这样才能正常从之前的保存点去加载。 
  - 调整并行度 
  - 暂停应用程序
+ 使用限制：状态的拓扑结构和数据类型不变
  - 保存点中状态都是以算子ID-状态名称这样的 key-value 组织起来的，算子ID 可以在代码中直接调用SingleOutputStreamOperator 的.uid()方法来进行指定
  ```java
  DataStream<String> stream = env 
    .addSource(new StatefulSource()) 
    .uid("source-id") 
    .map(new StatefulMapper()) 
    .uid("mapper-id") 
    .print(); 
  ```
  - 对于没有设置ID的算子，Flink默认会自动进行设置，所以在重新启动应用后可能会导致ID 不同而无法兼容以前的状态。所以为了方便后续的维护，强烈建议在程序中为每一个算子手动指定ID。 
+ 保存点使用
  - 保存点创建：命令行：./bin/flink savepoint :
    - jobId [:targetDir]，其中:jobId 是作业的ID，
    - :targetDir 是保存点的目标路径，可以不指定
    - 默认路径可通过flink-conf.yaml 中的state.savepoints.dir : dir配置项来指定。
    - 单独的作业也可通过执行环境配置：env.setDefaultSavepointDir("hdfs:///flink/savepoints"); 
    - 创建并关闭job：bin/flink stop --savepointPath [:targetDirectory] :jobId 
  - 保存点启动：命令行：./bin/flink run -s :savepointPath [:stateBackend] ，相当与正常启动作业，只不过指定了保存点的路径。


### 状态一致性
#### 端到端的一致end to end
+ 完整是应用，应该包括了数据源、流处理器(flink 保证一致性)和外部存储系统(事务保证一致性)三个部分，end-to-end实现关键在于实现数据源的一致性。

+ 预写日志：通用且实现简单，但对性能有要求
  - 先把结果数据作为日志（log）状态保存起来 
  - 进行检查点保存时，也会将这些结果数据一并做持久化存储 
  - 在收到检查点完成的通知时，将所有结果一次性写入外部系统。

+ 两阶段提交2PC
  - 当第一条数据到来时，或者收到检查点的分界线时，Sink任务都会启动一个事务。 
  - 接下来接收到的所有数据，都通过这个事务写入外部系统；这时由于事务没有提交，所以数据尽管写入了外部系统，但是不可用，是“预提交”的状态。 
  - 当Sink任务收到JobManager发来检查点完成的通知时，正式提交事务，写入的结果就真正可用了。
  - 需求：
    - 外部系统必须提供事务支持，或者Sink任务必须能够模拟外部系统上的事务。 
    - 在检查点的间隔期间里，必须能够开启一个事务并接受数据写入。 
    - 在收到检查点完成的通知之前，事务必须是“等待提交”的状态。在故障恢复的情况下，这可能需要一些时间。如果这个时候外部系统关闭事务（例如超时了），那么未提交的数据就会丢失。 
    - Sink任务必须能够在进程失败后恢复事务。 
    - 提交事务必须是幂等操作。也就是说，事务的重复提交应该是无效的。 

+ end-to-end exactly-once
  - 输入端保证：数据源可重放数据，或者说可重置读取数据偏移量，加上Flink的Source算子将偏移量作为状态保存进检查点，就可以保证数据不丢。这是达到at-least-once一致性语义的基本要求，当然也是实现端到端exactly-once的基本要求。 
  - 输出端保证：可选事务写入、幂等写入
  - 事务写入：预写日志、两阶段提交协议
  - 幂等写入：最终结果一致，但可能产生中间重复结果。

#### **Kafka与flink连接的exactly-once**
+ Flink 内部 
  Flink 内部可以通过检查点机制保证状态和处理结果的exactly-once语义。 
+ 输入端 
  输入数据源端的Kafka可以对数据进行持久化保存，并可以重置偏移量（offset）。所以我们可以在Source任务（FlinkKafkaConsumer）中将当前读取的偏移量保存为算子状态，写入到检查点中；当发生故障时，从检查点中读取恢复状态，并由连接器FlinkKafkaConsumer向Kafka重新提交偏移量，就可以重新消费数据、保证结果的一致性了。 
+ 输出端 
  输出端保证exactly-once 的最佳实现，当然就是两阶段提交（2PC）。作为与Flink天生一对的Kafka，自然需要用最强有力的一致性保证来证明自己。Flink 官方实现的Kafka连接器中，提供了写入到Kafka的FlinkKafkaProducer，它就实现了TwoPhaseCommitSinkFunction 接口：
  ```java
  public class FlinkKafkaProducer<IN> extends TwoPhaseCommitSinkFunction<IN, 
  FlinkKafkaProducer.KafkaTransactionState, 
  FlinkKafkaProducer.KafkaTransactionContext> { 
  ... 
  } 
  ```

+ 我们写入Kafka的过程实际上是一个两段式的提交：处理完毕得到结果，写入Kafka 时是基于事务的“预提交”；等到检查点保存完毕，才会提交事务进行“正式提交”。如果中间出现故障，事务进行回滚，预提交就会被放弃；恢复状态之后，也只能恢复所有已经确认提交的操作。
+ 具体步骤：
  - 启动检查点保存，进入了预提交阶段
  - 算子任务对状态做快照 
  - Sink 任务开启事务，进行预提交 
  - 检查点保存完成，提交事务
+ 需要的配置 
  - 必须启用检查点； 
  - 在FlinkKafkaProducer 的构造函数中传入参数Semantic.EXACTLY_ONCE； 
  - 配置Kafka读取数据的消费者的隔离级别为read_committed，这样就可以保证读取到已提交的消息。
    解释：预提交阶段数据已经写入，只是被标记为“未提交”（uncommitted），而 Kafka 中默认的隔离级别 isolation.level 是 read_uncommitted，也就是可以读取未提交的数据。这样一来，外部应用就可以直接消费未提交的数据，对于事务性的保证就失效了。所以应该将隔离级别配置 为read_committed，表示消费者遇到未提交的消息时，会停止从分区中消费数据，直到消息被标记为已提交才会再次恢复消费。当然，这样做的话，外部应用消费数据就会有显著的延迟。 
  - 事务超时配置 :kafka的事务超时时间应该大于flink集群配置的事务超时时间
    解释：Flink的Kafka连接器中配置的事务超时时间transaction.timeout.ms默认是1小时，而Kafka集群配置的事务最大超时时间transaction.max.timeout.ms 默认是 15 分钟。所以在检查点保存时间很长时，有可能出现Kafka已经认为事务超时了，丢弃了预提交的数据；而Sink任务认为还可以继续等待。如果接下来检查点保存成功，发生故障后回滚到这个检查点的状态，这部分数据就被真正丢掉了。所以这两个超时时间，前者应该小于等于后者。

## Table API && SQL
+ IDEA依赖
```xml
<!--桥接器，用于Java API和Table API之间的交互。当然也有scala版本的-->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-table-api-java-bridge_${scala.binary.version}</artifactId>
    <version>${flink.version}</version>
</dependency>

<!--Table API和SQL的运行时环境，包含了Table API和SQL的所有运行时依赖-->
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-table-planner-blink_${scala.binary.version}</artifactId>
    <version>${flink.version}</version>
</dependency>
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-streaming-scala_${scala.binary.version}</artifactId>
    <version>${flink.version}</version>
</dependency>

<!--可选配置用于自定义数据格式来做序列化-->        
<dependency> 
  <groupId>org.apache.flink</groupId> 
  <artifactId>flink-table-common</artifactId> 
  <version>${flink.version}</version> 
</dependency> 
```
+ 应用框架
```java
// 创建表环境
TableEnvironment tableEnv = ...;
// 创建输入表，连接外部系统读取数据
tableEnv.executeSql("CREATE TEMPORARY TABLE inputTable ... WITH ( 'connector' = ... )");
// 注册一个表，连接到外部系统，用于输出
tableEnv.executeSql("CREATE TEMPORARY TABLE outputTable ... WITH ( 'connector' = ... )");
// 执行SQL对表进行查询转换，得到一个新的表
Table table1 = tableEnv.sqlQuery("SELECT ... FROM inputTable... ");
// 使用Table API对表进行查询转换，得到一个新的表
Table table2 = tableEnv.from("inputTable").select(...);
// 将得到的结果写入输出表
TableResult tableResult = table1.executeInsert("outputTable");    
```
+ 表环境作用
  - 执行SQL查询
  - 注册表、Catalog目录
  - 注册UDF
  - DataStream转换成Table
+ 输出表：，输出一张表最直接的方法，就是调用 Table 的方法 executeInsert()方法将一个 Table 写入到注册过的表中，方法传入的参数就是注册的表名。 
  ```java
  // 注册表，用于输出数据到外部系统 
  tableEnv.executeSql("CREATE TABLE OutputTable ... WITH ( 'connector' = ... )"); 
  // 经过查询转换，得到结果表 
  Table result = ... 
  // 将结果表写入已注册的输出表中 
  result.executeInsert("OutputTable"); 
  ```

### DataType
#### 原子类型：Interger、String、Double
#### 复合类型：Tuple、Row、POJO
+ Tuple类型：
  - Table 支持Flink 中定义的元组类型Tuple，对应在表中字段名默认就是元组中元素的属性名f0、f1、f2...。可调用as方法重命名。
  ```java
  // 将数据流转换成包含f0和f1字段的表，在表中f0和f1位置交换 
  Table table = tableEnv.fromDataStream(stream, $("f1"), $("f0")); 
  ```
+ POJO类型：
  - 将POJO类型的DataStream转换成Table，如果不指定字段名称，就会直接使用原始POJO类型中的字段名称。POJO中的字段同样可以被重新排序、提却和重命名
+ Row类型：行
  - Table中数据的基本组织形式。Row 类型也是一种复合类型，它的长度固定，而且无法直接推断出每个字段的类型，所以在使用时必须指明具体的类型信息
  - ，Row类型还附加了一个属性RowKind，用来表示当前行在更新操作中的类型。这样，Row 就可以用来表示更新日志流（changelog stream）中的数据，从而架起了Flink中流和表的转换桥梁。所以在更新日志流中，元素的类型必须是Row，而且需要调用ofKind()方法来指定更新类型。下面是一个具体的例子： 
  ```java
  DataStream<Row> dataStream = 
    env.fromElements( 
      Row.ofKind(RowKind.INSERT, "Alice", 12), 
      Row.ofKind(RowKind.INSERT, "Bob", 5), 
      Row.ofKind(RowKind.UPDATE_BEFORE, "Alice", 12), 
      Row.ofKind(RowKind.UPDATE_AFTER, "Alice", 100)); 
  // 将更新日志流转换为表 
  Table table = tableEnv.fromChangelogStream(dataStream); 
  ```

### 表和流的转换
#### Table to DataStream
+ 直接调用toDataStream()方法即可
  ```java
  Table aliceVisitTable = tableEnv.sqlQuery( 
    "SELECT user, url " + 
    "FROM EventTable " + 
    "WHERE user = 'Alice' " 
  ); 

  // 将表转换成数据流,aliceVisitTable为待转换的表对象
  tableEnv.toDataStream(aliceVisitTable).print(); 
  ```
+ 调用toAppendStream()方法，得到一个AppendStream，表示追加模式的数据流。
  - AppendStream：表示数据流中的数据是按照插入的顺序追加的，并且数据不会更新或删除。这种数据流可以保证exactly-once的语义，因为数据只被插入一次，不会被修改或删除。
#### DataStream to Table
+ 调用fromDataStream()方法
  - 因为流中的数据本身就是定义好的POJO类型Event，所以我们将流转换成表之后，每一行数据就对应着一个Event，而表中的列名就对应着Event中的属性。 
  ```java
  StreamExecutionEnvironment env = 
  StreamExecutionEnvironment.getExecutionEnvironment(); 
  // 获取表环境 
  StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env); 
  // 读取数据源 
  SingleOutputStreamOperator<Event> eventStream = env.addSource(...) 
  // 将数据流转换成表 
  Table eventTable = tableEnv.fromDataStream(eventStream);
  ```
  - 在fromDataStream()方法中增加参数，用来指定提取哪些属性作为表中的字段名，并可以任意指定位置.需要注意的是，timestamp本身是SQL中的关键字，所以我们在定义表名、列名时要尽量避免。这时可以通过表达式的as()方法对字段进行重命名：
  ```java 
  Table eventTable2 = tableEnv.fromDataStream(eventStream, $("timestamp"), $("url")); 
  ```
+ 调用createTemporaryView()方法 
  - 调用fromDataStream()方法简单直观，可以直接实现DataStream到Table的转换；不过如果我们希望直接在SQL中引用这张表，就还需要调用表环境的createTemporaryView()方法来创建虚拟视图了。 
  - 对于这种场景，也有一种更简洁的调用方式。我们可以直接调用 createTemporaryView()方法创建虚拟表，传入的两个参数，第一个依然是注册的表名，而第二个可以直接就是DataStream。之后仍旧可以传入多个参数，用来指定表中的字段 
    ```java
    tableEnv.createTemporaryView("EventTable", eventStream, 
    $("timestamp").as("ts"),$("url")); 
    //这样，我们接下来就可以直接在SQL中引用表EventTable了。 
    ```
+ 调用fromChangelogStream ()方法 
  - 表环境还提供了一个方法 fromChangelogStream()，可以将一个更新日志流转换成表。这个方法要求流中的数据类型只能是 Row，而且每一个数据都需要指定当前行的更新类型（RowKind）；所以一般是由连接器帮我们实现的，直接应用比较少见，感兴趣的读者可以查看官网的文档说明

### create table
+ 连接器表 ConnectTable
  - 过连接器（connector）连接到一个外部系统，然后定义出对应的表结构
  ```java
  tableEnv.executeSql("CREATE [TEMPORARY] TABLE MyTable ... WITH ( 'connector' = ... )"); 
  ```
  - 可自定义目录名、库名：tEnv.useCatalog("custom_catalog"); | tEnv.useDatabase("custom_database"); 
+ 虚拟表 VirtualTable
  - 需要在表环境中注册后才可使用，类似SQL中的视图。
  ```java
  //执行SQL语句，保存在表对象中
  Table newTable = tableEnv.sqlQuery("SELECT ... FROM MyTable... "); 
  //将表对象注册到表环境中，供其他查询使用
  tableEnv.createTemporaryView("NewTable", newTable); 
  ```
 
### 表的查询SQL
+ 目前Flink 支持标准 SQL 中的绝大部分用法，并提供了丰富的计算函数。这样我们就可以把已有的技术迁移过来，像在MySQL、Hive中那样直接通过编写SQL实现自己的处理需求，从而大大降低了Flink上手的难度。 
  - eg:
  ```java
  // 创建表环境 
  TableEnvironment tableEnv = ...;  
  // 创建表 
  tableEnv.executeSql("CREATE TABLE EventTable ... WITH ( 'connector' = ... )"); 
  // 查询用户Alice的点击事件，并提取表中前两个字段 
  Table aliceVisitTable = tableEnv.sqlQuery( 
    "SELECT user, url " + 
    "FROM EventTable " + 
    "WHERE user = 'Alice' " 
  ); 
  ```
  - 例如，我们也可以通过GROUP BY关键字定义分组聚合，调用COUNT()、SUM()这样的函数来进行统计计算： 
  ```java
  Table urlCountTable = tableEnv.sqlQuery( 
    "SELECT user, COUNT(url) " + 
    "FROM EventTable " + 
    "GROUP BY user " 
  ); 
  ```
+ 调用Table API进行查询转换
  - 嵌入在Java和Scala语言内的查询API，核心就是Table接口类，通过一步步链式调用Table的方法，就可以定义出所有的查询转换操作。每一步方法调用的返回结果，都是一个Table。 
  ```java
  Table maryClickTable = eventTable 
    .where($("user").isEqual("Alice"))
    .select($("url"), $("user")); 
  ```
### 流处理中的（动态）表
+ 个Table转换成DataStream 时，有“仅插入流”（Insert-Only Streams）和“更新日志流”（Changelog Streams）两种不同的方式，具体使用哪种方式取决于表中是否存在更新（update）操作。
+ 动态表：表中数据不断变化，查询结果随之变化
  - 动态表在关系型数据库中，我们一般把它称为更新日志流（changelog stream）。如果我们保存了表在某一时刻的快照（snapshot），那么接下来只要读取更新日志流，就可以得到表之后的变化过程和最终结果了。
+ 持续查询步骤：
  - 流（stream）被转换为动态表（dynamic table）； 
  - 对动态表进行持续查询（continuous query），生成新的动态表； 
  - 生成的动态表被转换成流。

+ DataStream转换为动态表
  - 如果把流看作一张表，那么流中每个数据的到来，都应该看作是对表的一次插入（Insert）操作，会在表的末尾添加一行数据。因为流是连续不断的，而且之前的输出结果无法改变、只能在后面追加；所以我们其实是通过一个只有插入操作（insert-only）的更新日志（changelog）流，来构建一个表。

+ 用SQL持续查询
  - ，当原始动态表不停地插入新的数据时，查询得到的urlCountTable会持续地进行更改。由于count数量可能会叠加增长，因此这里的更改操作可以是简单的插入（Insert），也可以是对之前数据的更新（Update）。换句话说，用来定义结果表的更新日志（changelog）流中，包含了INSERT和UPDATE两种操作。这种持续查询被称为更新查询（Update Query）
+ 追加查询：执行一个简单的条件查询，结果表中就会像原始表EventTable一样，只有插入（Insert）操作
  ```java
  Table aliceVisitTable = tableEnv.sqlQuery("SELECT url, user FROM EventTable WHERE user = 'Cary'"); 
  ```
  - 它定义的结果表的更新日志（changelog）流中只有 INSERT 操作。追加查询得到的结果表，转换成DataStream 调用方法没有限制，可以直接用toDataStream()，也可以像更新查询一样调用toChangelogStream()。
  - 当有update操作时必须调用：toChangelogStream()
+ 查询代价
  - 持续查询：数据随时间而增长，导致内存空间不足。
  - 更新查询：数据变大后，更新排名的计算代价也会增加。

+ 动态表转化为DataStream
  - 仅追加（Append-only）流 ：仅通过插入（Insert）更改来修改的动态表，可以直接转换为“仅追加”流。这个流中发出的数据，其实就是动态表中新增的每一行。 
  - 撤回（Retract）流 ：撤回流是包含两类消息的流，添加（add）消息和撤回（retract）消息。 
  - 更新插入（Upsert）流：更新插入流中只包含两种类型的消息：更新插入（upsert）消息和删除（delete）消息
  - 在代码里将动态表转换为DataStream 时，只支持仅追加（append-only）和撤回（retract）流，我们调用 toChangelogStream()得到的其实就是撤回流；这也很好理解，DataStream 中并没有key的定义，所以只能通过两条消息一减一增来表示更新操作。而连接到外部系统时，则可以支持不同的编码方法，这取决于外部系统本身的特性。

### 数据属性和窗口
+ 把时间属性的定义分成事件时间（event time）和处理时间（processing time）两种情况。
#### 事件时间watermark
+ 在创建表的DDL中定义：可通过WATERMARK语句来定义事件时间属性。WATERMARK语句主要用来定义水位线（watermark）的生成表达式，这个表达式会将带有事件时间戳的字段标记为事件时间属性，并在它基础上给出水位线的延迟时间。具体定义方式如下： 
  ```java
  CREATE TABLE EventTable( 
    user STRING, 
    url STRING, 
    ts TIMESTAMP(3), 
  WATERMARK FOR ts AS ts - INTERVAL '5' SECOND 
  //ts字段定义为事件时间属性，而且基于ts设置了5秒的水位线延迟
  //“5秒”是以“时间间隔”的形式定义的，格式是INTERVAL <数值> <时间单位>： INTERVAL '5' SECOND 这里的数值必须用单引号引起来，而单位用SECOND和SECONDS是等效的。
  ) WITH ( 
    ... 
  ); 
  ```
+ Flink 中支持的事件时间属性数据类型必须为TIMESTAMP或者TIMESTAMP_LTZ。这里TIMESTAMP_LTZ 是指带有本地时区信息的时间戳（TIMESTAMP WITH LOCAL TIME ZONE）；一般情况下如果数据中的时间戳是“年-月-日-时-分-秒”的形式，那就是不带时区信息的，可以将事件时间属性定义为TIMESTAMP类型。 而如果原始的时间戳就是一个长整型的毫秒数，这时就需要另外定义一个字段来表示事件时间属性，类型定义为TIMESTAMP_LTZ会更方便： 
  ```java
  CREATE TABLE events ( 
    user STRING, 
    url STRING, 
    ts BIGINT, 
    ts_ltz AS TO_TIMESTAMP_LTZ(ts, 3), 
  //定义了一个字段ts_ltz，是把长整型的ts转换为TIMESTAMP_LTZ得到的；进而使用WATERMARK语句将它设为事件时间属性，并设置5秒的水位线延迟。
  WATERMARK FOR ts_ltz AS time_ltz - INTERVAL '5' SECOND 
  ) WITH ( 
    ... 
  ); 
  ```  
+ 事件时间属性也可以在将DataStream 转换为表的时候来定义。我们调用fromDataStream()方法创建表时，可以追加参数来定义表中的字段结构；这时可以给某个字段加上.rowtime() 后缀，就表示将当前字段指定为事件时间属性。这个字段可以是数据中本不存在、额外追加上去的“逻辑字段”，就像之前 DDL 中定义的第二种情况；也可以是本身固有的字段，那么这个字段就会被事件时间属性所覆盖，类型也会被转换为TIMESTAMP。
  - 不论那种方式，时间属性字段中保存的都是事件的时间戳（TIMESTAMP类型）。 需要注意的是，这种方式只负责指定时间属性，而时间戳的提取和水位线的生成应该之前就在DataStream 上定义好了。
  - 由于DataStream 中没有时区概念，因此Flink 会将事件时间属性解析成不带时区的TIMESTAMP类型，所有的时间值都被当作UTC标准时间。 
  - 在代码中的定义方式如下： 
  ```java
  // 方法一: 
  // 流中数据类型为二元组Tuple2，包含两个字段；需要自定义提取时间戳并生成水位线 
  DataStream<Tuple2<String, String>> stream = 
  inputStream.assignTimestampsAndWatermarks(...); 
  // 声明一个额外的逻辑字段作为事件时间属性 
  Table table = tEnv.fromDataStream(stream, $("user"), $("url"), 
  $("ts").rowtime()); 
  // 方法二: 
  // 流中数据类型为三元组Tuple3，最后一个字段就是事件时间戳 
  DataStream<Tuple3<String, String, Long>> stream = 
  inputStream.assignTimestampsAndWatermarks(...); 
  // 不再声明额外字段，直接用最后一个字段作为事件时间属性 
  Table table = tEnv.fromDataStream(stream, $("user"), $("url"), 
  $("ts").rowtime());
  ```
#### 处理时间(即系统时间)
+ 在创建表的DDL中定义 ：在创建表的DDL（CREATE TABLE语句）中，可以增加一个额外的字段，通过调用系统内置的PROCTIME()函数来指定当前的处理时间属性，返回的类型是TIMESTAMP_LTZ。 
  ```java
  CREATE TABLE EventTable( 
    user STRING, 
    url STRING, 
    ts AS PROCTIME() 
  ) WITH ( 
    ... 
  ); 
  ```
- 这里的时间属性，其实是以“计算列”（computed column）的形式定义出来的。所谓的计算列是Flink SQL 中引入的特殊概念，可以用一个AS语句来在表中产生数据中不存在的列，并且可以利用原有的列、各种运算符及内置函数。在前面事件时间属性的定义中，将 ts 字段转换成TIMESTAMP_LTZ类型的ts_ltz，也是计算列的定义方式。 
+ 在数据流转换为表时定义 :
  - 处理时间属性同样可以在将 DataStream 转换为表的时候来定义。我们调用fromDataStream()方法创建表时，可以用.proctime()后缀来指定处理时间属性字段。
  - 由于处理时间是系统时间，原始数据中并没有这个字段，所以处理时间属性一定不能定义在一个已有字段上，只能定义在表结构所有字段的最后，作为额外的逻辑字段出现。 代码中定义处理时间属性的方法如下： 
  ```java
  DataStream<Tuple2<String, String>> stream = ...; 
  // 声明一个额外的字段作为处理时间属性字段 
  332 
  Table table = tEnv.fromDataStream(stream, $("user"), $("url"), 
  $("ts").proctime());
  ```
### 窗口TVF
+ 在窗口TVF的返回值中，除去原始表中的所有列，还增加了用来描述窗口的额外3个列：“窗口起始点”（window_start）、“窗口结束点”（window_end）、“窗口时间”（window_time）。起始点和结束点比较好理解，这里的“窗口时间”指的是窗口中的时间属性，它的值等于window_end - 1ms，所以相当于是窗口中能够包含数据的最大时间戳。

+  滚动窗口（Tumbling Windows）； 
  - 滚动窗口在SQL中的概念与DataStream API中的定义完全一样，是长度固定、时间对齐、无重叠的窗口，一般用于周期性的统计计算。
  ````java
  TUMBLE(TABLE EventTable, DESCRIPTOR(ts), INTERVAL '1' HOUR) 
  //ts是时间字段，INTERVAL '1' HOUR 表示每个滚动窗口的长度为1小时。
  ````

+  滑动窗口（Hop Windows，跳跃窗口）； 
  ```java
  HOP(TABLE EventTable, DESCRIPTOR(ts), INTERVAL '5' MINUTES, INTERVAL '1' HOURS)); 
  //ts为时间字段，INTERVAL '5' MINUTES 表示滑动窗口的滑动步长为5分钟，INTERVAL '1' HOUR 表示每个滑动窗口的长度为1小时
  ```

+  累积窗口（Cumulate Windows）；
- 固定时间输出当前累计统计值
```java
CUMULATE(TABLE EventTable, DESCRIPTOR(ts), INTERVAL '1' HOURS, INTERVAL '1' DAYS))
// ts为时间字段，INTERVAL '1' HOURS 表示累积窗口的长度从1小时开始，并且每次增加1小时，INTERVAL '1' DAYS 表示累积窗口的长度最大为1天。
//即统计一天的累计值，但每小时需要输出当前累计值
```
+  会话窗口（Session Windows，目前尚未完全支持）
  


### 聚合查询：Aggerations
+ 分组聚合
  - 在流处理中，分组聚合同样是一个持续查询，而且是一个更新查询，得到的是一个动态表；每当流中有一个新的数据到来时，都会导致结果表的更新操作。因此，想要将结果表转换成流或输出到外部系统，必须采用撤回流（retract stream）或更新插入流（upsert stream）的编码方式；如果在代码中直接转换成DataStream 打印输出，需要调用toChangelogStream()。
  - 在持续查询的过程中，由于用于分组的key可能会不断增加，因此计算结果所需要维护的状态也会持续增长。为了防止状态无限增长耗尽资源，Flink Table API和SQL以在表环境中**配置状态的生存时间（TTL），可能导致统计结果不准确。**

+ 窗口聚合
  -  “窗口表值函数”（Windowing TVF），窗口本身返回的是就是一个表，所以窗口会出现在FROM后面，GROUP BY后面的则是窗口新增的字段window_start和window_end。
  - Flink SQL 目前提供了滚动窗口TUMBLE()、滑动窗口HOP()和累积窗口（CUMULATE）三种表值函数（TVF）。 
  ```java 
  Table result = tableEnv.sqlQuery(
      "SELECT " +
      "user, " +
      "window_end AS endT, " +
      "COUNT(url) AS cnt " +
      "FROM TABLE( " +
      //TUMBLE为窗口表值函数，得到是一个表，所有的聚合在表中完成
      "TUMBLE( TABLE EventTable, " +
      //ts为时间字段，INTERVAL '1' HOUR 表示每个滚动窗口的长度为1小时。
      "DESCRIPTOR(ts), " +
      "INTERVAL '1' HOUR)) " +
      //
      "GROUP BY user, window_start, window_end "
  );
      
  ```
  - 除了应用简单的聚合函数、提取窗口开始时间（window_start）和结束时间(window_end)之外，窗口TVF还提供了一个window_time字段，用于表示窗口中的时间属性；这样就可以方便地进行窗口的级联（cascading window）和计算了。另外，窗口TVF还支持GROUPING SETS
  
+ 开窗聚合：对每一行进行一次聚合，聚合后行数不变
  - over可选参数: PARTITION BY <字段 1>[, <字段 2>, ...]:指定分区字段， ORDER BY <时间属性字段> ：指定排序字段，flink中仅支持时间属性的升序。
  - 开窗范围：BETWEEN ... PRECEDING AND CURRENT ROW ，从某一行到另一行，可基于范围间隔也可基于行间隔。
    - 范围间隔 ：范围间隔以RANGE为前缀，就是基于ORDER BY指定的时间字段去选取一个范围，般就是当前行时间戳之前的一段时间。例如开窗范围选择当前行之前1小时的数据：RANGE BETWEEN INTERVAL '1' HOUR PRECEDING AND CURRENT ROW
    - 行间隔 行间隔以ROWS为前缀，就是直接确定要选多少行，由当前行出发向前选取就可以了。例如开窗范围选择当前行之前的5行数据（最终聚合会包括当前行，所以一共6条数据）：ROWS BETWEEN 5 PRECEDING AND CURRENT ROW 
  ```java
  SELECT 
      <聚合函数> OVER ( 
      [PARTITION BY <字段 1>[, <字段2>, ...]] 
      ORDER BY <时间属性字段> 
      <开窗范围>), 
    ... 
  FROM ... 
  ```

### 连接查询：Join

+ 等值内联结（INNER Equi-JOIN），仅支持 = 操作
  ```java
  //返回笛卡尔积中符合的部分
  SELECT * 
  FROM Order 
  INNER JOIN Product 
  ON Order.product_id = Product.id 
  ```
+ 等值外联结（OUTER Equi-JOIN），与SQL一致
  ```java
  SELECT * 
  FROM Order 
  FULL OUTER JOIN Product 
  ON Order.product_id = Product.id
  ```
+ 间隔连接
  - 比普通连接多了一个时间间隔的限制
  - 两表的联结 ：将要联结的两表列出来就可以，用逗号分隔，返回两表中所有行的笛卡尔积。 
  - 联结条件 ：联结条件用 WHERE 子句来定义，用一个等值表达式描述。交叉联结之后再用 WHERE进行条件筛选，效果跟内联结INNER JOIN ... ON ...非常类似。 
  - 时间间隔限制：在WHERE子句中，联结条件后用AND追加一个时间间隔的限制条件；做法是提取左右两侧表中的时间字段，然后用一个表达式来指明两者需要满足的间隔限制。具体定义方式有下面三种，
    - ltime = rtime //分别用ltime和rtime表示左右表中的时间字段
    - ltime >= rtime AND ltime < rtime + INTERVAL '10' MINUTE  
    - ltime BETWEEN rtime - INTERVAL '10' SECOND AND rtime + INTERVAL '5' SECOND 
+ “时间联结”（Temporal Join）：
  - 那对于有更新操作的表，又怎么办呢？除了间隔联结之外，Flink SQL 还支持时间联结（Temporal Join），这主要是针对“版本表”（versioned table）而言的。所谓版本表，就是记录了数据随着时间推移版本变化的表，可以理解成一个“更新日志”（change log），它就是具有时间属性、还会进行更新操作的表。

### 函数
+ 系统函数直接使用，UDF表环境注册后使用。

#### 系统函数
+ 标量函数：= 、<>、IS NOT NULL、AND、OR、NOT、IS、IS NOT、RAND()
+ 字符处理函数：
  - string1 || string2  两个字符串的连接 
  - UPPER(string)  将字符串string 转为全部大写 
  - CHAR_LENGTH(string)  计算字符串string的长度 
+ 时间函数
  - DATE string  按格式"yyyy-MM-dd"解析字符串string，返回类型为SQL Date 
  - TIMESTAMP string  按格式"yyyy-MM-dd HH:mm:ss[.SSS]"解析，返回类型为SQL timestamp 
  - CURRENT_TIME  返回本地时区的当前时间，类型为SQL time（与LOCALTIME等价） 
  - INTERVAL string range  返回一个时间间隔。string表示数值；range可以是DAY，MINUTE，DAT TO HOUR等单位，也可以是YEAR TO MONTH这样的复合单位。如“2年10 个月”可以写成：INTERVAL '2-10' YEAR TO MONTH 
+ 聚合函数
  - COUNT(*)  返回所有行的数量，统计个数 
  - SUM([ ALL | DISTINCT ] expression)  对某个字段进行求和操作。默认情况下省略了关键字ALL，表示对所有行求和；如果指定DISTINCT，则会对数据进行去重，每个值只叠加一次。 
  - RANK()   返回当前值在一组值中的排名 ，排名函数常用语over中
  - ROW_NUMBER()    对一组值排序后，返回当前值的行号。与RANK()的功能相似 

#### UDF函数
+ 使用流程
  - 注册函数：tableEnv.createTemporarySystemFunction("MyFunction", MyFunction.class); ，此处注册为临时系统函数，也可以用createTemporaryFunction()方法注册为临时目录函数，
  - 使用函数：在SQL查询中直接使用函数名即可，在Table API中需要用call()方法调用函数,call()方法有两个参数，一个是注册好的函数名MyFunction，另一个则是函数调用时本身的参数。

+ 标量函数（Scalar Functions）：将输入的标量值转换成一个新的标量值；
  -  实现方式：继承ScalarFunction类，并实现一个或多个eval()方法，eval()方法中定义函数逻辑,但**ScalarFunction类未定义eval方法不可直接重写，此处方法名应Table API框架要求必须为eval**。
  - eg:UDF哈希函数，**注意：由于Table API在对函数进行解析时需要提取求值方法参数的类型引用，必须标注输入参数类型。**
  ```java
  public static class HashFunction extends ScalarFunction {
      // 接受任意类型输入，返回 INT 型输出
      public int eval(@DataTypeHint(inputGroup = InputGroup.ANY) Object o) {
          return o.hashCode();
      }
  }

  // 注册函数
  tableEnv.createTemporarySystemFunction("HashFunction", HashFunction.class);

  // 在 SQL 里调用注册好的函数
  tableEnv.sqlQuery("SELECT HashFunction(myField) FROM MyTable");   
  ```

+ 表函数（Table Functions）：将标量值转换成一个或多个新的行数据，也就是扩展成一个表 
  - 实现方式：继承TableFunction类，并实现一个或多个eval()方法，eval()方法中没有返回值通过调用collect方法发送行数据。
  ```java
  // 注意这里的类型标注，输出是Row类型，Row中包含两个字段：word和length。
  @FunctionHint(output = @DataTypeHint("ROW<word STRING, length INT>"))
  public static class SplitFunction extends TableFunction<Row> {
      public void eval(String str) {
          for (String s : str.split(" ")) {
              // 使用collect()方法发送一行数据
              collect(Row.of(s, s.length()));
          }
      }
  }

  // 注册函数
  tableEnv.createTemporarySystemFunction("SplitFunction", SplitFunction.class);

  // 在 SQL 里调用注册好的函数
  // 1. 交叉联结
  tableEnv.sqlQuery(
      "SELECT myField, word, length " +
      "FROM MyTable, LATERAL TABLE(SplitFunction(myField))"
  );
  // 2. 带ON TRUE条件的左联结
  tableEnv.sqlQuery(
      "SELECT myField, word, length " +
      "FROM MyTable " +
      "LEFT JOIN LATERAL TABLE(SplitFunction(myField)) ON TRUE"
  );
  // 重命名侧向表中的字段
  tableEnv.sqlQuery(
      "SELECT myField, newWord, newLength " +
      "FROM MyTable " +
      "LEFT JOIN LATERAL TABLE(SplitFunction(myField)) AS T(newWord, newLength) ON TRUE"
  );   
  ```


+ 聚合函数（Aggregate Functions）：将多行数据里的标量值转换成一个新的标量值
  - 要继承抽象类 AggregateFunction。AggregateFunction 有两个泛型参数<T, ACC>，T 表示聚合输出的结果类型，ACC则表示聚合的中间状态类型。 
  - AggregateFunction 需要实现3个方法：
    - createAccumulator()：创建一个新的累加器，用于保存聚合的中间状态，返回一个ACC
    - accumulate()： 是更新聚合状态，所以没有返回类型。
      - 第一个参数为ACC，需要注意的是，accumulate()与之前的求值方法eval()类似，也是底层架构要求的，必须为public，方法名必须为accumulate，且无法直接override、只能手动实现。 
    - getValue()：从累加器ACC中提取聚合结果，返回一个T
      - 对于复杂类型，需要使用getTypeInformation()方法和getResultType()方法来指定ACC和T类型信息
  - AggregateFunction 可选方法
    - 会话窗口进行聚合，merge()方法就是必须要实现的，它会定义累加器的合并操作
    - 聚合函数用在 OVER 窗口聚合中，就必须实现 retract()方法，保证数据可以进行撤回操作
    - resetAccumulator()方法则是重置累加器，这在一些批处理场景中会比较有用
  - AggregateFunction 的所有方法都必须是 公有的（public），不能是静态的（static），而且名字必须跟上面写的完全一样。createAccumulator、getValue、getResultType 以及getAccumulatorType 这几个方法是在抽象类 AggregateFunction 中定义的，可以 override；而其他则都是底层架构约定的方法。 
  ```java
  // 累加器类型定义
  public static class WeightedAvgAccumulator {
      public long sum = 0; // 加权和
      public int count = 0; // 数据个数
  }

  // 自定义聚合函数，输出为长整型的平均值，累加器类型为 WeightedAvgAccumulator
  public static class WeightedAvg extends AggregateFunction<Long, WeightedAvgAccumulator> {
      @Override
      public WeightedAvgAccumulator createAccumulator() {
          return new WeightedAvgAccumulator(); // 创建累加器
      }

      @Override
      public Long getValue(WeightedAvgAccumulator acc) {
          if (acc.count == 0) {
              return null; // 防止除数为0
          } else {
              return acc.sum / acc.count; // 计算平均值并返回
          }
      }

      // 累加计算方法，每来一行数据都会调用
      public void accumulate(WeightedAvgAccumulator acc, Long iValue, Integer iWeight) {
          acc.sum += iValue * iWeight;
          acc.count += iWeight;
      }
  }

  // 注册自定义聚合函数
  tableEnv.createTemporarySystemFunction("WeightedAvg", WeightedAvg.class);
  // 调用函数计算加权平均值
  Table result = tableEnv.sqlQuery(
      "SELECT student, WeightedAvg(score, weight) FROM ScoreTable GROUP BY student"
  );    
  ```


+ 表聚合函数（Table Aggregate Functions）：将多行数据里的标量值转换成一个或多个新的行数据
  - 要继承抽象类TableAggregateFunction。TableAggregateFunction的结构和原理与AggregateFunction非常类似，同样有两个泛型参数<T, ACC>，用一个ACC类型的累加器（accumulator）来存储聚合的中间结果。
  - 聚合函数中必须实现的三个方法，在TableAggregateFunction中也必须对应实现：
    - createAccumulator()：创建一个新的累加器，用于保存聚合的中间状态，返回一个ACC
    - accumulate()： 是更新聚合状态，所以没有返回类型。
      - 第一个参数为ACC，需要注意的是，accumulate()与之前的求值方法eval()类似，也是底层架构要求的，必须为public，方法名必须为accumulate，且无法直接override、只能手动实现。 
      - emitValue(): 用于输出结果，可以输出多个结果，所以没有返回类型。
        - 相对于getValue()方法；区别在于 emitValue 没有输出类型，而输入参数有两个：第一个是ACC类型的累加器，第二个则是用于输出数据的“收集器”out ,是调用out.collect()方法，调用多次就可以输出多行数据了
  - 目前SQL中没有直接使用表聚合函数的方式，所以需要使用Table API的方式来调用
  ```java
  // 聚合累加器的类型定义，包含最大的第一和第二两个数据
  public static class Top2Accumulator {
      public Integer first;
      public Integer second;
  }

  // 自定义表聚合函数，查询一组数中最大的两个，返回值为(数值，排名)的二元组
  public static class Top2 extends TableAggregateFunction<Tuple2<Integer, Integer>, Top2Accumulator> {
      @Override
      public Top2Accumulator createAccumulator() {
          Top2Accumulator acc = new Top2Accumulator();
          acc.first = Integer.MIN_VALUE; // 为方便比较，初始值给最小值
          acc.second = Integer.MIN_VALUE;
          return acc;
      }

      // 每来一个数据调用一次，判断是否更新累加器
      public void accumulate(Top2Accumulator acc, Integer value) {
          if (value > acc.first) {
              acc.second = acc.first;
              acc.first = value;
          } else if (value > acc.second) {
              acc.second = value;
          }
      }

      // 输出(数值，排名)的二元组，输出两行数据
      public void emitValue(Top2Accumulator acc, Collector<Tuple2<Integer, Integer>> out) {
          if (acc.first != Integer.MIN_VALUE) {
              out.collect(Tuple2.of(acc.first, 1));
          }
          if (acc.second != Integer.MIN_VALUE) {
              out.collect(Tuple2.of(acc.second, 2));
          }
      }
  }

  // 注册表聚合函数函数 
  tableEnv.createTemporarySystemFunction("Top2", Top2.class); 
  
  // 在Table API中调用函数 
  tableEnv.from("MyTable") 
    .groupBy($("myField")) 
    .flatAggregate(call("Top2", $("value")).as("value", "rank")) 
    .select($("myField"), $("value"), $("rank")); 
  ```
### SQL_cline:测试开发
+ 首先启动本地集群 
  - ./bin/start-cluster.sh 
+ 启动Flink SQL客户端 
  - ./bin/sql-client.sh 
  - SQL 客户端的启动脚本同样位于Flink的bin目录下。默认的启动模式是embedded，也就是说客户端是一个嵌入在本地的进程，这是目前唯一支持的模式。未来会支持连接到远程SQL客户端的模式。 
+ 设置运行模式 
  - 启动客户端后，就进入了命令行界面，这时就可以开始写SQL了。一般我们会在开始之前对环境做一些设置，比较重要的就是运行模式。 首先是表环境的运行时模式，有流处理和批处理两个选项。默认为流处理：Flink SQL> SET 'execution.runtime-mode' = 'streaming'; 其次是SQL客户端的“执行结果模式”，主要有table、changelog、tableau三种，默认为table模式
    - table 模式： Flink SQL> SET 'sql-client.execution.result-mode' = 'table'; table 模式就是最普通的表处理模式，结果会以逗号分隔每个字段
    - changelog更新日志模式，会在数据前加上“+”（表示插入）或“-”（表示撤回）的前缀；
    - tableau 经典的可视化表模式，结果会是一个虚线框的表格。 
  + 此外我们还可以做一些其它可选的设置，比如之前提到的空闲状态生存时间（TTL）： Flink SQL> SET 'table.exec.state.ttl' = '1000'; 除了在命令行进行设置，我们也可以直接在 SQL 客户端的配置文件 sql-cli-defaults.yaml中进行各种配置，甚至还可以在这个yaml文件里预定义表、函数和catalog
+ 执行SQL查询
  ```sql
  Flink SQL> INSERT INTO ResultTable SELECT user, COUNT(url) as cnt FROM EventTable GROUP BY user;   
  ```
+ 在SQL客户端中，每定义一个SQL查询，就会把它作为一个Flink作业提交到集群上执行。所以通过这种方式，我们可以快速地对流处理程序进行开发测试。

### 连接到外部系统
+ 连接到控制台：WITH中定义connector为print就可以了

#### 连接到Kafka
+ 引入依赖,想在SQL客户端里使用Kafka连接器，还需要下载对应的jar包放到lib目录下
  ```xml
  <dependency> 
    <groupId>org.apache.flink</groupId> 
    <artifactId>flink-connector-kafka_${scala.binary.version}</artifactId> 
    <version>${flink.version}</version> 
  </dependency> 
  ```
  - 根据Kafka连接器中配置的格式，我们可能需要引入对应的依赖支持。以CSV为例.由于SQL客户端中已经内置了CSV、JSON的支持，因此使用时无需专门引入；而对于没有内置支持的格式（比如Avro），则仍然要下载相应的jar包。
    ```xml 
    <dependency> 
      <groupId>org.apache.flink</groupId> 
      <artifactId>flink-csv</artifactId> 
      <version>${flink.version}</version> 
    </dependency>
    ```
+  创建连接到Kafka的表,with定义连接器和配置参数
  ```java
  CREATE TABLE KafkaTable ( 
    `user` STRING, 
    `url` STRING, 
    `ts` TIMESTAMP(3) METADATA FROM 'timestamp' 
  ) WITH ( 
    'connector' = 'kafka', 
    'topic' = 'events', 
    'properties.bootstrap.servers' = 'localhost:9092', 
    'properties.group.id' = 'testGroup', 
    'scan.startup.mode' = 'earliest-offset', 
    'format' = 'csv' 
  ) 
  ```
+ Upsert Kafka
  - 正常情况下，Kafka作为保持数据顺序的消息队列，读取和写入都应该是流式的数据，对应在表中就是仅追加（append-only）模式。如果我们想要将有更新操作（比如分组聚合）的结果表写入Kafka，就会因为Kafka无法识别撤回（retract）或更新插入（upsert）消息而导致异常。
  - 为了解决这个问题，Flink专门增加了一个“更新插入Kafka”（Upsert Kafka）连接器。这个连接器支持以更新插入（UPSERT）的方式向Kafka的topic中读写数据，具体来说，Upsert Kafka 连接器处理的是更新日志（changlog）流
    - 如果作为TableSource，连接器会将读取到的topic中的数据（key, value），解释为对当前key的数据值的更新（UPDATE），也就是查找动态表中key对应的一行数据，将value更新为最新的值；因为是Upsert操作，所以如果没有key 对应的行，那么也会执行插入（INSERT）操作。另外，如果遇到 value 为空（null），连接器就把这条数据理解为对相应key那一行的删除（DELETE）操作。 
    - 如果作为 TableSink，Upsert Kafka 连接器会将有更新操作的结果表，转换成更新日志（changelog）流。如果遇到插入（INSERT）或者更新后（UPDATE_AFTER）的数据，对应的是一个添加（add）消息，那么就直接正常写入 Kafka 主题；如果是删除（DELETE）或者更新前的数据，对应是一个撤回（retract）消息，那么就把value为空（null）的数据写入Kafka。由于Flink是根据键（key）的值对数据进行分区的，这样就可以保证同一个key上的更新和删除消息都会落到同一个分区中。 
  ```java
  CREATE TABLE pageviews_per_region (
      user_region STRING,
      pv BIGINT,
      uv BIGINT,
      PRIMARY KEY (user_region) NOT ENFORCED
  ) WITH (
      'connector' = 'upsert-kafka',
      'topic' = 'pageviews_per_region',
      'properties.bootstrap.servers' = '...',
      'key.format' = 'avro',
      'value.format' = 'avro'
  );

  CREATE TABLE pageviews (
      user_id BIGINT,
      page_id BIGINT,
      viewtime TIMESTAMP,
      user_region STRING,
      WATERMARK FOR viewtime AS viewtime - INTERVAL '2' SECOND
  ) WITH (
      'connector' = 'kafka',
      'topic' = 'pageviews',
      'properties.bootstrap.servers' = '...',
      'format' = 'json'
  );

  -- 计算 pv、uv 并插入到 upsert-kafka 表中
  INSERT INTO pageviews_per_region
  SELECT
      user_region,
      COUNT(*),
      COUNT(DISTINCT user_id)
  FROM pageviews
  GROUP BY user_region;     
  ```
  - 这里我们从Kafka表pageviews中读取数据，统计每个区域的PV（全部浏览量）和UV（对用户去重），这是一个分组聚合的更新查询，得到的结果表会不停地更新数据。为了将结果表写入Kafka的pageviews_per_region主题，我们定义了一个Upsert Kafka表，它的字段中需要用PRIMARY KEY来指定主键，并且在WITH子句中分别指定key和value的序列化格式。

#### 连接到文件系统
+ 已内置，无需引入依赖
  ```java
  CREATE TABLE MyTable ( 
    column_name1 INT, 
    column_name2 STRING, 
    ... 
    part_name1 INT, 
    part_name2 STRING 
  ) PARTITIONED BY (part_name1, part_name2) WITH ( 
    'connector' = 'filesystem',           -- 连接器类型 
    'path' = '...',  -- 文件路径 
    'format' = '...'                      -- 文件格式 
  )
  ```

#### 连接到JDBC
+ 作为TableSink向数据库写入数据时，有主键全支持，无主键仅可追加。。
+ 引入依赖
  ```xml
  <dependency> 
    <groupId>org.apache.flink</groupId> 
    <artifactId>flink-connector-jdbc_${scala.binary.version}</artifactId> 
    <version>${flink.version}</version> 
  </dependency> 
  <!--连接到特定的数据库，我们还用引入相关的驱动器依赖，比如MySQL： -->
  <dependency> 
      <groupId>mysql</groupId> 
      <artifactId>mysql-connector-java</artifactId> 
      <version>5.1.38</version> 
  </dependency>
  ```
+ eg:
  ```java
  // 创建一张连接到 MySQL的 表 
  CREATE TABLE MyTable ( 
    id BIGINT, 
    name STRING, 
    age INT, 
    status BOOLEAN, 
    PRIMARY KEY (id) NOT ENFORCED 
  ) WITH ( 
    'connector' = 'jdbc', 
    'url' = 'jdbc:mysql://localhost:3306/mydatabase', 
    'table-name' = 'users' 
  ); 
  // 将另一张表 T的数据写入到 MyTable 表中 
  INSERT INTO MyTable 
  SELECT id, name, age, status FROM T; 
  ```

#### 连接到Elasticsearch：分布式搜索分析引擎
+ Flink提供的Elasticsearch的SQL连接器只能作为TableSink，可以将表数据写入Elasticsearch的索引（index）。Elasticsearch连接器的使用与JDBC连接器非常相似，写入数据的模式同样是由创建表的DDL中是否有主键定义决定的。
+ 引入依赖
  ```xml
  <!--6.x-->
  <dependency> 
    <groupId>org.apache.flink</groupId>  
    <artifactId>flink-connector-elasticsearch6_${scala.binary.version}</artifactId> 
    <version>${flink.version}</version> 
  </dependency> 

  <!--9以上版本-->
  <dependency> 
    <groupId>org.apache.flink</groupId>  
    <artifactId>flink-connector-elasticsearch7_${scala.binary.version}</artifactId> 
    <version>${flink.version}</version> 
  </dependency> 
  ```
+ eg：
  ```java
  //创建一张连接到 Elasticsearch的 表 
  CREATE TABLE MyTable ( 
    user_id STRING, 
    user_name STRING 
    uv BIGINT, 
    pv BIGINT, 
    PRIMARY KEY (user_id) NOT ENFORCED 
  ) WITH ( 
    'connector' = 'elasticsearch-7', 
    'hosts' = 'http://localhost:9200', 
    'index' = 'users' 
  ); 
  ```
#### 连接到Hbase
+ 引入依赖
  ```xml
  <!---1.4版本引入依赖如下-->
  <dependency> 
    <groupId>org.apache.flink</groupId> 
    <artifactId>flink-connector-hbase-1.4_${scala.binary.version}</artifactId> 
    <version>${flink.version}</version> 
  </dependency> 
  <!--对于HBase 2.2版本，引入的依赖则是-->
  <dependency> 
    <groupId>org.apache.flink</groupId> 
    <artifactId>flink-connector-hbase-2.2_${scala.binary.version}</artifactId> 
    <version>${flink.version}</version> 
  </dependency>
  ```
+ 由于HBase并不是关系型数据库，因此转换为Flink SQL中的表会稍有一些麻烦。在DDL创建出的HBase表中，所有的列族（column family）都必须声明为ROW类型，在表中占据一个字段；
  - 而每个family中的列（column qualifier）则对应着ROW里的嵌套字段。我们不需要将HBase中所有的family和qualifier都在Flink SQL的表中声明出来，只要把那些在查询中用到的声明出来就可以了。
  - 除了所有ROW类型的字段（对应着HBase中的family），表中还应有一个原子类型的字段，它就会被识别为HBase的rowkey。在表中这个字段可以任意取名，不一定非要叫rowkey。 
  - 下面是一个具体示例：
  ```java
  // 创建一张连接到 HBase的 表 
  CREATE TABLE MyTable ( 
  rowkey INT, 
  family1 ROW<q1 INT>, 
  family2 ROW<q2 STRING, q3 BIGINT>, 
  family3 ROW<q4 DOUBLE, q5 BOOLEAN, q6 STRING>, 
  PRIMARY KEY (rowkey) NOT ENFORCED 
  ) WITH ( 
    'connector' = 'hbase-1.4', 
    'table-name' = 'mytable', 
    'zookeeper.quorum' = 'localhost:2181' 
  ); 
  //假设表T的字段结构是 [rowkey, f1q1, f2q2, f2q3, f3q4, f3q5, f3q6] 
  INSERT INTO MyTable 
  SELECT rowkey, ROW(f1q1), ROW(f2q2, f2q3), ROW(f3q4, f3q5, f3q6) FROM T; 
  ```

#### 连接到Hive（实时数仓）
+ Flink 与 Hive 的集成比较特别。Flink提供了“Hive目录”（HiveCatalog）功能，允许使用Hive 的“元存储”（Metastore）来管理Flink的元数据。
  - Metastore 可以作为一个持久化的目录，因此使用HiveCatalog可以跨会话存储Flink特定的元数据。这样一来，我们在HiveCatalog中执行执行创建Kafka表或者ElasticSearch表，就可以把它们的元数据持久化存储在Hive的Metastore中；对于不同的作业会话就不需要重复创建了，直接在SQL查询中重用就可以。 
  - 使用HiveCatalog，Flink 可以作为读写Hive表的替代分析引擎。这样一来，在Hive中进行批处理会更加高效；与此同时，也有了连续在Hive中读写数据、进行流处理的能力，这也使得“实时数仓”（real-time data warehouse）成为了可能。

+ flink只有Blink的计划器（planner）提供了Hive 集成的支持，所以需要在使用Flink SQL时选择Blink planner。
  - Hive是hadoop组件，需在环境变量中设置HADOOP_CLASSPATH，export HADOOP_CLASSPATH=`hadoop classpath` 
  - 引入hive依赖，此依赖打包时不要打包到jar包中，方便适应运行环境
  ```xml
  <!-- Flink 的Hive连接器--> 
  <dependency> 
    <groupId>org.apache.flink</groupId> 
    <artifactId>flink-connector-hive_${scala.binary.version}</artifactId> 
    <version>${flink.version}</version> 
  </dependency> 
  
  <!-- Hive 依赖 --> 
  <dependency> 
      <groupId>org.apache.hive</groupId> 
      <artifactId>hive-exec</artifactId> 
      <version>${hive.version}</version> 
  </dependency> 
  ```
+ 连接到hive：通过在表环境中配置HiveCatalog来实现的，将表环境的planner设置为Blink。
  ```java
  EnvironmentSettings settings = 
  EnvironmentSettings.newInstance().useBlinkPlanner().build(); 
  TableEnvironment tableEnv = TableEnvironment.create(settings); 
  
  String name            = "myhive"; 
  String defaultDatabase = "mydatabase"; 
  String hiveConfDir     = "/opt/hive-conf"; 
  
  // 创建一个HiveCatalog，并在表环境中注册 
  HiveCatalog hive = new HiveCatalog(name, defaultDatabase, hiveConfDir); 
  tableEnv.registerCatalog("myhive", hive); 
  
  // 使用HiveCatalog作为当前会话的catalog 
  tableEnv.useCatalog("myhive"); 
  ```
  - SQL客户端中也可配置
    ```java
    Flink SQL> create catalog myhive with ('type' = 'hive', 'hive-conf-dir' = 
    '/opt/hive-conf'); 
    [INFO] Execute statement succeed. 
    
    Flink SQL> use catalog myhive; 
    [INFO] Execute statement succeed. 
    ```
+ 设置SQL方言：HQL、FQL
  - SQL中设置 
    - 通过配置table.sql-dialect 属性来设置SQL方言：set table.sql-dialect=hive; 
    - 使用SQL客户端，我们还可以在配置文件sql-cli-defaults.yaml中通过“configuration”模块来设置：
      ```yaml 
      execution: 
      planner: blink 
      type: batch 
      result-mode: table 
      configuration: 
      table.sql-dialect: hive 
      ```
  - Table API 中设置 
    ```java 
    // 配置hive方言 
    tableEnv.getConfig().setSqlDialect(SqlDialect.HIVE); 
    // 配置default方言 
    tableEnv.getConfig().setSqlDialect(SqlDialect.DEFAULT);
    ```  
+ 读写Hive表
  - 在批处理模式下，Flink会在执行查询语句时对Hive表进行一次性读取，在作业完成时将结果数据向Hive表进行一次性写入；
  - 流处理模式下，Flink会持续监控Hive表，在新数据可用时增量读取，也可以持续写入新数据并增量式地让它们可见。 
  - 更灵活的是，我们可以随时切换SQL方言，从其它数据源（例如Kafka）读取数据、经转换后再写入Hive。下面是以纯SQL形式编写的一个示例，我们可以启动SQL客户端来运行：
  ```java
  // 设置SQL方言为hive，创建Hive表
  SET table.sql-dialect=hive;
  CREATE TABLE hive_table (
      user_id STRING,
      order_amount DOUBLE
  ) PARTITIONED BY (dt STRING, hr STRING) STORED AS parquet TBLPROPERTIES (
      'partition.time-extractor.timestamp-pattern'='$dt $hr:00:00',
      'sink.partition-commit.trigger'='partition-time',
      'sink.partition-commit.delay'='1 h',
      'sink.partition-commit.policy.kind'='metastore,success-file'
  );

  // 设置SQL方言为default，创建Kafka表
  SET table.sql-dialect=default;
  CREATE TABLE kafka_table (
      user_id STRING,
      order_amount DOUBLE,
      log_ts TIMESTAMP(3),
      WATERMARK FOR log_ts AS log_ts - INTERVAL '5' SECOND -- 定义水位线
  ) WITH (...);

  // 将Kafka中读取的数据经转换后写入Hive
  INSERT INTO TABLE hive_table
  SELECT user_id, order_amount, DATE_FORMAT(log_ts, 'yyyy-MM-dd'), DATE_FORMAT(log_ts, 'HH')
  FROM kafka_table;
  ```
## Flink CEP(复杂事件处理)
+ CEP流程
  - 定义一个匹配规则(模式：包含简单事件特征、事件组合关系) 
  - 将匹配规则应用到事件流上，检测满足规则的复杂事件 
  - 对检测到的复杂事件进行处理，得到结果进行输出 

+ 应用常见
  - 实时监控告警告：用户连续登录失败
  - 用户画像：用户行为分析
  - 运维监控：连续错误日志处理

+ 引入依赖
  ```xml 
  <dependency> 
    <groupId>org.apache.flink</groupId> 
    <artifactId>flink-cep_${scala.binary.version}</artifactId> 
    <version>${flink.version}</version> 
  </dependency>
  ```
  - 为了精简和避免依赖冲突，Flink 会保持尽量少的核心依赖。所以核心依赖中并不包括任何的连接器（conncetor）和库，这里的库就包括了SQL、CEP以及 ML 等等。所以如果想要**在Flink 集群中提交运行CEP作业，应该向Flink SQL那样将依赖的jar包放在/lib目录下。** 

+ 简单示例
  ```java
  //单独定义一个登录事件POJO类
  public class LoginEvent {
      public String userId;
      public String ipAddress;
      public String eventType;
      public Long timestamp;

      public LoginEvent(String userId, String ipAddress, String eventType, Long timestamp) {
          this.userId = userId;
          this.ipAddress = ipAddress;
          this.eventType = eventType;
          this.timestamp = timestamp;
      }

      public LoginEvent() {}

      @Override
      public String toString() {
          return "LoginEvent{" +
              "userId='" + userId + '\'' +
              ", ipAddress='" + ipAddress + '\'' +
              ", eventType='" + eventType + '\'' +
              ", timestamp=" + timestamp +
              '}';
      }
  }


  //定义一个模式(Pattern)，将模式应用到DataStream上得到一个PatternStream，对其镜像转换处理，提取复杂事件包装输出报警信息
  import org.apache.flink.api.common.eventtime.SerializableTimestampAssigner;
  import org.apache.flink.api.common.eventtime.WatermarkStrategy;
  import org.apache.flink.cep.CEP;
  import org.apache.flink.cep.PatternSelectFunction;
  import org.apache.flink.cep.PatternStream;
  import org.apache.flink.cep.pattern.Pattern;
  import org.apache.flink.cep.pattern.conditions.SimpleCondition;
  import org.apache.flink.streaming.api.datastream.KeyedStream;
  import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

  import java.util.List;
  import java.util.Map;

  public class LoginFailDetect {
      public static void main(String[] args) throws Exception {
          StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
          env.setParallelism(1);

          // 获取登录事件流，并提取时间戳、生成水位线
          KeyedStream<LoginEvent, String> stream = env
                .fromElements(
                          new LoginEvent("user_1", "192.168.0.1", "fail", 2000L),
                          new LoginEvent("user_1", "192.168.0.2", "fail", 3000L),
                          new LoginEvent("user_2", "192.168.1.29", "fail", 4000L),
                          new LoginEvent("user_1", "171.56.23.10", "fail", 5000L),
                          new LoginEvent("user_2", "192.168.1.29", "success", 6000L),
                          new LoginEvent("user_2", "192.168.1.29", "fail", 7000L),
                          new LoginEvent("user_2", "192.168.1.29", "fail", 8000L)
                  )
                .assignTimestampsAndWatermarks(
                          WatermarkStrategy.<LoginEvent>forMonotonousTimestamps()
                                .withTimestampAssigner(
                                          new SerializableTimestampAssigner<LoginEvent>() {
                                              @Override
                                              public long extractTimestamp(LoginEvent loginEvent, long l) {
                                                  return loginEvent.timestamp;
                                              }
                                          }
                                  )
                  )
                .keyBy(r -> r.userId);

          // 1. 定义Pattern，连续的三个登录失败事件
          Pattern<LoginEvent, LoginEvent> pattern = Pattern
                .<LoginEvent>begin("first") // 以第一个登录失败事件开始
                .where(new SimpleCondition<LoginEvent>() {
                      @Override
                      public boolean filter(LoginEvent loginEvent) throws Exception {
                          return loginEvent.eventType.equals("fail");
                      }
                  })
                .next("second") // 接着是第二个登录失败事件
                .where(new SimpleCondition<LoginEvent>() {
                      @Override
                      public boolean filter(LoginEvent loginEvent) throws Exception {
                          return loginEvent.eventType.equals("fail");
                      }
                  })
                .next("third") // 接着是第三个登录失败事件
                .where(new SimpleCondition<LoginEvent>() {
                      @Override
                      public boolean filter(LoginEvent loginEvent) throws Exception {
                          return loginEvent.eventType.equals("fail");
                      }
                  });

          // 2. 将Pattern应用到流上，检测匹配的复杂事件，得到一个PatternStream
          PatternStream<LoginEvent> patternStream = CEP.pattern(stream, pattern);

          // 3. 将匹配到的复杂事件选择出来，然后包装成字符串报警信息输出
          patternStream
                .select(new PatternSelectFunction<LoginEvent, String>() {
                      @Override
                      public String select(Map<String, List<LoginEvent>> map) throws Exception {
                          LoginEvent first = map.get("first").get(0);
                          LoginEvent second = map.get("second").get(0);
                          LoginEvent third = map.get("third").get(0);
                          return first.userId + " 连续三次登录失败！登录时间：" +
                                  first.timestamp + ", " + second.timestamp + ", " + third.timestamp;
                      }
                  })
                .print("warning");

          env.execute();
      }
  }
      
  ```
### 模式API(Pattern API)
#### 个体模式：
+ 这里的每一个简单事件并不是任意选取的，也需要有一定的条件规则；所以我们就把每个简单事件的匹配规则，叫作“个体模式”（Individual Pattern）
  - 个体模式一般都会匹配接收一个事件，个体模式都以一个“连接词”开始定义的，比如begin、next等
+ 个体模式可以匹配接收一个事件，也可以接收多个事件。可以给个体模式增加一个“量词”（quantifier），就能够让它进行循环匹配，接收多个事件，用Map中的一个列表保存。 以map.get("first").get(0);提取
  - .oneOrMore（） ：匹配事件出现一次或多次也可用a+来简单表示。 
  - .times（N）：匹配事件发生特定次数（times）
  - .times（fromTimes，toTimes） ：指定匹配事件出现的次数范围  
  - .greedy() ：只能用在循环模式后，使当前循环模式变得“贪心”（greedy），也就是总是尽可能多地去匹配。例如a.times(2, 4).greedy()，如果出现了连续 4个a，那么会直接把aaaa检测出来进行处理，其他任意2个a是不算匹配事件的。 
  - .optional() ：使当前模式成为可选的，也就是说可以满足这个匹配条件，也可以不满
+ 匹配条件：
  - 限定子类型 ：pattern.subtype(SubEvent.class); ：当事件是SubEvent类型时，匹配成功 
  -  简单条件（Simple Conditions）：根据当前事件的特征来决定是否接受它。这在本质上其实就是一个filter操作，需实现SimpleCondition类
  - 迭代条件（Iterative Conditions） 依靠之前事件来做判断的条件，就叫作“迭代条件”可用IterativeCondition抽象类。这其实是更加通用的条件表达，查需要实现一个filter()方法，这个方法有两个参数：除了当前事件之外，还有一个上下文Context。调用这个上下文的.getEventsForPattern()方法，传入一个模式名称，就可以拿到这个模式中已匹配到的所有数据了。
  - 终止条件：（stop Conditions）：循环匹配时，遇到终止条件，就会停止匹配，不再接收后续的事件，调用模式对象的.until()方法来实现的，同样传入一个IterativeCondition 作为参数。需要注意的是，终止条件只与 oneOrMore()或者oneOrMore().optional()结合使用。
  - 组合条件（Combining Conditions）：组合多个条件，连续调用where为and，调用.or()为or.
#### 模式序列：多个简单模式的组合
+ 组合模式形式
  ```java
  Pattern<Event, ?> pattern = Pattern 
    .<Event>begin("start").where(...) 
    .next("next").where(...) 
    .followedBy("follow").where(...) 
    ... 
  ```
+ 初始模式（Initial Pattern） 
  - 所有的组合模式，都必须以一个“初始模式”开头；而初始模式必须通过调用Pattern的静态方法.begin()来创建。如下所示：
  ```java 
  Pattern<Event, ?> start = Pattern.<Event>begin("start"); 
  //- start为模式的名称，检测流中事件的基本类型，这里我们定义为Event。第二个则是当前模式里事件的子类型，由子类型限制条件指定。我们这里用类型通配符（？）代替，就可以从上下文直接推断了。 
  ```
  - 可调用within()限制匹配时间，eg：middle.within(Time.seconds(10));
+ 近邻条件（Contiguity Conditions） 
  - 在初始模式之后，我们就可以按照复杂事件的顺序追加模式，组合成模式序列了。模式之间的组合是通过一些“连接词”方法实现的，这些连接词指明了先后事件之间有着怎样的近邻关系，这就是所谓的“近邻条件”（Contiguity Conditions，也叫“连续性条件”）。 
  - 严格近邻:严格地按顺序一个接一个出现,用next()方法,与times、oneOrMore()搭配使用。
  - 宽松近邻:允许事件之间被其他事件打断，用followedBy()方法
  - 非确定性宽松近邻:允许事件之间被其他事件打断，但打断的事件类型必须满足一定的条件，用followedByAny()方法

+ 其他限制条件：
  - .notNext() ：表示前一个模式匹配到的事件后面，不能紧跟着某种事件。
  - .notFollowedBy() ：表示前一个模式匹配到的事件后面，不能紧跟着某种事件序列。
+ 循环模式中的近邻条件   
  - 近邻关系同样有三种：严格近邻、宽松近邻以及非确定性宽松近邻。对于定义了量词（如oneOrMore()、times()）的循环模式，默认内部采用的是宽松近邻。
  - 可通过调用.consecutive()方法，将循环模式中的近邻条件改为严格近邻相当于next
  - 可通过调用.nonConsecutive()方法，将循环模式中的近邻条件改为非确定性宽松近邻相当于followedByAny

#### 模式组：模式序列的组合
+ 在模式组中，每一个模式序列就被当作了某一阶段的匹配条件，返回的类型是一个GroupPattern。而GroupPattern本身是Pattern的子类；所以个体模式和组合模式能调用的方法，比如times()、oneOrMore()、optional()之类的量词，模式组一般也是可以用的。
  ```java
  // 以模式序列作为初始模式 
  Pattern<Event, ?> start = Pattern.begin(
      Pattern.<Event>begin("start_start").where(...)
    .followedBy("start_middle").where(...)
  );

  // 在start后定义严格近邻的模式序列，并重复匹配两次 
  Pattern<Event, ?> strict = start.next(
      Pattern.<Event>begin("next_start").where(...)
    .followedBy("next_middle").where(...)
  ).times(2);

  // 在start后定义宽松近邻的模式序列，并重复匹配一次或多次 
  Pattern<Event, ?> relaxed = start.followedBy(
      Pattern.<Event>begin("followedby_start").where(...)
    .followedBy("followedby_middle").where(...)
  ).oneOrMore();

  // 在start后定义非确定性宽松近邻的模式序列，可以匹配一次，也可以不匹配 
  Pattern<Event, ?> nonDeterminRelaxed = start.followedByAny(
      Pattern.<Event>begin("followedbyany_start").where(...)
    .followedBy("followedbyany_middle").where(...)
  ).optional();
  ```
#### 匹配后跳过策略
+  策略可以在Pattern的初始模式定义中，作为begin()的第二个参数传入：
  ```java
  Pattern.begin("start", AfterMatchSkipStrategy.noSkip()) 
    .where(...) 
    ... 
  ``` 
+ 以“a a a b”匹配a开头，共有6个匹配结果：：（a1 a2 a3 b），（a1 a2 b），（a1 b），（a2 a3 b），（a2 b），（a3 b）为例

+ 跳至下一个（.skipToNext()） 
  - 找到每个子匹配的最大匹配。最终得到（a1 a2 a3 b），（a2 a3 b），（a3 b）。可以看到，这种跳过策略跟使用.greedy()效果是相同的。 
+ 跳过所有子匹配（.skipPastLastEvent()）  
  - 找到 a1 开始的匹配（a1 a2 a3 b）之后，直接跳过所有a1直到a3开头的匹配，相当于把这些子匹配都跳过了。最终得到（a1 a2 a3 b），这是最为精简的跳过策略。 
+ 跳至第一个（.skipToFirst(“a”)） 
  - 传入一个参数，指明跳至哪个模式的第一个匹配事件，即找到a1开始的匹配（a1 a2 a3 b）后，仅匹配以a1开头的匹配。最终得到（a1 a2 a3 b），（ a1 a2 b），（ a1 b）
+ 跳至最后一个（.skipToLast(“a”)） 
  - 同样传入一个参数，指明跳至哪个模式的最后一个匹配事件。找到a1开始的匹配（a1 a2 a3 b）后，跳过所有a1、a2开始的匹配，跳到以最后一个a（也就是a3）为开始的匹配。最终得到（a1 a2 a3 b），（a3 b）。

### 模式的检测处理

#### 将模式应用到流上 
+ 调用 CEP 类的静态方法.pattern()，将数据流（ DataStream）和模式（Pattern）作为两个参数传入就可以了。最终得到的是一个PatternStream： 
  ````java
  DataStream<Event> inputStream = ... 
  Pattern<Event, ?> pattern = ... 
  PatternStream<Event> patternStream = CEP.pattern(inputStream, pattern); 
  ````
- 这里的DataStream，也可以通过keyBy进行按键分区得到KeyedStream，接下来对复杂事件的检测就会针对不同的key单独进行了。 
+ 模式中定义的复杂事件，发生是有先后顺序的，这里“先后”的判断标准取决于具体的时间语义。默认情况下采用事件时间语义，那么事件会以各自的时间戳进行排序；如果是处理时间语义，那么所谓先后就是数据到达的顺序。对于时间戳相同或是同时到达的事件，我们还可以在CEP.pattern()中传入一个比较器作为第三个参数，用来进行更精确的排序： 
  ```java
  // 可选的事件比较器 
  EventComparator<Event> comparator = ...  
  PatternStream<Event> patternStream = CEP.pattern(input, pattern, comparator); 
  得到PatternStream 后，接下来要做的就是对匹配事件的检测处理了。 
  ``` 
#### 处理匹配事件 
+ PatternStream 的转换操作主要可以分成两种：简单便捷的选择提取（select）操作，和更加通用、更加强大的处理（process）操作,：选择操作传入的是一个PatternSelectFunction，处理操作传入的则是一个PatternProcessFunction(**最常用**)

+  匹配事件的通用处理（process）
  - 调用PatternStream的.process()方法，传入一个PatternProcessFunction，在底层选择操作最终也会被转换为processFunction进行处理。
  ```java
  // 3. 将匹配到的复杂事件选择出来，然后包装成报警信息输出
  // ctx上下文
  patternStream.process(new PatternProcessFunction<LoginEvent, String>() {
      @Override
      public void processMatch(Map<String, List<LoginEvent>> map, Context ctx, Collector<String> out) throws Exception {
          LoginEvent first = map.get("fails").get(0);
          LoginEvent second = map.get("fails").get(1);
          LoginEvent third = map.get("fails").get(2);
          out.collect(first.userId + " 连续三次登录失败！登录时间：" + first.timestamp +
                  ", " + second.timestamp + ", " + third.timestamp);
      }
  }).print("warning");
  ```

+ 匹配事件的选择提取
  - .select(new MyPatternSelectFunction());
  - PatternSelectFunction 是 Flink CEP 提供的一个函数类接口，它会将检测到的匹配事件保存在一个Map里，对应的key就是这些事件的名称。这里的“事件名称”就对应着在模式中定义的每个个体模式的名称；而个体模式可以是循环模式，一个名称会对应多个事件，所以最终保存在Map里的value就是一个事件的列表（List）。但是**PatternFlatSelectFunction使用更加灵活更常用**
  ```java
  class MyPatternSelectFunction implements PatternSelectFunction<Event, String>{  
    @Override 
    public String select(Map<String, List<Event>> pattern) throws Exception { 
      //调用Map的.get(key)方法后得到的是一个事件的List；如果个体模式是单例的，那么List中只有一个元素，直接调用.get(0)就可以把它取出。
      Event startEvent = pattern.get("start").get(0); 
      Event middleEvent = pattern.get("middle").get(0); 
      return startEvent.toString() + " " + middleEvent.toString(); 
    } 
  } 
  ```
  - PatternStream还有一个类似的方法是.flatSelect()，传入的参数是一个PatternFlatSelectFunction。从名字上就能看出，这是PatternSelectFunction的“扁平化”版本；内部需要实现一个flatSelect()方法，它与之前select()的不同就在于没有返回值，而是多了一个收集器（Collector）参数out，通过调用out.collet()方法就可以实现多次发送输出数据了。
  ```java
  patternStream.flatSelect(new PatternFlatSelectFunction<LoginEvent, String>() {
      @Override
      public void flatSelect(Map<String, List<LoginEvent>> map, Collector<String> out) throws Exception {
          LoginEvent first = map.get("fails").get(0);
          LoginEvent second = map.get("fails").get(1);
          LoginEvent third = map.get("fails").get(2);
          out.collect(first.userId + " 连续三次登录失败！登录时间：" + first.timestamp +
                  ", " + second.timestamp + ", " + third.timestamp);
      }
  }).print("warning");
  ```

#### 处理超时事件
+ Flink CEP 中，提供了一个专门捕捉超时的部分匹配事件的接口，叫作TimedOutPartialMatchHandler。
  - 这个接口需要实现一个 processTimedOutMatch()方法，可以将超时的、已检测到的部分匹配事件放在一个Map中，作为方法的第一个参数；
  - 方法的第二个参数则是PatternProcessFunction 的上下文 Context。所以这个接口必须与PatternProcessFunction结合使用，对处理结果的输出则需要利用侧输出流来进行。
+ 使用PatternProcessFunction 的侧输出流,推荐使用 
  ```java
  class MyPatternProcessFunction extends PatternProcessFunction<Event, String> 
          implements TimedOutPartialMatchHandler<Event> {
      // 正常匹配事件的处理
      @Override
      public void processMatch(Map<String, List<Event>> match, Context ctx,
                              Collector<String> out) throws Exception {
          ...
      }
      // 超时部分匹配事件的处理
      @Override
      public void processTimedOutMatch(Map<String, List<Event>> match, Context ctx)
              throws Exception {
          Event startEvent = match.get("start").get(0);
          //processTimedOutMatch()方法中定义了一个输出标签（OutputTag）。调用ctx.output()方法，就可以将超时的部分匹配事件输出到标签所标识的侧输出流了
          OutputTag<Event> outputTag = new OutputTag<Event>("time-out") {};
          ctx.output(outputTag, startEvent);
      }
  }
  ```
+ 使用PatternTimeoutFunction ，前者的简化版本
  - 调用PatternStream的.select()方法时需要传入三个参数：侧输出流标签（OutputTag），超时事件处理函数PatternTimeoutFunction，匹配事件提取函数PatternSelectFunction。
  - 在超时事件处理的过程中，从Map里只能取到已经检测到匹配的那些事件；如果取可能未匹配的事件并调用它的对象方法，则可能会报空指针异常（NullPointerException）。
  - 超时事件处理的结果进入侧输出流，正常匹配事件的处理结果进入主流，两者的数据类型可以不同。 
  ```java
  // 定义一个侧输出流标签，用于标识超时侧输出流
  OutputTag<String> timeoutTag = new OutputTag<String>("timeout") {};

  // 将匹配到的，和超时部分匹配的复杂事件提取出来，然后包装成提示信息输出
  SingleOutputStreamOperator<String> resultStream = patternStream
      .select(timeoutTag,
          // 超时部分匹配事件的处理
          new PatternTimeoutFunction<Event, String>() {
              @Override
              public String timeout(Map<String, List<Event>> pattern, long timeoutTimestamp) throws Exception {
                  Event event = pattern.get("start").get(0);
                  return "超时：" + event.toString();
              }
          },
          // 正常匹配事件的处理
          new PatternSelectFunction<Event, String>() {
              @Override
              public String select(Map<String, List<Event>> pattern) throws Exception {
                  ...
              }
          }
      );

  // 将正常匹配和超时部分匹配的处理结果流打印输出
  resultStream.print("matched");
  resultStream.getSideOutput(timeoutTag).print("timeout");
  ```

#### 处理迟到数据
+ Flink CEP 中沿用了通过设置水位线（watermark）延迟来处理乱序数据的做法。当一个事件到来时，并不会立即做检测匹配处理，而是先放入一个缓冲区（buffer）。缓冲区内的数据，会按照时间戳由小到大排序；当一个水位线到来时，就会将缓冲区中所有时间戳小于水位线的事件依次取出，进行检测匹配。这样就保证了匹配事件的顺序和事件时间的进展一致，处理的顺序就一定是正确的。这里水位线的延迟时间，也就是事件在缓冲区等待的最大时间。 
  - 。经处理匹配数据得到结果数据流之后，可以调用.getSideOutput()方法来提取侧输出流，捕获迟到数据进行额外处理。
  ```java
  PatternStream<Event> patternStream = CEP.pattern(input, pattern);
  // 定义一个侧输出流的标签
  OutputTag<String> lateDataOutputTag = new OutputTag<String>("late-data") {};
  SingleOutputStreamOperator<ComplexEvent> result = patternStream
        .sideOutputLateData(lateDataOutputTag) // 将迟到数据输出到侧输出流
        .select(
                  // 处理正常匹配数据
                  new PatternSelectFunction<Event, ComplexEvent>() {
                      ...
                  }
          );
  // 从结果中提取侧输出流
  DataStream<String> lateData = result.getSideOutput(lateDataOutputTag);
  ```
### CEP底层原理(状态机实现)
+ Flink CEP 中对复杂事件的检测，关键在模式的定义。我们会发现CEP中模式的定义方式比较复杂，而且与正则表达式非常相似：正则表达式在字符串上匹配符合模板的字符序列，而Flink CEP 则是在事件流上匹配符合模式定义的复杂事件。 
+ Flink CEP 的底层工作原理其实与正则表达式是一致的，是一个“非确定有限状态自动机”（Nondeterministic Finite Automaton，NFA）


# Flink部署
+ 组件：JobManager、TaskManager(任务管理器)、Client
+ 流程：Client提交任务给JobManager，JobManager将任务分发给TaskManager，
  TaskManager执行任务并返回结果给JobManager，JobManager收集结果并反馈给Client
+ 集群规划：1个JobManager(conf/maters)，3个TaskManager(conf/workers)
## 部署模式
+ 会话模式(Session Mode)：
  -  先启动集群，保持一个会话，集群一直都在。
  -  客户端再提交作业，共享集群资源，作业与作业之间相互独立，作业运行完成之后资源就被释放了。
  -  适合小作业、执行时间短的大量任务
+ 单作业模式(Per-Job Mode)：
  - 先提交作业，启动集群，作业运行完成，集群即关闭，作业与集群一对一。
  - **需要配合其他资源管理器使用，如yarn，最常用**
+ 应用模式(Application Mode)：
  - 先提交应用，启动集群，集群一直都在。
  - 应用于集群一对一。
## 应用模式部署
+ 应用模式下不会提前创建集群，所以不能调用 start-cluster.sh 脚本。我们可以使用同样在bin 目录下的 standalone-job.sh 来创建一个 JobManager。
- 进入到 Flink 的安装路径下，将应用程序的 jar 包放到 lib/目录下。
    \$ cp ./FlinkTutorial-1.0-SNAPSHOT.jar lib/
  - 执行以下命令，启动 JobManager。
    \$ ./bin/standalone-job.sh start --job-classname com.atguigu.wc.StreamWordCount
  这里我们直接指定作业入口类，脚本会到 lib 目录扫描所有的 jar 包。
  - 同样是使用 bin 目录下的脚本，启动 TaskManager。
    \$ ./bin/taskmanager.sh start
  - 如果希望停掉集群，同样可以使用脚本，命令如下。
    \$ ./bin/standalone-job.sh stop
    \$ ./bin/taskmanager.sh stop
## 本地模式&Flink部署(独立模式的会话模式)
+ 环境配置
  - Java8、hadoop2.7.5以上、配置集群时间同步、关闭防火墙、免密登录
  - Flink1.13.2
+ 进入 Flink 的安装路径下的 conf 目录下，修改配置文件: flink-conf.yaml，
  增加如下配置。
  ```
  high-availability: zookeeper
  high-availability.storageDir: hdfs://hadoop102:9820/flink/standalone/ha
  high-availability.zookeeper.quorum:
  hadoop102:2181,hadoop103:2181,hadoop104:2181
  high-availability.zookeeper.path.root: /flink-standalone
  high-availability.cluster-id: /cluster_atguigu
  ```
+ 修改配置文件: masters，配置备用 JobManager 列表。
  hadoop102:8081
  hadoop103:8081
+ 分发修改后的配置文件到其他节点服务器。
+ 在/etc/profile.d/my_env.sh 中配置环境变量
  - export HADOOP_CLASSPATH=`hadoop classpath`
  注意:
  - 需要提前保证 HAOOP_HOME 环境变量配置成功
  - 分发到其他节点
+ 具体部署方法如下：
  - 首先启动 HDFS 集群和 Zookeeper 集群。
  - 执行以下命令，启动 standalone HA 集群。
  \$ bin/start-cluster.sh
  - 可以分别访问两个备用 JobManager 的 Web UI 页面。
    http://hadoop102:8081
    http://hadoop103:8081
  - 在zkCli.sh 中查看谁是 leader。
    ```
      [zk: localhost:2181(CONNECTED) 1] get
      /flink-standalone/cluster_atguigu/leader/rest_server_lock
      杀死 hadoop102 上的 Jobmanager, 再看 leader。
      [zk: localhost:2181(CONNECTED) 7] get
      /flink-standalone/cluster_atguigu/leader/rest_server_lock
    ```
    注意: 不管是不是 leader，从 WEB UI 上是看不到区别的, 都可以提交应用。
### 作业提交
+ web页面提交
  -  提交jar包到集群运行即可，需设置执行入口、并行度、保存点等参数。
+ 命令行提交
  - 上传jar包到集群
  -  ./bin/flink rum -m hadoop102:8081 -c com.atguigu.flink.job.WordCount -p 2 ./flink-demo-1.0-SNAPSHOT.jar(-c：指定执行入口方法，-p：指定并行度)  


## yarn&Flink部署
+ flink1.8之前需要找到支持yarn的，同时需要去官网上找到对应的支持包上传到安装目录的lib目录下
### 环境配置
+ 配置环境变量，增加环境变量配置如下：
  这里必须保证设置了环境变量 HADOOP_CLASSPATH。
  ```
  $ sudo vim /etc/profile.d/my_env.sh
  HADOOP_HOME=/opt/module/hadoop-2.7.5
  export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
  export HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop
  export HADOOP_CLASSPATH=`hadoop classpath`
  ```
+ 修改 flink-conf.yaml 文件
  行 Standalone 模式配置的时候进行过讲解，若在提交命令中不特定指明，这些配置将作为默认配置。
  ```
  $ cd /opt/module/flink-1.13.0-yarn/conf/
  $ vim flink-conf.yaml
  jobmanager.memory.process.size: 1600m
  taskmanager.memory.process.size: 1728m
  taskmanager.numberOfTaskSlots: 8
  parallelism.default: 1
  ```
### yarn会话模式
+ YARN 的会话模式与独立集群略有不同，需要首先申请一个 YARN 会话（YARN session）来启动 Flink 集群
#### 启动集群
+ 启动 hadoop 集群(HDFS, YARN)。
+ 执行脚本命令向 YARN 集群申请资源，开启一个 YARN 会话，启动 Flink 集群。
  - $ bin/yarn-session.sh -nm test
    - -d：分离模式，如果你不想让 Flink YARN 客户端一直前台运行，可以使用这个参数，即使关掉当前对话窗口，YARN session 也可以后台运行。
    - -jm(--jobManagerMemory)：配置 JobManager 所需内存，默认单位 MB。
    - -nm(--name)：配置在 YARN UI 界面上显示的任务名。
    - -qu(--queue)：指定 YARN 队列名。
    - -tm(--taskManager)：配置每个 TaskManager 所使用内存。
  - 注意：Flink1.11.0 版本不再使用-n 参数和-s 参数分别指定 TaskManager 数量和 slot 数量，
+ YARN 会按照需求动态分配 TaskManager 和 slot。所以从这个意义上讲，YARN 的会话模式也不会把集群资源固定，同样是动态分配的。
+ YARN Session 启动之后会给出一个 web UI 地址以及一个 YARN application ID，如下所示，用户可以通过 web UI 或者命令行两种方式提交作业。
#### 作业提交
+ 通过 Flink web UI 提交作业
+ 通过命令行提交作业
  - 将 Standalone 模式讲解中打包好的任务运行 JAR 包上传至集群
  - 执行以下命令将该任务提交到已经开启的 Yarn-Session 中运行。
    ```
    $ bin/flink run -c com.atguigu.wc.StreamWordCount FlinkTutorial-1.0-SNAPSHOT.jar
    ```
    客户端可以自行确定 JobManager 的地址，也可以通过-m 或者-jobmanager 参数指定JobManager 的地址，JobManager 的地址在 YARN Session 的启动页面中可以找到。
  - 任务提交成功后，可在 YARN 的 Web UI 界面查看运行情况。

### 单作业模式
+ 在 YARN 环境中，由于有了外部平台做资源调度，所以我们也可以直接向 YARN 提交一个单独的作业，从而启动一个 Flink 集群。
+ 执行命令提交作业。
  - $ bin/flink run -d -t yarn-per-job -c com.atguigu.wc.StreamWordCount FlinkTutorial-1.0-SNAPSHOT.jar

  - 早期版本也有另一种写法： $ bin/flink run -m yarn-cluster -c com.atguigu.wc.StreamWordCount FlinkTutorial-1.0-SNAPSHOT.jar 注意这里是通过参数-m yarn-cluster 指定向 YARN 集群提交任务。
+ 在 YARN 的 ResourceManager 界面查看执行情况，如图 3-16 所示。

### 应用模式
+ 应用模式同样非常简单，与单作业模式类似，直接执行 flink run-application 命令即可。
+ 执行命令提交作业。
  ```
  $ bin/flink run-application -t yarn-application -c com.atguigu.wc.StreamWordCount FlinkTutorial-1.0-SNAPSHOT.jar
  ```
+ 在命令行中查看或取消作业。
  ```
  $ ./bin/flink list -t yarn-application -Dyarn.application.id=application_XXXX_YY
  $ ./bin/flink cancel -t yarn-application -Dyarn.application.id=application_XXXX_YY <jobId>
  ```
+ 也可以通过 yarn.provided.lib.dirs 配置选项指定位置，将 jar 上传到远程。
  
  ```
  $ ./bin/flink run-application -t yarn-application -Dyarn.provided.lib.dirs="hdfs://myhdfs/my-remote-flink-dist-dir" hdfs://myhdfs/jars/my-application.jar
  ```
  - 这种方式下 jar 可以预先上传到 HDFS，而不需要单独发送到集群，这就使得作业提交更加轻量了。
### 高可用模式
+ YARN 模式的高可用和独立模式（Standalone）的高可用原理不一样。Standalone 模式中, 同时启动多个 JobManager, 一个为“领导者”（leader），其他为“后备”（standby）, 当 leader 挂了, 其他的才会有一个成为 leader。而 YARN 的高可用是只启动一个 Jobmanager, 当这个 Jobmanager 挂了之后, YARN 会再次启动一个, 所以其实是利用的 YARN 的重试次数来实现的高可用。
+ 在 yarn-site.xml 中配置,注意: 配置完不要忘记分发, 和重启 YARN。
  ```
  <property>
    <name>yarn.resourcemanager.am.max-attempts</name>
    <value>4</value>
    <description>
      The maximum number of application master execution attempts.
    </description>
  </property>
  ```
+ 在 flink-conf.yaml 中配置。
  ```
  yarn.application-attempts: 3
  high-availability: zookeeper
  high-availability.storageDir: hdfs://hadoop102:9820/flink/yarn/ha
  high-availability.zookeeper.quorum:
  hadoop102:2181,hadoop103:2181,hadoop104:2181
  high-availability.zookeeper.path.root: /flink-yarn
  ```
+ 启动 yarn-session。
+ 杀死 JobManager, 查看复活情况。注意: yarn-site.xml 中配置的是 JobManager 重启次数的上限, flink-conf.xml 中的次数应该小于这个值。
###  K8S 模式
+ 容器化部署是如今业界流行的一项技术，基于 Docker 镜像运行能够让用户更加方便地对应用进行管理和运维。容器管理工具中最为流行的就是 Kubernetes（k8s），而 Flink 也在最近的版本中支持了 k8s 部署模式。基本原理与 YARN 是类似的，具体配置可以参见官网说明























