[toc]
***
# Hive(数据分析)
## hive基础
+ hive本质：Hadoop数据仓库工具，将结构化的数据映射为一张表。
+ 外部表：删除表时，元数据会被删除，但HDFS数据不会删除。
+ **元数据**：表名、表所属数据库（默认是default）、数据的类型、表的拥有者、列名、分区、表的类型（是否是外部表）、表的数据所在目录等。
+ 特点
  - Hive 处理的数据存储在 HDFS
  - Hive 分析数据底层的实现是 MapReduce
  - 执行程序运行在 Yarn 上
+ HQL工作流程：client上运行Driver，Driver将元数据和HQL编写为MapRedus任务
+ Driver驱动器工作流
  - 词法分析：生成语法树AST
  - 语法分析：根据AST判断有无语法错误
  - 逻辑计划生成：
  - 逻辑计划优化：
  - 物理计划生成：
  - 物理计划优化：
  - 执行：
+ hive特点：
  - 利用集群计算，擅长处理大数据
  - 针对数仓设计，读多写少，不建议对数据进行修改。
  - HiveQL与SQL语法类似，容易上手
  - 执行延时较高，不适用于实时查询，常用与数据分析。
  - hive执行效率较低，因生成的MapReduce不够智能，且因hive颗粒度较大调优困难。
+ hive使用
  - -e：非交互式执行“HQL”，hive -e "select * from table_name"
  - -f：执行“HQL”文件，hive -f /opt/module/hive/data/hive.sql
  - hive> set mapreduces.job.reduces=10//设置reduce个数,在本次运行起效。
+ hive服务启停：cd $HIVE_HOME/
  ```
  - 启动：可加nohup让其在后台运行
  bin/hive --service metastore
  bin/hive --service server2

  bin/hive --service stop metastore
  bin/hive --service stop server2
  ```
### **hive运行模式**
+ 本地模式：MapReduce运行在同一主机同一节点上，的同一进程，适用于测试环境。
  - 通过设置mapreduce.framwork.name=local覆盖掉运行与yarn的配置，临时开启本地模式。
+ 默认模式：MapReduce运行在yarn上。
### hive架构
+ hiveservers：提供db访问和用户认证服务
  - 当同时配置JDBC和hiveserver2时，会直接访问hiveserver2，而不会访问JDBC。
+ Metastore：为cle或server提供元数据访问接口，元数据通常保持在本地数据库
  - 运行模式（通过hive-site.xml配置）：
    - 内嵌模式：元数据存储在Hive自带的Derby数据库中，仅能一个客户端连接，适用于测试环境。**即配置JDBC(JDBC_URL、Driver、user、passwd)**
    - 独立服务模式：元数据存储在远程的MySQL数据库中，可支持多用户连接，**适用于生产环境**，需要远程连接的client删除JDBC配置**添加服务器主机、端口、metasort服务器地址**的core-site.xml配置。
+ client：CLI命令端和JDBC/ODBC
### hive最小化安装
+ hive最小化安装
  - 上传合适安装包，设置Linux环境变量并刷新。
  - 解决日志jar包冲突：mv `$HIVE_HOME/lib/log4j-slf4j-impl2.10.0.jar $HIVE_HOME/lib/log4j-slf4j-impl-2.10.0.bak`
+ 安装适合mysql-5.7.28-1.el7.x86_64（需提前卸载自带MySQL）
  - rpm -qa | grep mariadb //查看是否安装过MySQL
  - rpm -e --nodeps mariadb-libs
  - 安装需要的MySQL服务（存在依赖必须顺序安装）
    - common、libs、compat、client、server
    - sudo rpm -ivh （在上传的/opt/software下）
+ MySQL配置
  - 查看/etc/my.cnf中的datadir路径，删除该路径下的所有文件。
  - 初始化MySQL：sudo mysqld --initialize --user=mysql
  - 查看临时密码：cat /var/log/mysqld.log的末尾host：12&ss
  - 启动MySQL服务：sudo systemctl start mysqld
  - 登录MySQL：mysql -uroot -p'临时密码'
  - 修改密码：set password=password('root');//root为修改后的密码
  - 设置root用户允许任何IP登录：> update mysql.user set host='%' where user='root';
  - 刷新权限：flush privileges;
  - 修改配置：vim core-site.xml，重启集群
