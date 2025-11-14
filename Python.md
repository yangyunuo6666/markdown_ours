[toc]
*** 

#  Python基础及参考网站
1.	根据执行方式不同，编程语言分为两类
+ 静态语言 使用编译执行的编程语言 C/C++语言、Java语言-
脚本语言 使用解释执行的编程语言 Python语言、JavaScript语言、PHP语言
- 优点：静态语言 编译器一次性生成目标代码，优化更充分程序运行速度更快
脚本语言 执行程序时需要源代码，维护更灵活，源代码在维护灵活、跨多个操作系统平台。
* [网站1](http://www.runoob.com/python3/python3-tutorial.html)
- 永久配置第三方网址：pip config set global.inndex-url 网址//https://pypi.tuna.tsinghua.edu.cn/simple
## Python库
### turtle库（海龟绘图）
+ turtle.setup(长，宽，位置X，位置Y)//其中（x,y）为相对左上角坐标，为可选参数。
+ turtle.goto(x,y)//去到（x,y）绝对坐标。
+ turtle.bk(x)//向右X  turtle.fd(x)//向左X  turtle.circle(r,anger)以为半径走曲线。
+ turtle.seth(angle)转到angle度采用右手系。 turtle.left(angle)向左X度 turtle.right(angle) 向右X度

### subprocess:系统命令、进程管理
+ result = subprocess.run( 
            ["ssh", host, command], # 命令列表，相当于ssh host command
            check=True, # 如果命令执行失败，则抛出异常
            capture_output=True, # 捕获标准输出和标准错误
            text=True, # 将输出作为字符串处理
            timeout=300 
        )
  - 命令也可使用字符串给出，"ps -ef | grep python"
  - result.returncode == 0 # 检测命令是否执行成功
#### paramiko: SSH2协议，远程命令执行，代替subprocess-ssh
+ 用于替代ssh命令，通过 Python 直接执行远程命令（比subprocess调用ssh更可控
+ 创建 SSH 客户端：
  - ssh = paramiko.SSHClient(); 
  - ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
+ 连接到远程主机: ssh.connect(hostname="hadoop102", username="root",password="xxx") #若配置了公钥认证，则不需要密码
+ 执行命令：
  - stdin, stdout, stderr = ssh.exec_command("ls -l")
  - stdout.read()获取输出
  - 可用 for cmd in cmds：一次执行多条命令
+ 文件传输：
  ```python
  sftp = ssh.open_sftp()
  sftp.put("/local/path/file.txt", "/remote/path/file.txt")
  sftp.get("/remote/path/file.txt", "/local/path/file.txt")
  sftp.close()
  ```

### os：OS接口
+ os.path.isdir(path): 检查是否是目录
+ os.path.isfile(path): 检查是否是文件
+ os.path.dirname(path): 获取路径的父目录
+ os.path.basename(path): 获取文件名
+ os.path.abspath(path): 获取路径的绝对路径，如根据相对路径获取绝对路径
+ os.makedirs(path, exist_ok=True): 递归创建目录，True忽略已经存在的目录
+ os.getcwd()：获取当前工作目录，用于检查当前执行目录是否符合预期
+ os.environ.get("HADOOP_HOME")：获取环境变量
  - os.environ["HADOOP_HOME"] = "/data/software/hadoop-3.3.5" #设置环境变量
+ os.system("ls"): 执行系统简单命令
+ pathlib库: 代替os.path，更简洁的路径操作
  - 代替os.path，更简洁的路径操作（如获取父目录、文件名等）
  - path.absolute()：获取绝对路径
  - path.parent/path.name：获取父目录 / 文件名
  - path.exists()：检查路径是否存在
  - path.mkdir(parents=True, exist_ok=True)：递归创建目录
  - path.suffixes()：获取文件拓展名
  - path.name：获取文件名,stem()获取文件名（不带拓展名）

### sys: 系统相关参数函数
+ sys.argv: 获取命令行参数，列表形式
  - 第一个元素为sys.argv[0]是脚本名
  - sys.argv[1:]为参数列表
+ sys.exit(num): 退出程序，可传入参数作为退出码，
  - 默认为0正常退出，1表示异常退出
+ sys.stdout.write("hello"): 输出重定向，默认输出到控制台
+ sys.stderr.write("error"): 错误输出重定向，默认输出到控制台
#### argparse: 命令行多参数解析
+ parser = argparse.ArgumentParser(description="脚本描述")：创建解析器。
+ 定义参数
  - parser.add_argument("action", choices=["start", "stop", "status"], help="操作类型") #定义位置参数，choices限制参数取值范围。
  - parser.add_argument("-d", "--date", help="日期参数") #定义可选参数，-d为短选项，--date为长选项，help为帮助信息。
  - parser.add_argument("-v", "--verbose", action="store_true", help="详细模式") #若参数action="store_true"，则参数args.verbose被设为True，否则为False。
+ args = parser.parse_args()：解析参数
  - {}args.action：获取参数值
  
### configparser：INI配置文件解析/修改
+ 读取配置：
  - config = configparser.ConfigParser() # 创建配置解析器
  - config.read("config.ini") # 读取配置文件
+ 获取配置
  ```python
  if "setting" in config: # 检查section是否存在
      startTime = config.get("setting", "startTime") # 获取startTime配置
  ```
+ 修改配置(配置已经存在)：
  ```python
  config.set("section", "key", "new_value");
  with open("file.setting", "w") as f:
    config.write(f) # 如generate_one_day_logs.sh中修改日志生成时间
  ```
+ 新增配置：
  - config.add_section("section") # 新增section节
  - config.set("section", "key", "value") # 新增key-value对
+ config.sections()：获取所有section
### logging: 日志模块
+ 日志级别：DEBUG < INFO < WARNING < ERROR < CRITICAL，默认输出WARNING及以上级别
  ```python
  # 配置日志
  logging.basicConfig(
      level=logging.WARNING, # 日志级别WARNING及以上
      format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
      handlers=[
          logging.FileHandler("app.log"), # 输出到文件
          logging.StreamHandler() # 输出到控制台
      ]
  )
  ```
+ `logger = logging.getLogger(__name__)` # 创建日志记录器
+ logging.info("启动成功")：记录正常日志
+ logging.error("命令执行失败")：记录错误日志
+ logger.debug("调试信息") 
+ logger.warning("警告信息") 
+ logger.critical("严重错误")

### time库 
+ time显示时间戳（是凭证文档由以下三个部分组成，文件摘要，DTS接收文件时间，DTS的数字签名）。asctime()返回一个元组，保存的时间戳可以直接读。
+ sleep(x)休眠X秒
+ datetime: 日期时间
  - datetime.now()：获取当前时间
  - timedelta(days=n)：表示时间差
    - eg:yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%F")获取前一天日期 
  - strftime("%F")：将时间转为字符串（"%F"对应YYYY-MM-DD格式）。
  - strptime(date_str, format)：将字符串转换时间（如校验输入日期格式）

#### hdfs: HDFS操作
+ InsecureClient库：
  - client = InsecureClient("http://hadoop102:9870", user="atguigu")
  - client.makedirs(hdfs_path) #创建目录
  - client.status(hdfs_path, strict=False) #检测路径是否存在 
  - client.list(hdfs_path) #列出目录下的文件
  - client.upload(hdfs_path, local_path) #上传文件
  - client.download(hdfs_path, local_path) #下载文件
  - client.delete(hdfs_path, recursive=True)删除路径
### pyarrow库: Hadoop交互
+ Parquet.hdfs as hdfs
  - fs = hdfs.connect("hadoop102", 9870, user="atguigu") # 连接Hadoop
+ Parquet.pyquet
  - 读取Parquet：pyarrow.parquet.read_table(hdfs_path)
  - 写入Parquet：pyarrow.parquet.write_table(table, "hdfs://hadoop102:9870/path/to/new_file.parquet", filesystem=fs)
  - df = table.to_pandas()  # 转换为Pandas DataFrame


## Python小技巧与易错
### 技巧
  1.  **singer in ['C','c'] #singer为C（不论大小写）**
  2.  import 库名 as 库别名（可简化库名）
  3.  常用常量：PI E，**三个双引号为一组，两组括起来可多行注释，Ctrl + L可注释**
  4.  print可一次输出多个表达式，用逗号隔开即可。print('''收件人''')三个引号可打印多行。
  5.   序列解包赋值，eg：x,y,z=1,2,3  x,y=y,x   (nums=1,2,3    x,y, z=nums)
    链式赋值：x=y=z=1
  6.  ****print("%d*%d=%d" % (i,j,i*j),end=" ")**%为转换说明符，使（）内的值与%d对应起来。
  7.  **#! /usr/bin/python3** //代码移植到Linux中不出问题
      **#-\*-coding:UTF-8 -\*-** //出现中文不乱码。
  8.  assert断言//assert 条件 ，报错信息（为假出现报错）
  9.  from math import * //导入模块中所有方法
  10.  **print("\n")//进行了两次换行，利用*运算符可创建含相同元素的列表等**
  11.  二维数组类似写法：list1.append(list(map(int,input().split())))
  12.  python的多行注释：用三个连续的双引号。一个tab等于4个space,quit()可退出Python3命令行环境。
  13. str("11111")==11111,str.join(list1)//以str为中间字符将list1中的元素连接起来。
  14. “第一页”.center(20,"-"),//将“第一页”居中，两边用-填充。
#### random模块
 + random模块的随机选择函数：choice随机选择容器中的一个元素，sample随机选择容器中的n个元素。
#### 推导式
+ 列表推导式：list2=[x**2 for x in range(1,10)]
+ list2=[x**2 for x in range(1,10) if x%2==0]//列表推导式可加条件
+ 也可用于字典推导式：dict2={x:x**2 for x in range(1,10)}
### 易错
  - 字典的修改：~~dict[name]="ksdlf"~~,应为dict["name"]=ksdlf.
###  查看已安装依赖包,安装所有的依赖包 ：
  ```python
    pip list 或pip freeze
    pip freeze   > requirements.txt//输出所有的依赖项
              >重定向  输入到依赖文件requirements.txt
    pip install -r requirements.txt//安装所有的依赖项
  ```  
## **异常处理与assert断言，异常具有传递性**
+ try...except...结构(**意义在于不让异常中断代码执行**)
  ```python
   try：
    x = int(x)#需要执行的代码
  except Exception1: #也可用(EX1,EX2)一次多个类型异常
    print{'error'}#出错后执行的代码
  except Exception2: #捕获特定的异常EX2
    print{'error'}#出错后执行的代码
  except Exception3:
    print{'error'}#出错后执行的代码 
  ```
###  **try...except...else...结构**
```python
   try：
    x = int(x)#需要执行的代码
  except Exception1:
    print{'error'}#出错后执行的代码
  else:#未出错后执行
    print{'planB')
```
1. **try...except...finally...结构**
  ```python
   try：
    x = int(x)#需要执行的代码
  except Exception1:
    print{'error'}#出错后执行的代码
  finally:#无论是否出错都要执行
    print{'free(p)') 
  ```
### assert 断言与with上下文
+ **assert，XXX（抛出的信息）指定必须满足的条件，上线后通常删除**
   assert a != 0,
   return a / b 
+ with XXX as：当下面语句执行完毕后，自动关闭XXX。
```python
with open('a.txt','w') as file:
    file.write('hello world')
```
  
### raise 引发异常的关键字
+ raise Exception("这是一个异常消息")
  - raise 后面跟着异常类的名称，通常是内置异常类（例如  Exception，ValueError，TypeError 等）或者你自定义的异常类。
  - 异常消息是一个字符串，用于描述异常的具体情况。
+ 当爬虫处理数据时，有时需要过滤或丢弃某些数据项。在这种情况下，你可以使用 **raise DropItem()** 来明确指定要丢弃的数据项。**这是scrapy的一个异常类，引发后丢弃当前item**
##  **切片：**
1.  获取元素：alist[::-1]逆序返回元素
2.  插入元素：
  + alist[len(alist):] = [9] //尾插入
  + alist[:0] = [1,2] //头插入
  + alist[3:3] = [4] //在alist[3]插入
3.  修改元素 ：alist[:3] = [1,2,3,]
   
## 常用函数
+	range (起始,end,步长) eg：range（1,10,1） [1,2….,8,9] 没有起始值默认为0，步长默认为1
+ abs() 绝对值函数
+ round（x.n）四舍五入函数，n为小数位数默认为0
+ 强制转换函数 int()  float()  bool()  str()(强制转换为字符串)
+	All（） 全真为true ,any() 一真为真。
+	Len() 返回目标长度和项目个数
+	Sorted() 排序函数
+	Type() 返回类型
+	Help（）获得库函数信息
+	Bin（）以二进制显示数据 eg：print（bin（2））#ob10
+	Eval（）执行一个字符表达式，返回表达式的值
+	Pow（）求幂值
+	Open（）打开文件 eg：f1 = open(“teast.txt”,”      r”)//以只读模式打开文件taset.txt
+	Close() 关闭文件   eg：f1.close
+	Read() 从打开的文件读取一个字符串 eg：printf(“文本内容：”,f1.read() )和readline读取一行。
+	Write（）写入一个字符串 eg：f1.write(str1)
+ random() 召唤0.0到1.0之间的一个随机数，unitform(a,b)生成随机浮点数 randrange(a,b,步长) 
+ zip(可迭代对象1，可迭代对象2) //把1,2元素合并在一起，返回一个zip对象。
+ chr() 将机内码转化为字符，ord()可将字符转换为机内码。
+ lower（）大写转换为小写，upper（）小写转换为大写。
+ **进制转换**int("111",2)//将二进制转换为10进制,bin oct hex将二进制，八进制，十六进制转换为十进制。
+ eval() 计算字符串的值。
+ reverse() 对可迭代对象进行翻转。
+ ord 通过 字符 找到对应的 序号
+ chr 通过 序号 找到对应的 字符
## **模块（python的代码块）**：
### 模块导入：
 + from 模块 import 函数(其中*表示全导入)
 + 后接 as 别名 可为模块取别名
 + From 模块_name import 函数_name1 函数_name2（导入N个函数，无需使用前缀）
 + **导入顺序：基础模块，第三方模块，自定义模块，按字母顺序，可使用代码优化类的模块优化**
### **自定义模块**
   + 每个Python文件都可作为一个模块，但是命名需要符合命名规则。**当导入多个模块的同名函数的时后一个会覆盖前一个**
   + **_ _ mian _ _ == '_ _ main _ _'**直接输入main按Tab即可补全。
    ```python
    if __main__ == '__main__':
    //当直接右键运行时__maim__变量初始化为‘__mian__’条件成立，通过模块导入时条件不成立
      f(x,b)
    ```
  + --all--**all变量值为列表，保存函数名等**
   - --all--变量若在模块中定义了__all__变量，用import * 时只能导入在__all__变量的的内容。
### 自定义Python包
1. 包定义：一个**含--init--.py文件**的含多个模块文件的文件夹。本质上是模块集合。
2. 自定义包：新建包(右击项目名)->新建模块(右击包新建文件)
   + 用import导入即可使用eg：improve bao.mode1(导入bao包中的mode1模块)
   + 包里也有--all--
3. 安装第三方包
   + pip install 包名（从国外安装）（Windows报错可加--user）
   + pip install -i 网址 包名(从指定网址安装)
    //https://pypi.tuna.tsinghua.edu.cn/simple
   + 永久配置第三方网址：pip config set global.inndex-url 网址
## **类**：
+ 类的实例化：实例 = 类名()
   - **面向对象的编程：设计类模块实例化后解决问题。**

+  Class (class首字母大写类名)(继承的父类,父2)：
      成员名
      成员
    **def** 成员函数（**调用用点运算符即可**）
+ 继承：**无特定父类用object，当继承了多个父类有同名方法时以第一个父类为准**  
+ 复写：子类中定义同名成员。

+ **以下划线开头的成员有特殊的含义**
  -  _xxx(单下划线开头):这样的对象叫做保护变量，不能用'from module import *'导入，只有类对象和子类对象能访问这些变量；
  -  _ _xxx_ _(双下划线开头与结尾)：系统定义的特殊成员名字；
  - __xxx(双下划线开头)：类中的私有成员，只有类对象自己的成员可使用(**eg:self.__hi()**)，实例化后不可使用子类不可使用。
### **继承的特点：**
   - 在继承中，基类的构造方法（_init_()方法）不会被自动调用，需要在子类的构造方法中专门调用。
   - 在调用父类的方法时：**父类名.方法(self)**
   - 在Python中，首先查找对应类型的方法，如果在子类中找不到对应的方法，才到基类中逐个查找。
 - 可以多重继承，以逗号隔开，方法从子类到父类从左至右查找。
### **多态**
  + 定义：同样的行为不同的对象得到不同的结果。
  + 子类复写了父类方法，传入父类方法执行的子类的方法。
  + 抽象类（接口）实现：父类定义了有哪些方法，具体方法子类实现。(父类确定标准(顶层设计)，子类具体实现标准)。
```python
    def f(x):
      pass //父类方法中用来占位的语句 
```
###  **特殊方法**  
  +   __ init __（）方法
      类实例化时会init方法会自动执行内部的代码，将传入的数据给init函数使用。
        ```python
        class student:
          name = None   
          age = None
          def __init__(self,name,age):
            self.name=name
            self.age=age
        ```
  + __ str__()方法
    转化为字符串，直接输出会有多余的地址。
      ```python
      def __str__(self):
        return {self.name}
      ```
  + __ it__()方法，大小比较
    ```python
    def __it__(self,other):
      return self.age < other.age
    ```
  + __ le__()方法，大小等于比较。
  + __ eq__()方法，等于比较
  +  __ del__()析构方法：
     释放对象时自动调用。
6.  实例变量以__(两个下划线开头)，就会变为私有变量外部不能访问。
7.  属性（特殊的成员方法）：
   可设置成员 w wb 等属性。
8.  实例变量（实例属性）：实例变量是属于特定实例的变量，在每个类的实例中具有不同的值。它们在类的方法中通过self关键字进行访问和设置。类变量（类属性）：类变量是类的所有实例共享的变量，它们在所有实例中具有相同的值。类变量在类的内部定义，但在方法之外。通过类名.变量名或实例.变量名
###  **成员方法：**
   #### 实例方法：
    实例可以用方法，可以通过实例进行调用。它第一个参数必为self，传递变量时无需传递，可以self.x访问类变量。
     ```python
     class student:
      name = None
      def say_hi(self):
        print("hellow I'm {self.name}")
     ```
   #### 类方法：
   类方法是绑定到类本身的方法，通过@classmethod装饰器进行标识。类方法的第一个参数通常命名为cls，用于引用类本身。类方法可以在不创建类的实例的情况下被调用。
   #### 静态方法：
   静态方法是属于类的独立方法，不需要访问实例或类。通过@staticmethod装饰器进行标识。静态方法在类的内部定义，但与类和实例没有直接关联。
   + dir（）函数可获得一个对象的所有属性和方法。
### 装饰器(紧跟在函数或方法定义之前)
  +  @classmethod 装饰器：
```python
class MyClass:
    @classmethod
    def class_method(cls, arg1, arg2, ...):
        # 类方法体
@classmethod 装饰器用于定义类方法。
cls 是类方法的第一个参数，用于引用类本身。
类方法可以被类直接调用，而不需要创建实例。
```
  + @staticmethod 装饰器：
```python
class MyClass:
    @staticmethod
    def static_method(arg1, arg2, ...):
        # 静态方法体
@staticmethod 装饰器用于定义静态方法。
静态方法与类或实例无关，不需要传递额外的参数引用类或实例。
静态方法可以被类或实例直接调用。
```

  + @abstractmethod 装饰器：
```python
from abc import ABC, abstractmethod

class MyAbstractClass(ABC):
    @abstractmethod
    def my_abstract_method(self, arg1, arg2, ...):
        pass
@abstractmethod 装饰器用于定义抽象方法，要求子类必须实现这些方法。
抽象方法在基类中没有具体实现，因此需要在子类中提供实现。
抽象类必须继承自 ABC（Abstract Base Class）类。
```
 + @property 装饰器：
```python
class MyClass:
    def __init__(self, value):
        self._value = value

    @property
    def my_property(self):
        return self._value

    @my_property.setter
    def my_property(self, value):
        self._value = value

    @my_property.deleter
    def my_property(self):
        del self._value
    @property 装饰器用于定义属性的 getter 方法。
    @<property_name>.setter 用于定义属性的 setter 方法。
    @<property_name>.deleter 用于定义属性的 deleter 方法。
    这种装饰器允许你在访问属性时执行自定义逻辑，以及在属性赋值或删除时执行相应的逻辑。
  ```

## 迭代
1. map(f(x),迭代对象) //利用f(x)对后面可迭代的对象进行迭代，**特别的f(x)不是整个函数而是函数名不含形参表，返回一个对象，需要按需转换**
+ 可用的内置函数：int：强制类型转换，str(): 将对象转换为字符串，float(): 将对象转换为浮点数。bool(): 将对象转换为布尔值。str.upper(): 将字符串转换为大写。
1. reduce(f(x),list) // 将一个双参函数以迭代的方式从左至右依次作用到一个序列上,如序列求和f(x)的第一次的结果会与序列的下一个值进行函数调用。
2. filter(f(x),迭代对象) //利用单参函数进行迭代，常用于序列的过滤返回过滤后的序列。  
## 术语
  1.  类：有相同属性和方法的对象的集合。
  2.  对象：含两个数据成员（类变量和实例变量）和方法。
  3.  类变量：定义在类中方法之外，也称为属性。
  4.  数据成员：类变量或实例变量用于处理类及其实例对象的相关数据
  5.  实例变量：定义在方法中且只作用于当前实例的类。
  6.  多态：对不同类的对象使用同样的操作。
  7.  封装：对外部隐藏工作细节。(**将现实事物的属性和行为用成员变量和方法来描述**)
  8.  继承：子类继承父类所有的字段和方法。
  9.  实例化：创建类的实例、类的具体对象。
  10. 序列化：将数据结构或对象转换为二进制序列。
 10.	**正则表达式**：每一篇文章都有一个数字ID可用正则表达式提取：
- **正则表达式符号**：\d匹配数字 +匹配前一个数字一次或多次。
  * 单一个点，匹配除‘\n’外任意一个字符。
  * \d<=>[0-9]匹配一个数字，\D<=>[^0-9]匹配一个非数字
  * \s匹配空白字符， \S匹配非空白字符
  * \w<=>[A-Za-z0-9]匹配任意单词字符，\W匹配任意非单词字符。eg：'\w\w\d'可匹配‘py3’
  *  **\^表示开头(^\d表示必须以数字开头)，$表示结尾(\d\$表示必须与数字结尾)。|表示或(A|a匹配A,a),后接{1,19}则是限制了变量长度为1到19，正常是贪婪匹配（匹配尽可能多），末尾加？可变为非贪婪匹配** ***后接加号匹配至少由一个数字、字母、下划线组成的字符串，后接乘号匹配由字母或下化线开头后接任意个数字组成的字符串***
## Python的输入输出	
1.输入，通常一行写完一句语句，若太长可在末尾加\来实现多行语句。
+ Python 提供了input（）内置函数从标准输入设备读入一行文本，默认的标准输入设备是键盘。Input（）函数可以接收一个Python表达式作为输入，并将运算结果返回。代码如下：str =input("请输入：");#等待用户输入（单行注释用#，多行注释用三个单引号）
print(“你输入的内容是”，str)#显示用户输入内容
###   input函数的使用 
  -  a = int(input('我最喜欢的数字：'))
 b = float(input('我认为适宜的温度：'))
 print(a,type(a))#先输出内容，然后type()函数看类型。
 print(b,type(b))
  - **如何一行输入多个字符**：a,b,c = map(int,input().split())
//这种方式输入了3个int型的数字，split()代表以空格隔开。
print(a,b,c)
index = list(map(int,input().split()))
//这种方式可以输入任意个int型的数字，在这里采用列表来存储。
print(index)
+ f1 = open("cmucc.txt","r")#打开一个文件，参数为只读
	print("文件名：",f1.name)#输出文件名
print(“文本内容：”,f1.read())#读取文件
f1.close()#关闭文件
###	输出(格式化输出符号与C相同)
+	Print（）函数作为Python 最常用的输出语句，可以输出字符串、数值和变量等。
  print（“中国医科大学计算机教研室”)   print（）函数默认换行的，若要连续输出则可在print（）函数中加入“end="”语句。代码如下：
  print（"中国医科大学"，end=")
  print（“计算机教研室”）输出为：中国医科大学计算机教研室
  print("a + b 输出结果："，a + b)#连接字符串
  print("a*2 输出结果：”, a*2)#重复输出两次字符串
  print("圆周率为：%.0f" % pi)格式化输出
  print('圆周率为：%.2f' % pi) 格式化输出
+ print有一个默认参数end="\n",可替换为无即可不换行输出，可选参数set='\t'可指定分隔符。
+ print("element的值是{element[0]}")

## Python数据类型
1.	Python的变量不需要声明，但是使用前必须赋值，赋值后变量才会被创建，根据值得到相应的类型（浮点数只有float没有double，数字还有complex复数类型，**Python的变量可以重新赋不同类型值**
## Python的容器
###	String(不可修改的数据容器) 
+ 可以使用单引号或双引号创建字符串，str[1]表示第二个字符。**(不可修改：不可追加，移除，修改元素)**
+ print(f"Hello, {name}")//f-string格式化字符串，它允许在字符串中嵌入表达式，并使用大括号{}来表示嵌入的表达式。
+ 编码方式： 
  * UTF-8 全球编码，1字节表示英文，3字节表示中文。
  * GB2312 中国制定的编码方式，1字节表示英文，2字节表示中文。
  * GBK 对GB2312进行了扩充。
  * CP936 微软在GBK基础上进行了再开发。
  
+ Python 也可以在方括号中使用范围来获取字符串的中间“一段”（称为子串），其基本语法格式为string\[start: end:step]，string字符串名，后依次为开始字符（省略默认为首字符），结束字符（省略默认为尾字符），步长（间隔步长截取字符，负数为反方向截取，省略默认为1，最后一个：可省略）eg：print（a[1:2:1]）
+ 方法
  - find（str,beg=,end=）找到返回位置，否则返回-1
  - join（list1）连接可迭代对象为字符串（str1的第一个字符与str2的第二个字符交替连接），并返回已连接的字符串。
  - lower将所以大写字符转化为小写字符,upper与之相反。swapcase大小写翻转
  - replace(str-old,str2,number)将字符串中的str-old替换为str2重复number次。
  - split(str,number)以str为分割number次，，无str默认为空格，分割后str不存在了。
  - strip（str1）去除头尾中相同的str1，默认参数为空格，默认去除前后空格。
  - translate(strin,strout)根据strin与strout的一一对应关系进行转化。
  - 字符串连接与**新增字符**：用+
### 列表
+ 创建列表：列表的数据项不需要具有相同的类型，它和其他语言的数组比较类似，但功能更强。Eg：1ist1=[智能’,“医学’，2008，2019] 创建一个列表，只要将不同的数据项用逗号分隔，使用方括号括起来即可
+ **None**Python中用来表示空，可用来创建含N个空元素的列表。eg：sq=[None]*5
+ ***列表的方法***
  - **对象.方法(参数)为基础格式**
  - append列表尾增加元素，insert(list,位置)插入一个元素。extend在末尾追加可迭代元素。
  - count统计元素出现次数
  - extend在末尾增加另一列表多个值
  - index查找元素
  - pop(X)移除第X个元素，并返回被移除元素，无参数为最后一个元素。
  - remove移除列表中第一个值为X的元素。
  - reverse无需参数，用于翻转列表。
  - sort与sorted，**前者对原列表排序，后者对原列表取副本排序并返回排序好的列表不改变原列表。sort有两个可选参数，key=len(由短到长排列) reverse=Ture(降序排序)**
  - clear清空列表，无需参数。
  - copy复制并返回列表。
+ **列表的相关操作：**
  - 访问列表中的值可以使用下标索引来访问列表中的值1ist2[1:4]
  - 更新列表可以对列表的数据项进行更新。代码如下：1ist =['中国”，“医大'，2000，2019]  1ist[2] =2010
  - **分块赋值**list[0,]='is'**替换**前两个元素。**也可增加新元素**listl[2,2]='word'在第二个和第三个元素中插入Word，
  - 删除列表元素可以使用del语句删除列表中的元素 del 1ist[2]
  - **添加元素**list.append(新元素) //list为列表名。
  - 列表支持嵌套使用。
+ 列表推导式：
  - 列表推导式是Python中一种强大的可以用来创建列表的生成式。
  - 列表推导式格式：[表达式 for 变量 in 列表]
### 元组(不可修改的数据容器)
+ 定义：（不可修改的列表，一旦定义不可修改）：创建元组只需要在小括号中添加元素，并使用逗号隔开即可tup2 =(1,2,3,4,5) ，只有单个元素必须在末尾加逗号。
+ 访问可用下标，不允许增减元素，但是可修改嵌套与元组中的可修改的容器元素。
+ 但可以使用del语句删除整个元组。**可用tuple转换为元组**，元组不可修改但是可使用+连接。
### 字典用大括号
+  **不允许键重复，key和value可以是任意数据类型但是key不可为字典**
+ **字典创建，一个元素为一个键值对**：
  * 字典键和对应值成对成键/值对，dict1 = {'ID':'1001', 'Name': 'lucy', 'Age': 19)或用dict函数deta1=(name='小明'，number=‘1001’)***字典的键不可变，可用数字、字符串、元组充当，不可用列表*** **dict内部存放顺序与键放入顺序无关**说明：每个键与值用冒号隔开，每对用逗号分隔，整体放在花括号中。键必须一无二，但值则不必。值可以取任何数据类型，但键必须是不可变的，如字符串、数或元组。
  * **keys = [1,2,3] values = [a,b,c] d=dict(zip(keys,values))使用dict函数创建，
  * frommkeys('nmae','age','sex')创建有键无值的字典**
+ 访问字典里的值要访问字典里的值，就把相应的键放入方括号。print("dict['Name']:", dict['Name'])   print(tb[0]["name"],tb[0]["age"]，tb[0]["city"]）#输出第一行数据
+ 修改字典修改字典的方法是增加新的键/值对或修改已有键/值对。dict['Age']= 21
dict['School'] = "CMU"
+ **字典方法，不可使用下标**
  * clear无参数，清除字典。
  *  del dict['Name']#删除键是Name的条目
  *  copy复制并返回字典
  *  fromkeys(seq,value)seq键值列表value键对应的值。  
  *  get（key，default=None）查找key对应的值，不存在返回default对应的None
  *  update(dict2)将dict2中添加到dict1中并覆盖dict1中与dict2中相同的键对，同时也可用来增加字典元素。
  *  **values()**以列表形式返回字典中的所有值，可包含重复元素。  
  *  **items()**返回可历遍的键对。
  *  **keys()**返回所有键
  *  setdefault(key,default=None)查找key对应的值，无值设定为default=的值。
- **dict与list**
  * dict插入与查找极快但空间占用大，以空间换时间。
  * list插入与查找时间，元素越多时间越长。但占用空间少。
### 集合 （无序，去重的容器）
- 元素可以是不同的类型，如数字、元组、字符串等。要创建集合，可以将所有元素放在花括号内，以逗号分隔。或者使用set（）函数。创建一个没有任何元素的集合，可使用set（）函数（不包含任何参数）eg：sl= (1,2,'A'}  s3 = set('Hello')**关系运算符在集合中表示集合之间的包含关系。**
- **集合方法，不支持下标索引故不可用while循环**
 + add增加一个元素
 + update增加可迭代元素
 + remove(X)移除元素X
 + pop随机取一个元素
 + clean清空元素
 + set1.difference(set2)取set1-set2差集
 + set1.difference_update(set2)在set1中去除与set2相同的元素。
 + union合并集合
## Python基本运算符
1.  **幂运算，/除法运算 **//整除运算 有复合运算符**，没有++和—
2.  比较运算符与C一样，但结果是Ture或False
3.  逻辑运算符，是and or not 
4.  成员运算符：**in 与not in** eg:if(a in list1)printf(“变量a在list1中”)
5.  优先级：较为常用的几种运算符的优先级由高到低依次为幂运算符、正负号和~、算术操作符（* / % // + - >> <<）、位运算符（& ^ |）、比较操作符、赋值运算符（含+=）、身份运算符、成员运算符、逻辑运算符。
6.  位运算符：同C语言。
7.  身份运算符：**is not is**（比较两个对象的存储单元）
 
# 循环体
1.  If （）：  if x%2 == 0 :
语句      printf(“yes”)
   Else:      else
	语句	  printf(“no”) 
2.	 
	If () :
	  语句
	Elif () :
  	语句
3. While 表达式 ：//**自定义循环条件**
	  语句       
4. For 临时变量 in 容器：
+ **//从容器中依次取出元素，赋给临时变量用语句处理**
        语句
+   for i in a[::-1]:从容器中逆序取元素。
5.	Pass 空语句
6.	 Typ :
  被测试语句
Except<异常名>
  异常处理  

# 自定义函数
1.	自定义函数def f(x) :（通常函数名中单词以-name-隔开）
            函数定义
            Return S （return即可结束又可带回S的值）
+	如果函数中没有return，那么函数的返回值默认为 None， return 后面没有任何内容，返回值也是None。
- **多返回值函数**，可以在return后面，每个数据之间用逗号隔开，调用函数之后接收到的是个元组形式的数据
+	函数定义的三种形参：
-	**必需参数** 　如：def add_num(a, b, c) ，a,b,c三个参数都必须要传
-	**默认参数**（缺省参数） 如：def add_num(a, b, c=99) ，c是默认参数，可以传，可以不传（不传时直接使用c=99）
-	**不定长参数（可选参数）**： 
 * 一个星号为位置不定长参数args，**即个数不确定，用容器接收**，自动合并为一个元组。
 * 两个星号为关键字不定长参数kwargs，**即个数不确定的键值对传入**，自动合并为字典。
- **关键字参数**：add(a=,b=)通过关键字指定，无需依次传入。
-  **位置参数**：add(a,b)必须依次传入数据，与关键字参数混用时必须前置。
-  **函数参数**:将一个函数作为参数传入，实际是计算逻辑的传递进去。
-  **声明局部变量关键字**global 在函数内部声明全局变量,作用域拓展。 
-  异常 如果想用一个块捕捉多个异常，可以将它们用元组列出。
+ 自定义函数需要类型注解才会提示类型，**ctrl+p可提示库函数参数，类型注解仅仅作为提示作用**
 - **基础类型的语法：变量:类型 eg：val1:int = 10**
 - **类对象的语法：类：类型 eg：stu:student=studennt()**
 - **容器类型注解：变量：类型或详细注解 my_list:list[int]=[1,2,3]**
 - **在注释中注解：#type：类型**
 - **函数形参注解：形参：类型，函数返回值注解：f(x): -> 类型:**
## 匿名函数：
+   lambda 形参 一句语句（仅可使用一次的函数）
   eg：lambda x,y:x+y 自动return：后的语句，但函数体仅可有一句语句。 
## yield生成器与next、iter迭代器
+ yield惰性求值，**含yield关键字变成生成器函数，调用它返回一个生成器对象**yield关键字：保留中间算法，下次继续执行
+ 当调用next方法时，遇到yield就是暂停运行，并且返回yield后面的值，next的参数为生成器。
当再次调用next时，会从刚才暂停的地方继续运行，直到运行下一个yield
+ __ iter__()方法返回迭代器自身，__ next__()方法返回序列中的下一个值。
```python
def __iter__(self):
  return self//返回迭代器本身
```

# 文件与文件夹操作（文件有打开必有关闭）
1.	open(fliename="str",enconding='UTF-8',mode='w') //**当文件不存在时，自动创建文件**
+  filename//文件不在当前目录，可使用路径：**file = open('/path/to/your/file.txt', 'r')**
+  mode='r'//文件打开的方式
+  buffering=-1//设置缓冲
+  encoding='UTF-8'//文件编码方式
+  errors=None//报错级别
+  newline=None//区分换行符
+  closefd=True//传入的file参数类型
+  opener=None  //设置自定义开启器，开启器的返回值必须是一个打开的文件描述符。 
2.	刷新缓冲区（将缓冲区中的数据立刻写入文件，同时清空缓冲区）：filename.flush();
3.  **OS模块**：
+  **文件重命名**：os.rename('name1','new-name'),文件删除os.remove('fliename')。 保存文件时动态命名：fp = open(name + '.text','w')
+  **创建目录上级目录必须存在**：os.mkdir(name + '\\temps')
+  **创建多级目录**OS.mkdirs()创建多级目录，会自动创建中间缺少的目录。
+  rmdir()删除目录，目录中不能有文件及子文件夹
+  remobe()删除文件
+  listdir()返回目录下的文件和目录列表
+  stat()返回文件属性
1. **shutil标准库**
   + 复制文件：copyfile()
   + 压缩文件：make_archive()
   + 解压缩文件；unpack_archive()
   + 删除文件：rmtree()
   + 复制文件夹：copytree()
2. **常用方法**：	
+ filename.read(size)： 
  size – 从文件中读取的字符数（文本模式）或字节数（二进制模式），默认为 -1，表示读取整个文件。
+ Filename.readline():
   方法用于从文件读取整行，包括 “\n” 字符。如果指定了一个非负数的参数，则返回指定大小的字节数，包括 “\n” 字符。
+ Filename.readlines():
  将每一行作为一个字符串存入并返回列表，对于大文件占用内存较大。
+ filename.write( str) 
   write() 方法用于向文件中写入指定字符串，在文件关闭前或缓冲区刷新前，字符串内容存储在缓冲区中，这时你在文件中是看不到写入的内容的。
+ writelines()
   方法用于向文件中写入一序列的字符串。filename.writelines( str) str – 要写入文件的字符串序列。Eg：f = open("shit.txt", "r+")
   seq = ['you', 'are', 'a', 'pig']
   f.writelines(seq)
   f.close()
   
### 文件打开方式 
| mode | 描述 |
| :--- |:---:|
|t|	文本模式 (默认)。|
|x	|写模式，新建一个文件，如果该文件已存在则会报错。|
|b|	二进制模式。|
|+|	打开一个文件进行更新(可读可写)。|
|U|	通用换行模式（Python 3 不支持）。|
|r|	以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。|
|rb|	以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。一般用于非文本文件如图片等。|
|r+	|打开一个文件用于读写。文件指针将会放在文件的开头。|
|rb+|	以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。一般用于非文本文件如图片等。|
|w	|打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
|wb|	以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。|
|w+|	打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
|wb+	|以二进制格式打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。|
|a|	打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。|
|ab|	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。|
|a+	|打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。|
|ab+|	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。|

# pycharm
## 虚拟环境(venv)
+ 每次使用pip命令安装第三方包时到解释器根目录下，若包更新可能导致新包与旧代码冲突，导致更新地狱。**可为每个项目创建独立的解释器虚拟环境，解决.**
+ pycharm:项目->解释器->添加解释器（基于X解释器==复制该解释器）
## 注释
+ 单行注释：#
+ 多行注释：''' '''
## 整体缩进
+ 整体缩进:鼠标拉选住代码块,按下tab键。
+ 反向缩进:鼠标拉选住代码块,按下shift+tab键。
## 代码折叠
+ 我们观察一下代码左侧的折叠线。这条细线显示在代码左侧，标记了代码块区域。单击一下折叠线，可以展开或折叠代码块。

## panda库

## conda库

## numpy库