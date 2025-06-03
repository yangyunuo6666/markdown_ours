[toc]

# Java基础
## 技巧
+ 重写每一个类tostring方法，方便测试。1000L表示long类型，项目开发不使用sout用日志记录信息
+ 包的命名：com.公司名.项目名.模块名
+ Thread.sleep(1000);//当前线程休眠1秒，用于控制数据生成速度。
+ Calendar.getInstance().getTimeInMillis()//获取当前时间戳
+ 类型擦除：当你使用泛型（如List<String>）时，Java编译器在编译阶段会检查类型安全，确保你放入和取出元素类型正确。但编译完成后，泛型类型信息会被擦除，替换为原生类型（如List）或上界类型（如Object或Number）。当运行时JVM看不到泛型类型信息，只能看到原生类型或上界类型，导致了运行时类型信息缺失的代价。（使用TypeHint类可在运行时提供类型信息）
+ Lambda 表达式的基本结构：(参数列表) -> { 函数体 }
  - nums.sort((a, b) -> a - b);//sort需要的是compare方法，lambda表达式直接实现了compare方法。
  - list.forEach(s -> System.out.println(s));//历遍输出数组元素
+ 大小比较的方法
  - .equals()：比较字符串内容是否相同
+ SAM(单一抽象接口)：只有一个抽象方法的接口，可以用来实现Lambda表达式，通过接口来实现了灵活的函数式编程。
+ Ctrl+o:重写父类方法
## 问题解决
+ Cannot run program "D:\idea\JDK\bin\java.exe" (in directory " "C:\Users\杨雨糯\AppData\Local\JetBrains\IntelliJIdea2024.1\compile-server"): CreateProcess error=2, 
  - 问题描述：环境变量已正确配置、JDK8以正确安装、IDEA已正确配置JDK，但运行程序时报错找不到指定文件，显示使用路径为以前的jdk路径，更换jdk17后可正常使用，但jdk8仍报错。
  - 解决方案：IDEA残留旧的JDK配置，删除jdk.table.xml文件后可正常使用。（文件路径：C:\Users\杨雨糯\AppData\Roaming\JetBrains\IntelliJIdea2024.1\options\jdk.table.xml）
## 专业术语及设计思想
### 设计思想
#### 模拟修饰器设计模式（处理流为例）：
+ 1、设计抽象类 2、设计继承抽象类的处理不同情况的处理子类 3、设计处理类，处理类中包含一个抽象类的对象，通过调用抽象类的方法实现处理。**Java是单继承的**
#### 面对对象三大特征
+ 封装：将数据和方法封装在内部为一个类，程序的其他部分仅有通过授权的方法才能操作数据
    - 封装步骤：属性私有化private属性，提供public方法提供外部访问方法（getXXX、setXX）外部访问方法可加入身份验证代码 
    - 构造器：使用构造器时在构造器中加入访问方法，可进行身份验证
+ 继承：子类继承（extend）父类方法，Java类单继承，接口可多继承
    - 父类私有属性子类仅可通过父类提供的方法访问。
    - 创建子类对象时必须调用父类构造器完成父类初始化，**自动默认(不用写编译器会自动在子类构造器方法上加上super();调用父类无参构造器)**调用父类无参构造器，父类没有无参构造器时需要在子类构造器中通过super指定（super(vue1,vue2);）。父类构造器调用是递归的。
    - this和super都只能在第一行使用，二者只可取其一。 
+ 多态：一个父类有多个子类，通过子类赋给父类变量，调用方法时根据实际类型调用相应的方法。
    - 方法的多态：方法的覆盖和重写。
    - 对象的多态：对象的编译类型和运行类型可以不一致，编译类型在定义时确定，运行类型在运行时确定。（运行类型有=右边决定）
    - 转型：向上转型父类接受子类对象运行类型为子类对象，向下转型子类接受父类的运行类型**需要强制转换**。
#### 动态绑定：
+ 在运行时根据对象的实际类型来调用相应的方法，而属性哪里定义用哪里无动态绑定。
#### 代理
+ 代理类与被代理类实现同一个接口，代理类实现重要方法。代理类中包含被代理类的对象，通过调用被代理类的方法实现代理。
### 关键字
+ implements:实现接口关键字（class a implements Runnable）
### interface 注解
- @Override : 覆盖父类方法注解，可防止出错。
- @Deprecated : 标记弃用方法。
- @SuppressWarnings(value={"erro1","erro2"}) : 取消特定几种警告,一种时不用加value={}
  - unchecked : 未检查的转化警告。
  - deprecation : 使用了不推荐使用的方法的警告。
  - serial : 实现了Serializable接口但是没定义serialVersionUID常量。
  - rawtypes : 使用旧语法创建泛型对象。
  - finally ：finally子句不能完成。
  - fallthrough : Switch中的case语句后无break。
  - all : 取消所有警告。
+ @beferore : 指定方法在某个方法前执行。
+ @After : 指定方法在某个方法后执行。
+ @Around : 指定方法在某个方法前后执行。
+ @Test : 指定方法为测试方法。
+ @RunWith : 指定测试运行器。
+ @BeforeClass : 指定方法为类加载时执行的方法。
+ @AfterClass : 指定方法为类卸载时执行的方法。
+ @Ignore : 指定方法为忽略测试方法。

## 设计一个函数的实例(jar包)
+ 设计initiative方法，检验参数个数、参数类型是否合法（getCategory方法）。
+ 设置work方法，处理参数正确的调用。
+ 设置errorwork方法，处理参数错误的调用。
## Java相关知识
### JDK与JRE与JVM
+ JDK：Java Development Kit，Java开发工具包，是整个Java的核心，包括了Java运行环境JRE、Java工具和Java基础类库。
+ JVM：Java Virtual Machine，Java虚拟机，是整个Java实现跨平台的最核心的部分，能够运行以Java语言写作的程序。
### 运行
+ 源代码（.java）通过 javac 文件名.java 命令编译成字节码（.class），通过 Java 文件名无后缀 命令运行。
+ **java程序保存时文件名必为类名，且首字母大写**
+ 报错包路径找不到，光标至于报错行包名前，Alt+enter后单击move
+ ctrl+滚轮控制字体大小：设置+编辑器+常规
+ new project setup：新项目设置可调整创建新项目时的设置。
### maven
+ 作用：依赖管理，通过编写pom.xml文件，可自动下载需要的jar包到本地maven仓库，在项目中引入依赖。
+ 依赖管理
  - 依赖遵循依赖传递原则，即如果A依赖B，B依赖C，那么A也依赖C
  - 就近原则：当依赖的版本冲突时，优先使用距离当前模块最近的依赖版本
  
+ 模块化：将一个项目拆分成多个模块，每个模块是一个独立的工程，模块之间可以相互依赖。

+ 工程结构
  ```
  my-project/
  ├── src/
  │   ├── main/
  │   │   ├── java/          # Java 源代码
  │   │   ├── resources/     # 配置文件（如 application.yml）
  │   │   └── webapp/        # Web资源（如JSP、静态文件）
  │   └── test/
  │       ├── java/          # 测试代码
  │       └── resources/     # 测试配置文件
  ├── target/                # 输出目录，.class
  └── pom.xml                # Maven 项目配置文件
  ```
+ 常用maven命令
  - mvn clean：清理(删除target目录下所有文件即所有字节码)
  - mvn compile：编译主程序
  - mvn test-compile：编译测试程序
  - mvn test：运行测试程序
  - mvn package：打包(web项目打包成war包，java项目打包成jar包)
    - cmd: java -jar xxx.jar //运行jar包
  - mvn install：安装(将打包的文件复制到"仓库"指定位置)
  - mvn deploy：部署(将war包复制到容器指定目录下使其可以运行)
+ maven仓库配置
  - 下载maven，解压到无中文无空格目录下，下载maven插件，**添加用户变量：MAVEN_HOME，"D:apache-maven-3.2.2"和环境变量path-D:apache-maven-3.2.2\bin**
  - 配置本地仓库：settings.xml文件中修改\<localRepository>本地仓库路径\</localRepository>。
  - 配置镜像：settings.xml文件中修改mirrors标签的值。
  - 配置远程仓库：pom.xml文件中添加repositories标签。
+ **Jav包打包工具：maven-assembly-plugins**
+ 统一各个模块中junit依赖版本
  - 思路：创建父工程，将junit依赖统一到父工程中，子工程继承父工程，子工程中不再添加junit依赖。
  - 项目结构
    ```
    parent-project/       # 父项目根目录
    ├── pom.xml           # 父 POM 文件（packaging 为 pom）
    ├── module-common/    # 公共模块（如工具类、通用组件）
    │   └── pom.xml
    ├── module-service/   # 业务逻辑模块
    │   └── pom.xml
    └── module-web/       # Web 层模块（如 Spring Boot 入口）
        └── pom.xml
    ```
  - 步骤：创建父工程Parent且指定其打包方式为pom,在parent工程中添加junit依赖和配置依赖管理、聚合。在子工程中以\<artifactID>Parent\</artifactID>继承父工程，并添加\<relativePath>../Parent\</relativePath>声明父工程相当当前文件路径。
+ 示例
 - 父工程
  ```xml
  <groupid>com.yimei.shiyan</groupid><!-- 公司域名倒序+项目名 -->
  <artifactid>Hellow</artifactid><!-- 模块名 -->
  <version>1.0-SNAPSHOT</version><!-- 版本号 -->
  <packaging>pom</packaging><!-- 关键：多模块必须为 pom -->
  <name>Parent Project</name><!-- 项目名 -->

  <!-- 子模块列表 -->
  <modules>
      <module>module-common</module>
      <module>module-service</module>
      <module>module-web</module>
  </modules>

  <!-- 统一管理依赖版本，在需要使用的地方使用<version>${yimie.spring.version}<\version>引用 -->
  <properties>
      <java.version>17</java.version>
      <spring-boot.version>3.1.5</spring-boot.version>
      <lombok.version>1.18.30</lombok.version>
  </properties>

  <!-- 依赖管理（子模块需显式声明依赖，但无需指定版本） -->
  <dependencyManagement>
      <dependencies>
          <!-- Spring Boot Starter -->
          <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-web</artifactId>
              <version>${spring-boot.version}</version>
          </dependency>
          <!-- 需要排除的不稳定依赖 -->
          <exclusions>
              <exclusion>
                  <groupId>org.springframework.boot</groupId>
                  <artifactId>spring-boot-starter-logging</artifactId>
              </exclusion>
          </exclusions>
          <!-- Lombok -->
          <dependency>
              <groupId>org.projectlombok</groupId>
              <artifactId>lombok</artifactId>
              <version>${lombok.version}</version>
              <scope>provided</scope>
          </dependency>
      </dependencies>
  </dependencyManagement>
  <!-- 统一插件配置 -->
  <build>
      <pluginManagement>
          <plugins>
              <!-- 编译插件 -->
              <plugin>
                  <groupId>org.apache.maven.plugins</groupId>
                  <artifactId>maven-compiler-plugin</artifactId>
                  <version>3.11.0</version>
                  <configuration>
                      <source>${java.version}</source>
                      <target>${java.version}</target>
                  </configuration>
              </plugin>
              <!-- Spring Boot 打包插件 -->
              <plugin>
                  <groupId>org.springframework.boot</groupId>
                  <artifactId>spring-boot-maven-plugin</artifactId>
                  <version>${spring-boot.version}</version>
              </plugin>
          </plugins>
      </pluginManagement>
  </build>
  ```
- 子模块1
  ```xml
  <project xmlns="http://maven.apache.org/POM/4.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
      <modelVersion>4.0.0</modelVersion>

      <!-- 继承父项目 -->
      <parent>
          <groupId>com.example</groupId>
          <artifactId>parent-project</artifactId>
          <version>1.0.0-SNAPSHOT</version>
      </parent>

      <!-- 子模块自身信息 -->
      <artifactId>module-common</artifactId>
      <packaging>jar</packaging>

      <!-- 子模块的依赖 -->
      <dependencies>
          <!-- 无需指定版本（由父 POM 管理） -->
          <dependency>
              <groupId>org.projectlombok</groupId>
              <artifactId>lombok</artifactId>
          </dependency>
      </dependencies>
  </project>
  ```

### Docker
+ docker官网:github.docker.com
+ 作用：容器技术，将应用和最小化运行环境打包成一个镜像，解决了开发环境和运行环境不一致的问题，并可以做到快速部署服务
+ 原理：Docker是一个client-server架构的系统，Docker守护进程运行在主机上，通过Socket从客户端访问，DockerServer守护进程接收到Docker-Client的指令，管理相应的容器。
+ 与虚拟机对比：与属主机共享OS无额外资源损失、秒级部署、面向软件开发者，VM面向硬件运维分钟级响应。
+ Docker三要素：
  - client客户端：用于操作docker.
  - Docker home:存放docker的文件，包括镜像、容器(container)、数据卷、网络等。
  - Repositories仓库：存放镜像的地方，分为公有仓库Docker Hub(alyun Docker)和私有仓库。
+ Docker安装：https://www.runoob.com/docker/docker-install.html
+ 容器：可看做一个简易的Linux系统环境(包括root用户权限、进程空间、用户空间和网络空间等)和运行在其中的应用程序，大部分的Linux命令在容器中都可以使用。
#### Docker命令
+ docker --help:查看docker帮助文档
##### 镜像命令
+ docker images:查看本地所有镜像,**-a查看所有镜像(含中间镜像层)，-q只显示镜像id,**--detail显示摘要信息,--no-trunc显示完整信息。
+ docker search image_name:搜索镜像，**-s num：收藏数大于num的镜像**，--atomated：只显示自动构建的镜像。
+ docker pull image_name:3.2:下载3.2版image_name镜像,不写:3.2默认下载最新版。
+ docker rmi image_name:3.2 image_name:3.1:删除3.2和3.1版镜像，**-f强制删除镜像，$:docker images -qa删除查到的所有镜像**。
+ docker run -it image_name:以交互形式启动镜像，--name container_name:指定容器名称,-d：后台运行，守护进程通常用于需要等待访问的服务端，-p(用于指定服务端口提供访问服务) host_port:container_port:映射端口，-P：随机端口，-v host_path:container_path:映射文件。
+ docker exec -it container_id /bin/bash：进入容器终端
+ docker attach container_name：进入容器终端
##### 容器命令
+ docker ps:查看正在运行的容器，**-a查看所有容器，-q只显示容器id，-l只显示最近创建的容器，-n num只显示最近num个创建的容器，--no-trunc不截断输出**。
+ exit：退出并停止容器，ctrl+p+q：退出容器不停止容器。
+ docker start container_name/container_id:启动容器。
+ docker stop container_name/container_id:正常停止容器。
+ docker commit container_id -m "commit message" -a "author" image_name:3.2:提交容器为镜像，**-m提交信息，-a作者**。
+ 将镜像推送到仓库
  - docker login:登录docker仓库，docker logout:退出docker仓库。
  - docker tag image_name:3.2 username/repository_name:3.2:给镜像打标签，**username/repository_name:3.2**表示用户名/仓库名:版本号。
  - docker push username/repository_name:3.2:将镜像推送到仓库。
+ docker kill container_name/container_id:强制停止容器。
+ docker restart container_name/container_id:重启容器。
+ docker rm container_name/container_id:删除以停止的容器，**-f强制删除容器**,$(docker ps -qa):删除所有容器/doker ps -qa | xargs docker rm:删除所有容器。
+ docker log container_name:查看容器日志,-f:查看实时日志,-t：显示时间戳,--tail num:显示最后num条日志。
+ docker top container_name:查看容器内进程。
#### Docker容器数据卷
+ 容器数据共享和数据持久化
+ dockerfile:镜像配置文件，描述了镜像用于构建镜像，使用docker build命令构建镜像。
+ 容器间数据共享，活动U盘挂载在容器上，容器间共享数据。
  - 容器2、3继承容器1的data volume，即可以实现容器间数据共享，但容器1、2删除不影响3已有的数据，即**数据卷的生命周期与最后一个有它的容器结束同时结束**
##### 数据卷命令
+ 命令方式容器内添加data volume
  - docker run -it -v /宿主机绝对路径:/容器内路径 镜像名
  - docker inspert docker_id//查看容器详细信息，查看挂载是否成功
  - docker run -it -v /宿主机绝对路径:/容器内路径:ro 镜像名 //赋予读r写o权限
+ 使用Dockerfile添加（1~n个）data volume
  - 1.编写dockerfile并在Dockerfile中添加VOLUME指令，创建容器内路径，VOLOME ["/容器内路径", "/容器内路径2"]
  - 2.docker build -f Dockerfile -t 镜像名 . //将dockerfile文件构建镜像到.(当前目录)下
##### dockerfile构建
+ 编写规则
  - 每条指令大写且至少有一个参数
  - 指令从上到下顺序执行，以#表示注释
  - 每条指令会创建一个镜像层同时对镜像进行提交。
+ 构建过程：根据基础镜像构建容器，在容器内执行指令，将指令执行结果提交为镜像层，重复以上步骤最终形成镜像。
+ dockerfile指令
  - FROM scratch/centos/ubuntu:基础镜像，scratch表示所有镜像的父镜像。
  - MAINTAINER 作者信息
  - LABEL:标签 \ (\表示换行连接)
  - RUN:容器构建时需要执行的命令,如RUN yum install -y vim
  - ENV:设置构建时环境变量，可在其他命令中直接使用($PATH_NAME)，如ENV JAVA_HOME /usr/local/java
  - EXPOSE:暴露端口
  - WORKDIR:指定终端登录后进入的工作目录
  - ADD:将宿主机文件复制到容器内，**并自动解压**
  - COPY:将宿主机文件复制到容器内，**但不会自动解压**
  - VOLUME:创建挂载点，挂载数据卷
  - ENTRYPOINT:容器启动时执行的命令，**ENTRYPOINT命令不会被docker run命令的参数覆盖**
  - CMD echo "hello world"//容器启动时执行的命令，**CMD命令会被docker run命令的参数覆盖**
  - CNBUILD:触发器，当子继承父时父镜像的onbulid会被触发，构建镜像


#### Docker安装应用
+ 安装MySQL：
  - docker search mysql:5.7//查找mysql5.7镜像
  - docker pull mysql:5.7//下载mysql5.7镜像
  - docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root --name mysql mysql:5.7//启动mysql容器，-d后台运行，-p端口映射，-e设置环境变量，--name容器名，mysql:5.7镜像名
  - docker attach mysql//进入容器
+ 安装Redis：
  - docker search redis:5.7//查找redis5.7镜像
  - docker pull redis:5.7//下载redis5.7镜像,同时可以验证是否下载成功
  - docker run -d -p 6379:6379 --name redis redis:5.7//启动redis容器
  - docker attach redis//进入容器

### Java注解
+ 注解：一种元数据，用于为Java代码提供额外的信息，可使用注解为类、方法、参数、变量等添加信息。
+ 注解使用：@注解名(属性名=属性值,属性名=属性值)

### IDEA技巧
#### 配置
+ 设置字体大小：设置-字体
+ 设置项目编码为UTF-8可使用中文。
+ Ctrl+shift+ALT+S：更换JDK。
#### 快捷键
+ ctrl + j:查看可用方法快捷键
+  sout+enter：生成输出语句。
+  Ctrl+alt+L:格式化代码。
+  **鼠标放在类名：alt+insert：生成构造器。**
+  Ctrl+H:查看类继承关系。
+  **Ctrl+b:查看源码**
+  **new Scanner(System.in).var + enter：自动生成变量名**
+  **alt+enter:自动导入包**（需要先配置设置->编译器->自动导入->勾选自动添加的两个方框）。
+  Ctrl+X：删除一行
+  Ctrl+D：复制当前行
+  Ctrl+/:注释、
+  Ctrl+O：重写方法
+  Ctrl+I：实现方法
+  Ctrl+F12：查看文件结构
+  Ctrl+H：查看类继承关系
+  Ctrl+R:替换文本
+  Ctrl+F:查找文本
+  Ctrl+U：跳转到父类
+  Ctrl+Shift+T：**创建测试类**
+  Ctrl+Shift+U：大小写切换
+  Ctrl+shift+F10：运行。
+  Ctrl+Shift+Space：智能代码补全
+  Ctrl+ALT+L:格式化代码
+  Ctrl+ALT+O:优化import
+  Ctrl+ALT+I:自动缩进
+  Ctrl+ALT+V:**自动生成变量名**
+  Ctrl+ALT+T：包代码包在一块内
+  a!=null.if + enter：自动生成if语句
+  选中代码，在选try可在外出包上try-catch语句。
+  方法名+enter：自动生成需要重写的方法。
#### 模板（templater）快捷键使用
+ 设置+实时模板（可自定义模板）
+ main+enter：生成main函数。
+ fori+enter:生成for循环。
+ sout+enter：生成输出语句。
+ .var+enter:自动生成变量名。
+ .for+enter:自动生成for循环。
  
#### 其他
+ scr 右击新建软件包com.baby.pkj,使用包管理package com.baby.pkj;，package语句需要放在类最上面是打包语句。
+ 文件夹->右击->Mark dir as：标记文件夹作用
+ module：flie->project structure->modules->+->new module：新建module
+ target文件夹未显示：设置->Tree Appearance->show Excluded flies
+ 反射机制：运行时动态地获取类的信息，并能够操作类的属性和方法的能力
  - 动态加载类
  - 动态调用方法
  - 动态访问属性
  - 动态创建对象
  - 动态代理

### 常用方法与单词
#### 常用方法
+ .equals(obj)//判断两个对象是否相等
#### 单词
+ mapper:方法

## 方法格式
+ 修饰符 返回值类型 方法名(参数类型 参数名){
    方法体
    return 返回值;
}
### 修饰符
+ public：公共的，所有类都可以访问。
+ protected：受保护的，只有同一包和子类可以访问。
+ default（默认）：同一包内可见，不同包需要子类继承。
+ private：私有的，只有同一类可以访问。
### 返回值类型
+ void：无返回值。
+ 基本数据类型：返回对应的基本数据类型。
+ 引用数据类型：返回对应的对象。
### 参数类型
+ 基本数据类型：传递基本数据类型的值。
+ 引用数据类型：传递引用数据类型的地址值。
### 注释
+ 单行注释：//
+ 多行注释：/* */

## 变量与字符
### 变量类型
+ 基本数据类型：byte（1字节）、short（2字节）、int（4字节）、long（8字节）、float（4字节）**定义时必须加上f**、double（8字节）、boolean（布尔型）。
+ **常量**：变量定义前加上final关键字，常量值在定义后不能被修改。
+ 引用数据类型：类class、接口interface、数组int [] 、字符串（String）、记录record、注解interface。
+ 局部自动变量：var d = 3.1//自动根据值识别类型。
#### 引用数据类型
+ record 记录
  - 特点：无需定义方法，类型为final，成员类型为final，可转换为字符串，可哈希，可比较。
  - 
      ```
      public record students(String name,int id){
          //定义记录的成员
      }
      ```
+ enum 枚举
   - 特点：不可在方法内部声明,编译后可生成一个enum.class文件，可作为一个特殊的类使用。
   -
     ```
     public enum enum1{
        red,yellow;
     };
     ```
 
 
    
### 高精度
+ java.math.BigInteger
+ java.math.BigDecimal
### 数组
#### 定义与初始化
+ 定义：数据类型[] 数组名 = new 数据类型[数组长度];
+ 初始化：
 - 静态初始化：
```
int arr
```
  - 动态初始化
```

arr【0】= new int【1】；

int [][] arr = new int[3][4];
arr【0】【0】= 1；
```
+ 赋值：数组名[下标] = 值;
#### 查看数组长度、拷贝数组、数组排序、转换为字符串
+ 数组名.length
+ 拷贝：
 - System.arraycopy(源数组，源数组起始位置，目标数组，目标数组起始位置，复制长度)
 - arr2=arr1
+ Arrays.sort(数组名);
+ Arrays.toString(数组名);
### 变量类型转换
+ 自动类型转换：将容量小的类型自动转换为容量大的数据类型。
+ 强制类型转换：将容量大的类型强制转换为容量小的数据类型，需要强制转换符。(eg:a=(int)b;)
### 字符
+ 转义字符： f换页  r回车  b退格
+ Java程序中可以用 xxx（三位八进制数）表示字符或 uxxxx（四位十六进制数）表示字符。
## 作用域
+ 成员变量：作用于整个类，在类的方法中使用。
+ 其他变量：同C语言。

## 运算符（同C）
+ 算术运算符：+、-、*、/(同为整数结果为整除结果)、%、++、--。
+ 赋值运算符：=、+=、-=、*=、/=、%=、&=、|=、^=、<<=、>>=。
+ 比较运算符：==、!=、>、<、>=、<=。
+ 逻辑运算符：&&、||、!。
+ 位运算符：&、|、^、~、>>、<<、>>>（按位无符号右移）
+ 三元运算符：a?b:c。

## 对象类型（list、set、dict）
### 对象框架Map和Collection（对象中需要实现的接口）
#### Collection接口
+ add(E) : 添加元素e,remove()、isEmpty、size(返回元素个数)、contains(X)(是否存在元素X)、iterator()（封装为迭代器返回）、
+ addALL、removeALL、removeIF(删除符合条件的数据)、containsALL(X)（是否存在元素集合X）、clear(清空集合)、retain(A)（仅保留A集合中的元素）
+ 常用方法
  - Collections.sort(List1) //对List1中的元素进行排序
  - Collections.sort(List1,Comparator) //对List1中的元素进行排序，Comparator为比较器
  - Colllections.shuffle(List1) //对List1中的元素进行随机排序
  - Collections.min/max(list,(Comparator))
#### Map接口
+ put(K,V) : 添加元素(K,V)、get(K)（返回K对应的V）,remove(K)（删除K对应的V）、contaionsKey(K)(是否存在K键)、contaionsValue(V)(是否存在V值)、size(返回键值对个数)、isEmpty(是否为空)、replace(K,V)(替换K对应的V)
+ putAll(Map\<K,V>)、clear(清空)、keySet(返回键集合)、values(返回值集合)、entrySet(返回键值对集合)
### **迭代器**（Iterator）
+ 实现了Iterator接口的类可使用迭代器，for循环的增强就是弱化迭代器，底层也是。
+ hasNext() //返回迭代器中是否还有对象
+ next() //返回迭代器中的下一个对象,指针下移
+ remove() //删除迭代器中的对象,同时删除了集合中的对象。
```java
Iterator iterator1 = myList.iterator();//封装为迭代器返回
while(iterator1.hasNext()){
    Syster.out.println(iterator1.next());
}
```
### **比较器**（Comparator）
+ 一般通过lambada表达式创建，也可通过实现Comparator接口创建
+ **比较器实现和使用示例**
  ```java
  Comparator<String> com = (x,y)->x.length()-y.length();// 创建了一个比较string型的匿名函数函数返回XY的长度之差。
  Collections.sort(list,com);
  ```
+ 实现Comparator接口
  ```java
  import java.util.Comparator;
  public class PersonComparator implements Comparator<Person> {
      @Override
      public int compare(Person p1, Person p2) {
          // 比较规则：按年龄升序排序
          return Integer.compare(p1.getAge(), p2.getAge());
      }
  }
  ```

### list
+ add(index,x)//在指定位置插入元素x、
+ get(index)//返回指定位置元素、
+ set(index,x)//修改指定元素值、
+ remove(index)//删除指定位置元素
+ indexOf(x)//查找X第一次出现位置
+ lastIndexOf(x)//查找X最后一次出现位置
+ subList(from,to)//返回从from到to的子列表。
#### ArrayList最常用的list实现类
+ list\<string> list1 = new ArrayList\<string>();
+ listiterator()方法可返回ListIterator对象，该对象可用来双向遍历List。
  - 为iterator的子类。
  - hasPrevious():返回是否有前一个元素。
  - previous():返回前一个元素。
  - nextIndex():返回下一个元素的索引。
  - previousIndex():返回前一个元素的索引。
  - remove():删除当前元素。
  - set():修改当前元素。
#### Linklist单链表
+ LinkedList\<String> list = new LinkedList\<String>();
+ addFirst(x)/addLast(x) //在头部/尾部插入元素x
+ getFirst()/getLast() //返回头部/尾部元素
+ removeFirst()/removeLast() //删除头部/尾部元素
+ offer(x)/offerFirst(x)/offerLast(x) //在头部/尾部插入元素x
+ peek()/peekFirst()/peekLast() //返回头部/尾部元素
+ poll()/pollFirst()/pollLast() //返回并删除头部/尾部元素
#### Vector动态数组
+ Vector\<String> list = new Vector\<String>();
+ addElement(x) //在尾部插入元素x
+ firstElement() //返回头部元素
+ lastElement() //返回尾部元素
+ removeElement(x) //删除第一个x元素
+ removeElementAt(index) //删除指定位置元素
+ setElementAt(x,index) //修改指定位置元素


### Set类
#### HastSet子类(无序散列集合)
+ s1.addALL(s2):求s1和s2的并集。
+ s1.removeAll(s2):求s1和s2的差集。
+ s1.retainAll(s2):求s1和s2的交集。
+ s1.containsAll(s2):判断s1是否包含s2。 
#### TreeSet子类(红黑树集合)
+ TreSet(c/比较器/有序集) //按字母序/比较器/有序集顺序生成树集合
+ first返回第一个元素、last返回最后一个元素
+ subSet(from,to)返回从from到to的有序子集
+ headSet(to)返回小于to的有序子集
+ tailSet(from)返回大于或等于from的有序子集

### queue类
+ element()返回队头元素
+ offer(e)插入元素E
+ peek()返回队头元素
+ poll()返回并删除队头元素
#### Dqueue双向队列
+ addFirst(e)/addLast(e)、getFirst()/getLast()....
##### LinkedList双向链表(线性表实现Dqueue)
+ 同时实现了list和Dqueue接口，唯一允许插入空元素的队列
+ addFirst(e)/addLast(e)、getFirst()/getLast().
##### ArrayDeque双向数组链表(可变数组实现Dqueue)
+ 不允许出现空元素
#### PriorityQueue优先级队列

### map
+ **迭代器**：map.keySet().iterator()对键集进行迭代、map.entrySet().iterator()、map.values().iterator()//对值进行迭代
#### HashMap
+ 创建：HashMap(int x)//x为初始容量、HashMap(int x,float f)//x为初始容量、f为负载因子(0~1之间，默认为0.75)、HashMap(Map m)//m为另一个map
#### TreeMap
+ 创建：TreeMap():根据字母序创建空字典、TreeMap(Map m):根据字母序创建包含m的树字典、TreeMap(Comparator c):根据比较器c创建空字典
  
## 异常处理、断言、上下文管理
### 异常分类
+ 检查异常：编译错误。
+ 非检查异常：运行错误
### 异常类
+ Error:系统内部错误。
+ Exception:（非）检查异常。
#### 自定义异常类
+ 
### 异常处理
+ try ... catch(异常类型 exception1|异常类型 exception2)...finall //同python，但从Java7开始实现资源自动管理（即try模块结束后按资源打开的顺序关闭资源）。
+ **throw/throws:不处理但抛出异常**
  - static void method (int x) throws exception1 //方法抛出exception1.
  - throw a //抛出异常对象a

### 断言
+ assert [exp] : 报错附加信息


## **流程控制**
+ if语句、Switch语句同C语言，但是Switch除执行语句外还可返回一个值赋给变量。
```java
int date = switch(month){
    case 1,3,5,7,8,12 -> 31;
    case 4,6,9,11 -> 30;
}
```
+ while循环、do...while循环、for循环同C语言。
  - **特别的for循环可以用each循环写**：
  ```java
  for(int a1 ：a ){
      system.out.println(a1);//输出所有数字
  }
  ```
+ **标签的使用**：
```java
start: //标签的定义
for (int i ; i<10;i++){
    for (int j; j<i;j++ ){
        if (j==2){
            break/contine start; //跳出/到标签标识的循环
        }
    }
}
```

# 输入与输出
## 常用方法
### 输入（需要先创建一个scanner实例）
+ Scanner scanner = new Scanner(System.in);//创建一个扫描器实例
+ s.nextInt();//输入一个整数
+ s.nextDouble();//输入一个浮点数
+ s.next();//输入一个字符串
+ s.nextLine();//输入一行字符串
### 输出
+ System.out.println("小明今年刚满" + i + “岁”);//输出一个字符串，并换行
+ System.out.print();//输出一个字符串，不换行
+ System.out.printf();//格式化输出
+ System.out.format();//格式化输出
+ System.out.printf("%d",a);//输出一个整数  

## 标准输入流System.in
+ 对应键盘
## 标准输出流System.out
+ 对应显示器  



# 类与包
## 包（类和相关接口的集合）
+ 用户定义的类都应该在包中，package可指定类归属的包,**需置于程序首行**(为了包名唯一通常将域名翻转为包名如：com,bada.xy)
## 类
### 类导入
+ import语句：import 包名.类名;
+ 通配符：import 包名.*;//导入该包下所有类
+ **当导入的包含有相同的类时如直接实例化会报错，需使用类名.class**
### 基础类库
+ java.lang //基础语言类无需导入即可使用
+ java.util //基础工具类包括集合类和接口定义
+ java.io //输入输出类
+ java.net //网络类
+ java.sql //数据库类
+ java.awt/javax.swing //图形化界面  
+ javax.sql //数据库类
+ java.math //数学类
+ java.time //时间类
## 专业术语
+ 封装：通过private、protected、public等关键字来控制成员变量的访问权限。
+ 继承：通过extends关键字来实现继承。
+ 多态：通过重写父类的方法、接口实现、父类引用子类对象、来实现多态。
+ 抽象类：通过abstract关键字来实现抽象类。
+ 接口：通过interface关键字来实现接口。
+ 内部类：通过class关键字来实现内部类。
## 定义与实例化
### 定义
+ 定义一个类：class 类名{}
+ 或：public class 类名{}
+ **应用**：
  - 定义一个私用成员变量(属性)：private 数据类型 成员变量名，而后定义一个get方法提供访问接口，set方法提供修改接口。
    ```java
    class student
    {
        private int age;
        public int getAge(){
            return this.age;
        }
        public void setAge(int age){
            this.age = age;
        }
    }
    ```
  - 定义一个公有的成员方法(行为)：public 返回值类型 方法名(参数列表){
      方法体
      }
    ```java
    class student
    {
        public void study(){
            System.out.println("学习");
        }
    }
    ```
### 类实例化
+ 类名 对象名 = new 类名();
## 自定义类库
+ 正常定义类（需要包含主类），在项目scr目录下创建名为MANIFEST.MF的清单文件，文件内容为：Manifest-Version: 1.0 //冒号后有空格
Main-Class: 包名.类名 //冒号后有空格
                    //空行不可省略
+ 打包：在项目目录下执行命令：jar -cvf 包名.jar MANIFEST.MF 包名/类名.class //包名.class为需要打包的文件 (或点击项目名，选择JAR files，选择需要打包的文件和MANIFEST.MF文件)
+ 使用：点击项目名，选择Build Path，点击Add External Archives，选择b文件。

## 继承(类仅可单继承，接口可多继承)
### object基类（所有类的父类）
+ getClass()：获取当前对象的类对象。
+ hashCode()：获取当前对象的哈希值。
+ equals()：比较当前对象与指定对象是否相等，通过比较引用地址是否相同来判断，若相同则哈希值相同。
+ clone()：复制当前对象。
+ toString()：获取当前对象的字符串表示。
+ notify()：唤醒一个等待当前对象的线程。
+ notifyAll()：唤醒所有等待当前对象的线程。
+ wait()：使当前线程等待当前对象。
+ notify()：唤醒一个等待当前对象的线程。
+ finalize()：当垃圾回收器确定不存在对该对象的更多引用时，由对象的垃圾回收器调用此方法。
### 其他
+ 继承格式，
  ```java
  class 子类名 extends 父类名{}
  ```
+ 子类特点，同Python。
+ 重写父类方法，同Python。
+ 用final修饰的类不可被继承，用final修饰的方法不可被重写，用final修饰的变量不可被修改。
+ instanceof判断一个对象是否为某个类的实例，variable instanceof 类名。
## 构造方法（必须与类同名）
+ 实例
```java
班级学生
{
    private int age;
    public student(int age){//构造方法1
        this.age = age;
    }
    public student(){//构造方法2
        this.age = 0;
    }
}
```
+ 调用父类构造方法：super(value1,value2)
## 方法重载与重写
+ 方法重载：在同一个类中，允许存在一个以上的同名方法，只要它们的参数个数或参数类型不同即可。
+ 方法重写：子类中存在与父类中同名的方法，并且参数列表完全相同，**返回值类型一致且权限不可小于父类方法**，优先级：private > 默认（不写） > protected > public。
## 静态成员
+ 静态成员变量：使用static关键字修饰的成员变量。
+ 静态成员方法：使用static关键字修饰的成员方法。
+ 静态代码块：使用static关键字修饰的代码块。
+ 静态内部类：使用static关键字修饰的内部类。
+ 静态导包：使用import static关键字导入静态成员。
## this与super关键字
+ this代指当前类
+ super代指父类。
## static与final
+ static修饰的XX变量为静态XX，可被该类所有的实例直接通过类名.xxx来访问。
+ static修饰的代码块：只执行一次，且优先于非静态代码块执行,通常用于给类初始，static {},
+ final修饰的类不可继承，修饰方法不可重写，修饰变量基础变量不可修改，引用变量类型不可修改。

## 方法的定义
### 参数范围的限定
#### 通配符？的使用
+ ？表示可接受元素是任意类型的的list对象，此处的list<>为集合定义不是泛型定义。
```java
public static printlist(list<?> list){
    for (Object elem : list1){
        System.out.println(elem);
    }
}
```
#### 上界限定
+ public static printlist(list<? extend Number> list){} // 限定参数为number及其子类。
#### 下界限定
+ public static printlist(list<? super Number> list){} // 限定参数为number及其父类。

### 匿名方法
+ 无需lambda关键字，Comparator\<sting> com = (x,y)->x.length-y.length; 
## 泛型类与方法
### 泛型类
+ 实例
    ```java
    public class Node<T,S>{ //TS都是泛型变量。
        public T data; //T是泛型成员，T只可是引用类型。
        public T get(){}; // 可定义方法
    }
    ```
+ 调用：Node <string> stringnode = new Node<string>();
### 泛型方法
+ 必须在返回值之前指定泛型类型。
+ 实例：
  ```java
  public static <S,T> boolean comp(pair<S,T>p1,pair<S,T>p2){
    return p1.getKey().equals(p2.getKey());
  }
  ```

## 抽象类与接口
### 抽象类（以 abstract修饰）
+ 抽象类不能被实例化，抽象类中可以包含抽象方法，抽象方法没有方法体，可有普通变量、公共静态变量、普通方法。
+ public abstract void eat();//抽象方法, 不可有大括号。
### 接口（将class替换为interface）
+ 其内定义的所有方法都是抽象方法，接口中不能包含普通变量，只能包含常量，接口中不能包含构造方法。
+ 接口中定义的变量默认为public static final，接口中定义的方法默认为public abstract，接口中定义的变量可省略public static final。

## 内部类（定义在另一个类中的类）
### 成员内部类：
+ 定义在另一个类中的成员位置的类。
+ 不能使用start关键字修饰，可访问外部类的所有成员。
+ 在main方法中要创建成员内部类实例，需先创建外部类实例，再创建成员内部类实例。
```java
public class OuterClass{
    private int age;
    public class InnerClass{
        public void print(){
            System.out.println(age);
        }
        
    }
    public static void main(String[] args){
        OuterClass outer = new OuterClass();
        OuterClass.InnerClass inner = outer.new InnerClass();
        inner.print();
    }
}
```
### 静态内部类：
+ 定义在另一个类中的静态位置的类。
+ 不能使用start关键字修饰，可访问外部类的所有成员。
+ 在main方法中要创建静态内部类实例，直接创建即可。
```java
public class OuterClass{
    private int age;
    public static class InnerClass{
        public void print(){
            System.out.println(age);
        }
    }
    public static void main(String[] args){
        OuterClass.InnerClass inner = new OuterClass.InnerClass();
        inner.print();
    }
}
```
### 局部内部类：
+ 定义在方法体或语句块内的类，在块外无法访问，因此不可用修饰符修饰。
### 匿名内部类：
+ 仅仅需要使用一次的类，定义和实例化同时进行，没有类名的类。
+ eg: Typename obj = new Typename(){ };
### 接口内部类：
+ 定义在另一个类中的接口位置的类。

# 常用函数
+ math.random()：返回一个随机数。
  - nextBoolean()：返回一个随机布尔值。
  - nextInt()：返回一个随机整数。
  - nextDouble()：返回一个随机浮点数。
  - nextLong(); 返回一个长整数。

# 常用类
## string（创建后不可修改）
### str创建
+ var str = "string new"
+ var str = new String() //创建一个空字符串
### string常用函数
+ length() //返回字符串长度
+ toCharArray() //转化为字符数组
+ substring(beginIndex,endIndex)//截取being到end字符子串，e
+ nd不写默认为结束
+ indexOf(str，int fromindex,int endindex) //查找字符串位置,fromindex为可选参数指定从fromindex开始查找，endindex结束查找。
+ lastindexOF(str，int fromindex,int endindex) //查找字符串最后一次出现的位置
+ toUpper/toLower //大小写转化
+ equals(str2) //字符串比较
+ concat(str) //链接字符串
+ replace(oldchar,newchar) //替换字符串
+ charAt(index) //返回下标为index的字符串
+ trim() //去除前后空白字符
+ repeat(intX) //返回重复X次的子字符串
+ isEmpty() //判断字符串是否为空,Ture or False
+ isBlank() //判断字符串是否含空白字符，Ture or False
+ strip() //删除前空格和后空格
+ stripLeading() //删除前空格
+ stripTrailing() //删除后空格
## StringBuilder 可变字符串类
### 新增方法
  
# **文件操作与IO流**
## 文件操作
### 特殊点
+ 在Java中\为特殊字符故文件路径：C:\ \Users\ \Administrator\ \Desktop\ \a.txt
+ 字符流要手动刷新，字节流不用
### File类(在Java7之后用path对象代替file类)
+ java.nin.file类
+ 创建path对象：var path1 = Paths.get("D:");
### 常用方法
#### create and delete
+ path = Files.createDirectories(path); //创建路径
+ file = Files.createFile(path1); //创建文件
+ Files.delete(path); //删除指定的文件或空目录，无法删除则抛出异常
+ Files.deleteIfExists(path); //删除指定的文件或空目录，但若文件为空无需抛出异常。
#### 文件属性操作
+ if(!Files.exists(path1)) // 检查path1指向的对象是否存在
+ Files.notexists(path1) //检查path1指向对象是否存在，不存在返回true，若两个都返回false则文件不可检查。
+ isReadable//检查是否可读，isWritable //是否可写，isExecutable//是否可执行。
+ isRegularFile//检查是否为文件，isDirectory //检查是否为目录
+ Files.newDirectoryStream(path1) //获取所有子文件名称
+ size //返回文件字节大小
+ get/setLastModifiedTime // 返回/设置文件最后修改时间。
+ get/setOwener // 返回/设置文件所有者
+ get/setAttribute(path1,string) //返回/设置字符串所指定的文件属性，string可为creationtime获取创建时间
#### copy and move
+ File.copy(path.source ,path.target,option);
  - ATOMIC_MOVE //将移动作为一个原子的文件系统操作
  - COPY_ATTRIBUTES //连属性一起复制
  - REPLACE_EXISTING //若文件存在则将其覆盖
+ copy与流操作
  - copy(in , path1 , option) //将输入流in复制到path文件中
  - copy(path1 , out) //将文件复制到输出流中
+ File.move(path.soure,path.target,option);
  - REPLACE_EXISTING //若目标文件存在移动也不失败。

## IO流（input、output）
+ 分类：字符流、字节流。

|抽象基类|字符流|字节流|
|:--- |:--- |:--- |
|输入流| Reader | InputStream |
|输出流|Writer | OutputStream |
+ 由抽象基类可派生出其他子类。[Javaclass图片](G:\Word-Markdown\Markdown-GitHub\图片\Javaclass.png)

+ 分类：节点流（对特定数据源进行操作）、 包装/处理流（通过对节点流包装为已有的流提供强大处理能力，其有一个Reader/Writer型属性in/out可用于封装一个节点流。））

|分类|字节输入流|字节输出流|字符输入流|字符输出流|
|:--- |:--- |:--- |:--- |:--- |
|节点流抽象基类|InputStream|OutputStream|Reader|Writer|
|访问文件|FileInputStream|FileOutputStream|FileReader|FileWriter|
|访问数组|ByteArrayInputStream|ByteArrayOutputStream|CharArrayReader|CharArrayWriter|
|访问管道|PipedInputStream|PipedOutputStream|PipedReader|PipedWriter|
|访问字符串|--|--|StringReader|StringWriter|
|对象流|ObjectInputStream|ObjectOutputStream|--|--|

|分类|字节输入流|字节输出流|字符输入流|字符输出流|
|:--- |:--- |:--- |:--- |:--- |
|处理流|BufferedInputStream|BufferedOutputStream|BufferedReader|BufferedWriter|
|转换流|--|--|InputStreamReader|OutputStreamWriter|
|抽象基类|FilterInputstream|FilterOutputstream|--|--|
|打印流|--|PrintStream|--|PrintWriter|
|推回输入流|PushbackInputStream|--|PushbackReader|--|
|特殊流|DataInputStream|DataOutputStream|--|--|

### Object对象流,修饰器模式
+ 意义：保存数据时同时保存数据类型，即对象的序列化。
+ 注意事项
   - **反序列化的顺序必须要与序列化的顺序一致** 
   - 加上serialVersionUID序列化版本号，提高兼容性。(private static final long serialVersionUID = 1L;)
   - 序列化时，start和transient修饰的成员不会被序列化。（transient修饰表示禁止序列化，序列化是该成员会被置null）
   - 可序列化属性可被子类继承。
+ 要求：类必须实现两者之一,class dog implements Serializable//implements表示dog类实现了该标记接口。
  - Serializable接口，无方法比较好用，为标记接口。
    + 序列化：ObjectOutputStream.writeObject(Object obj) //将对象序列化到文件中
    + 反序列化：ObjectInputStream.readObject() //从文件中读取对象
  - Externalizable接口
    + 序列化： ObjectOutputStream.writeObject(Object obj) //将对象序列化到文件中
    + 反序列化：ObjectInputStream.readObject() //从文件中读取对象

#### ObjectOutputStream
##### 构造方法
+ ObjectOutputStream(new FileOutputStream(path)) //通过文件路径创建ObjectInputStream对象
##### 常用方法
+ **writeUTF(String str) //写入一个字符串**
+ writeObject(Object obj) //写入一个对象
+ writeBoolean(boolean b) //写入一个布尔值
+ writeChar(char c) //写入一个字符
+ writeDouble(double d) //写入一个double值
+ writeFloat(float f) //写入一个float值
+ writeInt(int i) //写入一个int值
+ writeLong(long l) //写入一个long值
#### ObjectInputStream
##### 构造方法
+ ObjectInputStream(new FileInputStream(path)) //通过文件路径创建ObjectInputStream对象
##### 常用方法
+ **readUTF() //读取一个字符串**
+ readObject() //读取一个对象
+ readBoolean() //读取一个布尔值
+ readChar() //读取一个字符
+ readDouble() //读取一个double值
+ readFloat() //读取一个float值
+ readInt() //读取一个int值
+ readLong() //读取一个long值

### ByteStream字节输入流
#### ByteArrayInputStream
##### 构造方法
+ ByteArrayOutputStream() //创建ByteArrayOutputStream对象
##### 常用方法
+  toCharArray() //将字节数组转换为字符数组
+  toString() //将字节数组转换为字符串
+  toString(String charsetName) //将字节数组转换为指定字符集的字符串
+  write(byte[] b) //写入一个字节数组
+  write(byte[] b,int off,int len) //写入字节数组从off开始到len个字符
+  write(int b) //写入一个字节
#### ByteArrayInputStream
##### 构造方法
+ ByteArrayInputStream(byte[] buf) //创建ByteArrayInputStream对象
##### 常用方法
+  read() //读取一个字节
+  read(byte[] b) //读取一个字节数组
+  read(byte[] b,int off,int len) //读取字节数组从off开始到len个字符
+  skip(n) //跳过N个字符的读取。
+  close() //关闭流

### FileReader字符输入流
+ 构造方法：FileReader(File file/String name) //通过文件对象/路径创建FileReader对象
+ 常用方法：
  + read([char[] a]) //读取一个字符无字符返回-1，可选参数字符数组读取一个数组的字符。
  + new String(char[]) //将字符数组转换为字符串。
  + read([char[] a,int off,int len]) //从数组a的off位置开始读入len个字符
### FileWriter字符输出流
+ 构造方法：FileWriter(File file/String name) //通过文件对象/路径创建FileWriter对象
+ 常用方法：
  + write(File/String str,[true]) //写入一个字符串,ture为可选项表示开启追加模式。
  + write(String str,int off,int len) //写入字符串从off开始到len个字符
  + write(int c) //写入一个字符
  + write(char[] a) //写入一个字符数组
  + write(char[] a,int off,int len) //写入字符数组从off开始到len个字符
  + toCharArray:将字符串转换为字符数组。
  + **flush() //刷新缓冲区，filewrite使用后必须关闭或刷新才会真正写入到文件中**


### InputStream
#### FileInputStream
##### 构造方法
+ FileInputStream(File file/String name) //通过文件对象/路径创建FileInputStream对象
##### 常用方法
+ read([byte[] b]) //无参读取一个字符无字符返回-1，有参读入b.length个字符存入数组，**返回读取字符数。**
+ read([byte[] b,int off,int len]) //从数组b的off位置开始读入len个字符
+ skip(n) //跳过N个字符的读取。
+ close() //关闭流
+ **new String(buf,0,len) //将buf数组中从0开始到len个字符转换成字符串,此为字符串的一个方法。**

#### BufferedInputStreams按字节操作输入处理流
##### 构造方法
+ new BufferedInputStream(new InputStream in,[int size]) //将InputStream包装为BufferedInputStream,用于读取in中的数据,可通过可选参数指定输入缓冲区大小。
##### 常用方法
+ read() //读取一个字节，返回int类型，无字节返回-1。
+ read([byte[] b]) //读取b.length个字节存入数组，返回读取字节个数。
+ read([byte[] b,int off,int len]) //从数组b的off位置开始读入len个字节
+ skip(n) //跳过N个字符的读取。
+ close() //关闭流

#### BufferedReaderStreams按字符操作输入处理流
+ 对输入流进行包装，通过in参数设置可实现对不同类型的输入流的处理。**修饰器模式**
##### 构造方法
+ new BuffereReader(new FileReader("filepath")) //将FileReader包装为BufferedReader,用于读取filepath下的文件。
##### 常用方法
+ readline() //读取一行数据，返回字符串，无数据返回null。
+ readLine([char[] cbuf,int off,int len]) //读取一行数据存入字符数组cbuf中，从off开始到len个字符，返回读取字符数。 
+ read(char[] cbuf) //读取一行数据存入字符数组cbuf中，返回读取字符数。
+ read() //读取一个字符，返回int类型，无字符返回-1。

### OutputStream
#### FileOutputStream
##### 构造方法
+ FileOutputStream(String path,[true]) //true为可选项，表示为追加模式，默认为覆盖模式。
##### 常用方法方法
+ write(int b) //写入一个字节
+ write(byte[] b) //写入b.length个字节。
+ write(byte[] b, readLen) //**利用读取返回值写入数据防止通过此写入多余的错误数据**
+ write("hello world".getBytes()); //getBytes()为将字符串转换为字节数组。

#### BufferedOutputStreams按字节操作输出处理流 
##### 构造方法 
+ new BufferedOutputStream(new OutputStream out,[int size]) //将OutputStream包装为BufferedOutputStream,用于向out中写入数据,可通过可选参数指定输出缓冲区大小。
##### 常用方法 
+ write(int b) //写入一个字节
+ write(byte[] b, off,len) //写入b数组中从off开始到len个字节
+ flash() //刷新缓冲区,将缓冲区数据写入到文件中。


##### BufferedWriterStreams按字符操作输出处理流
+ 对输出流进行包装，通过Out参数设置可实现对不同类型的输出流的处理。**模拟修饰器设计模式**
+ **不要去操作二进制文件可能导致二进制文件损坏**
###### 构造方法
+ new BuffereWriter(new FileWriter("filepath")) //将FileWriter包装为BufferedWriter用于向filepath下的文件写入数据。
###### 常用方法
+ newLine() //写入一个换行符(大小与系统保持一致)。
+ write(String str) //写入一个字符串
+ write(String str,int off,int len) //写入字符串从off开始到len个字符
+ flush() //刷新缓冲区,

### 转化流（解决文件乱码）
+ 节点流：直接与文件等节点进行交互的流。
+ 转化流：将节点流转化为字符流或字节流。
#### InputStreamReader
+ new InputStreamReader(new FileInputStream("filepath"),"utf-8") //将FileInputStream包装为InputStreamReader并以utf-8编码用于读取filepath下的文件
#### OutputStreamWriter
+ new OutputStreamWriter(new FileOutputStream("filepath","gbk")) //将FileOutputStream包装为OutputStreamWriter并以gbk编码用于向filepath下的文件写入数据。

# **Java网络编程**
## 网络基础
+ 网络通信：通过网络实现数据传输，java.net包提供接口。
+ IP可唯一标识网络中的主机。ipv4用4个字节32位表示（一个字节四位）ipv4是IPv6的四倍16个字节，IP地址组成：网络地址+主机地址。ipconfig查看WindowsIP地址。
  - IPv4地址分类：A类（1-126）、B类（128-191）、C类（192-223）、D类（224-239）、E类（240-255）
  - 特殊IP地址：
    - 0.0.0.0：表示本机IP地址
    - 255.255.255.255：表示广播地址
    - 127.0.0.1：表示本机回环地址
+ 端口（port）：用于标识主机进程，即用于绑定具体的程序。
  - 端口分类
    - 公有端口：0~1024（开发不使用因为其已被知名程序占用）
    - 其他端口：1024~65535（开发使用）
    - 常见端口：http：80、Tomcat：8080、MySQL；3306、oracle：1521、SQLserver：1433。
## InetAddress类
### InetAddress重要方法
+ getLocalHost() //获取本地主机地址
+ getByName(String host) //根据主机名(域名)获取InetAddress对象
+ getHostName() //通过InetAddress对象获取主机名（域名）。
+ getHostAddress() //通过InetAddress对象获取IP地址。
+ 输出流的重要方法：write.shutdownOutput()//写入结束标记。

### socket两种编程

#### TCP编程（可靠）

##### 常用CMD指令
+ netstat -an |  more //查看当前网络连接并分页显示
   - 外部地址：有没有外部链接连到本地端口。
   - 状态：listening正在监听， establ lshed已连接
+ netstat -an | findstr 9999 //查看9999端口
+ netstat -anb //查看网络连接并显示使用程序，需要管理员权限。
+ exit//退出控制台
##### socket类(套接口)
+ 定义：通信两段都要有socket类对象，用于建立网络连接，数据在socket中以IO流传输，主动发起请求通常称为客户端。
+ 作用：向socket写入数据，服务器通过监听得到数据。
###### socket重要方法
+ socket = new Socket(host,port) //创建socket对象，host为域名或IP地址，port为端口号。
+ ServerSocket  serverSocket = new  serversocket(9999);//监听9999端口等待客户端连接，前提是9999端口未被监听，否则报端口占用，serversocket对象为服务端的socket对象为保证有多个客户端的连接，可通过accept返回多个socket对象。
+ Socket inputStream = socket.accept() //监听端口，等待客户端建立连接后返回socket对象。
+ OutputStream outputStream = socket.getOutputStream() //获取输出流
+ getInputStream getinputStream = socket.getInputStream() //获取输入流
+ socket.getClass() //获取socket类。
+ outputStream.close() //关闭输出流。
+ outputStream.write(str.getBytes()) //向输出流中写入数据,其中getBytes方法为将str转化为字节数组，**可在()内指定编码方式。最后注意要writeline写入一空行表示结束。**
+ **flush()//写入数据后刷新缓冲区，将数据写入到数据通道中。**
+ 上传文件时先将数据读取到字节数组再写入到流中。
+ socket.close() //关闭socket对象。
+ seversocket.close() //关闭seversocket对象。

#### UDP编程（不可靠，单个数据最大64K,故建立数组大小也可参考）
+ 基本流程：建立发送端和接收端、建立数据包、调用DatagramSocket的发送和接收方法、关闭DatagramSocket。
+ 特点：没有明确的服务端和客户端，仅有接收端和发送端。
+ DatagramSocket：用于发送和接收数据包。
+ DatagramPacket：用于封装数据包，可指定接收端口，接收到后需要拆包。
##### DatagramSocket重要方法 
+ DatagramSocket(int port) //创建DatagramSocket对象，用于处理port端口的数据包。
+ DatagramSocket.send(DatagramPacket dp) //发送数据包（byte[] data = "hellow，明天吃火锅".getBytes(); 将字符串转换为字符数组）
+ DatagramSocket.receive(DatagramPacket packet);//接收数据包,填充到packet对象中。（若没有数据包，会阻塞端口）
##### DatagramPacket重要方法
+ packet = new DatagramPacket (byte[] buf,int length,InetAddress address,int port) //创建DatagramPacket对象，用于发送数据包，buf为数据包内容，length为数据包长度，address为接收端地址(接收端省略)可通过getByName("域名/ip")获取，port为接收端端口(接收端可省略)。
+ byte[] data = DatagramPacket.getData() //获取数据包内容
+ 配合：String str = new String(data,0,data.length) //将字节数组转化为字符串，便于读取。
+ DatagramPacket.getLength() //获取数据包长度






# 多线程
+ 一个进程可以有多个线程，线程是进程创建的。
+ 并发：cup快速轮换执行任务，并行：多核心cup同时执行多个任务。
### 线程使用
#### Thread类（实现了runnable接口）
+ 程序启动后会自动创建主线程即main线程，main线程启动子线程后不会阻塞，会继续执行，但他们都是进程的线程，相互独立。
+ 创建线程方法：继承Thread类，重写run方法，创建线程对象，调用start方法启动线程。
```java
public class MyThread extends Thread{ //继承Thread类,就可当成线程使用

    @Override //此注解表示重写父类方法
    public void run(){ //重写run方法
        //线程任务
    }

}
```
+ 构造方法
  + Thread(String name) //创建线程对象，并指定线程名
  + Thread(Runnable target) //创建线程对象，并指定线程任务(实现了Runnable接口的对象)
  + Thread(Runnable target,String name) //创建线程对象，并指定线程任务和线程名
+ 常用方法
  + setName() //设置线程名
  + getName() //获取线程名
  + currentThread() //获取当前线程对象
  + start() //**启动线程，底层会调用run()方法,不可直接调用run方法，因start会创建线程**
  + run() //线程体
  + setPriority(int newPriority) //设置线程优先级
  + getPriority() //获取线程优先级
  + sleep(long millis) //线程休眠
  + interrupt() //中断线程休眠
  + yield() //线程让步让出cup，但让的时间不一定，故让不一定成功
  + join() //线程插队，插队成功后先会执行完该线程的所有任务
  + isInterrupted() //判断线程是否被中断
  + setDaemon(true) //设置线程为守护线程
+ 注意事项
  + start底层会创建新的线程，run不会。
  + 线程优先级：1-10，默认为5，优先级高不一定先执行，只是概率大。
  + 中断线程，未结束线程，中断一般用于中断正在休眠的线程。
  + 守护线程：后台线程，为其他线程服务，如垃圾回收线程，所有线程退出时守护线程会自动退出。
#### Runnable接口(最终需要配合Thread类使用，**建议使用**)
+ 创建线程方法：实现Runnable接口，重写run方法，创建线程对象（调用thread方法），调用start方法启动线程。（解决了因Java单继承导致的无法继承Thread类又需要创建线程） 
+ **更加适合多个线程共享一个资源的情况，避免了单继承的限制**
```java
public class MyRunnable implements Runnable{ //实现Runnable接口,就可当成线程使用

    @Override //此注解表示重写父类方法
    public void run(){ //重写run方法
        //线程任务
    }

}
```

+ 可为Runnable类封装多个thread实例，共享Runable中剩余票数这个资源，达到开启多个窗口同时进行卖票的目的。
### 线程同步(Synchroized互斥锁)
+ 同步定义：同一数据同时仅有一个线程可访问，用this表示锁
+ 同步方法
  - 同步代码块
    ```java
    synchronized(this){ //得到同步对象，同时仅有一个线程（得到了this锁）可访问。
        //同步代码块
    }
    ```
  - 同步方法
    ```java
    public synchronized void run(){ //表示该方法为同步方法,同时仅有一个线程可访问
        //同步代码块
    }
    ``` 
  - 执行同步时：调用了sleep、yield方法暂停当前线程但是锁不会释放。
  - 执行同步时：其他线程调用了该线程的suspend()方法将该线程挂起，该线程不会释放锁，尽量避免使用suspend和resume方法，易导致死锁。

### 线程终止
+ 通知方式：main线程调用t1.setLoop(false)//设置t1中loop变量通知子线程终止。
+ 调用interrupt方法中断线程，一般用于中断当前线程的休眠（会抛出一个InterruptException异常，用catch捕获后可执行中断后需要进行的操作），sleep用于使当前线程休眠。



# JDBC
## 相关知识
### 实例
+ 实例（需要先导入Java的connector实现包）
```java
Class.forName("com.mysql.jdbc.Driver"); 
// 通过Class.forName方法加载驱动类，Java5以上可省略。

String url = "jdbc:mysql://mysql_ip/data_name？useSSL=false";
// useSSL=false 表示不使用SSL加密,解决安全警告。
String user = "root";
String password = "root";
Connection conn = DriverManager.getConnection(url,user,password);
// 连接数据库

String sql = "select * from 表名";
// 创建SQL语句
Statement stmt = conn.createStatement();
//创建执行SQL的对象
String rs = stmt.executeQuery(sql);
//执行SQL语句,保存在rs中

stmt.close(); //关闭SQL对象
conn.close();//关闭数据库连接。
```
### 相关类
+ Driver接口：提供给数据库供应商的实现接口，**需要自己加载到classPath中**
+ DriverManager类:用于加载驱动类，并获取数据库连接。
+ Connection(实例如conn)：数据库连接对象，用于执行SQL语句。
  - 对象管理
    - Statement(实例如stmt)：普通执行SQL语句的对象，创建为conn.createStatement()。
    - PreparedStatement：预编译执行SQL语句的对象，**防止SQL注入。**，创建为：conn.prepareStatement()。
    - CallableStatement：执行存储过程的对象。
  - Statement类
    - executeQuery(sql)：执行查询语句，返回ResultSet对象。
      - ResultSet(实例如rs)：结果集对象，保存查询结果。
        - next():移动到下一行，返回一个bool值表示是否成功，通常为while(rs.next())。
        - getXxx(int index)：获取指定列的值，index为列的索引，从1开始，Xxx为数据类型。
        - getXxx(String columnName)：获取指定列的值，columnName为列名，，Xxx为数据类型。
        - **通常将查询结果封装到自定义的Account对象中并存于List1集合中便于后续处理**
    - executeUpdate(sql)：执行更新DML/DDL语句，返回int型改变的行数/是否执行成功。
  - PreparedStatement类(extend Statement)：
    - sql注入攻击通过输入字符串，导致SQL语句语义被修改达到攻击目的。（eg:password = " ' or '1' = '1 " 输入后SQL变为username = 'saldg' and password='' or '1' = '1',因为and和or为截断式判断导致表达式为恒真。）
    - 预防：1.SQL语句中的参数用'？'占位符代替。2.使用preparedStatement(sql)创建SQL执行对象(PreparedStatement pst=conn.prepareStatement(sql))。3.设置参数值(pst.setXxx)：setXxx(参数1，参数2)/(参数index,参数);给参数赋值，Xxx为参数类型。4.执行SQL语句
    - 原理：将非法输入中的可作为SQL语句的敏感字符进行转义使其仅作为文本参数,同时预编译先将SQL发送给了服务器可提高性能。
    - **开启使用**：**预编译功能默认不开启需要手动开启,在URL中添加useServerPrepStmts=true** (eg:String url = "jdbc:mysql://mysql_ip/db1?useSSL=false&useServerPrepStmts=true";)
  - 事务管理三个方法(**conn.X调用**)
    - setAutoCommit(boolean false/ture)：设置是否自动提交事务,通常为false保证事务管理的进行。
    - commit()：提交事务。
    - rollback()：回滚事务。
    - **通过try..commit()..catch...rollback()...来实现事务管理**
### 数据库连接池
+ 数据库连接池：用于管理数据库连接的容器，当需要连接数据库时，从连接池中获取一个连接，使用完毕后，将连接放回连接池中。
+ 连接池的优点：
  - 资源重用：避免频繁创建连接，减少系统开销。
  - 更快的系统反应速度.
  - 统一的连接管理，避免数据库连接泄漏。
+ 连接池实现(DataSource接口实现)：
  - Druid(德鲁伊):阿里巴巴创建的连接池，性能高，功能全，使用简单。
    - 导入jar包，直接复制到项目中即可，使用请查看文档。 
  - DBCP:
  - C3P0: