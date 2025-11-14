[toc]

***

# Spark3.X
+ 分布式集群中心化架构：主从架构（Master+Worker），批量离线处理框架
+ 功能组合在Driver端完成，后拆分为多个task，由Executor执行。
+ spark不支持文件操作，文件操作是有hadoop完成的。
+ spark基于MR开发，文件读取部分采用hdfs
+ 常用端口：内部通信：7077、查看任务：8080、历史服务器：18080
+ 资源配置的理解
  - data分区（并行度）
  - 数据倾斜（识别、解决（加盐（打散倾斜KEY））、预聚合、分离大key单独处理、广播join代替）
  - shuffle优化：此操作目的是节约珍贵的网络资源。
  - 内存管理：Executor内存划分，堆外内存
+ **spark shuffle优化**：
  - 资源扩充升级
  - 增加磁盘读写缓冲区
    - reduce端：spark.reducer.maxSizeInFlight：默认48M，可调大
    - map端：spark.shuffle.file.buffer：默认32k，可调大
  - 预聚合reduceByKey，此方法可在shuffle之前分区内预聚合（不影响最终结果情况下）
  - 吊装分区数：coalesce操作，比如240个map，我们合成60个map，也就是窄依赖。这样再shuffle，过程产生的文件数会大大减少
+ 基于RDD（弹性分布式数据集），RDD|仅读
  - RDD核心：创建环境用final变量保存，调用方法，关闭资源（不同于基于对象，无需用变量保存对象，因其仅使用一次）
  - 触发计算的是：action（行动）算子
  - sc.textFile(path):sc是SparkCTX对象，textFile是读取文件的方法，path是文件路径
  - 依赖关系：窄依赖（父RDD分区与子RDD分区一一对应）、宽依赖（父RDD分区与子RDD分区一对多）
  - 阶段：一个作业中的RDD计算流程，可被shuffle分开。
  - 任务：每个计划的执行计算单元。个数=阶段数
+ groupBy（shuffle，需要文件落盘）：打标记，用统一标记标记。（除此分区操作，其他数据处理操作后数据所在分区不变）
+ 任务管理器性能：插槽能放几个。
+ spark+hive：sparkSQL处理结构化数据，spark执行快开发难，hive执行慢开发简单。
    - 因hive更新速度过慢，产生了两条技术路线
      - spark on hive：SparkSQL：spark自己解析SQL转换RDD，hive仅做数据库使用
      - Hive on spark：hive解析SQL转换成MR任务spark执行：等待hive更新
+ **在yarn提交spark任务**，提交任务使用shell脚本
  ```
  bin/spark-submit   \
  --class com.atguigu.ad.spark.HiveToClickhouse \
  --master yarn   \
  ad_hive_to_clickhouse-1.0-SNAPSHOT-jar-with-dependencies.jar   \
  --hive_db ad   \
  --hive_table dwd_ad_event_inc \
  --hive_partition 2025-06-02   \
  --ck_url  jdbc:clickhouse://hadoop102:8123/ad_report   \
  --ck_table dwd_ad_event_inc   \
  --batch_size 1000
  ```
  + [yarn_spark_submit](Markdown\图片\spark_yarn提交任务流程图.png)
    - class：指定主类
    - master：指定提交到yarn集群
    - executor-cores : 每个executor使用的内核数，默认为1，官方建议2-5个
    - num-executors : 启动executors的数量，默认为2
    - executor-memory : executor内存大小，默认1G
    - driver-cores : driver使用内核数，默认为1
    - driver-memory : driver内存大小，默认512M 
+ 大数据开发原则
  - 数据量大，无关数据删除
  - 数据倾斜，识别、解决（加盐（打散倾斜KEY））、预聚合、分离大key单独处理、广播join代替
  - 缺什么数据不什么数据。
+ **数据倾斜**
  - 原因：shuffle数据分别不均匀、建表设计不合理（join出现null=0（默认值s））、数据本身不均匀
  - 识别：出现OOM、单个task占时过长等 、检测有shuffle的算子、 使用pairs对数数据采样分析
  - 解决：
    - 业务层：对大城市key进行拆分
    - 提高shuffle的并行度：调整reduce个数
    - 使用hive中间表进行预聚合操作
    - 两阶段聚合：先给每个key加一个随机数，再按key聚合，最后结果去掉随机数全局聚合
    - 将reduce join转为map join

## spark-modelel
+ spark-core：spark核心模块，包含RDD、SparkContext、任务调度等核心内容。
+ spark-sql：sparkSQL模块，包含对结构化数据的处理功能。
+ spark-streaming：sparkStreaming模块，包含对实时流数据的处理功能。
+ spark-mllib：sparkMLlib模块，包含机器学习算法库。
## RDD：数据模型
+ RDD：一定是**一个对象（final）**、封装属性和方法、适合分布式处理（分割数据（多个分区）、并行计算）
+ 多个RDD组成数据管道，采用修饰器模式，最终执行器执行复合的计算逻辑。
+ RDD（弹性分布式数据集），RDD|仅读
  - RDD核心：创建环境用final变量保存，调用方法，关闭资源（不同于基于对象，无需用变量保存对象，因其仅使用一次）
  - 触发计算的是：action（行动）算子
  - sc.textFile(path):sc是SparkCTX对象，textFile是读取文件的方法，path是文件路径
  - 依赖关系：窄依赖（父RDD分区与子RDD分区一一对应）、宽依赖（父RDD分区与子RDD分区一对多）
  - 阶段：一个作业中的RDD计算流程，可被shuffle分开。
  - 任务：每个计划的执行计算单元。个数=阶段数
