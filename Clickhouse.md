[toc]

---
# Clickhouse
+ 服务启停：
    ```
    sudo systemctl start clickhouse-server
    sudo systemctl stop clickhouse-server
    sudo systemctl restart clickhouse-server
    sudo systemctl enable clickhouse-server
    sudo systemctl status clickhouse-server
    ```
+ 开启clickhouse客户端：                
  clickhouse-client -m

## 数据类型
### 基本类型
+ int:Int8~Int64（8/16/32/64）
+ uint:UInt8~UInt64（8/16/32/64）
+ float:Float32、Float64
+ decimal高精度:Decimal32、Decimal64、Decimal128
+ string:字符串
### 复杂数据类型
+ 枚举：Enum8、Enum16
  ```sql
  --创建一个带有一个枚举 Enum8('hello' = 1, 'world' = 2) 类型的列
  CREATE TABLE t_enum
  (
  x Enum8('hello' = 1, 'world' = 2)
  )
  ENGINE = TinyLog
  ```
  - 使用场景：对一些状态、类型的字段算是一种空间优化，也算是一种数据约束。但是实际使用中往往因为一些数据内容的变化增加一定的维护成本，甚至是数据丢失问题。所以谨慎使用。
+ 时间（2字节保存）
  - Date 接受年-月-日的字符串比如 ‘2019-12-16’
  - Datetime 接受年-月-日 时:分:秒的字符串比如 ‘2019-12-16 20:50:10’
  - Datetime64 接受年-月-日 时:分:秒.亚秒的字符串比如‘2019-12-16 20:50:10.66
+ 数组：Array(T)
  - T 可以是任意类型，包含数组类型。 但不推荐使用多维数组，ClickHouse 对多维数组的支持有限。例如，不能在 MergeTree 表中存储多维数组。

## **表引擎**：
+ 名称对大小写敏感，必须显式在创建表时定义该表使用的引擎，以及引擎使用的相关参数。
+ 表引擎决定了：
  - 数据的存储方式和位置，写到哪里以及从哪里读取数据。
  - 支持哪些查询以及如何支持。
  - 并发数据访问。
  - 索引的使用（如果存在）。
  - 是否可以执行多线程请求。
  - 数据复制参数。
### TinyLog&& Memory
+ TinyLog：以列文件的形式保存在磁盘上，不支持索引，没有并发控制。一般保存少量数据的小表，生产环境上作用有限。可以用于平时练习用 
+ Memory引擎：数据保存内存，读写操作不会相互阻塞，不支持索引。简单查询下有非常非常高的性能表现（超过 10G/s），一般用到它的地方不多，除了用来测试，就是在需要非常高的性能，同时数据量又不太大（上限大概 1 亿行）的场景。

### **MergeTree合并树**
```sql
create table t_order_mt(
id UInt32,
sku_id String,
total_amount Decimal(16,2),
create_time Datetime
) engine =MergeTree
partition by toYYYYMMDD(create_time)
primary key (id)
order by (id,sku_id);
```
+ partition by 分区字段(可选)
  - 降低扫描范围，优化查询速度，不填默认一个分区。
  - 分区目录：MergeTree 是以列文件+索引文件+表定义文件组成的，但是如果设定了分区那么这些文件就会保存到不同的分区目录中。
  - 并行：分区后，面对涉及跨分区的查询统计，ClickHouse 会以分区为单位并行处理。
  - 数据写入与分区合并：任何一个批次的数据写入都会产生一个临时分区，不会纳入任何一个已有的分区。写入后的某个时刻（大概 10-15 分钟后），ClickHouse 会自动执行合并操作（等不及也可以手动通过 optimize 执行），把临时分区的数据，合并到已有分区中。

+ primary key 主键字段(可选)
  - 提供一级索引，**但不是唯一约束**，意味可存在相同的主键。
  - 主键的设定主要依据是查询语句中的 where 条件。根据条件通过对主键进行某种形式的二分查找，能够定位到对应的 index granularity（稀疏索引）,避免了全表扫描。

+ order by 排序字段（**必填**）
  - order by 设定了分区内的数据按照哪些字段顺序进行有序保存。
  - order by 是 MergeTree 中唯一一个必填项，甚至比 primary key 还重要，因为当用户不设置主键的情况，很多处理会依照 order by 的字段进行处理。
  - 要求：主键必须是 order by 字段的前缀字段。比如 order by 字段是 (id,sku_id) 那么主键必须是 id 或者(id,sku_id)


+ 二级索引：
  - ClickHouse 支持二级索引，二级索引也叫做跳数索引（skip index），用于加速查询。
  - 跳数索引是一种空间换时间的方式，通过建立索引元数据文件，在元数据文件中记录了索引数据和对应的数据文件偏移量。通过元数据文件就可以快速定位到索引数据在数据文件中的位置，从而跳过这部分数据，达到加速查询的目的。















































































## 集群部署
+ CentOS 取消打开文件数限制，同步配置文件
  - vim /etc/security/limits.conf,在文件末尾添加 
    ```
    * soft nofile 65536
    * hard nofile 65536
    * soft nproc 131072
    * hard nproc 131072
    ```
  - vim /etc/security/limits.d/20-nproc.conf 文件的末尾加入以下内容
    ```
    * soft nofile 65536
    * hard nofile 65536
    * soft nproc 131072
    * hard nproc 131072
    ```

+ 安装依赖
  - `sudo yum install -y libtool`
  - `sudo yum install -y *unixODBC*`

+  sudo vim /etc/selinux/config,并同步配置文件
  - SELINUX=disabled

+ 安装：
  - mkdir /opt/software/clickhouse
  - 上传安装文件，并分发。
  - 在每台机器上执行：sudo rpm -ivh *.rpm 
  - 修改并分发配置文件：sudo vim /etc/clickhouse-server/config.xml
    - 把<listen_host>::</listen_host> 的注释打开，这样的话才能让 ClickHouse 被除本机以外的服务器访问。
    - 补充：数据文件路径：\<path>/var/lib/clickhouse/</path>，日志文件路径：\<log>/var/log/clickhouse-server/clickhouse-server.log</log>
  - 三台机器上关闭开机自启sudo systemctl disable clickhouse-server