+ hive配置
  - 驱动拷贝：cp /opt/software/mysql-connector-java-5.1.37.jar $HIVE_HOME/lib
  - 修改hive-site.xml，设置元数据采用MySQL存储
  - 登录MySQL，创建hive数据库：create database metastore;
  - 初始化hive元数据库：$HIVE_HOME/bin/schematool -initSchema -dbType mysql -verbose
  - 启动hive：bin/hive
  - **修改hive-site.xml后应重启服务**
  -  jps | grep HiveMetaStore //检查是否启动成功
#### 安装错误解决
+ hive执行HQL报错：FAILED: HiveException java.lang.RuntimeException: Unable to instantiate org.apache.hadoop.hive.ql.metadata.SessionHiveMetaStoreClient
  - 表明： Hive 在尝试连接元数据库（Metastore）时发生了异常，通过检测Metastore日志，发现是Metastore未正确初始化。
  - schematool -dbType mysql -dropSchema//删除元数据库
    schematool -dbType mysql -initSchema//初始化元数据库
### hive 常见配置
#### hive日志配置
+ 默认日志位置：$HIVE_HOME/logs/hive.log
+ 修改日志位置：vim $HIVE_HOME/conf/hive-log4j.properties.template
  - mv hive-log4j.properties.template hive-log4j.properties
  - property.hive.log.dir=$HIVE_HOME/logs/hive.log
#### hive命令行客户端配置
+ 显示当前使用数据库：vim hive-site.xml，hive.cli.print.header=true;hive.cli.print.current.db=true
#### JVM堆内存设置
+ 原因：默认堆内存256MB，当开启小任务本地运行优化时，任务会超出默认堆内存，导致任务失败。
+ 修改：vim $HIVE_HOME/conf/hive-env.sh
  - mv hive-env.sh.template hive-env.sh
  - 修改：export HADOOP_HEAPSIZE=1048
#### hive虚存检测关闭
+ 原因：默认虚存检测开启，当内存不足时，会优先使用虚存，导致任务失败。
  - vim yarn-site.xml,yarn.nodemanager.vmem-check-enabled=false
# hive数据库
## hive-DDL
+ create database [if not exists] db_name [comment 'db_comment'] [location hdfs-db_path][with dbproperties (key1=value1,key2=value2)];**多location可指定DB储存位置,k:v可修改其他信息**
+ show databases [like 'db_name'];//查看数据库
+ desc database [extended] db_name;//查看数据库详情,extended可查看其他信息
### DB_ALT
+ alter database db_name set dbproperties (key1=value1,key2=value2);//修改数据库属性
+ alter database db_name set location hdfs-db_path;//修改数据库存储位置
+ alter database db_name set owner user_name;//修改数据库所有者
+ drop database [if exists] db_name [restrict|cascade];//删除数据库,restrict:如果数据库中有表，则删除失败，cascade:级联删除
## hive-DML
### 创建表
+ create [temporary] [external] table [if not exists] da_name(col_name data_type,……) [comment] [partitioned by [comment clo_comment],……] [clustered by (col_name,……)] [sorted by (col_name [asc|desc],……)] [into num_buckets buckets] [row format] [stdored as] [location hdfs_path] [talpropreties (property_name=property_value,……)]
+ create table …… as select……;//根据查询结果创建表,但**不允许选择external参数**
+ create table …… like ……;//根据已有表结构创建表,可指定外键等
#### **参数说明**：
+ external：外部表hive仅保存元数据，相应的内部表hive保存元数据和HDFS数据。
+ row format:指定序列化和反序列化参数,指定行解析方式，**核心参数**
  - row format:指定序列化和反序列化参数
    - delimited关键字：DELIMITED [field terminated by char] [collection terminated by char] [map keys terminated by char] [lines terminated by char] [null defined as char] //指定分隔符，依次为列、items、map-k-v、行分割符，用于SERDE(反、序列化操作)
    - SERDE关键字：指定已定义的SERDE如JSON SERDE,如：serde serde_name with parameters (key1=value1,key2=value2,……)
+ stdored as:指定存储格式即文件读取格式默认textfile，**核心参数**
  - sequencefile:二进制文件，可压缩，可分割，可并行读取，
  - rc :列式存储，可压缩，可分割，可并行读取
  - parquet ：列式存储，可压缩，可分割，可并行读取，
+ talpropreties (property_name=property_value,……):配置表的k-v属性。
+ partitioned by:指定分区表(指定不同字段，相同字段数据放在同一位置)
+ clustered by 字段 sorted by 字段 into…… buckets:指定分桶表(将hive表分散到不同的文件中)，根据字段进行哈希决定位置。
+ sorted by:指定排序表
#### 分区表(数据按日期分区处理)
+ 将一个表按需分配到多个目录储存一个目录称为一个分区，查询时通过where分区字段过滤数据，提高查询效率。（分区可嵌套分区）
+ 创建：通过partitioned by指定分区字段
+ 增、减分区：alter table tb_name add partition(day='2024-11-30 18:46:38')，或alter table tb_name add partition(day='2024-11-30 18:46:38') partition(day='2024-11-30 18:46:39')一次增加多个，删除换drop**特别的删除多个时有，号隔开**
+ 写入数据：
  - load data [path] into table tb_name partition(day='2024-11-30 18:46:38')
  - insert into table tb_name partition(day='2024-11-30 18:46:38') select……
+ 查询：可作为一个伪字段来查询分区字段，也可用where day='2024-11-30 18:46:38'进行分区过滤查询。
+ 分区信息修复：原因：分区信息保存在元数据中，仅有hdfs上路径与元数据上路径一致才可读取，当手动修改分区路径会导致不一致错误
  - msck repair table tb_name [add/drop/sync partitions]修复，sync为同步。
+ **多级分区**：partitioned by(day='20240401' and hour='12')//day为第一级分区，hour为第二级分区。(此应用场景为：数据需要按12h处理一次)
+ 动态分区：在插入数据时，根据每行数据最后一个字段的值自动创建分区，需开启动态分区默认开启(hive.exec.dynamic.partition)
  - 严格模式：hive.exec.dynamic.partition.mode=strict(默认)，需要至少有一个分区为静态分区。=nonstrict非严格模式允许所有分区为动态分区。
  - insert语句创建最大分区数：hive.exec.max.dynamic.partitions.pernode=1000
  - 单条insert可创建文件数：hive.exec.max.created.files=1000
  - 单个map或reduce任务最大分区数：hive.exec.max.dynamic.partitions.pernode=1000
  - 查询结果为空且进行动态分区是否报错：hive.error.empty.result.set=false(默认)
#### 分桶表(mapreduce优化)
+ 将一张表根据字段哈希值取模后分散存储到不同文件中，利用哈希值提高查询效率类似字典形式。
+ 创建:clustered by 分桶字段 into 桶数 buckets
+ 写数据：无特殊
+ 分桶排序表创建：clustered by 分桶字段 buckets sorted by 排序字段 asc|desc into 桶数//分桶和排序字段可以不唯一


### data_type:
|dataType|REAMD|定义|
|:--|:--|:--|
|tinyint	|1byte有符号整数|
|smallint|	2byte有符号整数|
|int	|4byte有符号整数|
|bigint	|8byte有符号整数|
|boolean|	布尔类型，true或者false|
|float	|单精度浮点数|
|double	|双精度浮点数|
|decimal|	十进制精准数字类型|decimal(16,2)|
|varchar|	字符序列，需指定最大长度，最大长度的范围是[1,65535]|varchar(32)|
|string	|字符串，无需指定最大长度|
|timestamp|	时间类型|
|binary	|二进制数据|
|array|array<data_type>|arr[0]取值|
|map|map<string,int>|map[k]|
|struct|struct<id\:int,name\:string>|struct.id|

#### json
+ web前后端数据交互，有数组[]、对象{}、单体a三种数据结构。
  - 数组：[1,2,3,4],$.[2]取值,可嵌套
  - 对象：{"name":"zhangsan","age":18}，$.[0]:'name'取值，可包含任何数据类型。
+ json数据解析：get_json_object(json_string,json_path)
  - $:解析对象
  - .：'name'：解析对象name属性
#### array
+ array(1,2,3,4,5)；//创建数组，通常function(array(),……)使用
+ array_contains(array,clo)：判断数组中是否包含clo
+ sort_array(array)：对数组排序
+ size(array)：获取数组长度
#### map
+ map('name','zhangsan','age',18)//创建map
+ map_keys(map)：获取map的所有key
+ map_values(map)：获取map的所有value
#### struct
+ struct\<val1,val2,val3>：以值创建struct，默认对应为col1,col2,col3
+ name_struct\<name:age,age:18>：键值对创建struct


### 查看与修改、插入、删除和清空
#### 查看
+ show table [in db_name] tb_name;
+ show tables like 'stu';
+ desc [formatted] db|tb;//formated格式化显示数据库创建信息
#### 修改字段
+ **修改的仅是元数据，对HDFS上的数据无修改，类型修改时默认修改前后类型需要兼容，但可通过hive.metastore.disable.partitions=true忽略类型不兼容错误。**
+ alter table tb_name rename to new_tb_name;//修改表名
+ alter table tb_name add columns (col_name data_type,……);//添加列
+ alter table tb_name change old_col_name new_col_name data_type [after|first col_name];//修改列名和类型,after|first指定位置
+ alter table tb_name replace columns (col_name data_type,……);//替换所有列
#### 插入
+ 数据插入：insert into|overwrite table tb_name partition (partition_name=partition_value) [values(1),(2)|select……];//overwrite覆写数据。
+ 查询数据写入目标路径：insert overwrite [local] directory 'hdfs_path' [row format] [stored as] [select……];//将查询结果写入指定路径
  - local：写入本地路径，**仅可覆写不可追加**
#### 删除or清空
+ drop table [if exists] tb_name;//删除表
+ truncate table tb_name;//清空内部表数据
### hive数据的加载与备份
+ load data [local] inpath 'filepath' [overwrite] into table tablename [PARTITION (partcol1=val1, partcol2=val2 ...)];
  - local：从本地上传(cp-file)，默认从HDFS上传(mv-file)
  - overwrite：覆写数据**谨慎操作**
  - partition：指定分区
+ export table tb_name [partition (partcol1=val1, partcol2=val2 ...)] to 'hdfs_path';//将表数据(**元数据和HDFS数据**)导出到HDFS
+ import [external] table new_tb_name from 'source_paht' [location 'import_target_path'] ;//将**使用exprot导出**的表数据导入到hive
  - external：导入外部表
  - location：指定导入路径,from指定源数据路径。
### 数据查询HQL 
+ 相对SQL新增[cluster by clo_list ] [distribute by clo_list] [sort by clo_list]
+ **hive2.x**支持join但仅仅支持等值连接，不支持非等值连接。 (**即连接条件即可为a.id=b.id,不可为a.id>b.id**)
+ hive 支持left join、right join、full join(全连接)、笛卡尔积、union(去重)、union all(不去重，表拼接)、
  - hive join实现：针对每一个join生成一个mapreduce任务。
+ order by：全局排序，asc|desc
  - limit 3：可解决的N名问题，同时降低ruduce压力，map阶段会进行优化如需要5条数据，每个map仅返回5条给reduce端。
  - **在生产环境需谨慎全局排序无limit操作，可能会导致性能问题**
+ 三个by
  - sort by：指定排序字段，map到reduce排序使得reduce有序
  - distribute by：指定分区字段
  - cluster by：指定分区和排序为同一字段
#### function
+ show function
+ desc function extend//查看函数体
+ array()//数组
##### 流程控制
+ if(a>b,1,0)//a>b返回1否则返回0
+ case
    when score>90 then 'A' 
    when score>70 then 'B'
    else 'D'
  end 
  from select score from tb_name;
#### 常用函数
+ 算数运算
  - ~A:对A取反
  - round(a,b)//a取b位且四舍五入
  - ceil()//向下取整
  - floor()//向上取整
  - cast(a as data_type)//类型转换