+ RDD特性
  - 一组分区：数据集的基本组成单元表示数据是哪个分区的。
  - 一个计算函数：对每个分区进行计算。
  - RDD之间的依赖关系：依赖关系决定了数据计算的方向。
  - 一个partitioner：RDD的分片函数，控制分区的数据流向
  - 一个列表：保存每个partitioner的优先位置。（不匹配优先移动计算）
+ RDD类似数据管道，可以流转数据，但是不保存数据
+ RDD数据模型存在泛型，可封装任意类型数据，RDD处理方式与javaIO流一致，采用修饰器模式。
+ **惰性转换**：仅记录转换操作，不执行，直到遇到行动算子。
+ 编写spark代码时，调用转换算子仅是在Driver端组合功能不执行，真正执行是在Executor端，代码中的mian线程也称为Driver线程。
### RDD编程（方法名、IN、OUT）
+ **功能组合在Driver端完成（main线程称为driver线程），后拆分为多个task，由Executor执行。**
  - 在Excutor端使用到driver端创建的对象时（RDD方法中使用到的对象），该对象需要实现序列化接口，否则无法通过网络传输到Executor端，Excutor端无法使用。（`class student implements Serializable{}`）
  - JDK 1.8使用的对象模拟函数式编程，即创建一个对象，该对象包含一个方法，方法中封装了业务逻辑，该对象称为函数对象。
    - forEach(System.out::println)，相当于先创建一个System.out对象，再调用println方法
  - 若Executor端使用到Driver端数据，则需要将数量拉取到Executor端（以task为单位拉取）
+ 值类型
  - 单值：1、‘a'
  - 键值对：(1,2)
  - 元组的取值：t_1,t_2
  - JavaPairRDD<String, String> javaPairRDD = sc.parallelizePairs(Arrays.asList(new Tuple2<>("k", "v"), new Tuple2<>("k1", "v1"), new Tuple2<>("k2", "v2")));//创建元组，元素类型通过泛型指定
+ 当涉及数据库连接操作时
  - 使用foreachPartition代替foreach，在foreachPartition内获取数据库的连接。
+ 算子：
  - 转换算子
  - 行动算子
+ **函数式编程**
  ```java
  jsc
    .parallelize(Arrays.asList("hello", "spark"))
    .map(s -> s.toUpperCase())
    .collect()
    .forEach(System.out::println);
  ```
+ shuffle：数据重分区
  - shuffle可能导致数据倾斜，资源浪费
  - shuffle会将数据计算流程分为，一部分任务读磁盘，一部分任务写磁盘，在写操作完成前不允许读磁盘
  - RDD的分区与Task有关系，分区数=Task数
+ 示例
  ```java
  import org.apache.spark.SparkConf;
  import org.apache.spark.api.java.JavaRDD;
  import org.apache.spark.api.java.JavaSparkContext;

  import java.util.Arrays;
  import java.util.List;

  public class Test01_List {
      public static void main(String[] args) {

        // 1.创建配置对象
        final SparkConf conf = new SparkConf();
        conf.setMaster("local[*]");
        conf.setAppName("spark");

        // 2. 创建sparkContext
        final JavaSparkContext sc = new JavaSparkContext(conf);

        // 3. 编写代码
        final JavaRDD<String> stringRDD = sc.parallelize(Arrays.asList("hello", "spark"));

        final List<String> result = stringRDD.collect();

        for (String s : result) {
            System.out.println(s);
        }

        //将分区后的RDD保存到磁盘，每个分区一个文件
        result.saveAsTextFile("output");

        // 4. 关闭sc
        sc.close();
      }
  }
  ```
+ 环境准备：引入spark-core依赖：spark-core_2.12
  ```xml
  <dependency>
      <groupId>org.apache.spark</groupId>
      <artifactId>spark-core_2.12</artifactId>
      <version>3.3.1</version>
  </dependency>
  ```
  - 配置日志：在resources文件夹中添加log4j2.properties文件
  ```
  # Set everything to be logged to the console
  rootLogger.level = ERROR
  rootLogger.appenderRef.stdout.ref = console

  # In the pattern layout configuration below, we specify an explicit `%ex` conversion 
  # pattern for logging Throwables. If this was omitted, then (by default) Log4J would 
  # implicitly add an `%xEx` conversion pattern which logs stacktraces with additional 
  # class packaging information. That extra information can sometimes add a substantial 
  # performance overhead, so we disable it in our default logging config. 
  # For more information, see SPARK-39361. 
  appender.console.type = Console
  appender.console.name = console
  appender.console.target = SYSTEM_ERR
  appender.console.layout.type = PatternLayout
  appender.console.layout.pattern = %d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n%ex

  # Set the default spark-shell/spark-sql log level to WARN. When running the 
  # spark-shell/spark-sql, the log level for these classes is used to overwrite 
  # the root logger's log level, so that the user can have different defaults 
  # for the shell and regular Spark apps. 
  logger.repl.name = org.apache.spark.repl.Main
  logger.repl.level = warn
  logger.thriftserver.name = org.apache.spark.sql.hive.thriftserver.SparkSQLCLIDriver
  logger.thriftserver.level = warn

  # Settings to quiet third party logs that are too verbose 
  logger.jetty1.name = org.sparkproject.jetty
  logger.jetty1.level = warn
  logger.jetty2.name = org.sparkproject.jetty.util.component.AbstractLifeCycle
  logger.jetty2.level = error
  logger.replexprTyper.name = org.apache.spark.repl.SparkIMain$exprTyper
  logger.replexprTyper.level = info
  logger.replSparkILoopInterpreter.name = org.apache.spark.repl.SparkILoop$SparkILoopInterpreter
  logger.replSparkILoopInterpreter.level = info
  logger.parquet1.name = org.apache.parquet
  logger.parquet1.level = error
  logger.parquet2.name = parquet
  logger.parquet2.level = error

  # SPARK-9183: Settings to avoid annoying messages when looking up nonexistent UDFs in SparkSQL with Hive support 
  logger.RetryingHMSHandler.name = org.apache.hadoop.hive.metastore.RetryingHMSHandler
  logger.RetryingHMSHandler.level = fatal
  logger.FunctionRegistry.name = org.apache.hadoop.hive.ql.exec.FunctionRegistry
  logger.FunctionRegistry.level = error

  # For deploying Spark ThriftServer 
  # SPARK-34128: Suppress undesirable TTransportException warnings involved in THRIFT-4805 
  appender.console.filter.1.type = RegexFilter
  appender.console.filter.1.regex = .*Thrift error occurred during processing of message.*
  appender.console.filter.1.onMatch = deny appender.console.filter.1.onMismatch = neutral
  ```
