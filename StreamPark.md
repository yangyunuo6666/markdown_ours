[toc]

***

# StreamPark
+ 用于构建和管理流应用
  - 支持flink、spark、一站式流处理运营平台、连接器
  - StreamPark 由三部分组成：StreamPark-core、StreamPark-pump 、StreamPark-console
  - [streampark架构图](Markdown\图片\streampark架构图.png)
+ StreamPark-core：通过扩展 DataStream 相关方法，集成 DataStream 和 Flink sql api ，约定大于配置。
+ StreamPark-pump：类似于flinkx的组件，用于数据提取
+ StreamPark-console：综合性的实时低代码数据平台，可以更方便地管理Flink任务
+ 启停命令：
  - 启动：bash /opt/module/streampark_2.12-2.1.1/bin/startup.sh
  - 访问hadoop102:10000（默认用户名/密码：admin/streampark），可在作业管理右上角设置为简体中文



## 安装部署
+ 环境要求：Linux、JDK1.8、Node.js、Flink1.12+(SP1.2.2之前的仅支持scala2.11)
+ 准备 Maven
  - 下载Maven
    ```
    cd /opt/software 
    wget https://dlcdn.apache.org/maven/maven-3/3.8.8/binaries/apache-maven-3.8.8-bin.tar.gz --no-check-certificate
    ```
  - 解压
    ```
    tar -zxvf apache-maven-3.8.8-bin.tar.gz -C /opt/module
    sudo ln -s /opt/module/apache-maven-3.8.8 /bin/mvn /usr/bin/mvn
    ```
  - 使用阿里云镜像
  ```
    vim /opt/module/apache-maven-3.8.8/conf/settings.xml

    <mirrors>
    <mirror>
        <id>aliyunmaven</id>
        <mirrorOf>*</mirrorOf>
        <name>阿里云公共仓库</name>
        <url>https://maven.aliyun.com/repository/public</url>
    </mirror>
    </mirrors>
  ```
+ 上传StreamPark压缩包、JDBC驱动到lib目录
  ```
  tar -zxvf apache-streampark_2.12-2.1.1-incubating-bin.tar.gz -C /opt/module/streampark

  //需要自行下载驱动jar包并放在 $STREAMPARK_HOME/lib 中
  cp mysql-connector-j-8.0.31.jar /opt/module/streampark_2.12-2.1.1/lib
  ```
+ 初始化表结构
  - 目前支持mysql,pgsql, h2(默认,不需要执行任何操作)，这里我们使用mysql。
  - 初始化数据库和表结构
    - MySQL中执行：会自动创建一个名为streampark的库：source /opt/module/streampark_2.12-2.1.1/script/schema/mysql-schema.sql
    - 初始化数据：source /opt/module/streampark_2.12-2.1.1/script/data/mysql-data.sql
+ 修改配置
  - vim /opt/module/streampark_2.12-2.1.1/conf/application.yml
    ```yml
    spring:
      profiles.active: mysql #[h2,pgsql,mysql]


    streampark:
      proxy:
        yarn-url:
        lark-url:
      yarn:
        http-auth: sample
      hadoop-user-name: atguigu
      workspace:
      #本地的一个工作空间目录(很重要),建议单独放到其他地方,用于存放项目源码,构建的目录等.
        local: /opt/module/streampark_workspace
        remote: hdfs://hadoop102:8020/streampark
    ```
  - 手动创建本地目录：mkdir /opt/module/streampark_workspace
  - vim /opt/module/streampark_2.12-2.1.1/conf/application-mysql.yml,如果mysql用户的加密插件不是mysql_native_password，将allowPublicKeyRetrieval设为true,若密码正确，但是报错拒绝访问，那么可以尝试将密码加上单引号
    ```yml
    spring:
      datasource:
        username: root
        password: '000000'
        driver-class-name: com.mysql.cj.jdbc.Driver
        url: jdbc:mysql://hadoop102:3306/streampark?useSSL=false&useUnicode=true&characterEncoding=UTF-8&allowPublicKeyRetrieval=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=GMT%2B8
    ```

## 配置StreamPark
+ 设置maven配置文件
  - 设置中心 -> 系统配置 -> Maven Settings File Path
+ Flink设置
  - 设置中心 -> Flink 版本 -> 添加（设置flink名称、安装路径）
  - 配置flink配置文件，添加flink后可设置flink配置文件
    ```
    env.java.opts-all: -Dfile-encoding=UTF-8 

    classloader.check-leaked-classloader: false
    ```
  - “Flink集群”适用于Standalone、YarnSession和K8S Session等模式。Yarn的Application、Per-job模式不需要配置
+ yarn 队列设置
  - 设置中心 -> Yarn 队列 -> 添加（设置yarn队列名称）
### 配置报警设置：
+ 设置中心 -> 报警设置 -> 添加(设置邮箱报警、钉钉报警等)
+ 邮箱报警：
  - 设置 -> 账户 -> 管理服务 -> 开启POP3/IMAP?SMTP服务并审查授权码
  - 系统设置 -> 邮箱配置 -> 以授权码代替密码，其他正常填写
  - 报警设置 -> 添加 -> 邮箱报警 -> 添加故障报警类型(电子邮箱)-> 添加报警邮箱
+ 钉钉报警
  - 钉钉群中添加 -> StreamPark报警机器人(自定义机器人) ，安全设置：自定义关键词：StreamPark，勾选同意免责条款
  - 设置webhook地址，复制webhook地址(若泄露此地址有安全风险)，可使用此地址向钉钉群中推送消息。
  - 报警设置 -> 添加 -> 钉钉报警 -> 添加故障报警类型(钉钉机器人)
    - 钉钉URL：仅填复制的webhook地址中=前的内容末尾为_token=
    - 访问令牌：填复制的webhook地址中token=后的内容