+ 字符函数
  - substring(str,[a],int b)//可从a开始截取B个字符，默认从第一个字符开始截取
  - replace(str,a,b)//将字符串中a全替换为b
  - regexp_replace(a,re,c)//将符合re表达式的全替换为c
  - split(str,re)//以re切割字符串。
  - nvl(vul1,vulgar2)//若vul1非空返回vul1，否则返回vul2，用于设置默认值。
  - concat_ws(sep,array(str1,str2))//以sep分隔符连接数组中的字符串
+ 日期函数
  - unix_timestamp(time,'yyyy/mm/dd HH-MM-SS')//获取指定时间的unix时间戳
  - format_unix_timestamp(unix_timestamp,'GMT+8')//将unix时间戳转换为指定时区的时间
  - from_unixtime(unix_timestamp,'yyyy/mm/dd HH-MM-SS')//将unix时间戳转换为指定格式的utc时间
  - date_format(date,'str_format')//将指定日期转换为指定格式
  - current_date//获取当前时间
  - current_timestamp//获取当前时间戳
  - moth(time)获取指定时间月份、year()、day()、hour()、minute()、second()
  - datediff(date1,date2)//获取date1与date2相差的天数
  - date_add(date,int)//获取date加上int天后的日期，int可为负数，date_sub为减。
#### 聚合函数
+ count()、sum()、avg()、max()、min()
+ collect_list()//指定列以数组返回
+ collect_set()//指定多列以集合返回
#### UDTF(制表)函数(1进n出)
+ select explode(array(1,2,3)) as item;//将数组中元素拆为item列中的三行
+ select explode(map('a',1,'b',2)) as (key,value);//将map中元素拆为key、value两列
+ select posexplode(trans_array) as (pose,value);//将trans_array中元素拆为pose列数、value两列
+ inline(array(struct())) as ()//将结构体数组中元素拆为多列，一个结构体一行。
##### Lateral View
+  与UDTF联合使用，用于将UDTF的生成列与原表进行join生成新的虚拟表。
+  select name,hobbies,hobby 
    from person lateral view explode(hobbies) tmp_tb as hobby(生成字段名);
#### 窗口函数
+ 每行数据划分一个窗口，并用窗口函数对每个窗口进行计算并返回。
+ select id,name
    function(计算函数) over(计算范围) as total_amount
  from tb_name;
##### 窗口定义
  + 基于行：eg：求前n行到当前行， over(order by IDrows between [unbounded preceding|num preceding|current row|num following] and [])
    - unbounded preceding：窗口开始于第一行，unbounted无穷行
    - num preceding：窗口开始于当前行前num行
    - current row：窗口开始于当前行
    - num following：窗口开始于当前行后num行
    - **hive必须配合order by用，因mapreduce计算会切分数据块，使得表中数据条顺序与实际不同**
  + 基于值：eg：求值位于当前值减1到当前值之间的行，over(range between [同上] and [同上])
    - **同时在hive中必须配合order by使用**
##### window_function
+ 聚合函数：sum()、avg()、max()、min()、count()……
+ 偏移函数：
  - lead(字段名,n,default)、lag()//lag()获取当前n行数据,default为默认值,lag()为后N行，**不支持自定义窗口函数**
  - first_value(order_data,false)、last_value()//获取窗口第一行、最后一行的值,false为不忽略空值
+ 排名函数(**不支持自定义窗口**)：
  - row_number()、rank()、dense_rank()//row_number()为不重复排名，rank()为有并列排名，dense_rank()为有并列且连续排名
+ 自定义函数
  - UDF(一进一出)
    - eg:自定义xxx功能->创建maven项目->导入org.apache.hive>hive-exec>3.1.3依赖 ->创建类->打包上传jar包(add jar)->添加到classpath临时有效->创建临时函数并关联到jar包（create temporary function my_len as "com.atguigu.hive.udf.MyUDF";）
    - 也可创建永久函数：create function my_len as "com.atguigu.hive.udf.MyUDF" using jar "hdfs://hadoop102:8020/udf/my_len.jar";永久函数在其他数据库使用时需要使用库名.函数名
  - UDAF(多进一出)
  - UDTF(一进多出)

## 文件格式和压缩
+ hive底层为hadoop故压缩方式与hadoop相同。

