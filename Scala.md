[toc]

***

# Scala-2.12.11

+ [官方文档](https://www.scala-lang.org/)

+ 完全面向对象的支持函数式编程的java拓展语言，运行在JVM上，可调用java代码，可使用java开发工具，可使用java类库，可调用java框架

+ **函数是一等公民，函数可以作为参数传递，也可以作为返回值返回，可在任何代码块中定义**
+ 对象的本质：对数据和行为的封装。
+ 函数式编程：，将问题分解成一个一个的步骤，将每个步骤进行封装（函数），通过调用这些封装好的步骤，解决问题。

+ 基础知识
  - 注释：`//`、`/* */`、`/** */`同java，ctrl + alt + L 格式化代码
  - 标识符命名规范：大部分与java相同，但允许以操作符开头，且只包含操作符（+ - * / # !等）的特殊命名，关键字用反引号包裹后也可使用

+ scala中一切数据都是对象，都是any的子类。
  - [scala 类图]("F:\Word-Markdown\Markdown-GitHub\图片\scala_class.png")

+ **对象和伴生对象**：scala中类和对象是平级的，没有静态方法，但可以通过伴生对象实现静态方法。相当于将java中static定义的所有部分放在了伴生对象中。
  - 伴生对象(object定义)和对象(class定义)同名，私有成员共享,属性和方法都可以通过伴生对象名（类名）直接调用
  - 伴生对象中定义构造方法apply，调用时直接使用伴生对象名调用，无需.apply()此为scala底层自动进行的优化。
  ```scala
  object Person{ 
    val country:String="China" 
  } 
  ```


+ 匿名类：无类名的类，直接用{}包裹。
  - 用于抽象类的实现：var  student = new Student {
    override def study(): Unit = {
      println("study")
    }
  }

+ 声明变量赋初值可用下划线_，编译器自动推断类型，但只能用于声明变量，不能用于声明常量。
+ 类型判断：
  - obj.isInstanceOf[T]：判断 obj 是不是 T 类型。 
  - obj.asInstanceOf[T]：将 obj 强转成 T 类型。 

## 数据类型与变量定义

### 变量和常量
+ 要求：
  - **声明变量时数据类型可省略（编译器自动推断），必须赋初值**
  - 类型确定后不可修改，scala为强类型语言
  - var定义的变量可改变，val定义的变量不可改变
+ var i:Int = 10 //定义一个Int类型的变量i，并赋值为10
+ val i:Int = 10 //定义一个Int类型的常量i，并赋值为10
+ 字符串定义时：多行字符串，在Scala中，利用三个双引号包围多行字符串就可以实现。输入的内容，带有空格、\t之类，导致每一行的开始位置不能整洁对齐。 应用scala的stripMargin方法，在scala中stripMargin默认是“|”作为连接符，//在多行换行的行头前面加一个“|”符号即可。
    ```scala
    val s =
    """
        |select
        |  name,
        |  age
        |from user
        |where name="zhangsan"
    """.stripMargin
    ```
### 数据类型
+ [scala 类图]("F:\Word-Markdown\Markdown-GitHub\图片\scala_class.png")
    - scala中一切事数据都是对象，都是any的子类。
+ **类型转换**
  - 强制类型转换调用：.toXXX()方法：仅支持就近转换，越级转换需要链式调用。
  - 基本类型转为String：调用toString()方法
+ Unit：相当于void，表示无返回值，是一个数据类型仅有一个实例()
+ Null:表示空，是所有引用类型AnyRef的子类，只有一个实例null，不可赋给值类型AnyVal
+ Nothing：所有类型的子类，没有实例，一般用于抛出异常时使用
    ```scala
    object TestSpecialType {
    def main(args: Array[String]): Unit = {
        def test(): Nothing = {
        throw new Exception()
        }
        test()
    }
    }
    ```

#### 数值类型
+ 整数类型（Byte、Short、Int、Long），浮点类型（Float、Double），字符类型（Char），布尔类型（Boolean）：true、false
+ StringOps是对String的增强类型。
#### 引用类型





### 输入输出
#### 输入
+ StdIn.readLine()、StdIn.readShort()、StdIn.readDouble()
    ```scala
    import scala.io.StdIn 
    
    object TestInput { 
    
        def main(args: Array[String]): Unit = { 
            // 1 输入姓名 
            println("input name:") 
            var name = StdIn.readLine()
        }
    } 
    ```
#### 字符串输出
+ 用+连接的普通输出法
+ printf格式化输出法，用%传值。
+ 字符串模板(插值字符串)：通过\$符号传值，如：
  ```scala
  val name = "Tom";println($"Hello,$name")
  ```
  - 字符串模板：\$"string"


## 运算符
+ 基本与java相同
  - /：整数除法时舍弃小数部分，浮点数除法时保留小数部分
  - ==：java：比较变量值即对象在内存中地址，字符串用equals比较内容是否相同，scala：都是比较内容是否相同
  - 没有++、--运算符，但可以用+=1、-=1代替，在对象的运算中+=将对象整体加入、++=将对象中每一个元素分别加入

+ \>>>: 无符号右移运算符，无论正负数，高位补0

+ scala运算符本质：没有运算符都是方法调用
  - 调用对象方法时，点可省略用空格分割即可
  - 单参或无参方法调用时，括号可省略
+ 没有三元运算符，可通过if代替

## 流程控制
### if：同java，但if语句有返回值(最后一行)，可赋值给变量
```scala
val res: String = if (age < 18) {
  "童年"
} else if (age >= 18 && age < 30) {
  "中年"
} else {
  "老年"
}
```
### 模式匹配match：替代Switch
+ match语句中
  - 每个case分支中，不需要使用break，自动中断
  - 所有的匹配都不成功时，会执行case _分支，类似于default
  - 可匹配任何类型数据
  - =>后的代码块，直到下一个case语句之前的代码是**作为一个整体执行**，可以使用{}括起来，也可以不括
  ```scala
  object TestMatchCase {
    def main(args: Array[String]): Unit = {
      var a: Int = 10
      var b: Int = 20
      var operator: Char = 'd'

      var result = operator match {
        case '+' => a + b
        case '-' => a - b
        case '*' => a * b
        case '/' => a / b
        case _ => "illegal"
      }
      println(result)
    }
  }
  ```

+ 模式守卫：用于范围匹配
  ```scala
  object TestMatchGuard {
    def main(args: Array[String]): Unit = {
      def abs(x: Int): Int = x match {
        case i if i >= 0 => i
        case j if j < 0 => -j
      }
      println(abs(-5))
    }
  }
  ```
+ 匹配字面量（字符串、字符、数字、布尔值）
  ```scala
  object TestMatchVal {
    def main(args: Array[String]): Unit = {
      println(describe(6))
    }

    def describe(x: Any): String = x match {
      case 5 => "Int five"
      case "hello" => "String hello"
      case true => "Boolean true"
      case '+' => "Char +"
      case _ => "Other type" // 添加默认匹配分支，避免编译警告
    }
  }
  ```
+ 匹配类型
  ```scala
  object TestMatchClass { 
  
      def describe(x: Any) = x match { 
  
          case i: Int => "Int" 
          case s: String => "String hello" 
          case m: List[_] => "List" 
          case c: Array[Int] => "Array[Int]" 
          case someThing => "something else " + someThing 
      } 
  
      def main(args: Array[String]): Unit = { 
  
          //泛型擦除 
          println(describe(List(1, 2, 3, 4, 5))) 
  
          //数组例外，可保留泛型 
          println(describe(Array(1, 2, 3, 4, 5, 6))) 
          println(describe(Array("abc"))) 
      } 
  } 
  ```
+ 匹配数组、元组
  - scala模式匹配可以对集合进行精确的匹配，例如匹配只有两个元素的、且第一个元素为0的数组。
  ```scala
  object TestMatchArray {

    def main(args: Array[String]): Unit = {

      for (arr <- Array(
        Array(0),
        Array(1, 0),
        Array(0, 1, 0),
        Array(1, 1, 0),
        Array(1, 1, 0, 1),
        Array("hello", 90)
      )) { // 对一个数组集合进行遍历

        val result = arr match {
          case Array(0) => "0" // 匹配Array(0) 这个数组

          case Array(x, y) => x + "," + y // 匹配有两个元素的数组，然后将将元素值赋给对应的x,y

          case Array(0, _*) => "以0开头的数组" // 匹配以0开头和数组

          case _ => "something else"
        }

        println("result = " + result)
      }
    }
  }
  ```
+ 匹配list
  ```scala
  //方式一
  object TestMatchList {
    def main(args: Array[String]): Unit = {

      // list是一个存放List集合的数组
      // 请思考，如果要匹配 List(88) 这样的只含有一个元素的列表,并原值返回.应该怎么写
      for (list <- Array(
        List(0),
        List(1, 0),
        List(0, 0, 0),
        List(1, 0, 0),
        List(88)
      )) {

        val result = list match {
          case List(0) => "0" // 匹配List(0)
          case List(x, y) => s"$x,$y" // 匹配有两个元素的List
          case List(head) => head.toString // 新增：匹配单个元素的List，返回元素值
          case List(0, _*) => "0 ..."
          case _ => "something else"
        }

        println(result)
      }
    }
  }

  //方式二
  object TestMatchList {
    def main(args: Array[String]): Unit = {
      val list: List[Int] = List(1, 2, 5, 6, 7)

      list match {
        case first :: second :: rest =>
          println(s"$first-$second-$rest")
        case _ =>
          println("something else")
      }
    }
  }
  ```
+ 匹配元组
  ```scala
  //例一
  object TestMatchTuple {
    def main(args: Array[String]): Unit = {
      // 对一个元组集合进行遍历
      for (tuple <- Array((0, 1), (1, 0), (1, 1), (1, 0, 2))) {
        val result = tuple match {
          case (0, _) => "0 ..." // 是第一个元素是0的元组
          case (y, 0) => s"$y0" // 匹配后一个元素是0的对偶元组
          case (a, b) => s"$a $b"
          case _ => "something else" // 默认
        }
        println(result)
      }
    }
  }
  //例二
  object TestGeneric {
    def main(args: Array[String]): Unit = {
      // 特殊的模式匹配1   打印元组第一个元素
      for (elem <- Array(("a", 1), ("b", 2), ("c", 3))) {
        println(elem._1)
      }
      for ((word, count) <- Array(("a", 1), ("b", 2), ("c", 3))) {
        println(word)
      }
      for ((word, _) <- Array(("a", 1), ("b", 2), ("c", 3))) {
        println(word)
      }
      for (("a", count) <- Array(("a", 1), ("b", 2), ("c", 3))) {
        println(count)
      }
      println("--------------")

      // 特殊的模式匹配2 给元组元素命名
      var (id, name, age): (Int, String, Int) = (100, "zs", 20)
      println((id, name, age))
      println("--------------")

      // 特殊的模式匹配3   遍历集合中的元组，给count * 2
      var list: List[(String, Int)] = List(("a", 1), ("b", 2), ("c", 3))
      // println(list.map(t => (t._1, t._2 * 2)))
      println(
        list.map {
          case (word, count) => (word, count * 2)
        }
      )

      var list1 = List(("a", ("a", 1)), ("b", ("b", 2)), ("c", ("c", 3)))
      // 原代码中 list1 定义后没有后续操作，可根据需求补充
    }
  }  
  ```
+ 匹配对象及例样
  ```scala
  class User(val name: String, val age: Int) 
  object User {
    def apply(name: String, age: Int): User = new User(name, age)

    def unapply(user: User): Option[(String, Int)] = {
      if (user == null)
        None
      else
        Some(user.name, user.age)
    }
  }

  object TestMatchUnapply {
    def main(args: Array[String]): Unit = {
      val user: User = User("zhangsan", 11)
      val result = user match {
        case User("zhangsan", 11) => "yes"
        case _ => "no"
      }
      println(result)
    }
  }
  ```
  - 当将User("zhangsan", 11)写在 case 后时[case User("zhangsan", 11) => "yes"]，会默认调用unapply 方法(对象提取器)，user 作为 unapply 方法的参数，unapply 方法将user 对象的name和age属性提取出来，与User("zhangsan", 11)中的属性值进行匹配
  - case中对象的unapply方法(提取器)返回Some，且所有属性均一致，才算匹配成功,属性不一致，或返回None，则匹配失败。
  - 若只提取对象的一个属性，则提取器为unapply(obj:Obj):Option[T] 
  - 若提取对象的多个属性，则提取器为unapply(obj:Obj):Option[(T1,T2,T3…)] 
  - 若提取对象的可变个属性，则提取器为unapplySeq(obj:Obj):Option[Seq[T]]
+ 匹配例样
  - 语法： case class Person (name: String, age: Int) 
  - 说明: 
    - 样例类仍然是类，和普通类相比，只是其自动生成了伴生对象，并且伴生对象中自动提供了一些常用的方法，如apply、unapply、toString、equals、hashCode和copy。 
    - 样例类是为模式匹配而优化的类，因为其默认提供了unapply方法，因此，样例类可以直接使用模式匹配，而无需自己实现unapply方法。 
    - 构造器中的每一个参数都成为val，除非它被显式地声明为var（不建议这样做） 
  ```scala
  case class User(name: String, age: Int)

  object TestMatchUnapply {
    def main(args: Array[String]): Unit = {
      val user: User = User("zhangsan", 11)
      val result = user match {
        case User("zhangsan", 11) => "yes"
        case _ => "no"
      }
      println(result)
    }
  }
  ```
+ 声明变量中的模式匹配
  ```scala
  case class Person(name: String, age: Int)

  object TestMatchVariable {
    def main(args: Array[String]): Unit = {
      val (x, y) = (1, 2)
      println(s"x=$x,y=$y")

      val Array(first, second, _*) = Array(1, 7, 2, 9)
      println(s"first=$first,second=$second")

      val Person(name, age) = Person("zhangsan", 16)
      println(s"name=$name,age=$age")
    }
  }
  ```


+ 声明for循环中的模式匹配
  ```scala
  object TestMatchFor {
    def main(args: Array[String]): Unit = {
      val map = Map("A" -> 1, "B" -> 0, "C" -> 3)
      // 直接将map中的k - v遍历出来
      for ((k, v) <- map) {
        println(s"$k -> $v") // 3个
      }
      println("----------------------")

      // 遍历value = 0的 k - v ,如果v不是0,过滤
      for ((k, 0) <- map) {
        println(s"$k --> 0") // B->0
      }
      println("----------------------")

      // if v == 0 是一个过滤的条件
      for ((k, v) <- map if v >= 1) {
        println(s"$k ---> $v") // A->1 和 C->3
      }
    }
  }
  ```

+ 声明偏函数中的模式匹配
  - 偏函数定义：
    ```scala
    val second: PartialFunction[List[Int], Option[Int]] = { 
      case x :: y :: _ => Some(y) 
    }
    ```
  - 偏函数原理：编译时多了一个用于参数检查的函数：isDefinedAt，如果参数匹配，则返回true，否则返回false
  - 偏函数使用：调用偏函数不可直接使用，应该.applyOrElse(List(1,2,3), (_: List[Int]) => None) ,如果满足条件执行apply方法，否则执行default方法。
  ```scala
  object MainApp {
    def main(args: Array[String]): Unit = {
      val list = List(1, 2, 3, 4, 5, 6, "test")
      val list1 = list.map {
        a =>
          a match {
            case i: Int => i + 1
            case s: String => s + "1" // 修正：字符串拼接不能用 + 1，改为 + "1"
          }
      }
      println(list1.filter(_.isInstanceOf[Int]))
    }
  }
  ```


### for循环
+ **1 to 10:[1:10],1 until 10 [1:10)**

+ **循环返回值**：for循环的返回值是一个集合Vector，用yield关键字，将每次循环的值返回，并赋值给res
  ```scala
  val res = for (i <- 1 to 10) yield i
  ```

+ 基本语法
  ```scala
  for (i <- 1 to 10) {
    println(i)
  }
  ```

+ for循环守卫：if条件判断
  ```scala
  for (i <- 1 to 10 if i % 2 != 0) {
    println(i)
  }
  ```

+ for循环步长
  ```scala
  for (i <- 1 to 10 by 2) { 
    println("i=" + i) 
  } 
  ```
+ 循环嵌套：
  - 一行多个表达式，以;分割两个for循环
  ```scala
  for(i <- 1 to 3; j <- 1 to 3) { 
    println(" i =" + i + " j = " + j) 
  } 
  ```
  - 多行多个表达式，用{}包裹
  ```scala
  for {
    i <- 1 to 3
    j <- 1 to 3
  } {
    println(" i =" + i + " j = " + j)
  }
  ```
### while/do_while循环
+ while语句没有返回值，即整个while语句的结果是Unit类型() 
+ **scala中没有break和continue**
  - break：用抛出异常退出、用scala自带的函数退出
    ```scala
    import scala.util.control.Breaks

    def main(args: Array[String]): Unit = {
      Breaks.breakable {
        for (elem <- 1 to 10) {
          println(elem)
          if (elem == 5) Breaks.break()
        }
      }
      println("正常结束循环")
    }
    ```
  - continue：用if代替

## 函数式编程：
+ 函数是一等公民，函数可以作为参数传递，也可以作为返回值返回

+ 控制抽象：允许我们定义一个函数，该函数接受另一个函数作为参数，并使用该函数来控制程序的执行流程。

+ 惰性加载：当函数返回值值被声明为lazy时，函数的执行将被推迟，直到我们首次对此取值，该函数才会执行。这种函数我们称之为惰性函数，lazy不可修改var型变量。

+ 函数和方法的区别：函数是定义在类外的，方法定义在类中。
  - 函数没有重载和重写的概念；方法可以进行重载和重写
  - Scala语言可以在任何的语法结构中声明任何的语法 
  - **Scala中函数可以嵌套定义** 
+ 基本语法
  ```scala
  def my_sum(x: Int, y: Int): Int返回值类型 = {
    x + y
  }
  ```
+ 函数参数
  ```scala
  object TestFunction {

    def main(args: Array[String]): Unit = {
      // （1）可变参数
      def test(s: String*): Unit = {
        println(s)
      }

      // 有输入参数：输出 Array
      test("Hello", "Scala")

      // 无输入参数：输出List()
      test()

      // (2)如果参数列表中存在多个参数，那么可变参数一般放置在最后
      def test2(name: String, s: String*): Unit = {
        println(name + "," + s)
      }

      test2("jinlian", "dalang")

      // (3)参数默认值
      def test3(name: String, age: Int = 30): Unit = {
        println(s"$name, $age")
      }

      // 如果参数传递了值，那么会覆盖默认值
      test3("jinlian", 20)

      // 如果参数有默认值，在调用的时候，可以省略这个参数
      test3("dalang")

      // 一般情况下，将有默认值的参数放置在参数列表的后面
      def test4(sex: String = "男", name: String): Unit = {
        println(s"$name, $sex")
      }

      // Scala函数中参数传递是，从左到右
      // test4("wusong")

      //（4）带名参数
      test4(name = "ximenqing")
    }
  }
  ```
### 函数至简原则
+ return 可以省略，Scala会使用函数体的最后一行代码作为返回值 
+ 如果函数体只有一行代码，可以省略花括号 
+ 返回值类型如果能够推断出来，那么可以省略（:和返回值类型一起省略），同时必须省略return，有return，则不能省略返回值类型，必须指定  
+ Scala 如果期望是无返回值类型，可以省略等号 
+ 如果函数无参，但是声明了参数列表，那么调用时，小括号，可加可不加 
+ 如果函数没有参数列表，那么小括号可以省略，调用时小括号必须省略 
+ 如果不关心名称，只关心逻辑处理，那么函数名（def）可以省略 
+ 如果函数明确声明unit，那么即使函数体中使用return关键字也不起作用 
```scala
def main(args: Array[String]): Unit = {
  // （0）函数标准写法
  def f(s: String): String = {
    return s + " jinlian"
  }
  println(f("Hello"))

  // 至简原则:能省则省

  //（1） return可以省略,Scala会使用函数体的最后一行代码作为返回值
  def f1(s: String): String = {
    s + " jinlian"
  }
  println(f1("Hello"))

  //（2）如果函数体只有一行代码，可以省略花括号
  def f2(s: String): String = s + " jinlian"

  //（3）返回值类型如果能够推断出来，那么可以省略（:和返回值类型一起省略）
  def f3(s: String) = s + " jinlian"
  println(f3("Hello3"))

  //（4）如果有return，则不能省略返回值类型，必须指定。
  def f4(): String = {
    return "ximenqing4"
  }
  println(f4())

  //（5）如果函数明确声明unit，那么即使函数体中使用return关键字也不起作用
  def f5(): Unit = {
    return "dalang5"
  }
  println(f5())

  //（6）Scala如果期望是无返回值类型,可以省略等号
  // 将无返回值的函数称之为过程
  def f6() {
    "dalang6"
  }
  println(f6())

  //（7）如果函数无参，但是声明了参数列表，那么调用时，小括号，可加可不加
  def f7() = "dalang7"
  println(f7())
  println(f7)

  //（8）如果函数没有参数列表，那么小括号可以省略,调用时小括号必须省略
  def f8 = "dalang"
  // println(f8())
  println(f8)

  //（9）如果不关心名称，只关心逻辑处理，那么函数名（def）可以省略
  val f9 = (x: String) => {
    println("wusong")
  }

  def f10(f: String => Unit) = {
    f("")
  }

  f10(f9)
  println(f10((x: String) => {
    println("wusong")
  }))
}
```

### 函数高级
+ 函数可以作为值传递
  ```scala
  object TestFunction { 
  
      def main(args: Array[String]): Unit = { 
  
          //（1）调用foo函数，把返回值给变量f 
          //val f = foo() 
          val f = foo 
          println(f) 
          //（2）在被调用函数foo后面加上 _，相当于把函数foo当成一个整体，
  传递给变量f1 
          val f1 = foo _ 
  
          foo() 
          f1() 
    //（3）如果明确变量类型，那么不使用下划线也可以将函数作为整体传递给
  变量 
    var f2:()=>Int = foo  
      } 
  
      def foo():Int = { 
          println("foo...") 
          1 
      }
  }
  ```

+ 函数可作为参数传递：
  ```scala
  def main(args: Array[String]): Unit = { 
      
      // （1）定义一个函数，函数参数还是一个函数签名；f表示函数名称;(Int,Int)
  表示输入两个Int参数；Int表示函数返回值 
      def f1(f: (Int, Int) => Int): Int = { 
          f(2, 4) 
      } 
      
      // （2）定义一个函数，参数和返回值类型和f1的输入参数一致 
      def add(a: Int, b: Int): Int = a + b 
      
      // （3）将add函数作为参数传递给f1函数，如果能够推断出来不是调用，_
  可以省略 
      println(f1(add)) 
  println(f1(add _)) 
  //可以传递匿名函数 
  } 
  ```

+ 函数可以作为函数的返回值
  ```scala
  def main(args: Array[String]): Unit = {
    def f1() = {
      def f2() = {
        // 这里原代码为空，可根据实际需求补充逻辑
      }
      f2 _
    }

    val f = f1()
    // 因为f1函数的返回值依然为函数，所以可以变量f可以作为函数继续调用
    f()
    // 上面的代码可以简化为
    f1()()
  }
  ```
### 匿名函数
+ 函数形式：(x:Int)=>{函数体} 
  - 参数的类型可以省略，会根据形参进行自动的推导 
  - 类型省略之后，发现只有一个参数，则圆括号可以省略；其他情况：没有参数和参数超过1的永远不能省略圆括号。 
  - 匿名函数如果只有一行，则大括号也可以省略 
  - 如果参数只出现一次，则参数省略且后面参数可以用_代替

### 函数柯里化与闭包
+ 闭包：将函数运行所有的变量等保存下来，形成一个封闭的环境，这个环境就是闭包
+ 柯里化：把一个参数列表的多个参数，变成多个参数列表。
  ```scala
  object TestFunction {
    def main(args: Array[String]): Unit = {
      def f1() = {
        var a: Int = 10
        def f2(b: Int) = {
          a + b
        }
        f2 _
      }

      // 在调用时，f1函数执行完毕后，局部变量a应该随着栈空间释放掉
      val f = f1()

      // 但是在此处，变量a其实并没有释放，而是包含在了f2函数的内部，形成了闭合的效果
      println(f(3))

      println(f1()(3))

      // 函数柯里化，其实就是将复杂的参数逻辑变得简单化,函数柯里化一定存在闭包
      def f3()(b: Int) = { 
        a + b 
      }

      println(f3()(3))
    }
  }
  ```
### 递归
+ 递归不可无限进行。
+ scala中递归函数必须声明函数返回值类型


## 面对对象
+ 包的命名：com.公司名.项目名.模块名
+ 包对象：
  - scala中可为每个包定义一个同名包对象，定义在包中的一切，作为其包下的所有的class和object的共享变量
  ```scala
  package com.atguigu.chapter01{
    val school = "atguigu"
  }
  ```

+ 导包：
  - 和Java一样，可以在顶部使用import导入，在这个文件中的所有类都可以使用。 
  - 局部导入：什么时候使用，什么时候导入。在其作用范围内都可以使用 
  - 通配符导入：import java.util._ 
  - 给类起名：import java.util.{ArrayList=>JL} 
  - 导入相同包的多个类：import java.util.{HashSet, ArrayList} 
  - 屏蔽类：import java.util.{ArrayList =>_,_} 

+ 创建对象：new 类名()，var修饰对象不可修规对象引用(静态对象类似java的string)，**自动推导类型不能多态，多态需要显示声明**


### 类
+ java中的类若是public必须与文件名一致，scala中没有public关键字，默认都是public，一个scala文件中可以有多个类。

+ 基本语法：同java

+ 属性：
  ```scala
  package com.atguigu.scala.test

  import scala.beans.BeanProperty

  class Person {
    var name: String = "bobo" // 定义属性
    var age: Int = _ // _表示给属性一个默认值

    // Bean属性（@BeanProperty）
    @BeanProperty var sex: String = "男"
    // val修饰的属性不能赋默认值，必须显示指定
  }

  object Person {
    def main(args: Array[String]): Unit = {
      var person = new Person()
      println(person.name)

      person.setSex("女")
      println(person.getSex)
    }
  }
  ```

### 封装
+  把抽象出的数据和对数据的操作封装在一起，数据被保护在内部，私有成员，程序的其它部分只有通过被授权的操作（成员方法），才能对数据进行操作。

+ Scala中public属性，底层实际为private，并通过 get 方法（obj.field()）和 set 方法（obj.field_=(value)）对其进行操作。但可设置get、set方法以兼容Java反射机制。

+ 访问权限
  - Scala 中属性和方法的默认访问权限为public，但Scala中无public关键字。 
  - private 为私有权限，只在类的内部和伴生对象中可用。 
  - protected 为受保护权限，Scala 中受保护权限比 Java 中更严格，同类、子类可以访问，同包无法访问。 
  - private[包名]增加包访问权限，包名下的其他类也可以使用 


#### 方法
+ 基本方法
  ```
  def 方法名(参数列表) [：返回值类型] = {  
  方法体 
  } 
  ```
  
### **构造器**
+ Scala中类有一个主构造器和任意数量的辅助构造器，
  - 主构造器与类名定义在一起，辅助构造器使用关键字this定义。
  - 主构造器无参可省略小括号，调用时也可省略小括号。
  - 辅助构造器，函数的名称 this，可以有多个，编译器通过参数的个数及类型来区分。 
  - 辅助构造方法不能直接构建对象，必须直接或者间接调用主构造方法。
  ```scala
  class 类名(形参列表) { // 主构造器
    // 类体
    def this(形参列表) { // 辅助构造器
    }
    def this(形参列表) { // 辅助构造器可以有多个...
    }
  }
  ```

+ 构造器参数
  - 无修饰：局部变量
  - var修饰：成员属性，可修改
  - val修饰：只读属性，不可修改

### 继承和多态
+ 基本语法：class 子类名 extends 父类名 {类体}
  - 子类继承父类属性和方法
  - 仅支持单继承
+ **继承后构造方法的调用：**  
  - 调用顺序：父类构造器 -> 子类构造器
  - 棱形继承时：
    - 依次调用继承父类的方法，但每个方法仅会被调用一次
+ **调用父类方法super**
  - super[父类名].方法名()//多个实现时时
+ 动态绑定 
  - Scala中属性和方法都是动态绑定，而Java中只有方法为动态绑定

### 抽象类
+ 基本语法
  - 定义抽象类：abstract class Person{} //通过 abstract 关键字标记抽象类 
  - 定义抽象属性：val|var name:String //一个属性没有初始化，就是抽象属性 
  - 定义抽象方法：def  hello():String //只声明而没有实现的方法，就是抽象方法 

+ 继承和重写
  - 如果父类为抽象类，那么子类需要将抽象的属性和方法实现，否则子类也需声明为抽象类 
  - 重写非抽象方法需要用override修饰，重写抽象方法则可以不加override。 
  - 子类中调用父类的方法使用super关键字 
  - 子类对抽象属性进行实现，父类抽象属性可以用var修饰； 
  - 子类对非抽象属性重写，父类非抽象属性只支持val类型，而不支持var。 因为var修饰的为可变变量，子类继承之后就可以直接使用，没有必要重写 


### 特质Trait（类似java中接口）
+ 一个类可以混入（mixin）多个特质。即可代替接口也是对单继承机制的补充。
  - 特质可以同时拥有抽象方法和具体方法 
  - 一个类可以混入（mixin）多个特质 
  - 所有的Java接口都可以当做Scala特质使用 
  - 动态混入：可灵活的扩展类的功能 
    - 动态混入：创建对象时混入trait，而无需使类混入该trait 
    - 如果混入的trait中有未实现的方法，则需要实现 
+ 特质叠加：混入的特征具有相同的方法导致冲突，解决方法将冲突方法叠加起来即为特质叠加
  - 可通过super[class_name].method()调用特定的方法
+ 特质和抽象2方法：
  - 优先使用特质。一个类扩展多个特质是很方便的，但却只能扩展一个抽象类。 
  - 如果你需要构造函数参数，使用抽象类。因为抽象类可以定义带参数的构造函数，而特质不行（有无参构造）。 
+ 基本语法
  ```scala
  trait PersonTrait { 
    // 声明属性 
    var name:String = _ 

    // 声明方法 
    def eat():Unit={ } 

    // 抽象属性 
    var age:Int 

    // 抽象方法 
    def say():Unit 
  } 
  ```

+ 实现接口（特质）
  - 没有父类：class  类名 extends  特质1   with    特质2  
  - 有父类（必须先继承父类）：class  类名  extends  父类   with  特质1   with   特质2 

### 枚举、自定义和应用类
#### 枚举 Enumeration
+ 基本语法
  ```scala
  object Color extends Enumeration { 
      val RED = Value(1, "red") 
      val YELLOW = Value(2, "yellow") 
      val BLUE = Value(3, "blue") 
  }
  ```

#### 自定义类型
+ 基本语法
  ```scala
  object Test { 
    def main(args: Array[String]): Unit = { 
      type S=String 
      var v:S="abc" 
      def test():S="xyz" 
    } 
  }
  ```

#### 应用类 App
+ 基本语法
  ```scala
  // 应用类 
  object Test20 extends App { 
    println("xxxxxxxxxxx"); 
  } 
  ```

## 集合
+ Scala 的集合有三大类：序列Seq、集Set、映射Map，所有的集合都扩展自Iterable特质，集合类几乎都有可变、不可变两种，不可变集合类似于java中String不可修改。
+ [不可变集合继承图]("F:\Word-Markdown\Markdown-GitHub\图片\scala_集合不可变继承图.png")
  - IndexedSeq 是通过索引来查找和定位，因此速度快，比如String就是一个索引集合，可通过索引定位。
  - LinearSeq 是线型的，即有头尾的概念，这种数据结构一般是通过遍历来查找
  - Scala中的Map体系有一个SortedMap，说明Scala的Map可以支持排序
  - ）Seq 是Java没有的，我们发现List归属到Seq了，因此这里的List就和Java不是同一个概念了

+ [可变集合继承图]("F:\Word-Markdown\Markdown-GitHub\图片\scala_可变集合继承图.png")
  
  
### 集合常用的属性和操作
+ 合并集合：+作为一个元素并入 、++将集合中每一个元素加入、::同+、:::同++
+ 以 ：结尾的方法调用时从左到右调用。
+ mutable.XXX:可变集合,默认为不可变集合，通过mutable.XXX创建可变集合
+ 集合常用+=、-=增减数据，但要注意当操作对象是map时需要用()包裹k-v对，否则会被认为是双参数函数调用。eg：map += (("key", "value"))
+ println(set.mkString(",")),设置打印分割符。
+ 打印集合：
  - N.foreach(println)
  - for(elem <- N) println(elem)
  - for(elem <- N.iterate) println(elem)
+ 获取集合的头：head
+ 获取集合的尾（除了头的都是尾）：tail
+ 集合最后一个数据 ：last
+ 集合初始数据（不包含最后一个的所有元素）：init
+ 反转：reverse
+ 取前（后）n个元素
  - take(N)
  -  takeRight(N)
+ 删除前（后）n个元素
  -  drop(N)
  -  dropRight(N)
+ 集合操作
  - 并集：list1.union(list2)
  - 交集：list1.intersect(list2)
  - 差集：list1.diff(list2)
  - 拉链 注:如果两个集合的元素个数不相等，那么会将同等数量的数据进行拉链，多余的数据省略不用：list1.zip(list2)，结果为二元组集合[(x,y),(x,y),...]
  - 滑窗
    list1.sliding(2, 5).foreach(println)
+ 获取集合长度:length
+ 获取集合大小,等同于length :size 
+ 生成字符串 : list.mkString(",") //生成字符串，以,分隔
+ 是否包含元素：contains(元素)
### 集合常用简单计算函数
+ sum、max、min、product(乘积)
+ 排序：
  - sorted：升序，可传递隐式参数Ordering[T]实现自定义排序：N.sorted(Ordering[Int].reverse)
  - sortBy：根据指定属性排序，可柯里化传递第二个参数（隐式参数）Ordering[T]实现自定义排序，N.sortBy(x => x.name)(Ordering[Int].reverse)
  - sortWith：通过comparator函数根据指定规则排序，N.sortWith((x, y) => x > y)可简化为N.sortWith(_ > _)
### 集合的高级计算函数：flatmap
+ 扁平化：将集合中的每个元素的子元素映射到某个函数并返回新集合
+ 扁平化+映射 注：flatMap相当于先进行map操作，在进行flatten操作集合中的每个元素的子元素映射到某个函数并返回新集合
+ 实例
  ```scala
  object TestList {
    def main(args: Array[String]): Unit = {
      val list: List[Int] = List(1, 2, 3, 4, 5, 6, 7, 8, 9)
      val nestedList: List[List[Int]] = List(List(1, 2, 3), List(4, 5, 6), List(7, 8, 9))
      val wordList: List[String] = List("hello world", "hello atguigu", "hello scala")

      //（1）过滤
      println(list.filter(x => x % 2 == 0))

      //（2）转化/映射
      println(list.map(x => x + 1))

      //（3）扁平化
      println(nestedList.flatten)

      //（4）扁平化+映射 注：flatMap相当于先进行map操作，再进行flatten操作
      println(wordList.flatMap(x => x.split(" ")))

      //（5）分组
      println(list.groupBy(x => x % 2))
    }
  }
  ```
+ 约归操作(Reduce简化)：将数据进行聚合减少数据
  ```scala
  object TestReduce {
    def main(args: Array[String]): Unit = {
      val list = List(1, 2, 3, 4)

      // 将数据两两结合，实现运算规则
      val i: Int = list.reduce((x, y) => x - y)
      println(s"i = $i")

      // 从源码的角度，reduce底层调用的其实就是reduceLeft
      // val i1 = list.reduceLeft((x, y) => x - y)

      // ((4 - 3) - 2 - 1) = -2
      val i2 = list.reduceRight((x, y) => x - y)
      println(i2)
    }
  }
  ```
+ Fold折叠：化简的一种特殊情况。 
  ```scala
  //（1）案例实操：fold基本使用 
  object TestFold {
    def main(args: Array[String]): Unit = {
      val list = List(1, 2, 3, 4)

      // fold方法使用了函数柯里化，存在两个参数列表
      // 第一个参数列表为 ： 零值（初始值）
      // 第二个参数列表为： 简化规则

      // fold底层其实为foldLeft
      val i = list.foldLeft(1)((x, y) => x - y)

      val i1 = list.foldRight(10)((x, y) => x - y)

      println(i)
      println(i1)
    }
  }

  （2）案例实操：两个集合合并
  import scala.collection.mutable

  object TestFold {
    def main(args: Array[String]): Unit = {
      // 两个Map的数据合并
      val map1 = mutable.Map("a" -> 1, "b" -> 2, "c" -> 3)
      val map2 = mutable.Map("a" -> 4, "b" -> 5, "d" -> 6)
      val map3: mutable.Map[String, Int] = map2.foldLeft(map1) {
        (map, kv) =>
          val k = kv._1
          val v = kv._2
          map(k) = map.getOrElse(k, 0) + v
          map
      }
      println(map3)
    }
  }
  ```

### 数组
+ 访问数组元素：arr(0)，不用[]
+ 可变与不可变数组之间的转换
  - 不可变数组转可变数组：arr.toBuffer
  - 可变数组转不可变数组：arr.toArray
#### 不可变数组
+ 定义：val arr = new Array\[Int](10) // 定义一个长度为10的数组
  - val arr = Array(1,2,3,4,5) // 定义数组并赋给值
+ 应用
  ```scala
  object TestArray {
    def main(args: Array[String]): Unit = {
      //（1）数组定义
      val arr01 = new Array[Int](4)
      println(arr01.length) // 4

      //（2）数组赋值
      //（2.1）修改某个元素的值
      arr01(3) = 10
      //（2.2）采用方法的形式给数组赋值
      arr01.update(0, 1)

      //（3）遍历数组
      //（3.1）查看数组
      println(arr01.mkString(","))

      //（3.2）普通遍历
      for (i <- arr01) {
        println(i)
      }

      //（3.3）简化遍历
      def printx(elem: Int): Unit = {
        println(elem)
      }
      arr01.foreach(printx)
      // arr01.foreach((x) => {println(x)})
      // arr01.foreach(println(_))
      arr01.foreach(println)

      //（4）增加元素（由于创建的是不可变数组，增加元素，其实是产生新的数组）
      println(arr01)
      val ints: Array[Int] = arr01 :+ 5
      println(ints)
    }
  }
  ```
#### 可变数组
+ **需要导入**:scala.collection.mutable.ArrayBuffer
+ 定义：val arr = ArrayBuffer\[Int]() // 定义一个数组,数组中元素个数不定
+ 应用
    ```scala
    import scala.collection.mutable.ArrayBuffer

    object TestArrayBuffer {
      def main(args: Array[String]): Unit = {
        //（1）创建并初始赋值可变数组
        val arr01 = ArrayBuffer[Any](1, 2, 3)

        //（2）遍历数组
        for (i <- arr01) {
          println(i)
        }
        println(arr01.length) // 3
        println("arr01.hash=" + arr01.hashCode())

        //（3）增加元素
        //（3.1）追加数据
        arr01 += 4
        //（3.2）向数组最后追加数据
        arr01.append(5, 6)
        //（3.3）向指定的位置插入数据
        arr01.insert(0, 7, 8)
        println("arr01.hash=" + arr01.hashCode())

        //（4）修改元素
        arr01(1) = 9 // 修改第2个元素的值
        println("--------------------------")

        for (i <- arr01) {
          println(i)
        }
        println(arr01.length) // 这里原注释有误，按代码逻辑此时长度应为8而非5
      }
    }
    ```

#### 多维数组
+ 定义：val arr = Array.ofDim[Int](3, 4) // 定义一个3行4列的二维数组

### 列表List

#### 不可变列表
+ list默认是不可变的
  ```scala
  object TestList { 
  
      def main(args: Array[String]): Unit = { 
  
          //（1）List默认为不可变集合 
          //（2）创建一个List（数据有顺序，可重复） 
          val list: List[Int] = List(1,2,3,4,3) 
          
          //（7）空集合Nil 
          val list5 = 1::2::3::4::Nil 
  
          //（4）List增加数据 
          //（4.1）::的运算规则从右向左 
          //val list1 = 5::list 
          val list1 = 7::6::5::list 
          //（4.2）添加到第一个元素位置 
          val list2 = list.+:(5) 
  
          //（5）集合间合并：将一个整体拆成一个一个的个体，称为扁平化 
          val list3 = List(8,9) 
          //val list4 = list3::list1 
          val list4 = list3:::list1 
  
          //（6）取指定数据 
          println(list(0)) 
  
          //（3）遍历List 
          //list.foreach(println) 
          //list1.foreach(println) 
          //list3.foreach(println) 
          //list4.foreach(println) 
          list5.foreach(println) 
      } 
  } 
  ```

#### 可变列表
```scala
import scala.collection.mutable.ListBuffer

object TestList {
  def main(args: Array[String]): Unit = {
    //（1）创建一个可变集合
    val buffer = ListBuffer(1, 2, 3, 4)
    //（2）向集合中添加数据
    buffer += 5
    buffer.append(6)
    buffer.insert(1, 2)
    //（3）打印集合数据
    buffer.foreach(println)
    //（4）修改数据
    buffer(1) = 6
    buffer.update(1, 7)
    //（5）删除数据
    buffer -= 5
    buffer.remove(5)
  }
}
```

### set
+ **需要导入**：import scala.collection.mutable.Set
+ 不可变集合
  ```scala
  def main(args: Array[String]): Unit = {
    //（1）Set默认是不可变集合，数据无序,数据不可重复
    val set = Set(1, 2, 3, 4, 5, 6) 
  }
  ```
+ 可变集合
  ```scala
  import scala.collection.mutable

  object TestSet {
    def main(args: Array[String]): Unit = {
      //（1）创建可变集合
      val set = mutable.Set(1, 2, 3, 4, 5, 6)

      //（2）打印集合
      set.foreach(println)
      println(set.mkString(","))

      //（3）集合添加元素
      set += 8

      //（4）向集合中添加元素，返回一个新的Set
      val ints = set + 9
      println(ints)
      println("set=" + set)

      //（5）删除数据
      set -= 5
    }
  }
  ```

### map
+ +=：update操作(有则更新无则添加)： 用()包裹k-v对，否则会被认为是双参数函数调用。
  - eg：map += (("key", "value")) 
  - eg：map1.update("key", "value")
  - eg：map += "key" -> "value"
  - eg：map.put("a", 4)
+ 删除操作：eg：map -= ("key", "value")
+ 创建不可变集合Map：val map = Map("a" -> 1, "b" -> 2, "c" -> 3)
+ 创建可变集合Map：val map = mutable.Map("a" -> 1, "b" -> 2, "c" -> 3)
+ 访问map中元素，不存在返回默认值：map.getOrElse("d", 0)或map.get("d").getOrElse(0)
+ 不可变map
  ```scala
  object TestMap {
    def main(args: Array[String]): Unit = {
      
      val map = Map("a" -> 1, "b" -> 2, "c" -> 3)

      //（2）循环打印
      map.foreach((kv) => println(kv))
    }
  }
  ```

+ 可变map
  ```scala
  import scala.collection.mutable

  object TestSet {
    def main(args: Array[String]): Unit = { 
      val map = mutable.Map("a" -> 1, "b" -> 2, "c" -> 3)

      //（2）打印集合
      map.foreach(kv => println(kv))
    }
  }
  ```

### 元组(Tuple：保存不同元素的集合)
+ 元组中最大长度为22
+ 声明元组：val tuple = (1, "bobo", true)
+ 访问元素
  - tuple1._N:访问第N个元素
  - tuple1.productElement(N):访问第N个元素
  ```scala
  object TestTuple {
    def main(args: Array[String]): Unit = { 

      val tuple: (Int, String, Boolean) = (40, "bobo", true) 

      //Map中的键值对其实就是元组,只不过元组的元素个数为2，称之为对偶
      val map = Map("a" -> 1, "b" -> 2, "c" -> 3)
      val map1 = Map(("a", 1), ("b", 2), ("c", 3))

      map.foreach(tuple => println(tuple._1 + "=" + tuple._2))
    }
  }
  ```

### queue
+ 进队和出队的方法分别为enqueue和dequeue。
  ```scala
  object TestQueue { 
    def main(args: Array[String]): Unit = { 
      val que = new mutable.Queue[String]() 
      
      que.enqueue("a", "b", "c")  

      println(que.dequeue()) 
      println(que.dequeue()) 
      println(que.dequeue()) 
    } 
  } 
  ```

### 并行集合
+ 用于多核CPU环境下的并行计算。
  ```scala
  object TestPar {
    def main(args: Array[String]): Unit = {
      val result1 = (0 to 100).map {case  _ =>
        Thread.currentThread.getName
      }
      val result2 = (0 to 100).par.map { case _ =>
        Thread.currentThread.getName
      }

      println(result1)
      println(result2)
    }
  }
  ```

## 异常处理
+ 实例
  ```scala
  object ExceptionHandlingExample {
    def main(args: Array[String]): Unit = {
      try {
        var n = 10 / 0
      } catch {
        case ex: ArithmeticException =>
          // 发生算术异常
          println("发生算术异常")
        case ex: Exception =>
          // 对异常处理
          println("发生了异常1")
          println("发生了异常2")
      } finally {
        println("finally")
      }
    }
  }
  ```
+ 我们将可疑代码封装在try块中。在try块之后使用了一个catch处理程序来捕获异常。如果发生任何异常，catch处理程序将处理它，程序将不会异常终止。 
+ Scala 的异常的工作机制和Java一样，但是Scala没有“checked（编译期）”异常，即Scala 没有编译异常这个概念，异常都是在运行的时候捕获处理。 
+ 异常捕捉的机制与其他语言中一样，如果有异常发生，catch 子句是按次序捕捉的。因此，在catch子句中，越具体的异常越要靠前，越普遍的异常越靠后，如果把越普遍的异常写在前，把具体的异常写在后，在Scala中也不会报错，但这样是非常不好的编程风格。 
+ finally 子句用于执行不管是正常处理还是有异常发生时都需要执行的步骤，一般用于对象的清理工作，这点和Java一样。 
+ 用throw 关键字，抛出一个异常对象。所有异常都是Throwable的子类型。throw表达式是有类型的，就是Nothing，因为Nothing 是所有类型的子类型，所以throw 表达式可以用在需要类型的地方 
  ```scala
  def test():Nothing = { 
    throw new Exception("不对") 
  } 
  ```
+ java 提供了throws关键字来声明异常。可以使用方法定义声明异常。它向调用者函数提供了此方法可能引发此异常的信息。它有助于调用函数处理并将该代码包含在try-catch块中，以避免程序异常终止。在Scala中，可以使用throws注解来声明异常
  ```scala 
  def main(args: Array[String]): Unit = { 
    f11() 
  } 
  @throws(classOf[NumberFormatException]) 
    def f11()={ 
    "abc".toInt 
  }
  ```

## 隐式转换
+ ***当编译器第一次编译失败的时候，会在当前的环境中查找能让代码编译通过的方法，用于将类型进行转换，实现二次编译***

### 隐式函数
+ 说明 ：隐式转换可以在不需改任何代码的情况下，扩展某个类的功能
  ```scala
  //通过隐式转化为Int类型增加方法。
  class MyRichInt(val self: Int) {
    def myMax(i: Int): Int = {
      if (self < i) i else self
    }

    def myMin(i: Int): Int = {
      if (self < i) self else i
    }
  }

  object TestImplicitFunction {
    // 使用implicit关键字声明的函数称之为隐式函数
    implicit def convert(arg: Int): MyRichInt = {
      new MyRichInt(arg)
    }

    def main(args: Array[String]): Unit = {
      // 当想调用对象功能时，如果编译错误，那么编译器会尝试在当前作用域范围内查找能调用对应功能的转换规则，这个调用过程是由编译器完成的，所以称之为隐式转换。也称之为自动转换
      println(2.myMax(6))
    }
  }
  ```

### 隐式参数：
+ 普通方法或者函数中的参数可以通过implicit 关键字声明为隐式参数，调用该方法时，就可以传入该参数，编译器会在相应的作用域寻找符合条件的隐式值。 
  - 同一个作用域中，相同类型的隐式值只能有一个 
  - 编译器按照隐式参数的类型去寻找对应类型的隐式值，与隐式值的名称无关。 
  - 隐式参数优先于默认参数 
+ 实例
  ```scala
  object TestImplicitParameter { 
    implicit val str: String = "hello world!" 

    def hello(implicit arg: String="good bey world!"): Unit = { 
      println(arg) 
    } 
    
    def main(args: Array[String]): Unit = { 
      hello 
    } 
  } 
  ```
### 隐式类
+ 隐式类，可以使用 implicit 声明类，隐式类的非常强大，同样可以扩展类的功能，在集合中隐式类会发挥重要的作用
  - 其所带的构造参数有且只能有一个 
  - 隐式类必须被定义在“类”或“伴生对象”或“包对象”里，即隐式类不能是**顶级的**。
  ```scala
  object TestImplicitClass {
    implicit class MyRichInt(arg: Int) {
      def myMax(i: Int): Int = {
        if (arg < i) i else arg
      }

      def myMin(i: Int) = {
        if (arg < i) arg else i
      }
    }

    def main(args: Array[String]): Unit = {
      println(1.myMax(3))
    }
  }
  ```

### 隐式解析机制 
+ 首先会在当前代码作用域下查找隐式实体（隐式方法、隐式类、隐式对象）。（一般是这种情况） 
+ 如果第一条规则查找隐式实体失败，会继续在隐式参数的类型的作用域里查找。类型的作用域是指与该类型相关联的全部伴生对象以及该类型所在包的包对象。 
  ```scala
  package com.atguigu.chapter10

  import com.atguigu.chapter10.Scala05_Transform4.Teacher

  // （2）如果第一条规则查找隐式实体失败，会继续在隐式参数的类型的作用域里查找。
  // 类型的作用域是指与该类型相关联的全部伴生模块
  object TestTransform extends PersonTrait {
    def main(args: Array[String]): Unit = {
      // （1）首先会在当前代码作用域下查找隐式实体
      val teacher = new Teacher()
      teacher.eat()
      teacher.say()
    }

    class Teacher {
      def eat(): Unit = {
        println("eat...")
      }
    }
  }

  trait PersonTrait

  object PersonTrait {
    // 隐式类 : 类型1 => 类型2
    implicit class Person5(user: Teacher) {
      def say(): Unit = {
        println("say...")
      }
    }
  }
  ```

## 泛型

### 协变和逆变 
+ class MyList[T] //不变 
  - 逆变：Son是Father的子类，但MyList[Son]和MyList[Father]的没有关系，为默认情况。
  - 逆变：仅可用于输入类型如返回值，即当你有一个函数或方法接受一个泛型类型作为参数时，可以使用逆变。例如，一个函数接受一个打印器，并且你希望这个打印器可以处理父类型的元素。
+ class MyList[+T]{ //协变 }  
  - 协变：Son是Father的子类，则MyList[Son] 也作为MyList[Father]的“子类”。
  - 协变：仅可用于输出类型，即当你有一个函数或方法返回一个泛型类型时，可以使用协变。例如，一个函数返回一个列表，并且你希望这个列表可以包含子类型的元素。
+ class MyList[-T]{ //逆变 } 
  - 逆变：Son是Father的子类，则MyList[Son]作为MyList[Father]的“父类”。

+ 实例：
  ```scala
  // 泛型模板
  // class MyList<T>{}
  // 不变
  // class MyList[T]{}
  // 协变
  // class MyList[+T]{}
  // 逆变
  // class MyList[-T]{}

  class Parent
  class Child extends Parent
  class SubChild extends Child

  object Scala_TestGeneric {
    def main(args: Array[String]): Unit = {
      // var s: MyList[Child] = new MyList[SubChild]
    }
  }
  ```
### 泛型上下限 
+ 泛型的上下限 : 对传入的泛型进行限定，仅允许传入某一类的及其子类或父类。
+ 语法：
  ```scala
  Class PersonList[T <: Person]{ //泛型上限，仅允许传入Person及其子类
  } 
  Class PersonList[T >: Person]{ //泛型下限 
  }
  ```
+ 实例：
  ```scala
  class Parent
  class Child extends Parent
  class SubChild extends Child

  object Scala_TestGeneric {
    def main(args: Array[String]): Unit = {
      // test(classOf[SubChild])
      // test[Child](new SubChild)
    }

    // 泛型通配符之上限
    // def test[A <: Child](a: Class[A]): Unit = {
    //   println(a)
    // }

    // 泛型通配符之下限
    // def test[A >: Child](a: Class[A]): Unit = {
    //   println(a)
    // }

    // 泛型通配符之下限 形式扩展
    def test[A >: Child](a: A): Unit = {
      println(a.getClass.getName)
    }
  }
  ```
### 上下文限定 
+ 语法：
  ```scala
  def f[A : B](a: A) = println(a) //等同于 def f[A](a:A)(implicit arg:B[A])=println(a)
  ```
  - 上下文限定是将泛型和隐式转换的结合产物，以下两者功能相同，使用上下文限定[A : Ordering]之后，方法内无法使用隐式参数名调用隐式参数，需要通过implicitly[Ordering[A]]获取隐式变量，如果此时无法查找到对应类型的隐式变量，会发生出错误。
    ```scala
    implicit val x = 1 
    val y = implicitly[Int] 
    val z = implicitly[Double] 
    ```
+ 实例：
  ```scala
  def f[A:Ordering](a:A,b:A) =implicitly[Ordering[A]].compare(a,b) 
  def f[A](a: A, b: A)(implicit ord: Ordering[A]) = ord.compare(a, b) 
  ```










