[toc]

***

# SpringBoot3.X
+ 特性：简化开发，简化配置，简化整合，简化部署，简化监控，简化运维
  - 快速创建独⽴ Spring 应用（New project -> Spring init ->选择场景）
    - SSM：导包、写配置、启动运⾏
  - 直接嵌入Tomcat、Jetty or Undertow（⽆需部署 war 包）【Servlet容器】
    - linux java tomcat mysql： war 放到 tomcat 的 webapps下
  - jar： java环境； java -jar
    - 重点：提供可选的starter，简化应用整合
  - **场景启动器（starter）**：web、json、邮件、oss（对象存储）、异步、定时任务、缓存...导包一堆，控制好版本，**简化应用整合**
    - 为每一种场景准备了一个依赖； web-starter。mybatis-starter
  - **重点：按需自动配置 Spring 以及 第三方库**
    - 如果这些场景我要使用（生效）。这个场景的所有配置都会自动配置好。约定⼤于配置：每个场景都有很多默认配置。自定义：配置文件中修改⼏项就可以
  - 提供生产级特性：如 监控指标、健康检查、外部化配置等
    - 监控指标、健康检查（k8s）、外部化配置,⽆代码生成、⽆xml
+ 配置优先级：命令行>配置文件>环境变量>jar包默认设置
  - 配置文件：application.properties、application.yml，使用在当前路径下打开cmd窗口。
+ 高级开发：自定义组件、自定义配置、自定义starter
  - 这个场景自动配置导入了哪些组件，我们能不能Autowired进来使用
  - 能不能通过修改配置改变组件的一些默认参数
  - 需不需要自己完全定义这个组件
  - 场景定制化
+ 默认访问地址：http://localhost:8080/

+ 创建项目：
  - SpringInitalizr -> 选择tools（lambok）、web、SQL等

+ 项目结构：
    ```
    src/
    ├── main/
    │   ├── java/                  // 源代码
    │   │   └── com.example.demo/ 
    │   │       ├── DemoApplication.java   // 主类（入口）
    │   │       ├── controller/     // Web 控制器
    │   │       ├── service/        // 业务逻辑层
    │   │       └── repository/     // 数据访问层
    │   └── resources/             // 配置文件
    │       ├── static/            // 静态资源（HTML/CSS/JS）
    │       ├── templates/         // 模板文件（如 Thymeleaf）
    │       └── application.properties  // 主配置文件
    └── test/                      // 测试代码
    ```
### 开发小技巧
+  lombok：简化JavaBean开发
  - @Data：生成所有构造器、tostring方法、equals、hashCode，若有自定义方法则以自定义方法为准。
  - @Slf4j：生成日志信息
  ```xml
  <dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <scope>compile</scope>
  </dependency>
  ```

## 开发流程
+ 创建 Spring Boot 项目:浏览器发送/hello请求，返回"Hello,Spring Boot 3!"

  ```xml
  <!-- 所有springboot项目都必须继承自 spring-boot-starter-parent -->
  <parent>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-parent</artifactId>
      <version>3.0.5</version>
  </parent>

  <dependencies>
  <!-- web开发的场景启动器 -->
      <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter-web</artifactId>
      </dependency>
  </dependencies>

  <!-- SpringBoot应用打包插件-->
  <build>
      <plugins>
          <plugin>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-maven-plugin</artifactId>
          </plugin>
      </plugins>
  </build>

  ```
+ 开发程序
  ```java
  @SpringBootApplication //这是一个SpringBoot应用,入口程序，固定写法
  public class MainApplication {
      public static void main(String[] args) {
          SpringApplication.run(MainApplication.class,args);
      }
  }

  @RestController//业务逻辑
  public class HelloController {
      @GetMapping("/hello")
      public String hello(){
          return "Hello,Spring Boot 3!";
      }
  }
  ```
+ 打包：mvn clean package 把项目打成可执⾏的jar包
+ java -jar demo.jar 启动项目

## 核心原理
### 控制翻转IOC
+ 控制反转：将对象的创建、管理交给Spring容器，依赖关系由容器管理解耦合，而不是由程序员管理。
  - 组件：spring容器管理的对象，容器负责管理、创建、销毁，无需手动控制实例化组件。
### 依赖注入IO
+ 实现IOC的手段，将依赖关系注入到对象中 
### 约定大于配置
+ 默认配置和约定减少手动配置。
### 内嵌服务器
+ 将依赖打包到应用中，而非部署到服务器，通过springApplication.run()启动内嵌服务器。
### 事件驱动
+ 事件驱动：通过事件监听器、事件发布器实现事件驱动。
  - ApplicationStartedEvent：应用启动事件
  - ApplicationReadyEvent：应用完全事件
  - ContextRefreshedEvent：容器刷新事件
### **自动配置机制**
+ [springboot自动配置流程图](F:\Word-Markdown\Markdown-GitHub\图片\springboot自动配置.png)，导入starter --> 生效xxxxAutoConfiguration --> 组件 --> xxxProperties --> 配置文件
+ 核⼼流程：
  - 导入 starter ，就会导入 autoconfigure 包。
  - autoconfigure 包⾥⾯ 有一个文件 META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports ,⾥⾯指定的所有启动要加载的自动配置类
  - @EnableAutoConfiguration 会自动的把上⾯文件⾥⾯写的所有自动配置类都导入进来。xxxAutoConfiguration 是有条件注解进⾏**按需加载**
  - xxxAutoConfiguration 给容器中导入一堆组件，组件都是从 xxxProperties 中提取属性值
  - xxxProperties ⼜是和配置文件进⾏了绑定效果：导入 starter 、修改配置文件，就能修改底层⾏为。
+ 导入 starter-web ：导入了web开发场景
  - 场景启动器导入了相关场景的所有依赖： starter-json 、 starter-tomcat 、 sp
  ringmvc
  - 每个场景启动器都引入了一个 spring-boot-starter ，核⼼场景启动器。
  - 核⼼场景启动器引入了 spring-boot-autoconfigure 包。
  - spring-boot-autoconfigure ⾥⾯囊括了所有场景的所有配置。
  - 只要这个包下的所有类都能生效，那么相当于SpringBoot官方写好的整合功能就生效了。
  - SpringBoot默认却扫描不到 spring-boot-autoconfigure 下写好的所有配置类。
  （这些配置类给我们做了整合操作），默认只扫描主程序所在的包。
    -  @SpringBootApplication 标注的类就是主程序类，SpringBoot只会扫描主程序所在的包及其下⾯的⼦包，自动的component-scan功能自定义扫描路径@SpringBootApplication(scanBasePackages = "com.atguigu")@ComponentScan("com.atguigu") 直接指定扫描的路径
+ 主程序： @SpringBootApplication
  - SpringBootApplication 由三个注解组成 @SpringBootConfiguration 、 @EnableAutoConfiguratio 、 @ComponentScan
  - SpringBoot默认只能扫描自己主程序所在的包及其下⾯的⼦包，扫描不到 spring-boot-autoconfigure 包中官方写好的配置类
  - @EnableAutoConfiguration ：SpringBoot 开启自动配置的核⼼。
    - 是由 @Import(AutoConfigurationImportSelector.class) 提供功能：批量
    给容器中导入组件。
    - SpringBoot启动会默认加载 142个配置类。
    - 这142个配置类来自于 spring-boot-autoconfigure 下 META-INF/spring/o
    rg.springframework.boot.autoconfigure.AutoConfiguration.import
    s 文件指定的
    - 项目启动的时候利用 @Import 批量导入组件机制把 autoconfigure 包下的142 xx
    xxAutoConfiguration 类导入进来（自动配置类）
  - 按需生效：
    - 虽然导入了 142 个自动配置类并不是这 142 个自动配置类都能生效每一个自动配置类，都有条件注解 @ConditionalOnxxx ，只有条件成⽴，才能生效
+ xxxxAutoConfiguration 自动配置类
  - 给容器中使用@Bean 放一堆组件。
  - 每个自动配置类都可能有这个注解 @EnableConfigurationProperties(ServerProperties.class) ，用来把配置文件中配的指定前缀的属性值封装到 xxxProperties 属性类中
  - 以Tomcat为例：把服务器的所有配置都是以 server 开头的。配置都封装到了属性类中。
  - 给容器中放的所有组件的一些核⼼参数，都来自于 xxxProperties 。 xxxProperties 都是和配置文件绑定。只需要改配置文件的值，核⼼组件的底层参数都能修改 
### 运行机制：
+ SpringApplication.run()启动内嵌服务器，加载配置文件，创建Spring容器，注册组件，初始化事件监听器，启动服务器。

## yaml配置文件.yaml/.yml
+ 基本语法：
  - 大小写敏感
  - 使用缩进表示层级关系，k: v，使用空格分割k,v
  - 缩进时不允许使用Tab键，只允许使用空格。换⾏
  - 缩进的空格数目不重要，只要相同层级的元素左侧对⻬即可
  - \# 表示注释，从这个字符一直到⾏尾，都会被解析器忽略。
+ 细节：
  - 文本，单引号不转义，双引号转义
  - 大文本：以|开头，大文本写在下面，保留文本格式，换⾏符正确显示。以>开头，大文本写在下面，保留文本格式，换⾏符被省略
  - 多文档合并使用 --- 可以把多个yaml文档合并在一个文档中，每个文档区依然认为内容独⽴
+ 数据类型：
  - 对象：键值对的集合，可用{}，如：映射（map）/ 哈希（hash） / 字典（dictionary）
  - 数组：用 - 组按次序排列的值，如：序列（sequence） / 列表（list）
  - 纯量：单个的、不可再分的值，如：字符串、数字、bool、日期
+ eg:
  ```yaml
  person:
    name: 张三
    age: 18
    birthDay: 2010/10/10 12:12:12
    like: true
    child:
      name: 李四
      age: 20
      birthDay: 2018/10/10
      text: ["abc","def"]
    dogs:
      - name: ⼩⿊ #数组以-开头，每个值代表一个数组项
      age: 3
      - name: ⼩⽩
    age: 2
    cats:
      c1:
        name: ⼩蓝
        age: 3
      c2: {name: ⼩绿,age: 2} #对象也可用{}表示
  ```

## 注解驱动
+ SpringBoot摒弃XML配置方式，改为全注解驱动
+ 复合注解可能带来冗余功能，造成性能负担，当仅需要一个功能时，使用颗粒度更小的注解。




### 组件注册：
  - @Configuration：标记配置类
  - @SpringBootConfiguration：
  - @Bean：注册组件
  - @Scope：指定组件的作用域
  - @Controller： 标记类为SpringMVC的控制器用于处理http请求
  - @Service：标记为业务逻辑处理类
  - @Repository：标记为数据访问层组件，用于数据库操作
  - @Component：标记为通用组件
  - @Import：导入配置类
  - @ComponentScan：指定Spring容器扫描的包路径，以自动发现和注册Bean。

### 条件注解
  - @ConditionalOnXxx：当XXX存在，触发组件注册
  - @ConditionalOnMissingXXX：当容器中不存在某个XXX时，触发组件注册
  - @ConditionalOnBean：如果容器中存在这个Bean（组件），则触发指定⾏为
  - @ConditionalOnMissingBean：如果容器中不存在这个Bean（组件），则触发指定⾏为
  - @ConditionalOnBean（value=组件类型，name=组件名字）：判断容器中是否有这个类型的组件，并且名字是指定的值
  - @ConditionalOnClass (org.springframework.boot.autoconfigure.condition)：若存在类，则带有这个注解的配置类或 Bean 就会被加载
  - @ConditionalOnMissingClass (org.springframework.boot.autoconfigure.condition)：若不存在类，则带有这个注解的配置类或 Bean 就会被加载
  - @ConditionalOnBean (org.springframework.boot.autoconfigure.condition)：若存在这个 Bean，则带有这个注解的配置类或 Bean 就会被加载
  - @ConditionalOnMissingBean (org.springframework.boot.autoconfigure.：condition)：若不存在这个 Bean，则带有这个注解的配置类或 Bean 就会被加载
  
  - @ConditionalOnRepositoryType (org.springframework.boot.autoconfigure.data)
  - @ConditionalOnDefaultWebSecurity (org.springframework.boot.autoconfigure.security)
  - @ConditionalOnSingleCandidate (org.springframework.boot.autoconfigure.condition)
  - @ConditionalOnWebApplication (org.springframework.boot.autoconfigure.condition)
  - @ConditionalOnWarDeployment (org.springframework.boot.autoconfigure.condition)
  - @ConditionalOnJndi (org.springframework.boot.autoconfigure.condition)
  - @ConditionalOnResource (org.springframework.boot.autoconfigure.condition)
  - @ConditionalOnExpression (org.springframework.boot.autoconfigure.condition)
  - @ConditionalOnEnabledResourceChain (org.springframework.boot.autoconfigure.web)
  - @ConditionalOnNotWebApplication (org.springframework.boot.autoconfigure.condition)
  - @ConditionalOnProperty (org.springframework.boot.autoconfigure.condition)
  - @ConditionalOnCloudPlatform (org.springframework.boot.autoconfigure.condition)
  - @ConditionalOnMissingFilterBean (org.springframework.boot.autoconfigure.web.servlet)
  - @Profile (org.springframework.context.annotation)
  - @ConditionalOnInitializedRestarter (org.springframework.boot.devtools.restart)
  - @ConditionalOnGraphQlSchema (org.springframework.boot.autoconfigure.graphql)
  - @ConditionalOnJava (org.springframework.boot.autoconfigure.condition)

### 常用注解
+ @Data：是 @Getter、@Setter、@ToString、@EqualsAndHashCode 和 @RequiredArgsConstructor的复合注解，自动生成get、set、toString、equals、hashCode、constructor方法
  - 它是通过在编译时修改AST，来实现的。
  - 注意但有时它生成的方法（特别是 equals, hashCode, toString 包含所有字段）可能不符合你的具体业务需求，需要谨慎使用或使用更细粒度的 Lombok 注解替代。
### 属性绑定
+ @ConfigurationProperties： 声明组件的属性和配置文件哪些前缀开始项进⾏绑定
+ @EnableConfigurationProperties：快速注册注解：
  - 场景：SpringBoot默认只扫描自己主程序所在的包。如果导入第三方包，即使组件上标注了@Component、@ConfigurationProperties 注解，也没用。因为组件都扫描不进来，此时使用这个注解就可以快速进⾏属性绑定并把组件注册进容器  将容器中任意组件（Bean）的属性值和配置文件的配置项的值进⾏绑定
    - 给容器中注册组件（@Component、@Bean）
    - 使用@ConfigurationProperties 声明组件和配置文件的哪些配置项进⾏绑定

## 事件驱动：
+ 发布者-->发布事件-->多个监听者监听事件（监听者仅处理自己感兴趣的事件）-> 处理事件
+ 事件生命周期监听器：springAplicationRunlistener：在应用启动前后做什么。
  - ApplicationXXXlistener：回调监听器：监听一个生命周期的某个阶段，除了Applistener全阶段（基于事件）、SpringAppRunlister全阶段（基于回调）。



## 日志
+ springboot中：导入任何第三方框架，先排除它的日志包，因为Boot底层控制好了日志
  -  修改 application.properties 配置文件，就可以调整日志的所有⾏为。如果不够，可以编写日志框架自己的配置文件放在类路径下就⾏，比如 logback-spring.xml ， log4j2-spring.xml
  -  如需对接专业日志系统，也只需要把 logback 记录的日志灌倒 kafka之类的中间件，这和SpringBoot没关系，都是日志框架自己的配置，修改配置文件即可
+ 使用：**使用lombok可用@Slf4j**，或者在类中定义Logger log = LoggerFactory.getLogger(getClass());
+ 日志级别由低到⾼：ALL,TRACE, DEBUG, INFO(spring默认), WARN, ERROR,FATAL,OFF
  - ALL：打印所有日志
  - TRACE：追踪框架详细流程日志，一般不使用
  - DEBUG：开发调试细节日志
  - INFO：关键、感兴趣信息日志
  - WARN：警告但不是错误的信息日志，比如：版本过时
  - ERROR：业务错误日志，比如出现各种异常
  - FATAL：致命错误日志，比如jvm系统崩溃
  - OFF：关闭所有日志记录
  - 日志生成：仅会打印出当前级别及以上的日志信息，springboot默认级别为INFO。
  -  在application.properties/yaml中配置`logging.level.<logger-name>=<level>`指定日志级别，level可选TRACE, DEBUG, INFO, WARN, ERROR, FATAL, or OFF，定义在LogLevel类中
  - root 的logger-name叫root，可以配置logging.level.root=warn，代表所有未指定日志级别都使用 root 的 warn 级别
### 日志分组：
  - 将相关的logger分组在一起，统一配置。SpringBoot 也⽀持。比如：Tomcat 相关的日志统一设置  
  - springboot中默认两个组，web、sql
  ```yaml
  logging.group.tomcat=org.apache.catalina,org.apache.coyote,org.apache.tomcat
  logging.level.tomcat=trace
  ```
### 日志输出与文件归档
+ 日志输出
  - 默认输出到控制台，可在application.properties中添加logging.file.name 和 logging.file.path配置项
+ 文件归档（一天一个文件）、切割（单个文件小于10MB）
  - 每天的日志应该独⽴分割出来存档。如果使用logback（SpringBoot 默认整合），可以通过application.properties/yaml文件指定日志滚动规则。
  - 如果是其他日志系统，需要自⾏配置（添加log4j2.xml或log4j2-spring.xml）
  - 支持的滚动规则：logging.logback.rollingpolicy.
    - flie-name-pattern：日志文件名，默认是：log.%d{yyyy-MM-dd}.%i.log
    - max-history：日志文件保留天数，默认是：7
    - total-size-cap：日志文件总大小，默认是：10GB，大于后会删除最旧的文件
    - max-file-size：单个日志文件大小，默认是：10MB，超过后会滚动
### 实战
+ 导入任何第三方框架，先排除它的日志包，因为Boot底层控制好了日志
+ 修改 application.properties 配置文件，就可以调整日志的所有⾏为。如果不够，可以编写日志框架自己的配置文件放在类路径下就⾏，比如 logback-spring.xml ， log4j2-spring.xml
+ 如需对接专业日志系统，也只需要把 logback 记录的日志灌倒 kafka之类的中间件，这和SpringBoot没关系，都是日志框架自己的配置，修改配置文件即可
+ 业务中使用slf4j-api记录日志。不要再 sout 了

### 自定义配置：
+ 配置
  - Spring如果使用标准配置文件，spring 无法完全控制日志初始化,**springboot写日志配置，配置文件名加上 xx-spring.xml**
  - log4j2支持yaml、json格式的配置文件
  
  |日志系统|自定义|
  |:--|:--|
  |logback|logback-spring.xml、logback-spring.groovy、logback.xml、logback.groovy|
  |log4j2|log4j2-spring.xml、log4j2.xml|
  |JDK(Java Util Logging)|logging.properties|
+ 切换日志组合 
  - maven
  ```xml
  <dependencies>
      <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter-web</artifactId>
      </dependency>
      <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter</artifactId>
          <exclusions>
              <exclusion>
                  <groupId>org.springframework.boot</groupId>
                  <artifactId>spring-boot-starter-logging</artifactId>
              </exclusion>
          </exclusions>
      </dependency>
      <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter-log4j2</artifactId>
      </dependency>
  </dependencies>
  ``` 
  
### spring日志底层：
+ Spring使用commons-logging作为内部日志，但底层日志实现是开放的。可对接其他日志框架。
+ SpringBoot怎么把日志默认配置好的
  - 每个 starter 场景，都会导入一个核⼼场景 spring-boot-starter核⼼场景引入了日志的所用功能 spring-boot-starter-logging
  - 默认使用了 logback + slf4j 组合作为默认底层日志
  - 日志是系统一启动就要用，xxxAutoConfiguration 是系统启动好了以后放好的组件，后来用的。
  - 日志是利用监听器机制配置好的，ApplicationListener 
  - 日志所有的配置都可以通过修改配置文件实现。以 logging 开始的所有配置

### 日志格式：
+ 时间+级别+ 进程ID+“---”+线程名+类名+logger名(产生日志的类名)+日志内容
```
2023-03-31T13:56:17.511+08:00 INFO 4944 --- [ main] o.apache.cat
alina.core.StandardService : Starting service [Tomcat]
2023-03-31T13:56:17.511+08:00 INFO 4944 --- [ main] o.apache.cat
alina.core.StandardEngine : Starting Servlet engine: [Apache Tomcat/10.0.0-M17]
```

## springboot3-web开发
### web场景
+ 导入web场景的starter
  ```xml
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
  ```
  - 流程：引入了autoconfing功能，@EnableAutoConfiguration 注解使用 @Import(AutoConfigurationImportSelector.class) 批量导入组件，加载 META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports 文件中配置的所有组件，绑定了配置文件中的配置。
+ 默认效果
  - 包含了 ContentNegotiatingViewResolver 和 BeanNameViewResolver 组件，方便视图解析
  - 默认的静态资源处理机制： 静态资源放在 static 文件夹下即可直接访问
  - 自动注册了 Converter,GenericConverter,Formatter组件，适配常⻅数据类型转换和格式化需求
  - ⽀持 HttpMessageConverters，可以方便返回json等数据类型
  - 注册 MessageCodesResolver，方便国际化及错误消息处理
  - ⽀持 静态 index.html
  - 自动使用ConfigurableWebBindingInitializer，实现消息处理、数据绑定、类型转化、数据校验等功能
+ 默认配置相关
  -如果想保持 boot mvc 的默认配置，并且自定义更多的 mvc 配置，如：interceptors,formatters, view controllers 等。可以使用@Configuration注解添加一个WebMvcConfigurer 类型的配置类，并不要标注 @EnableWebMvc
  - 如果想保持 boot mvc 的默认配置，但要自定义核⼼组件实例，⽐如：RequestMappingHandlerMapping, RequestMappingHandlerAdapter, 或ExceptionHandlerExceptionResolver，给容器中放一个 WebMvcRegistrations 组件即可
  - 如果想全⾯接管 Spring MVC，@Configuration 标注一个配置类，并加上@EnableWebMvc注解，实现 WebMvcConfigurer 接⼝