|压缩格式|算法|拓展名|是否可切分|解码器|
|:---|:---|:---|:---|:---|
|deflate|deflate|.deflate|否|org.apache.hadoop.io.compress.DefaultCodec|
|gzip|deflate|.gz|否|org.………….GzipCodec|
|bzip2|bzip2|.bz2|是|org.…………BZip2Codec|
|lzo|LZO|.lzo|是|org.…………LzopCodec|
|snappy|snappy|.snappy|否|org.…………SnappyCodec|
### hive文件格式(stored as指定)
+ TextFile：默认格式，文本文件，行行对应。(数据整行读取)
+ ORC：列式存储，数据按列存储，每行数据由一列组成。(数据读取整列)
  + ORC文件由stripe(index Data，column1,...,Stripe Footer)、footer()、postscript()三部分组成，将行划分为多个块再进行列式存储,
    -文件头以header：ORC标识
    - stripe(index Data(索引数据记录max、min、行位置),Stripe Footer行编码信息)
    - file footer保存stripe起始位置、索引长度、数据长度、stripe footer长度和各column 统计信息max、min、hasNull等信息。 
    -  Postscript：保存File Footer的长度、版本号、压缩参数、Postscript的长度(文件最后一个字节保存)
    - 创建：stored as orc tblproperties (property_name=property_value, ...)，
    可指定参数：orc.compress=SNAPPY/ZLIB/NONE(压缩格式),orc.compress.size=262144(压缩块大小通常与stripe大小相同),orc.stripe.size(stripe大小),orc.row.index.stride=10000(每10000行记录索引)
+ Parquet：列式存储，
  + Parquet文件row group、Footer、PAR1组成
    - row group：由多个column chunk组成，每个column chunk保存一列数据，每个row group包含一定行数，默认为10000行，称为一页
    - Footer：保存文件元数据信息，每个row group的元数据信息对应一个Meta data（数据类型、编码、数据位置、统计信息）
    - PAR1：文件开头和结尾各一个，保存文件版本信息（4bit），文件结尾PAR1前以固定字节保存footer长度。
    - 创建：stored as parquet tblproperties (property_name=property_value, ...)，parquet.compression=SNAPPY/ZLIB/BROTLI/UNCOMPRESSED(压缩格式), parquet.page.size=262144(压缩块大小，通常与HDFS大小相同),parquet.dictionary.page.size=262144(页大小)
### 压缩
+ 压缩提高对磁盘空间的利用和查询性能，降低IO。
#### hive表中的压缩
+ TextFile：文本文件，默认格式，读取自动压缩，写数据需设置：set hive.exec.compress.output=true;  set mapreduce.output.fileoutputformat.compress.codec=org.apache.hadoop.io.compress.SnappyCodec;
+ ORC、parquet：建表时设置压缩格式即可。
#### hive计算中的压缩
+ 设置mapreduce的shuffle阶段压缩：set mapreduce.job.reduce.input.compress=true; set mapreduce.job.reduce.input.compress.codec=org.apache.hadoop.io.compress.SnappyCodec;
+ 设置多个map的中间数据压缩：set hive.exec.compress.intermediate=true; set hive.intermediate.compression.codec=org.apache.hadoop.io.compress.SnappyCodec;
# hive性能调优
+ explain select * from table_name; 查看执行计划
+ explain formatted select * from table_name; 查看执行计划，格式化输出
## hive计算资源调优
+ 主要是yarn和mapreduce的配置
  - Namenode中一个容器的内存：yarn.nodemanager.resource.memory-mb
  - namenode中一个容器的CPU：yarn.nodemanager.resource.cpu-vcores
+ 容器相关
  - 容器最小内存：yarn.scheduler.minimum-allocation-mb
  - 容器最大内存：yarn.scheduler.maximum-allocation-mb
+ map task相关
  - 单个Map Task申请的container容器内存大小：mapreduce.map.memory.mb
  - 单个Map Task申请的container容器CPU核数：mapreduce.map.cpu.vcores
+ reduce task相关
  - 单个Reduce Task申请的container容器内存大小：mapreduce.reduce.memory.mb
  - 单个Reduce Task申请的container容器CPU核数：mapreduce.reduce.cpu.vcores