+ 异常处理 
  - 果本机操作系统是Windows，在程序中使用了Hadoop相关的东西
    - 配置HADOOP_HOME环境变量
    - 在IDEA中配置Run Configuration，添加HADOOP_HOME变量
  - 权限不足：
    - 安装在windows上面的hadoop的bin文件夹中的hadoop.dll复制到C:\Windows\System32文件夹中
#### 创建RDD
+ 从集合中创建：sc.parallelize(Arrays.asList("hello", "spark"))
+ 从外部存储中创建：sc.textFile("path")，注意路径以项目路径为根，不是模块路径

#### 分区（**并行度**）
+ 优先级：方法参数 > 配置参数（conf） > 环境默认值 
  - 配置参数：conf.set("spark.default.parallelism", "5");**未配置时环境默认值**
  - 环境默认值：local[N]  N个分区，\*表示当前机器的核数个分区，yarn为虚拟核数。
  - 通常一核2、3个分区
+ 集合手动指定2个分区：sc.parallelize(Arrays.asList("hello", "spark", "hello", "spark", "hello"),2);
  - 分区左闭右开，多余放在最后一个分区
+ 文件： sc.textFile("input/1.txt",3);//填写的最小分区数3,和环境的配置分区数相比取小的值
  - 实际只需要看文件总大小/填写的分区数和块大小比较，谁小拿谁进行切分
  - 具体的分区数需要经过公式计算
    首先获取文件的总长度  totalSize
    计算平均长度  goalSize = totalSize / numSplits
    获取块大小 128M
    计算切分大小  splitSize = Math.max(minSize, Math.min(goalSize, blockSize));
    最后使用splitSize，按照**1.1倍原则**切分整个文件，得到几个分区就是几个分区（1.1：数据有多余若大小超过10%则分区数+1）
  - spark读取文件采用hdfs按行读取，读取位置以偏移量为单位计算。
+ RDD数据
  - 数据分区内有序，分区间无序，
  - 采用一个数据将所有的RDD执行完成，才处理下一个数据，可防止数据积压
+ **更改分区数方法：**
  - coalesce(N)：缩减分区数，没有shuffle
  - repartition(N)：更改分区数（扩大专用），**底层是coalesce，但会shuffle，效率低**
#### 单值转换算子：生成新RDD
+ 将旧RDD转换为新的RDD，组合多个RDD功能。
+ map(a->a*2)：对每一个元素进行操作
  ```java
  JavaRDD<String> mapRDD1 = lineRDD.map(new Function<String, String>() {
      @Override//String 传入的元素的泛型
      public String call(String IN) throws Exception {
          return IN + "||";
      }
  });
  ```
  - 采用匿名函数: a -> a + "||"
  + mapPartitions(a->a.map(b->b*2))：对每一个分区数据进行操作，一次处理一个分区的数据，输出是一个迭代器，将分区中所有数据加载到内存中，效率高可能OOM
  + mapPartitionsWithIndex((index, a)->a.map(b->index+"_"+b))：相当于多了分区号的mapPartitions，可用分区号对特定分区镜像操作，调试用
+  filter()：过滤， a -> a.length() == 5，注意过滤可能数据倾斜(可扩充分区数解决)
+ flatMap()：扁平映射，a -> Arrays.asList(a.split(" ")).iterator()，底层是迭代器、即做了扁平化又做了映射
+ groupBy():分组，a -> a.id%2 == 0 ：按id的奇偶分组
  - **底层是打上一个标记（return 组名），同标记在同一个组**
  - 需要重分区shuffle，一个分区中可以有多个组
  - Spark要求数据必须分组后才能进行后续操作，RDD不能保存数据，故shuffle需要数据落盘
+ disinct()：shuffle去重，需要落盘，效率低
  - hashset去重是将数据分在同一台机器内存中去重，而disinct()是shuffle去重，将数据分到不同机器内存中去重
+ sortBy(a->id,true)：shuffle排序，排序规则,是否降序,分区数量（默认与前面相同）
+ glom(): 将分区变成一个数组，用于查看数据的分布情况，快速诊断是否存在数据倾斜
  - eg：RDD.glom().map(partitionArray => partitionArray.length)