#### 静态资源
+ 静态资源映射（默认，映射规则在 WebMvcAutoConfiguration 中）
  - /webjars/** 的所有路径 资源都在 classpath:/META-INF/resources/webjars/
  -  /** 的所有路径 资源都在 classpath:/META-INF/resources/、classpath:/resources/、classpath:/static/、classpath:/public/
  - 所有静态资源都定义了缓存规则。【浏览器访问过一次，就会缓存一段时间】，但此功能参数⽆默认值
    - period： 缓存间隔。 默认 0S；
    - cacheControl：缓存控制。 默认⽆；
    - useLastModified：是否使用lastModified头。 默认 false；
+ 欢迎页(规则在 WebMvcAutoConfiguration 中)
  - 在静态资源目录下找 index.html
  - 没有就在 templates下找index模板⻚
+ Favicon
  - 在静态资源目录下找 favicon.ico
+ 自定义静态资源路径(配置文件版)
  - spring.mvc:： 静态资源访问前缀路径
  - spring.web ：
    - 静态资源⽬录
    - 静态资源缓存策略
  ```java
  #1、spring.web：
  # 1.配置国际化的区域信息
  # 2.静态资源策略(开启、处理链、缓存)
  #开启静态资源映射规则
  spring.web.resources.add-mappings=true
  #设置缓存
  spring.web.resources.cache.period=3600
  ##缓存详细合并项控制，覆盖period配置：
  ## 浏览器第一次请求服务器，服务器告诉浏览器此资源缓存7200秒，7200秒以内的所有此资源访问不用
  发给服务器请求，7200秒以后发请求给服务器
  spring.web.resources.cache.cachecontrol.max-age=7200
  ## 共享缓存
  spring.web.resources.cache.cachecontrol.cache-public=true
  #使用资源 last-modified 时间，来对⽐服务器和浏览器的资源是否相同没有变化。相同返回 304
  spring.web.resources.cache.use-last-modified=true
  #自定义静态资源文件夹位置
  spring.web.resources.static-locations=classpath:/a/,classpath:/b/,classpath:/s
  tatic/
  #2、 spring.mvc
  ## 2.1. 自定义webjars路径前缀
  spring.mvc.webjars-path-pattern=/wj/**
  ## 2.2. 静态资源访问路径前缀
  spring.mvc.static-path-pattern=/static/**
  ```
+ 自定义静态资源路径(代码方式)
  ```java
  // 容器中只要有一个 WebMvcConfigurer 组件。配置的底层⾏为都会生效
  // @EnableWebMvc //禁用boot的默认配置

  @Configuration // 这是一个配置类
  public class MyConfig implements WebMvcConfigurer {
      @Override
      public void addResourceHandlers(ResourceHandlerRegistry registry) {
          // 保留以前规则
          // 自己写新的规则
          registry.addResourceHandler("/static/**")
                  .addResourceLocations("classpath:/a/", "classpath:/b/")
                  .setCacheControl(CacheControl.maxAge(1180, TimeUnit.SECONDS));
      }
  }

  @Configuration // 这是一个配置类,给容器中放一个 WebMvcConfigurer 组件，就能自定义底层
  public class MyConfig /*implements WebMvcConfigurer*/ {
      @Bean
      public WebMvcConfigurer webMvcConfigurer() {
          return new WebMvcConfigurer() {
              @Override
              public void addResourceHandlers(ResourceHandlerRegistry registry) {
                  registry.addResourceHandler("/static/**")
                          .addResourceLocations("classpath:/a/", "classpath:/b/")
                          .setCacheControl(CacheControl.maxAge(1180, TimeUnit.SECONDS));
              }
          };
      }
  }
  ```
#### 路径匹配
+ 使用默认的路径匹配规则，是由 PathPatternParser 提供的
+ 如果路径中间需要有 **，替换成ant⻛格路径
+ 切换：
  ```xml
  # 改变路径匹配策略：
  # ant_path_matcher ⽼版策略；
  # path_pattern_parser 新版策略；
  spring.mvc.pathmatch.matching-strategy=ant_path_matcher
  ```
##### Ant风格路径匹配 
+ *：表示任意数量的字符。
+ ?：表示任意一个字符。
+ **：表示任意数量的⽬录,
  - /folder2/**/*.jsp 匹配在folder2⽬录下任意⽬录深度的.jsp文件。
  - /folder1/*/*.java 匹配在folder1⽬录下的任意两级⽬录下的.java文件。
+ {}：表示一个命名的模式占位符。
  - /{type}/{id}.html 匹配任意文件名为{id}.html，在任意命名的{type}⽬录下的文件
+ []：表示字符集合，例如\[a-z]表示⼩写字母
+ 注意：特殊字符需要转义，*、？等
#####  PathPatternParser风格路径匹配 
+ **特殊**
  - PathPatternParser 在 jmh 基准测试下，有 6~8 倍吞吐量提升，降低 30%~40%空间分配率
  - PathPatternParser 兼容 AntPathMatcher语法，并⽀持更多类型的路径模式
  - **PathPatternParser "\**" 多段匹配的⽀持仅允许在模式末尾使用**


### web-AutoConfig
+ 生效条件
  ```java
  @AutoConfiguration(after = { DispatcherServletAutoConfiguration.class, TaskExecutionAutoConfiguration.class,
    ValidationAutoConfiguration.class }) //在这些自动配置之后
  @ConditionalOnWebApplication(type = Type.SERVLET) //如果是web应用就生效，类型SERVLET、REACTIVE 响应式web
  @ConditionalOnClass({ Servlet.class, DispatcherServlet.class, WebMvcConfigurer.class })
  @ConditionalOnMissingBean(WebMvcConfigurationSupport.class) //容器中没有这个Bean，才生效。默认就是没有
  @AutoConfigureOrder(Ordered.HIGHEST_PRECEDENCE + 10)//优先级
  @ImportRuntimeHints(WebResourcesRuntimeHints.class)
  public class WebMvcAutoConfiguration {
  }
  ```
+ 效果
  - 放了两个fliter
    - HttpTraceFilter：页面表单提交Rest请求（GET、POST、PUT、DELETE）
    - WebContentInterceptor：表单内容Filter，GET（数据放URL后⾯）、POST（数据放请求体）请求可以携带数据，PUT、DELETE 的请求体数据会被忽略
  - 放于WebMvcConfigurer组件：给springMVC添加定制功能
    - 所有的功能最终与配置文件进行绑定，通过配置文件修改默认配置
    - WebMvcProperties：spring.mvc配置文件
    - WebProperties：spring.web配置文件

### WebMvcConfiguration接口,功能主要使用这些方法
```java 
addArgumentResolvers(List<HandlerMethodArgumentResolver>):void //参数解器
addCorsMappings(CorsRegistry):void //跨域
addFormatters(FormatterRegistry):void //格式化器
addInterceptors(InterceptorRegistry):void //拦截器
addResourceHandlers(ResourceHandlerRegistry):void //添加资源处理器: 处理静态资源映射
addReturnValueHandlers(List<HandlerMethodReturnValueHandler>):void //返回值处理器
addViewControllers(ViewControllerRegistry):void //视图控制器 xxx.html 页面
configureAsyncSupport(AsyncSupportConfigurer):void //异步支持
configureContentNegotiation(ContentNegotiationConfigurer):void //内容协商
configureDefaultServletHandling(DefaultServletHandlerConfigurer):void //默认处理 默认接受 /
configureHandlerExceptionResolvers(List<HandlerExceptionResolver>):void //配置异常解析器
configureMessageConverters(List<HttpMessageConverter<?>>):void //消息转化器
configurePathMatch(PathMatchConfigurer):void //路径匹配
configureViewResolvers(ViewResolverRegistry):void //视图解析
extendHandlerExceptionResolvers(List<HandlerExceptionResolver>):void //扩展: 异常解析器
extendMessageConverters(List<HttpMessageConverter<?>>):void//扩展: 消息转换
getMessageCodesResolver():MessageCodesResolver
getValidator():Validator 
```

### spring-web静态资源
```java
//规则源码
@Override
public void addResourceHandlers(ResourceHandlerRegistry registry) {
    if (!this.resourceProperties.isAddMappings()) {
        logger.debug("Default resource handling disabled");
        return;
    }
    // 1、
    addResourceHandler(registry, this.mvcProperties.getWebjarsPathPattern(),
            "classpath:/META-INF/resources/webjars/");
    addResourceHandler(registry, this.mvcProperties.getStaticPathPattern(), (registration) -> {
        registration.addResourceLocations(this.resourceProperties.getStaticLocations());
        if (this.servletContext != null) {
            ServletContextResource resource = new ServletContextResource(this.servletContext, SERVLET_LOCATION);
            registration.addResourceLocations(resource);
        }
    });
}
```
+ 规则一：访问： /webjars/** 路径就去 classpath:/META-INF/resources/webjars/ 下找资源.
  - maven 导入依赖 
+ 规则⼆：访问： /** 路径就去 静态资源默认的四个位置找资源
  - classpath:/META-INF/resources/
  - classpath:/resources/
  - classpath:/static/
  - classpath:/public/
+ 规则三：静态资源默认都有缓存规则的设置
  - 所有缓存的设置，直接通过配置文件： spring.web
  - cachePeriod： 缓存周期； 多久不用找服务器要新的。 默认没有，以s为单位
  - cacheControl： HTTP缓存控制；https://developer.mozilla.org/zhCN/docs/Web/HTTP/Caching
  - useLastModified：是否使用最后一次修改。配合HTTP Cache规则,如果浏览器访问了一个静态资源 index.js ，如果服务这个资源没有发生变化，下次访问的时候就可以直接让浏览器用自⼰缓存中的东⻄，⽽不用给服务器发请求。

### EnableWebMvcConfiguration源码
```java
//SpringBoot 给容器中放 WebMvcConfigurationSupport 组件。
//我们如果自⼰放了 WebMvcConfigurationSupport 组件，Boot的WebMvcAutoConfiguration都会失效。
@Configuration(proxyBeanMethods = false)
@EnableConfigurationProperties(WebProperties.class)
public static class EnableWebMvcConfiguration extends DelegatingWebMvcConfiguration implements ResourceLoaderAware
{

}
```
+ HandlerMapping ： 根据请求路径 /a 找那个handler能处理请求
  - WelcomePageHandlerMapping ：
    - 访问 /** 路径下的所有请求，都在以前四个静态资源路径下找，欢迎⻚也一样
    - 找 index.html ：只要静态资源的位置有一个 index.html 页面，项目启动默认访问

+ 为什么容器中放一个 WebMvcConfigurer 就能配置底层⾏为?
  - WebMvcAutoConfiguration 是一个自动配置类，它⾥⾯有一个 EnableWebMvcConfiguration
  - EnableWebMvcConfiguration 继承与 DelegatingWebMvcConfiguration ，这两个都生效
  - DelegatingWebMvcConfiguration 利用 DI 把容器中 所有 WebMvcConfigurer 注入进来
  - 别⼈调用 DelegatingWebMvcConfiguration的方法配置底层规则，⽽它调用所有 WebMvcConfigurer 的配置底层方法。

### web安全
+ 1. 认证
  - ApplicationConfigureradpter
  - samlesecurAppliction
+ 2. 授权
  - 指定什么请求需要什么权限
+ 3. 攻击防护
  - 

### 内容协商（多端内容适配）
+ 根据需求将数据转换为不同格式，如json、xml、html等，后返回。（浏览器常用xml、手机常用json）
+ 基于请求头（默认开启）
  - 客户端向服务端发送请求，携带HTTP标准的Accept请求头，Accept: application/json 、 text/xml 、 text/yaml
+ 基于请求参数（默认关闭）
  - 客户端向服务端发送请求，携带参数格式，如：http://localhost:8080/user?format=json，服务端根据参数格式返回对应数据。
+ eg：xml、json内容协商
  - 基于请求头
  ```java
  <dependency>
    <groupId>com.fasterxml.jackson.dataformat</groupId>
    <artifactId>jackson-dataformat-xml</artifactId>
  </dependency>

  @JacksonXmlRootElement // 可以写出为xml文档
  @Data
  public class Person {
    private Long id;
    private String userName;
    private String email;
    private Integer age;
  }
  ```
  - 基于请求参数
  ```java
  //开启基于请求参数的内容协商功能。 默认参数名：format。 默认此功能不开启
  spring.mvc.contentnegotiation.favor-parameter=true
  //指定内容协商时使用的参数名。默认是 format，修改为type,用type参数指定返回格式
  spring.mvc.contentnegotiation.parameter-name=type
  //自定义内容类型,新增一种媒体类型     
  spring.mvc.contentnegotiation.media-types.yaml=text/yaml
  ```
#### 自定义内容返回
+ 配置媒体类型⽀持:
  - spring.mvc.contentnegotiation.media-types.yaml=text/yaml
+ 编写对应的 HttpMessageConverter ，要告诉Boot这个⽀持的媒体类型
+ 把MessageConverter组件加入到底层
  - 容器中放一个` WebMvcConfigurer ` 组件，并配置底层的 MessageConverter

+ 增加yaml返回支持
  - 导入依赖
    ```xml
    <dependency>
      <groupId>com.fasterxml.jackson.dataformat</groupId>
      <artifactId>jackson-dataformat-yaml</artifactId>
    </dependency>
    ```
  - 把对象写出为yaml格式
    ```java
    public static void main(String[] args) throws JsonProcessingException {
        // Create and populate Person object
        Person person = new Person();
        person.setId(1L);
        person.setUserName("张三");
        person.setEmail("aaa@qq.com");
        person.setAge(18);

        // Configure YAML factory
        YAMLFactory factory = new YAMLFactory()
                .disable(YAMLGenerator.Feature.WRITE_DOC_START_MARKER);

        // Create ObjectMapper with YAML factory
        ObjectMapper mapper = new ObjectMapper(factory);

        // Serialize to YAML string
        String yamlString = mapper.writeValueAsString(person);

        // Print the result
        System.out.println(yamlString);
    }
    ```
  - 编写配置：`spring.mvc.contentnegotiation.media-types.yaml=text/yaml`
  - 编写HttpMessageConverter
    ```java
    @Bean
    public WebMvcConfigurer webMvcConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            // 配置一个能把对象转为 YAML 的 MessageConverter
            public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
                converters.add(new MyYamlHttpMessageConverter());
            }
        };
    }
    ```
+ eg：HttpMessageConverter的示例
  ```java
  public class MyYamlHttpMessageConverter extends AbstractHttpMessageConverter<Object> {
      private ObjectMapper objectMapper = null; // 用于将对象转换为YAML

      public MyYamlHttpMessageConverter() {
          // 告诉Spring Boot这个MessageConverter支持哪种媒体类型
          super(new MediaType("text", "yaml", Charset.forName("UTF-8")));
          
          YAMLFactory factory = new YAMLFactory()
                  .disable(YAMLGenerator.Feature.WRITE_DOC_START_MARKER);
          this.objectMapper = new ObjectMapper(factory);
      }

      @Override
      protected boolean supports(Class<?> clazz) {
          // 支持所有对象类型，不包括基本类型
          return !clazz.isPrimitive();
      }

      @Override
      protected Object readInternal(Class<?> clazz, HttpInputMessage inputMessage)
              throws IOException, HttpMessageNotReadableException {
          // 从输入流中读取YAML并转换为Java对象
          try {
              return objectMapper.readValue(inputMessage.getBody(), clazz);
          } catch (Exception e) {
              throw new HttpMessageNotReadableException("Could not read YAML: " + e.getMessage(), inputMessage, e);
          }
      }

      @Override
      protected void writeInternal(Object methodReturnValue, HttpOutputMessage outputMessage)
              throws IOException, HttpMessageNotWritableException {
          // 将Java对象转换为YAML并写入输出流
          try (OutputStream os = outputMessage.getBody()) {
              objectMapper.writeValue(os, methodReturnValue);
          } catch (Exception e) {
              throw new HttpMessageNotWritableException("Could not write YAML: " + e.getMessage(), e);
          }
      }
  }
  ```
#### 内容协商原理
+ @ResponseBody 由 HttpMessageConverter 处理，标注了 @ResponseBody 的返回值 将会由⽀持它的 HttpMessageConverter 写给浏览器
  - 请求进来先来到 DispatcherServlet 的 doDispatch() 进⾏处理
  - 找到一个 HandlerAdapter 适配器。利用适配器执⾏⽬标方法
  - RequestMappingHandlerAdapter 来执⾏，调用 invokeHandlerMethod（） 来执⾏⽬标方法
  - ⽬标方法执⾏之前，准备好两个东⻄
    - HandlerMethodArgumentResolver ：参数解析器，确定⽬标方法每个参数值
    - HandlerMethodReturnValueHandler ：返回值处理器，确定⽬标方法的返回值改怎么处理
  - RequestMappingHandlerAdapter ⾥⾯的 invokeAndHandle() 真正执⾏⽬标方法
  - ⽬标方法执⾏完成，会返回返回值对象
  - 找到一个合适的返回值处理器 HandlerMethodReturnValueHandler
  - 最终找到 RequestResponseBodyMethodProcessor 能处理 标注了 @ResponseBody 注解的方法
  - RequestResponseBodyMethodProcessor 调用 writeWithMessageConverters ,利用 MessageConverter 把返回值写出去
+ HttpMessageConverter 会先进⾏内容协商
  - 遍历所有的 MessageConverter 看谁⽀持这种内容类型的数据
  - 默认 MessageConverter 有以下
    - ByteArrayHttpMessageConverter ： ⽀持字节数据读写
    - StringHttpMessageConverter ： ⽀持字符串读写
    - ResourceHttpMessageConverter ：⽀持资源读写
    - ResourceRegionHttpMessageConverter : ⽀持分区资源写出
    - AllEncompassingFormHttpMessageConverter ：⽀持表单xml/json读写
    - MappingJackson2HttpMessageConverter ： ⽀持请求响应体Json读写
  - 最终因为要 json 所以 MappingJackson2HttpMessageConverter ⽀持写出json
  - jackson用 ObjectMapper 把对象写出去

### 模板引擎：
+ 由于 SpringBoot 使用了嵌入式 Servlet 容器。所以 JSP 默认是不能使用的。
+ 前后端不分离：如果需要服务端页面渲染，优先考虑使用 模板引擎。
+ 模板引擎页面默认放在 src/main/resources/templates，[Thymeleaf官⽹](https://www.thymeleaf.org/)
+ SpringBoot 包含以下模板引擎的自动配置
  - FreeMarker
  - Groovy
  - Thymeleaf
  - Mustache
+ Thymeleaf整合
  ```xml
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
  </dependency>
  ```
  - 开启了 org.springframework.boot.autoconfigure.thymeleaf.ThymeleafAutoConfiguration自动配置
  - 属性绑定在 ThymeleafProperties 中，对应配置文件 spring.thymeleaf 内容
  - 所有的模板页面默认在 classpath:/templates 文件夹下
  - 默认效果
    - 所有的模板页面在 classpath:/templates/ 下⾯找
    - 找后缀名为 .html 的页面





















#### th语法
+ **th:xxx ：动态渲染指定的 html 标签属性值、或者th指令（遍历、判断等）**
  - th:text ：标签体内文本值渲染
    - th:utext ：不会转义，显示为html原本的样⼦。 
  - th:属性 ：标签指定属性渲染
  - th:attr ：标签任意属性渲染
  - th:if th:each ... ：其他th指令
  ```java
  <p th:text="${content}">原内容</p>
  <a th:href="${url}">登录</a>
  <img src="../../images/gtvglogo.png"
  th:attr="src=@{/images/gtvglogo.png},title=#{logo},alt=#{logo}" />
  ```
+ 变量使用：$/*{}
```xml
<div th:object="${session.user}">
   <p>Name: <span th:text="*{firstName}">Sebastian</span>.</p>  