## hive任务优化
### 分组聚合优化Map
+ map-side聚合：
  - set hive.map.aggr=true; 开启map端聚合，默认为true
  - set hive.groupby.mapaggr.checkinterval=100000; map端聚合的测试行数，默认为100000，通过运行测试行数判断是否map段输出是否减少到固定比例，如果减少则开启map端聚合。
  - set hive.map.aggr.hash.min.reduction=0.5; map端聚合的最小比例，默认为0.5，map输出减少到此比例开启聚合。
  - set hive.map.aggr.hash.force.flush.memory.threshold=0.9; map端聚合的内存阈值，默认为0.9，当map段聚合内存使用达到此比例时，强制聚合输出，即刷新map内存。（这也是导致100组，而map输出103组的原因）
+ common join默认连接：
  - 多表连接且连接字段相同时，可合并为一个mapreduce任务，自动进行。
+ map join优化：
  - 大小表连接，小表制成哈希表传到HDFS，每个 map task加载哈希表到内存上，大表分布式存储，读取进行连接。
+ Bucket Map Join优化
  - 保证参与join的表均为分桶表，且关联字段为分桶字段，且其中一张表的分桶数量是另外一张表分桶数量的整数倍
  - map段保存保存分桶字段即可，无需缓存整个小表
+ Sort Merge Bucket Map Join（SMB join）
  - 要求，参与join的表均为分桶表，且需保证分桶内的数据是有序的，且分桶字段、排序字段和关联字段为相同字段，且其中一张表的分桶数量是另外一张表分桶数量的整数倍。
  - 创建分桶字段时，仅需创建部分字段，即较少数据到达的字段，因其有序无需全创建。
+ map设置采用的join优化
  - 启动Map Join自动转换：set hive.auto.convert.join=true;
  - 一个Common Join operator转为Map Join operator的判断条件,若该Common Join相关的表中,存在n-1张表的已知大小总和<=该值,则生成一个Map Join计划,此时可能存在多种n-1张表的组合均满足该条件,则hive会为每种满足条件的组合均生成一个Map Join计划,同时还会保留原有的Common Join计划作为后备(back up)计划,实际运行时,优先执行Map Join计划，若不能执行成功，则启动Common Join后备计划。
  set hive.mapjoin.smalltable.filesize=250000;
  - 开启无条件转Map Join：set hive.auto.convert.join.noconditionaltask=true;
  - 无条件转Map Join时的小表之和阈值,若一个Common Join operator相关的表中，存在n-1张表的大小总和<=该值,此时hive便不会再为每种n-1张表的组合均生成Map Join计划,同时也不会保留Common Join作为后备计划。而是只生成一个最优的Map Join计划。
  set hive.auto.convert.join.noconditionaltask.size=10000000;
+ bucker join参数设置：
  - 关闭cbo优化，cbo会导致hint信息被忽略：set hive.cbo.enable=false;
  - map join hint默认会被忽略(因为已经过时)，需将如下参数设置为false
  set hive.ignore.mapjoin.hint=false;
  - 启用bucket map join优化功能：set hive.optimize.bucketmapjoin = true;
+ sort merge bucket map join参数设置：
  - 启动Sort Merge Bucket Map Join优化：set hive.optimize.bucketmapjoin.sortedmerge=true;
  - 使用自动转换SMB Join：set hive.auto.convert.sortmerge.join=true;
### 数据倾斜优化
+ 数据倾斜：数据分布不均匀，集中在部分key上，导致部分task任务成为性能瓶颈。
+ 数据倾斜原因：
  - group by：选择字段，导致reduce段数据倾斜。
  - join：关联字段数据分布不均匀
#### 分组数据倾斜优化
+ 开启map端聚合
+ Skew-GroupBy:启动两个MapReduce任务，第一个MapReduce任务按随机数分区发送到Reduce，第二个MapReduce任务按正常方式进行聚合。(set hive.groupby.skewindata=true)
#### 聚合数据倾斜优化
+ 开启map端聚合
+ Skew-Join:启动两个MapReduce任务，为大表开启一个单独的mapreduce任务(set hive.optimize.skewjoin=true)
### 语法优化之并行度优化
#### map端并行度优化
+ 即map的任务个数，由输入文件的切片数决定，通常一个小文件启动一个任务
+ 查询大量小文件：多个小文件合并为一个任务：set hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat;
+ map端查询逻辑复杂：可提高map并行以提高查询速度，如re、json数据解析，：set mapreduce.input.fileinputformat.split.maxsize=256000000;
#### reduce端并行度优化
+ 参数
  - 指定Reduce端并行度，默认值为-1，表示用户未指定：set mapreduce.job.reduces;
  - Reduce端并行度最大值：set hive.exec.reducers.max;
  - 单个Reduce Task计算的数据量，用于估算Reduce并行度：set hive.exec.reducers.bytes.per.reducer;