+ sample(false,0.5)：随机抽样，false：不放回，0.5：抽样比例
+ pipe()：管道，将RDD中的数据通过管道传递给脚本，返回脚本的输出结果
#### 双值类型转换算子：
+ union()：并集，去重
+ intersection()：交集，去重
+ subtract()：差集，去重
+ cartesian()：笛卡尔积，两个RDD的笛卡尔积，数据量会爆炸
#### K-V类型转换算子：
+ pairRDD = parlleizePairs(tuple2)：由元组创建K-V类型的RDD
+ mapToPair(a->(a.id,a))：将单值RDD转为K-V类型的RDD
+ mapValues(a->a*2)：对每一个元素进行map，只对value进行操作
+ groupByKey()：按key分组，返回K-V类型的RDD
+ sortByKey()：按key排序，默认true升序
+ reduceByKey((a,b)->a+b)：按K对V归约s，**具有预聚合操作**，返回K-V类型的RDD
  - reduceByKey(Integer::sum):归约求和，同样的可用max等
  - 分区规则默认为哈希分区，可用第一个参数指定
+ foldByKey(zeroValue,func)：提供分区聚合初始值的聚合 
+ combineByKey(CreateCombiner, MergeValue, MergeCombiner)：最通用的/最底层基于键的聚合算子
  - CreateCombiner：创建初始值，用于聚合，返回值类型与value类型相同
  - MergeValue：分区内聚合，返回值类型与value类型相同
  - MergeCombiner：分区间聚合，返回值类型与value类型相同
+ join：内连接，两个RDD的join，返回K-V类型的RDD
+ cogroup:全外连接，返回K-V类型的RDD
#### 行动算子：触发Job执行
+ spark任务流程：功能组合、封装数据位置在Driver端完成，后拆分为多个task，由Executor执行，再将Executor端的执行后的结果拉取到Driver端
+ 将数据流转起来，返回一个结果
+ collect()：获取结果，行动算子触发job执行，将Executor端的执行后的结果拉取到Driver端，将结果封装为集合对象。
  - 一次性拉取数据在生成环境，可能导致OOM，故慎用
+ count()：统计执行结果数量
  - countByKey()：统计每个key的数量，返回K-V类型的RDD
+ first()：获取第一个结果
+ take(N)：获取前N个结果，但是不排序直接取
+ takeOrdered(N)：按获取前N个结果，无需全局排序，每个分区排序后取前N个后在Driver端reduce
+ reduce()：对RDD中的所有元素进行归约操作，返回一个结果
+ aggregate((zeroValue: U)( seqOp: (U, T) => U, combOp: (U, U) => U))：
  - 自定义reduce，zeroValue所有分区聚合器初始值可以是元组，seqOp：分区内聚合函数，combOp：分区间聚合函数
  - aggregateByKey：使用Key
  - eg：RDD.aggregate((0,0.0))((a,b)->a+b,(a,b)->a+b)：求和
+ forEach()：遍历，执行操作，在Executor端执行
+ countByKey()：统计每个key的数量，返回K-V类型的RDD
+ saveAsTextFile("path")：将结果保存为文本文件
+ saveAsObjectFile("path")：将结果保存为对象文件
#### 其他算子
+ forEach()：遍历，执行操作
  - 在转换算子调用时为分别式调用
  - 在行动算子调用时为单点调用

### RDD_Serializable_Kryo
+ Java的序列化能够序列化任何的类，但占用空间大速度慢，spark使用Kryo序列化（提速10倍），当RDD在Shuffle时，简单数据类型、数组和字符串类型已经在Spark内部使用Kryo来序列化。
+ spark自己已经使用了Kryo序列化（DataFrames和DataSet），但自定义类需要手动注册，否则默认Java序列化
  ```java
  SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("sparkCore")
          // 替换默认的序列化机制
          .set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
          // 注册需要使用kryo序列化的自定义类
          .registerKryoClasses(new Class[]{Class.forName("com.atguigu.bean.User")});
  ```
### RDD依赖关系
+ 相邻RDD之间的依赖关系：窄依赖（上面RDD的数据由下游一个RDD独享）、宽依赖（shuffle导致，上面RDD数据被多个RDD共享）
+ 血缘关系：第一个RDD为根RDD，后续的RDD为子RDD，根RDD到子RDD的路径为血缘关系
+ 依赖关系与任务数量、阶段数量
  - 作业Job：由行动算子触发（ActiveJob），一个作业包含一个或多个阶段
  - 阶段Stage：一个RDD的计算流程，称为一个阶段，但若有shuffle，流程会将分开的每一段称为一个阶段，前一个阶段不执行完后一个阶段不允许执行，**阶段数=shuffle数+1**
  - 任务Task：每个Executor执行的计算单元，一个任务对应一个分区，任务数量= 每个阶段最后一个RDD分区数量之和
+ 移动数据不如移动计算，故尽量减少shuffle。（移动数据需要拉取数据）
### RDD持久化
### RDD序列化缓存
+ RDD通过Cache或者Persist方法将前面的计算结果缓存，默认情况下会把数据以序列化的形式缓存在JVM的堆内存中（计算节点的JVM，故仅有当前AppMast查看保存的RDD）。
+ spark中cache
  - DataFrame的cache默认采用 MEMORY_AND_DISK 
  - RDD 的cache默认方式采用MEMORY_ONLY
+ cache()：底层调用的就是persist方法,缓存级别默认用的是MEMORY_ONLY
+ persist(缓存级别)：保存数据
  - MEMORY_ONLY：仅在内存保存一份，MEMORY_ONLY_2:保存两份
  - MEMORY_ONLY_SER:序列化保存，MEMORY_AND_DISK:内存不够时保存到磁盘，MEMORY_AND_DISK_SER:序列化保存在内存内存不够时保存到磁盘，