</div>

<div>
  <p>Name: <span th:text="${session.user.firstName}">Sebastian</span>.</p>
</div>
```
+ 表达式X{}：用于动态取值
  - $ ：变量取值；使用model共享给页面的值都直接用
  - @ ：url路径；
  - #{} ：国际化消息
  - ~ ：⽚段引用
  - * ：变量选择：需要配合th:object绑定对象
+ th系统⼯具&内置对象
  - param ：请求参数对象
  - session ：session对象
  - application ：application对象
  - #execInfo ：模板执⾏信息
  - #messages ：国际化消息
  - #uris ：uri/url⼯具
  - #conversions ：类型转换⼯具
  - #dates ：⽇期⼯具，是 java.util.Date 对象的⼯具类
  - #calendars ：类似#dates，只不过是 java.util.Calendar 对象的⼯具类
  - #temporals ： JDK8+ java.time API ⼯具类
  - #numbers ：数字操作⼯具
  - #strings ：字符串操作
  - #objects ：对象操作
  - #bools ：bool操作
  - #arrays ：array⼯具
  - #lists ：list⼯具
  - #sets ：set⼯具
  - #maps ：map⼯具
  - #aggregates ：集合聚合⼯具（sum、avg）
  - #ids ：id生成⼯具

#### th操作：可以嵌套组合
+ 文本操作：
  - 拼串： +
  - 文本替换：| The name is ${name} |
+ 布尔操作：
  - ⼆进制运算： and,or
  - 取反：!,not
+ 比较运算
  - ⽐较：>，<，<=，>=（gt，lt，ge,le）
  - 等值运算：==,!=（eq，ne）
+ 条件运算：
  - if-then： (if)?(then)
  - if-then-else: (if)?(then):(else)
  - default: (value)?:(defaultValue)
+ 特殊语法：无操作：_
+ eg：
  ```xml
  'User is of type ' + (${user.isAdmin()} ? 'Administrator' : (${user.type} ?:
  'Unknown'))
  ```
#### th属性设置：
  - th:href="@{/product/list}"
  - th:attr="class=${active}"
  - th:attr="src=@{/images/gtvglogo.png},title=${logo},alt=#{logo}"
  - th:checked="${user.active}"

#### th遍历/if/switch
+ th:each="元素名,迭代状态 : ${集合}"
  ```xml
  <tr th:each="prod : ${prods}">
  <td th:text="${prod.name}">Onions</td>
  <td th:text="${prod.price}">2.41</td>
  <td th:text="${prod.inStock}? #{true} : #{false}">yes</td>
  </tr>
  <tr th:each="prod,iterStat : ${prods}" th:class="${iterStat.odd}? 'odd'">
  <td th:text="${prod.name}">Onions</td>
  <td th:text="${prod.price}">2.41</td>
  <td th:text="${prod.inStock}? #{true} : #{false}">yes</td>
  </tr>
  ```
  + iterStat 有以下属性：
    - index：当前遍历元素的索引，从0开始
    - count：当前遍历元素的索引，从1开始
    - size：需要遍历元素的总数量
    - current：当前正在遍历的元素对象
    - even/odd：是否偶数/奇数⾏
    - first：是否第一个元素
    - last：是否最后一个元素

+ th:if
  ```xml
  <a
  href="comments.html"
  th:href="@{/product/comments(prodId=${prod.id})}"
  th:if="${not #lists.isEmpty(prod.comments)}"
  >view</a>
  ```
+ th:switch
  ```xml
  <div th:switch="${user.role}">
  <p th:case="'admin'">User is an administrator</p>
  <p th:case="#{roles.manager}">User is a manager</p>
  <p th:case="*">User is some other thing</p>
  </div>
  ```
#### th属性优先级
+ 片段(th:insert/replace)>
  - 遍历>
  - th:if th:unless th:switchth:case>
  - th:object th:with>
  - th:attr th:attrprepend th:attrappend>
  - th:value th:href th:src ...>
  - th:text th:utext>
  - th:fragment>
  - th:remove

#### th:fragment模板布局：导航栏制作
+ 作用：定义模板，可以复用，在web中用于导航栏制作
+ 使用
  - 定义模板： th:fragment
  - 引用模板： ~{templatename::selector}
  - 插入模板： th:insert 、 th:replace
+ web导航栏制作
  ```xml
  <!-- 定义模板 -->
  <div th:fragment="copy">
    &copy; 2011 The Good Thymes Virtual Grocery
  </div>
  <!-- 引用模板 -->
  <div th:insert="footer :: copy"></div>
  <div th:replace="footer :: copy"></div>
  <div th:include="footer :: copy"></div>
  <!-- 三个效果 -->
  <!-- <div>
    <div>
      &copy; 2011 The Good Thymes Virtual Grocery
    </div>
  </div>
  <div>
    &copy; 2011 The Good Thymes Virtual Grocery
  </div>
  <div>&copy; 2011 The Good Thymes Virtual Grocery</div> -->
  ```
### 国际化： MessageSourceAutoConfiguration
+ Spring Boot 在类路径根下查找messages资源绑定文件。文件名为：messages.properties
+ 多语⾔可以定义多个消息文件，命名为 messages_区域代码.properties 。如：
  - messages.properties ：默认
  - messages_zh_CN.properties ：中文环境
  - messages_en_US.properties ：英语环境
+ 在程序中可以自动注⼊ MessageSource 组件，获取国际化的配置项值
+ 在页面中可以使用表达式 #{} 获取国际化的配置项值
  ```java
  @Autowired // 国际化取消息用的组件
  private MessageSource messageSource;

  @GetMapping("/haha")
  public String haha(HttpServletRequest request) {
      // 获取请求的 Locale（语言环境）
      Locale locale = request.getLocale();
      
      // 利用代码的方式获取国际化配置文件中指定的配置项的值
      String login = messageSource.getMessage("login", null, locale);
      
      return login;
  }
  ```

### 错误处理
+ 错误处理的自动配置都在 ErrorMvcAutoConfiguration 中，两⼤核⼼机制：
  - SpringBoot 会自适应处理错误，响应页面或JSON数据
  - SpringMVC的错误处理机制依然保留，MVC处理不了，才会交给boot进⾏处理

+ [错误处理原理图]("F:\Word-Markdown\Markdown-GitHub\图片\springweb错误处理.png")

+ 发生错误以后，转发给/error路径，SpringBoot在底层写好一个BasicErrorController的组件，专⻔处理这个请求
  ```java
  // 返回 HTML 格式的错误页面
  @RequestMapping(produces = MediaType.TEXT_HTML_VALUE)
  public ModelAndView errorHtml(HttpServletRequest request, HttpServletResponse response) {
      // 获取 HTTP 状态码
      HttpStatus status = getStatus(request);
      
      // 获取错误属性并构建不可修改的模型
      Map<String, Object> model = Collections.unmodifiableMap(
          getErrorAttributes(request, getErrorAttributeOptions(request, MediaType.TEXT_HTML))
      );
      
      // 设置响应状态码
      response.setStatus(status.value());
      
      // 解析错误视图，如果解析失败则返回默认的 error 视图
      ModelAndView modelAndView = resolveErrorView(request, response, status, model);
      return (modelAndView != null) ? modelAndView : new ModelAndView("error", model);
  }

  // 返回 JSON 格式的错误信息
  @RequestMapping
  public ResponseEntity<Map<String, Object>> error(HttpServletRequest request) {
      // 获取 HTTP 状态码
      HttpStatus status = getStatus(request);
      
      // 如果状态码是 NO_CONTENT，则直接返回状态码
      if (status == HttpStatus.NO_CONTENT) {
          return new ResponseEntity<>(status);
      }
      
      // 获取错误属性并构建响应体
      Map<String, Object> body = getErrorAttributes(request, getErrorAttributeOptions(request, MediaType.ALL));
      
      // 返回包含错误信息的 ResponseEntity
      return new ResponseEntity<>(body, status);
  }
  ```

+ 错误页面是这么解析到的
  ```java
  //1、解析错误的自定义视图地址
  ModelAndView modelAndView = resolveErrorView(request, response, status, model);
  //2、如果解析不到错误页面的地址，默认的错误⻚就是 error
  return (modelAndView != null) ? modelAndView : new ModelAndView("error", model);
  ```

+ 容器中专⻔有⼀个错误视图解析器
  ```java
  @Bean
  @ConditionalOnBean(DispatcherServlet.class)
  @ConditionalOnMissingBean(ErrorViewResolver.class)
  DefaultErrorViewResolver conventionErrorViewResolver() {
    return new DefaultErrorViewResolver(this.applicationContext, this.resources);
  }
  ```
+ SpringBoot解析自定义错误⻚的默认规则
  +  解析⼀个错误⻚
  - 如果发生了500、404、503、403 这些错误
    - 如果有模板引擎，默认在 classpath:/templates/error/精确码.html
    - 如果没有模板引擎，在静态资源文件夹下找 精确码.html
  - 如果匹配不到 精确码.html 这些精确的错误⻚，就去找 5xx.html ， 4xx.html 模糊匹配
    - 如果有模板引擎，默认在 classpath:/templates/error/5xx.html
    - 如果没有模板引擎，在静态资源文件夹下找 5xx.html
  + 如果模板引擎路径 templates 下有 error.html 页面，就直接渲染

#### 自定义错误响应
+ 服务端渲染：
  - 业务错误
    - 核⼼业务，每⼀种错误，都应该代码控制，跳转到⾃⼰定制的错误⻚。
    - 通用业务， classpath:/templates/error.html ⻚⾯，显示错误信息。
  - 不可预知的⼀些，HTTP码表示的服务器或客户端错误
    - 给 classpath:/templates/error/ 下⾯，放常用精确的错误码⻚⾯。 500.html ， 404.html
    - 给 classpath:/templates/error/ 下⾯，放通用模糊匹配的错误码⻚⾯。 5xx.html ， 4xx.html

+ 前后端分离：
  - 后台发生的所有错误， @ControllerAdvice + @ExceptionHandler 进⾏统⼀异常处理

+ 自定义json响应
  - 使用@ControllerAdvice + @ExceptionHandler 进⾏统⼀异常处理
+ 自定义页面响应
  - 根据boot的错误页面规则，自定义页面模板

### 嵌入式容器：Servelet服务器容器
+ Servlet容器：管理、运⾏Servlet组件（Servlet、Filter、Listener）的环境，⼀般指服务器
  - SpringBoot 默认嵌⼊Tomcat作为Servlet容器。
  - ⾃动配置类是：ServletWebServerFactoryAutoConfiguration ， EmbeddedWebServerFactoryCustomizerAutoConfiguration
  - ⾃动配置类开始分析功能。xxxxAutoConfiguration
  ```java
  @AutoConfiguration
  @AutoConfigureOrder(Ordered.HIGHEST_PRECEDENCE) // 设置最高优先级
  @ConditionalOnClass(ServletRequest.class) // 当 ServletRequest 类存在时生效
  @ConditionalOnWebApplication(type = Type.SERVLET) // 仅在 Servlet Web 应用中生效
  @EnableConfigurationProperties(ServerProperties.class) // 启用 ServerProperties 配置属性
  @Import({
      ServletWebServerFactoryAutoConfiguration.BeanPostProcessorsRegistrar.class,
      ServletWebServerFactoryConfiguration.EmbeddedTomcat.class,
      ServletWebServerFactoryConfiguration.EmbeddedJetty.class,
      ServletWebServerFactoryConfiguration.EmbeddedUndertow.class
  })
  public class ServletWebServerFactoryAutoConfiguration {

  }
  ```
+ AutoConfiguration
  - ServletWebServerFactoryAutoConfiguration ⾃动配置了嵌⼊式容器场景
  - 绑定了 ServerProperties 配置类，所有和服务器有关的配置 server
  - ServletWebServerFactoryAutoConfiguration 导⼊了 嵌⼊式的三⼤服务器 Tomcat 、 Jetty 、 Undertow
    - 导⼊ Tomcat 、 Jetty 、 Undertow 都有条件注解。系统中有这个类才⾏（也就是导了包）
    - 默认 Tomcat 配置生效。给容器中放 TomcatServletWebServerFactory
    - 都给容器中 ServletWebServerFactory 放了⼀个 web服务器⼯⼚（造web服务器的）
    - web服务器⼯⼚ 都有⼀个功能， getWebServer 获取web服务器
    - TomcatServletWebServerFactory 创建了 tomcat。
  - ServletWebServerFactory 什么时候会创建 webServer出来。
  - ServletWebServerApplicationContext ioc容器，启动的时候会调用创建web服务器
  - Spring容器刷新（启动）的时候，会预留⼀个时机，刷新⼦容器。 onRefresh()
  - refresh() 容器刷新 ⼗⼆⼤步的刷新⼦容器会调用 onRefresh() ；

#### 自定义servlet
+ 修改 server 下的相关配置就可以修改服务器参数
+ 通过给容器中放⼀个 ServletWebServerFactory ，来禁用掉SpringBoot默认放的服务器⼯⼚，实现⾃定义嵌⼊任意服务器。(仅需要编写⼀个 WebMvcConfigurer配置类，并标注 @EnableWebMvc(禁用默认配置，实际上是放入组件，通过条件注解让默认配置组件不放) 即可 )

+ WebMvcAutoConfiguration ⾃动配置规则
  - WebMvcAutoConfiguration web场景的⾃动配置类
    - ⽀持RESTful的filter：HiddenHttpMethodFilter
    - ⽀持⾮POST请求，请求体携带数据：FormContentFilter
    - 导⼊ EnableWebMvcConfiguration ：
      - RequestMappingHandlerAdapter
      - WelcomePageHandlerMapping ： 欢迎⻚功能⽀持（模板引擎⽬录、静态资源⽬录放index.html），项⽬访问/ 就默认展示这个⻚⾯.
      - RequestMappingHandlerMapping ：找每个请求由谁处理的映射关系
      - ExceptionHandlerExceptionResolver ：默认的异常解析器
      - LocaleResolver ：国际化解析器
      - ThemeResolver ：主题解析器
      - FlashMapManager ：临时数据共享
      - FormattingConversionService ： 数据格式化 、类型转化
      - Validator ： 数据校验 JSR303 提供的数据校验功能
      - WebBindingInitializer ：请求参数的封装与绑定
      - ContentNegotiationManager ：内容协商管理器
    - WebMvcAutoConfigurationAdapter 配置生效，它是⼀个 WebMvcConfigurer ，定义mvc底层组件
      - 定义好 WebMvcConffigurer 底层组件默认功能；所有功能详⻅列表
      - 视图解析器： InternalResourceViewResolver
      - 视图解析器： BeanNameViewResolver ,视图名（controller方法的返回值字符串）就是组件名
      - 内容协商解析器： ContentNegotiatingViewResolver
      - 请求上下文过滤器： RequestContextFilter : 任意位置直接获取当前请求
      - 静态资源链规则
      - ProblemDetailsExceptionHandler ：错误详情
      - SpringMVC内部场景异常被它捕获：
    - 定义了MVC默认的底层⾏为: WebMvcConfigurer
  - @EnableWebMvc 禁用默认⾏为
      - @EnableWebMvc 给容器中导⼊ DelegatingWebMvcConfiguration 组件，他是 WebMvcConfigurationSupport
      - WebMvcAutoConfiguration 有⼀个核⼼的条件注解, @ConditionalOnMissingBean(WebMvcConfigurationSupport.class) ，容器中没有 WebMvcConfigurationSupport ， WebMvcAutoConfiguration 才生效.
      - @EnableWebMvc 导⼊ WebMvcConfigurationSupport 导致 WebMvcAutoConfiguration 失效。导致禁用了默认⾏为

#### WebMvcConfigurer 功能
|方法|核心参数|功能|默认|
|---|---|---|---|
|addFormatters|FormatterRegistry|格式化器：支持属性上@NumberFormat和@DateTimeFormat的数据类型转换|GenericConversionService|
|getValidator|无|数据校验：校验Controller上使用@Valid标注的参数合法性。需要导入starter - validator|无|
|addInterceptors|InterceptorRegistry|拦截器：拦截收到的所有请求|无|
|configureContentNegotiation|ContentNegotiationConfigurer|内容协商：支持多种数据格式返回。需要配合支持这种类型的HttpMessageConverter|支持json|
|configureMessageConverters|List&lt;HttpMessageConverter&lt;?&gt;&gt;|消息转换器：标注@ResponseBody的返回值会利用MessageConverter直接写出去|8个，支持byte，string,multipart,resource，json|
|addViewControllers|ViewControllerRegistry|视图映射：直接将请求路径与物理视图映射。用于无java业务逻辑的直接视图页渲染|无&lt;mvc:view - controller&gt;|
|configureViewResolvers|ViewResolverRegistry|视图解析器：逻辑视图转为物理视图|ViewResolverComposite|
|addResourceHandlers|ResourceHandlerRegistry|静态资源处理：静态资源路径映射、缓存控制|ResourceHandlerRegistry|
|configureDefaultServletHandling|DefaultServletHandlerConfigurer|默认Servlet：可以覆盖Tomcat的DefaultServlet。让DispatcherServlet拦截/|无|
|configurePathMatch|PathMatchConfigurer|路径匹配：自定义URL路径匹配。可以自动为所有路径加上指定前缀，比如/api|无|
|configureAsyncSupport|AsyncSupportConfigurer|异步支持：|TaskExecutionAutoConfiguration|
|addCorsMappings|CorsRegistry|跨域：|无|
|addArgumentResolvers|List&lt;HandlerMethodArgumentResolver&gt;|参数解析器：|mvc默认提供|
|addReturnValueHandlers|List&lt;HandlerMethodReturnValueHandler&gt;|返回值解析器：|mvc默认提供|
|configureHandlerExceptionResolvers|List&lt;HandlerExceptionResolver&gt;|异常处理器：|默认3个ExceptionHandlerExceptionResolver、ResponseStatusExceptionResolver、DefaultHandlerExceptionResolver|
|getMessageCodesResolver|无|消息码解析器：国际化使用|无| 

### 函数式Web
+ SpringMVC 5.2 以后 允许我们使用函数式的方式，定义Web的请求处理流程。函数式接⼝ Web请求处理的方式：
  - @Controller + @RequestMapping ：耦合式 （路由、业务耦合）
  - 函数式Web：分离式（路由、业务分离）

### 数据传输：
+ 导入数据库驱动
  ```xml 
  <dpendency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <scope>runtime</scope>
  </dependency>
  ```
+ 配置数据源
  ```yaml
  #数据源基本配置
  spring.datasource.url=jdbc:mysql://192.168.200.100:3306/demo
  spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
  spring.datasource.username=root
  spring.datasource.password=123456
  spring.datasource.type=com.alibaba.druid.pool.DruidDataSource
  # 配置StatFilter监控
  spring.datasource.druid.filter.stat.enabled=true
  spring.datasource.druid.filter.stat.db-type=mysql
  spring.datasource.druid.filter.stat.log-slow-sql=true
  spring.datasource.druid.filter.stat.slow-sql-millis=2000
  # 配置WallFilter防⽕墙
  spring.datasource.druid.filter.wall.enabled=true
  spring.datasource.druid.filter.wall.db-type=mysql
  spring.datasource.druid.filter.wall.config.delete-allow=false
  spring.datasource.druid.filter.wall.config.drop-table-allow=false
  # 配置监控⻚，内置监控⻚⾯的⾸⻚是 /druid/index.html
  spring.datasource.druid.stat-view-servlet.enabled=true
  spring.datasource.druid.stat-view-servlet.login-username=admin
  spring.datasource.druid.stat-view-servlet.login-password=admin
  spring.datasource.druid.stat-view-servlet.allow=*
  ```
+ jdbc场景的⾃动配置 ：
  - mybatis-spring-boot-starter 导⼊ spring-boot-starter-jdbc ，jdbc是操作数据库的场景
  - Jdbc 场景的⼏个⾃动配置
  - org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration
    数据源的⾃动配置
    所有和数据源有关的配置都绑定在 DataSourceProperties
    默认使用 HikariDataSource
  - org.springframework.boot.autoconfigure.jdbc.JdbcTemplateAutoConfiguration
    给容器中放了 JdbcTemplate 操作数据库
  - org.springframework.boot.autoconfigure.jdbc.JndiDataSourceAutoConfiguration
  - org.springframework.boot.autoconfigure.jdbc.XADataSourceAutoConfiguration
    基于XA⼆阶提交协议的分布式事务数据源
  - org.springframework.boot.autoconfigure.jdbc.DataSourceTransactionManagerAutoConfiguration
    ⽀持事务,具有的底层能⼒：数据源、 JdbcTemplate 、事务

### SpringBoot-基础特性
+ ⾃定义 banner(项目启动时控制台输出图形):
  - 类路径添加banner.txt或设置spring.banner.location就可以定制 banner，
  - 推荐制作banner⽹站：[Spring Boot banner 在线生成⼯具，制作下载英文 banner.txt，修改替换 banner.txt文字实现⾃定义，个性化启动 banner-bootschool.net](https://www.bootschool.net/ascii)
  ```yaml
  spring.banner.location=classpath:banner.txt #指定banner文件路径
  spring.main.banner-mode=off #关闭banner
  ```
#### SpringApplication
+ ⾃定义 SpringApplication，不建议使用
 - 将原本的一句代码拆开，可以更灵活的配置SpringApplication对象。原本为：SpringApplication.run(MyApplication.class, args);
  ```java
  @SpringBootApplication
  public class MyApplication {
      public static void main(String[] args) {

          SpringApplication application = new SpringApplication(MyApplication.class);

          //设置banner模式
          application.setBannerMode(Banner.Mode.OFF);

          application.run(args);
      }
  }
  ```

#### Profiles：环境隔离
+ 隔离开发、测试、生产环境
  - 标识环境：指定哪些组件、配置在哪个环境生效
  - 切换环境：这个环境对应的所有组件和配置就应该生效
  - ⽣效的环境 = 激活的环境/默认环境 + 包含的环境

+ 项⽬中的使用
  - 基础的配置 mybatis 、 log 、 xxx ：写到包含环境中
  - 需要动态切换变化的 db 、 redis ：写到激活的环境中

+ 环境分组：创建prod组，指定包含db和mq配置
    spring.profiles.group.prod[0]=db
    spring.profiles.group.prod[1]=mq

+ 应用
  - 指定环境：Spring Profiles 提供⼀种隔离配置的方式，使其仅在特定环境生效；任何@Component, @Configuration 或 @ConfigurationProperties 可以使用 @Profile(环境名) 标记，来指定何时被加载。
  - 配置激活指定环境(组)； 
    - 配置文件(推荐)：spring.profiles.active=dev,test//激活dev、test环境
    - 也可以使用命令⾏激活。--spring.profiles.active=dev,hsqldb
    - 还可以配置默认环境； 不标注@Profile 的组件永远都存在，即为默认环境
      - 以前默认环境叫default：spring.profiles.default=test

+ **容器中的组件都可以被 @Profile 标记**：eg：@Profile("dev") @Component public class MyBean {}，**被标记后仅在该环境下此类才会生效**

+ 环境包含
  - pring.profiles.active 和spring.profiles.default 只能⽤到 ⽆ profile 的⽂件中，如果在application-dev.yaml中编写就是⽆效的
  - 也可以额外添加⽣效⽂件，⽽不是激活替换。⽐如：
    ```yaml
    spring.profiles.include[0]=common
    spring.profiles.include[1]=local
    ```

+ Profile 配置⽂件
  - application.properties ：主配置⽂件，任意时候都⽣效
  - application-{profile}.properties ：指定环境配置⽂件，激活指定环境⽣效profile优先级 > application

#### 外部配置：
+ 配置优先级
  + Spring Boot 允许将配置外部化，以便可以在不同的环境中使⽤相同的应⽤程序代码。
  + 我们可以使⽤各种外部配置源，包括Java Properties⽂件、YAML⽂件、环境变量和命令⾏参数，**由低到⾼，命令⾏ > 配置⽂件 > springapplication配置**
    - 默认属性（通过 SpringApplication.setDefaultProperties 指定的）
    - @PropertySource指定加载的配置（需要写在@Configuration类上才可⽣效）
    - 配置⽂件（application.properties/yml等）
    - RandomValuePropertySource⽀持的random.*配置（如：@Value("${random.int}")）
    - OS 环境变量
    - Java 系统属性（System.getProperties()）
    - JNDI 属性（来⾃java:comp/env）
    - ServletContext 初始化参数
    - ServletConfig 初始化参数
    - SPRING_APPLICATION_JSON属性（内置在环境变量或系统属性中的 JSON）
    - 命令⾏参数(所有参数均可由命令⾏传⼊，使⽤ --参数项=参数值 ，将会被添加到环境变量中，并优先于配置⽂件 。)
    - 测试属性。(@SpringBootTest进⾏测试时指定的属性)
    - 测试类@TestPropertySource注解
    - Devtools 设置的全局属性。($HOME/.config/spring-boot)
  + 配置⽂件优先级如下：(后⾯覆盖前⾯，包外 > 包内 ，同级情况：profile配置 > application配置,命令⾏ > 包外config直接⼦⽬录 > 包外config⽬录 > 包外根⽬录 > 包内⽬录)
    - jar 包内的application.properties/yml
    - jar 包内的application-{profile}.properties/yml
    - jar 包外的application.properties/yml
    - jar 包外的application-{profile}.properties/yml

+ 导入额外配置：spring.config.import=my.properties

#### 单元测试-JUnit5 
+ 配置
  ```xml
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
  </dependency>
  ```
+ @test 

































