### 小文件合并
+ 合并Map端输入的小文件：是指将多个小文件划分到一个切片中，进而由一个Map Task去处理。目的是防止为单个小文件启动一个Map Task，浪费计算资源
  - 可将多个小文件切片，合并为一个切片，进而由一个map任务处理
    set hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat; 
+ 合并Reduce端输出的小文件，是指将多个小文件合并成大文件。目的是减少HDFS小文件数量。
  其原理是根据计算任务输出文件的平均大小进行判断，若符合条件，则单独启动一个额外的任务进行合并。
  - 合并小文件参数设置：
    - 开启合并map only任务输出的小文件
      set hive.merge.mapfiles=true;
    - 开启合并map reduce任务输出的小文件
      set hive.merge.mapredfiles=true;
    - 合并后的文件大小
      set hive.merge.size.per.task=256000000;
    - 触发小文件合并任务的阈值，若某计算任务输出的文件平均大小低于该值，则触发合并
      set hive.merge.smallfiles.avgsize=16000000;
### 其他优化
#### CBO优化
+ 计算成本优化，数据的行数、CPU、本地IO、HDFS IO、网络IO等方面
+ 是否启用cbo优化：set hive.cbo.enable=true;
#### 谓词下推
+ 将过滤条件尽可能提前执行，减少后续计算的数据量
+ 是否启用谓词下推：set hive.optimize.ppd=true;
#### 矢量化查询
+ 将多条运算合并为向量的运算，如多条加法运算，可转换为两列矢量和。
+ 可以极大的提高一些典型查询场景（例如scans, filters, aggregates, and joins）下的CPU使用效率。
+ 相关参数如下：set hive.vectorized.execution.enabled=true;
#### Fetch抓取是指
+ Hive中对某些情况的查询可以不必使用MapReduce计算。
+ 参数：set hive.fetch.task.conversion=more;
  - 是否在特定场景转换为fetch 任务
  - 设置为none表示不转换
  - 设置为minimal表示支持select *，分区字段过滤，Limit等
  - 设置为more表示支持select 任意字段,包括函数，过滤，和limit等
#### 本地模式
+ Hive可以通过本地模式在单台机器上处理所有的任务。对于小数据集，执行时间可以明显被缩短
+ 参数：
  - 开启自动转换为本地模式
    set hive.exec.mode.local.auto=true;  
  - 设置local MapReduce的最大输入数据量，当输入数据量小于这个值时采用local  MapReduce的方式，默认为134217728，即128M
    set hive.exec.mode.local.auto.inputbytes.max=50000000;
  - 设置local MapReduce的最大输入文件个数，当输入文件个数小于这个值时采用local MapReduce的方式，默认为4
    set hive.exec.mode.local.auto.input.files.max=10;
#### 并行执行
+ Hive会将一个查询转化成一个或者多个阶段,有些阶段不是完全依赖是可以并行执行的。
+ 参数：
  - 启用并行执行优化
    set hive.exec.parallel=true;       
  - 同一个sql允许最大并行度，默认为8
    set hive.exec.parallel.thread.number=8; 
#### 严格模式(阻止危险操作)
+ 分区表不使用分区过滤：将hive.strict.checks.no.partition.filter设置为true时，对于分区表，除非where语句中含有分区字段过滤条件来限制范围，否则不允许执行。
+ 使用order by没有limit过滤：将hive.strict.checks.orderby.no.limit设置为true时，对于使用了order by语句的查询，要求必须使用limit语句。
+ 使用order by没有limit过滤：将hive.strict.checks.cartesian.product设置为true时，会限制笛卡尔积的查询。