+ RDD的缓存容错机制保证了即使缓存丢失也能保证计算的正确执行
  - 缓存丢失时，因分区之间独立，仅需计算丢失的分区即可
+ shuffle算子自带缓存以提升其性能
+ 使用完了缓存，可以通过unpersist()方法释放缓存
+ cache会在血缘关系中增加一条依赖关系。
#### RDD_Checkpoint
+ 数据长时间保存需要保证数据安全，故需要重新计算一次保证结果正确。
  - 注意：**先使用序列化缓存，再使用检查点，即可避免重复计算**。
+ 不同应用之间不可共享内存，故需要检查点，将数据保存到HDFS中
+ 应用
  - System.setProperty("HADOOP_USER_NAME","atguigu"); 设置Hadoop用户名，否则无法读取HDFS文件
  - jsc.setCheckpointDir("hdfs://hadoop102:8020/directory")：设置检查点目录,通常使用HDFS等高可用的文件系统
  - RDD.checkpoint()：调用检查点，以二进制文件保存
+ **检查点切断血缘：在Checkpoint的过程中，该RDD的所有依赖于父RDD中的信息将全部被移除**
  
### RDD分区器
+ 仅有K-V型数据有分区器，分区id从0开始
  - 支持哈希分区（默认）、轮询分区、用户自定义分区
+ 哈希分区：根据key的哈希值对分区数取模，得到分区id
+ 轮询分区：
+ 用户自定义分区(继承Partitioner类，重写getPartition、numPartitions方法)
  ```java
  class MyPartitioner extends Partitioner {
      private int numPartitions;
      public MyPartitioner(int numPartitions) {
          this.numPartitions = numPartitions;
      }
      @Override
      public int numPartitions() {
          return numPartitions;
      }
      @Override
      public int getPartition(Object key) {
          return key.hashCode() % numPartitions;
      }
  }
  ```
### 广播变量
+ 广播变量：将变量广播到Executor（默认以task为单位传输数据，广播更改为Executor为单位，需要封装变量）。
  - 用于向Executor端发送大量数据，减少数据传输量，提升性能
  ```java
  Broadcast<List<Integer>> max_id = jsc.broadcast(max_id);//广播变量

  max_id.value();//获取广播变量  
  ```

## spark SQL
+ Spark SQL是Spark结构化数据处理的模块，包括SQL、DataSet API
  - 兼容hive，支持JDBC
  - 实际是sparkCore的封装，数据读取是按行读取
+ spark+hive：sparkSQL处理结构化数据，spark执行快开发难，hive执行慢开发简单。
    - 因hive更新速度过慢（hive基于HD，HD不升级hive不升级），产生了两条技术路线
      - spark on hive：SparkSQL（Shark）：spark自己解析SQL转换RDD，hive仅做数据库使用（数仓）
      - Hive on spark：hive解析SQL转换RDD执行：等待hive更新 
+ 依赖
  ```xml
  <dependency>
      <groupId>org.apache.spark</groupId>
      <artifactId>spark-sql_2.12</artifactId>
      <version>3.3.1</version>
  </dependency>
  ```
+ 不同场景下模型的数据对象的使用
  ```java
  ds.as(Encoders.bean(User.class))//将ds中Row对象转为User类型的ds

  System.out.println(user.getName());//获取user中的数据

  class User implements Serializable {
    private String name;
  }
  ```
+ SparkSession(整合了旧的SQLContext和HiveContext)：是Spark SQL的入口，用于创建DataFrame、DataSet、执行SQL
+ 示例
  ```java
  public class Test01_Method {
      public static void main(String[] args) {

          //1. 创建配置对象
          SparkConf conf = new SparkConf();
          conf.setAppName("sparksql");
          conf.setMaster("local[*]");

          //2. 获取sparkSession
          SparkSession sparkSession = SparkSession
            .builder() //构建器模式，用于构建对象，
            .config(conf) //也可直接用.set设置参数，不配置conf
            .getOrCreate();

          //3. 编写代码
          // 按照行读取，对接文件数据将其封装为Row对象
          Dataset<Row> ds = spark.read().json("input/user.json");

          //使用sql操作
          ds.createOrReplaceTempView("user"); //将数据模型转换为表
          String sql = "select * from user where age > 20";
          final Dataset<Row> result = sparSession.sql(sql);
          result.show();

          //4. 关闭sparkSession
          sparkSession.close();
      }
  }
  ```
### 不同环境转换
+ sparkCore --> sparkSQL：new sparkSession(new sparkContext(conf))  
+ sparkSQL --> sparkCore ： 
  - sparkSession().sparkContext() //scala_core环境
  - new JavaSparkContext(sparkContext()) //java_core环境

### 模型对象
+ 转换Row对象为模型对象
  ```java
  ds.as(Encoders.bean(User.class))//将ds中Row对象转为User类型的ds

  System.out.println(user.getName());//获取user中的数据

  class User implements Serializable {
    private String name;
  }
  ```
+ 模型对象的访问
  - SQL：
  ```java
  //创建视图 => 转换为表格 填写表名，临时视图的生命周期和当前的sparkSession绑定，orReplace表示覆盖之前相同名称的视图
  lineDS.createOrReplaceTempView("t1");
  // 支持所有的hive sql语法,并且会使用spark的又花钱
  Dataset<Row> result = spark.sql("select * from t1 where age > 18");
  ```
  - DSL(一般不用)
  ```java
  Dataset<Row> result = lineRDD.select(col("name").as("newName"),col("age").plus(1).as("newAge")).filter(col("age").gt(18));
  ```
