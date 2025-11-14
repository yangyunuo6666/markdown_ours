[toc]

---

# redis7.x
+ **基于内存的KV键值对内存NoSQL数据库**，常用mysql配合使用（mysql前的带刀侍卫）
+ 作用：缓存、消息队列、分布式锁、会话共享
+ Redis支持异步写入磁盘，将内存中的数据以异步方式写入磁盘，同时不影响继续服务，保证数据断电不丢失。
+ 支持高可用集群部署：主机、主从、哨兵、集群
+ 缓存穿透、雪崩、击穿
+ 分布式锁
+ 队列
+ 排行榜+点赞
+ 优点：
  - 读取110000次/s，写入81000次/s
  - 数据类型丰富，支持list、set、zset、hash、k-v等
  - 支持持久化，rdb、aof
  - 支持数据备份，即主从复制
+ [Redis官方文档](https://redis.io/documentation)
  - [redis命令](https://doc.redisfans.com)
  - [redis在线测试](https://try.redis.io/)
  - [redis命令参考](https://redis.cn/commands.html)
+ 启停Redis服务
  - 在安装目录小启动：redis-server redis.conf
  - 关闭：
    - 单实例关闭：shutdown
    - 多实例关闭：redis-cli -p 6379 shutdown
+ redis-cli客户端连接
  - redis-cli -a root（-p 6379不写默认6379,）
## Redis部署
+ 版本号第二位为偶数是稳定版，奇数是开发版
+ 依赖
  - gcc > 4.8
+ 解压安装文件。进入解压目录。执行make && make install 命令，编译源码并安装。安装后的目录如下
  - redis-benchmark：性能测试工具
  - check-aof：aof文件修复工具
  - check-dump：rdb文件修复工具
  - cli：客户端
  - sentinel：哨兵，集群使用
  - server：服务端启动命令
+  进入安装目录usr/local/bin,将其移动的合适目录。
+  修改配置文件redis.conf，注意提前备份
    ```
    daemonize yes #后台启动
    protected-mode no #允许远程访问
    #bind 127.0.0.1 #注释掉绑定地址，允许访问
    requirepass root #设置Redis密码
    ```
+ 卸载Redis：停止服务，删除安装目录

## Redis数据类型
+ Redis支持10种数据类型V(K仅支持字符串)：string、list、set、zset（有序）、hash、geo（地理空间）、hyperlog（基数统计）、bitmap、bitfield（位域）、stream
+ string：字符串，最大512M
+ 常用命令：                                                   


























































































































































## redis面试题