### 自定义函数
+ 用于自动函数，实现复杂逻辑，用于sql中（需要先注册udf().register）
+ UDF:一进一出：
  + sparkSession.udf.register("函数名",逻辑class{},返回类型);
    - 返回类型：DataType类型数据
      - 使用DataTypes.StringType
      - 或者使用scala语法操作，需要使用java访问scala对象的方式。eg：`StringType$$.MODULE$`
+ UDAF：多入一出，通常与groupBy一起使用
  - 底层需要一个缓冲区，存放中间结果。类似ruduce
  - **创建公共类继承org.apache.spark.sql.expressions.Aggregater类**
  ```java
  sparkSession.udf().register("avgAge",function.udaf(new MyAvg(),Encoders.LONG()));//因udf()不能注册udaf故需要unction.udaf转换一下

  //定义缓冲区
  public static class Buffer implements Serializable {
        private Long sum;
        private Long count;

        public Buffer() {
        }

        public Buffer(Long sum, Long count) {
            this.sum = sum;
            this.count = count;
        }

        public Long getSum() {
            return sum;
        }

        public void setSum(Long sum) {
            this.sum = sum;
        }

        public Long getCount() {
            return count;
        }

        public void setCount(Long count) {
            this.count = count;
        }
    }

    public static class MyAvg extends Aggregator<Long,Buffer,Double>{

        @Override
        //缓冲区初始化
        public Buffer zero() {
            return new Buffer(0L,0L);
        }

        @Override
        //缓冲区更新
        public Buffer reduce(Buffer b, Long a) {
            b.setSum(b.getSum() + a);
            b.setCount(b.getCount() + 1);
            return b;
        }

        @Override
        //缓冲区合并
        public Buffer merge(Buffer b1, Buffer b2) {

            b1.setSum(b1.getSum() + b2.getSum());
            b1.setCount(b1.getCount() + b2.getCount());

            return b1;
        }

        @Override
        //计算结果
        public Double finish(Buffer reduction) {
            return reduction.getSum().doubleValue() / reduction.getCount();
        }

        @Override
        //缓冲区编码器
        public Encoder<Buffer> bufferEncoder() {
            // 可以用kryo进行优化
            return Encoders.kryo(Buffer.class);
        }

        @Override
        //结果编码器
        public Encoder<Double> outputEncoder() {
            return Encoders.DOUBLE();
        }
    }
  ```
+ spark不支持UDTF

### 数据源
#### 文件源
+ 读取数据，支持JSON文件、CSV文件和列式存储(parquet)的文件
  ```java
  sparkSession.read()
    .csv("path") //读取csv文件,同理可替换json、parquet
    .option("sep",",") //设置分隔符
    .option("header",true) //设置第一行作为表头
  ```
  - 读取json数据时，因sql是core的封装，数据读取是按行读取，故json仅需行满足格式，无需整个文件都满足
  - 列式存储自带压缩
+ 写入数据
  ```java
  data.write()
    .csv("out_path") //写入csv文件,必须保证路径为空（否则要设置mode参数）
    .mode("append") //追加模式，可选参数：overwrite、append、ignore（忽略，存在不做不存在创建）、error（默认，存在则报错）  
  ```
#### hive
+ 可用内嵌hive，但企业开发用外部hive
+ Linux使用SQL
  - 添加MySQL连接驱动到spark-yarn的jars目录：cp /opt/software/mysql-connector-java-5.1.27-bin.jar /opt/module/spark-yarn/jars
  - 添加hive-site.xml文件到spark-yarn的conf目录：cp /opt/module/hive/conf/hive-site.xml /opt/module/spark-yarn/conf
  - 启动客户端： bin/spark-sql --master yarn
+ idea中使用
  - 配置
    ```XML
    <dependency>
        <groupId>org.apache.spark</groupId>
        <artifactId>spark-sql_2.12</artifactId>
        <version>3.3.1</version>
    </dependency>

    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>5.1.27</version>
    </dependency>

    <dependency>
        <groupId>org.apache.spark</groupId>
        <artifactId>spark-hive_2.12</artifactId>
        <version>3.3.1</version>
    </dependency>
    ```
  - 拷贝hive-site.xml到resources目录（如果需要操作Hadoop，需要拷贝hdfs-site.xml、core-site.xml、yarn-site.xml）
  - 设置用户名、添加hive支持
    ```java
    System.setProperty("HADOOP_USER_NAME","atguigu");//设置用户名
  
    SparkSession spark = SparkSession
        .builder()
        .enableHiveSupport()// 添加hive支持
        .config(conf)
        .getOrCreate();
    ```
#### mysql
+ 添加依赖
  ```XML
  <!-- 5.8(8.0)MySQL版本 -->
  <dependency>
      <groupId>mysql</groupId>
      <artifactId>mysql-connector-java</artifactId>
      <version>8.0.18</version>
  </dependency>
  ```
+ 实例
  ```java
  // 添加参数
  Properties properties = new Properties();
  properties.setProperty("user","root");
  properties.setProperty("password","000000");

  Dataset<Row> jdbc = spark.read()
    .jdbc("jdbc:mysql://hadoop102:3306/gmall?useSSL=false&useUnicode=true&characterEncoding=UTF-8&allowPublicKeyRetrieval=true", "test_info", properties);//读取数据

  jdbc.write()
    .jdbc("jdbc:mysql://hadoop102:3306/gmall?useSSL=false&useUnicode=true&characterEncoding=UTF-8&allowPublicKeyRetrieval=true", "test_write_info", properties);//写入数据
  jdbc.show();
  ```

## Spark Streaming
+ 用于流处理
  - source：kfk、flume、HDFS
  - 处理：map、reduce、join、window
  - Sink： HDFS 、DB 
+ 实时处理：毫秒延迟，离线处理：小时、天延迟，准实时：秒、分钟级延迟
+ DStream：离散化流，将流数据拆分成一个个小的批次，每个批次作为一个RDD（即每个时间段封装为一个RDD）
+ 流处理架构：
  - SockeData：数据接收器，将数据传输给流处理框架（一直工作）
  - StreamingContext（封装了core）：负责接收数据，并将数据分发给Executor
  - Executor：负责处理数据
+ foreachRDD()中，可以重用我们在Spark中实现的所有行动操作(action算子)
+ 依赖
  - 同样的使用kfk需要添加依赖：spark-streaming-kafka_
  ```xml
  <dependency>
      <groupId>org.apache.spark</groupId>
      <artifactId>spark-streaming_2.12</artifactId>
      <version>3.3.1</version>
  </dependency>

  <dependency>
      <groupId>org.apache.spark</groupId>
      <artifactId>spark-core_2.12</artifactId>
      <version>3.3.1</version>
  </dependency>
  ```

+ 控制每秒消费数据的速度：通过spark.streaming.kafka.maxRatePerPartition参数来设置Spark Streaming从kafka分区每秒拉取的条数
+ 背压机制：Spark Streaming会根据当前批次的处理速度来动态调整每个分区的数据拉取速度，以保持数据处理的稳定(spark.streaming.backpressure.enabled 参数设置为ture)
+ 优雅关闭流：把spark.streaming.stopGracefullyOnShutdown参数设置成ture，Spark会在JVM关闭时正常关闭StreamingContext，而不是立马关闭
+ 实例
  ```java
  JavaPairDStream<String, Integer> javaPairDStream = stringJavaDStream.mapToPair(new PairFunction<String, String, Integer>() {
      @Override
      public Tuple2<String, Integer> call(String s) throws Exception {
          return new Tuple2<>(s, 1);
      }
  });
  ```
###  DStream转换
+ 无状态转换：每个批次的数据相互独立，一个批次有多个RDD
  - map()：对DStream中的每个元素应用给定函数，返回由各元素输出的元素组成的DStream。
  - flatMap()：返回由各元素输出的迭代器组成的DStream
  - filter() 
  - mapToPair()：改变DStream的分区数，PairFunction<in, key, value>
  - reduceByKey()：将每个批次中键相同的记录规约，Function2<in, in, in>
  - groupByKey()：将每个批次中的记录根据键分组，ds.groupByKey()
+  WindowOperations<window_Length, slideInterval>： 基于对源DStream窗口的批次进行计算，返**回一个新的DStream**
  - 窗口时长：计算内容的时间范围，采集批次整数倍
  - 滑动步长：隔多久触发一次计算，采集批次整数倍
  ```java
  JavaPairDStream<String, Integer> window = javaPairDStream.window(Duration.apply(12000), Duration.apply(6000));
  window.reduceByKey(new Function2<Integer, Integer, Integer>() {
      @Override
      public Integer call(Integer v1, Integer v2) throws Exception {
          return v1+v2;
      }
  }).print();
  ```
+ reduceByKeyAndWindow(func, windowLength, slideInterval, [numTasks])：
  - 由(K,V)对的DStream上调用此函数，会返回一个新(K,V)对的DStream
  - 此处通过对滑动窗口中批次数据使用reduce函数来整合每个key的value值。

### DStream输出
+ saveAsTextFiles(prefix, [suffix])：以text文件形式存储这个DStream的内容。每一批次的存储文件名基于参数中的prefix和suffix。“prefix-Time_IN_MS[.suffix]”。每一批次写出一次，会产生大量小文件，在生产环境，很少使用。
+ rint()：在运行流程序的驱动结点上打印DStream中每一批次数据的最开始10个元素。这用于开发和调试。
+	**foreachRDD(func)**：通用操作，即将函数func用于产生DStream的每一个RDD。函数func应该实现将每一个RDD中数据推送到外部系统，如将RDD存入文件或者写入数据库。
+ foreachRDD(func)：mysql
  ```java
  resultDStream.foreachRDD(new VoidFunction<JavaPairRDD<String, Integer>>() {
      @Override
      public void call(JavaPairRDD<String, Integer> stringIntegerJavaPairRDD) throws Exception {
          // 获取mysql连接
          // 写入到mysql中
          // 关闭连接
      }
  });
  ```
### DStream关闭
+ 因为采集器会不断采集数据，所以需要手动关闭，kill太麻烦故使用使用外部文件系统来控制内部程序关闭
```java
//在行动算子前，开启监控
new Thread(new MonitorStop(javaStreamingContext)).start();

//当hdfs存在stopSpark文件时，关闭SparkStreaming
public static class MonitorStop implements Runnable {

    JavaStreamingContext javaStreamingContext = null;

    public MonitorStop(JavaStreamingContext javaStreamingContext) {
        this.javaStreamingContext = javaStreamingContext;
    }

    @Override
    public void run() {
        try {
            FileSystem fs = FileSystem.get(new URI("hdfs://hadoop102:8020"), new Configuration(), "atguigu");
            while (true){
                Thread.sleep(5000);
                boolean exists = fs.exists(new Path("hdfs://hadoop102:8020/stopSpark"));
                if (exists){
                    StreamingContextState state = javaStreamingContext.getState();
                    // 获取当前任务是否正在运行
                    if (state == StreamingContextState.ACTIVE){
                        // 优雅关闭
                        javaStreamingContext.stop(true, true);
                        System.exit(0);
                    }
                }
            }
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
```
## Spark内核及调优
+ Driver是一个线程。

### yarn模式提交流程
+ [spark_yarn提交任务流程图](图片\spark_yarn提交任务流程图.png)
### spark通讯架构
+ Driver对象：SparkConf、Sparkenv、SchedulerBackend <-- TaskScheduler <-- DAGScheduler
+ Executor对象：Driver_SchedulerBackend --> ExecutorBackend --> Executor --> ThreadPool
+ 通信框架Netty：环境NettyRpcEnv，类似邮件，互为客户端收发邮件

### Task任务调度执行
+ task执行流程：
  - job数量 = RDD行动算子数量
  - stage数量 = RDD依赖关系数量 = shuffle + 1
  - task数量 = 每一个阶段最后一个RDD分区数量之和
+ [stage任务划分](Markdown\图片\spark_stage任务划分.png)
+ [Task任务调度](Markdown\图片\spark_Task任务调度.png)
  - 放在ThreadPool池中，按FIFO调度（进入pool时先比较Job再比较阶段）

### Shuffle底层实现
+ SortShuffle(默认)：Task的数据先进行**归并排序**，后数据溢写入磁盘temp_flie保存每个Task合并自己的temp_flie，最后所有Task文件合并为一个file文件，同时以index文件记录每个task偏移量，用于后期读取。
  - 溢写：文件写入缓冲区，缓冲区满，溢写磁盘。
+ HashShuffle：Task的数据先进行哈希，后写入磁盘flie保存，同时以index文件记录每个task偏移量，用于后期读取。
  - 预聚合不可用，预聚合必须排序
  - 预聚合操作：必须排序、分区数量 <= 200（默认阈值）

### **Shuffle调优**
+ spark.reducer.maxSizeInFilght  此参数为reduce task能够拉取多少数据量的一个参数默认48MB，当集群资源足够时，增大此参数可减少reduce拉取数据量的次数，从而达到优化shuffle的效果，一般调大为96MB,，资源够大可继续往上调。

+ spark.shuffle.file.buffer  此参数为每个shuffle文件输出流的内存缓冲区大小，调大此参数可以减少在创建shuffle文件时进行磁盘搜索和系统调用的次数，默认参数为32k 一般调大为64k。


### Spark内存管理
+ java的内存管理：
  - 栈内存：方法执行时栈帧信息
  - 堆内存：程序执行时创建的对象（new、反射、clone、序列化）
  - 方法区内存：类的全部信息（反射）
  - **JVM 启动时占用1/64内存，最大占用1/4内存**

+ spark内存管理：
  - 堆内内存：JVM管理内存，程序在运行时动态地申请某个大小的内存空间
  - 堆外内存：直接向操作系统进行申请的内存，不受JVM控制，可控制。

+ 堆内存（动态内存但有默认比例）：
  - Storage(储存内存，30%)：保存数据（广播变量）
  - Execution(执行内存,30%)：计算（shuffle）
  - Othere(其他内存,40%)：spark对象等
  - 300M 预留内存：防止内存溢出
  - 动态内存管理机制：
    * 当一方内存不足时，动态占用另一方内存。
    * 动态占用：Execution优先即Excution可要求Storage归还占用的内存反之不行。（计算内存数据丢失结果不准，Storage内存数据丢失重新读取即可）

+ 堆外内存：
  - 堆内存有JVM管理，spark回收垃圾仅是标记了它是垃圾但是没有立即回收，所以堆内存回收不及时，所以使用堆外内存。
  - spark底层封装了堆内、堆外内存，统一管理，无需手动管理。 堆外内存管理需要手动控制，需要更高的编程水平。


## 部署
+ Local模式：在本地部署单个Spark服务
+ Standalone模式：Spark自带的任务调度模式。（国内不常用）
+ YARN模式：Spark使用Hadoop的YARN组件进行资源与任务调度。（国内最常用）
+ Mesos模式：Spark使用Mesos平台进行资源与任务的调度。（国内很少用）
### yarn-spark
+ 上传并解压安装包。
+ 配置环境变量
  - 修改并分发yarn-site.xml
  ```xml
  <!-- yarn-site.xml -->
  <!--是否启动一个线程检查每个任务正使用的物理内存量，如果任务超出分配值，则直接将其杀掉，默认是true -->
  <property>
      <name>yarn.nodemanager.pmem-check-enabled</name>
      <value>false</value>
  </property>

  <!--是否启动一个线程检查每个任务正使用的虚拟内存量，如果任务超出分配值，则直接将其杀掉，默认是true -->
  <property>
      <name>yarn.nodemanager.vmem-check-enabled</name>
      <value>false</value>
  </property>
  ```
  - 修改spark/conf/spark-env.sh,添加以下内容
  ```xml
  YARN_CONF_DIR=/opt/module/hadoop/etc/hadoop
  ```
  - 配置历史服务器：spark/conf/spark-defaults.conf
  ```
  spark.eventLog.enabled          true
  spark.eventLog.dir               hdfs://hadoop102:8020/directory
  ```
    - vim spark-env.sh
    ```
    export SPARK_HISTORY_OPTS="
    -Dspark.history.ui.port=18080 
    -Dspark.history.fs.logDirectory=hdfs://hadoop102:8020/directory 
    -Dspark.history.retainedApplications=30"
    ```
    - vim spark/conf/spark-defaults.conf
    ```
    spark.yarn.historyServer.address=hadoop102:18080
    spark.history.ui.port=18080
    ```