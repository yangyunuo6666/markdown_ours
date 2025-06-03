[toc]
***
# R
+ R 语言区分大小写，true 或 True 不能代表 TRUE。
+ **R 语言的变量定义，并不像一些强类型语言中的语法规则，需要专门为变量设置名称和数据类型，每当在 R 中使用赋值运算符时，实际上就是定义了一个新的变量** 
## 特殊
+ %% ：求余数
+ %/% ：取mod
+ next//跳过本次循环,替换了continue
+ ->> ：向右赋值
+ ：：用于创建一系列数字的向量
+ %in%	：用于判断元素是否在向量里，返回布尔值，有的话返回 TRUE，没有返回 FALSE
+ %*%	：用于矩阵与它转置的矩阵相乘
+ 常用数学函数
  - sqrt(n)	n的平方根
  - exp(n)	自然常数e的n次方，
  - log(m,n)	m的对数函数，返回n的几次方等于m
  - log10(m)	相当于log(m,10)
  - round	(n)	对 n 四舍五入取整，**当取整位是偶数的时候，五也会被舍去，这一点与 C 语言有所不同。**
  -	round(n, m)	对 n 保留 m 位小数四舍五入
  - ceiling	(n)	对 n 向上取整
  - floor	(n)	对 n 向下取整
+ R 的三角函数是弧度制：sin、asin、cos、acos、tan、atan、atan
+ 正态分布X_norm
  - d , 概率密度函数
  - p , 概率密度积分函数（从无限小到 x 的积分）
  - q , 分位数函数
  - r , 随机数函数（常用于概率仿真）
## R对象操作
+ is.typeof(x)判断x的类型
+ class(x)返回x的类型
+ 
## R包操作
+ 安装：install.packages("dplyr")
+ 加载：library(dplyr)
## 数据类型
+ 基本数据类型：数字、逻辑、文本。
### 向量vector
+ 创建： 
  - a = c(1,2,3,4,5)
  - rep(0,5) //生成5个0
  - seq(1,5,2) //生成1到5，步长为2的向量
  - seq(1,5,length.out=5) //生成1到5，长度为5的向量
  - **NA 和 NUL,NA 表示缺失值，NUL 表示空值**
+ 取值： a[1],a[1:3]//**注意此处非下标，是第N个，从1开始**
+ 数学运算
  - 常量加减 a-1=c(0,1,2,3,4)
  - 求平方 a^2=c(1,4,9,16,25)
  - sqrt、exp
  - sort(a)正排序、rev(a)倒排序、order(a)返回排序后的索引、unique(a)返回唯一值
  - var(a)方差、sd(a)标准差、mean(a)均值、median(a)中位数、range(a)范围、quantile(a,c(0.25,0.75))四分位数、
+ which::返回满足条件的索引:which(a>3)
  eg:从一个线性表中筛选大于等于 60 且小于 70 的数据,print(vector[which(vector >= 60 & vector < 70)])
### 字符串操作
```R
> toupper("Runoob") # 转换为大写
[1] "RUNOOB"
> tolower("Runoob") # 转换为小写
[1] "runoob"
> nchar("中文", type="bytes") # 统计字节长度
[1] 4
> nchar("中文", type="char") # 总计字符数量
[1] 2
> substr("123456789", 1, 5) # 截取字符串，从 1 到 5
[1] "12345"
> substring("1234567890", 5) # 截取字符串，从 5 到结束
[1] "567890"
> as.numeric("12") # 将字符串转换为数字
[1] 12
> as.character(12.34) # 将数字转换为字符串
[1] "12.34"
> strsplit("2019;10;1", ";") # 分隔符拆分字符串
[[1]]
[1] "2019" "10"   "1"
> gsub("/", "-", "2019/10/1") # 替换字符串
[1] "2019-10-1"
```
### 列表list
+ 列表用于保存对象的集合，可以包含不同类型的对象，如数字、字符串、向量、矩阵等。
+ 创建：a = list(1,2,3,"a","b","c")
  - list1 = c(1,2,3)
+ 元素命名：names(list1) = c("a","b","c")
+ 访问
  - list1[1]//访问第一个元素
  - list1$id//访问名为id元素
+ 合并：list2 = c(list1,list2)
+ unlist:将列表转换为向量,便于运算
+ 增删查改
```R
# 列表包含向量、矩阵、列表
list_data <- list(c("Google","Runoob","Taobao"), matrix(c(1,2,3,4,5,6), nrow = 2),
   list("runoob",12.3))

# 给列表元素设置名字
names(list_data) <- c("Sites", "Numbers", "Lists")

# 添加元素
list_data[4] <- "新元素"
print(list_data[4])

# 删除元素
list_data[4] <- NULL

# 删除后输出为 NULL
print(list_data[4])

# 更新元素
list_data[3] <- "我替换来第三个元素"
print(list_data[3])
```
### 矩阵matirx
+ 创建：
  - a = matrix(1:9,nrow=3,ncol=3)//创建3行3列的矩阵，元素从1到9
  - matrix(vector, nrow=2, ncol=3) //指定行数和列数,vector为一个向量
  - matrix(vector, nrow=2, ncol=3, byrow=TRUE) //指定行数和列数,vector为一个向量，byrow=TRUE表示按行填充
  - ，R 中的矩阵的每一个列和每一行都可以设定名称，colnames(m1) = c("x", "y", "z")， rownames(m1) = c("a", "b")
+ 取值：a[1,2]//第1行第2列
+ 运算
  - solve：求逆矩阵
  - t(m)：m的转置
  - apply：对矩阵的行或列进行操作
    - apply(m1, 1, sum) //对m1的每一行求和
### 数组array
+ 创建：array(data, dim = c(3, 3, 3)) //创建一个3x3x3的数组
  - data：数据源
  - dim：指定数组的维度，c(3, 3, 3) 表示 3 行 3 列 3 层
  - dimnames：指定数组的维度名称,可选
+ **特别的R中数据以1为索引启动，无下标**
+ 聚合操作可仅仅针对某个维度进行
```R
# 创建一个3维数组
my_array <- array(1:12, dim = c(2, 3, 2))
# 对第一个和第三个维度同时应用mean函数
result <- apply(my_array, c(1, 3), mean)
print(result)
```
+ apply(X, MARGIN, FUN, ...)
  - X：需要操作的数组
  - MARGIN：指定操作的方向，1 表示行，2 表示列，c(1, 2) 表示行和列
  - FUN：需要应用的函数
  - ...：其他参数
### 字符串string
+ 定义：'' or ""
  - 注意当字符中本含有其中一个，需要用另一个来定义
+ paste(..., sep = " ", collapse = NULL)
  - ...：需要连接的字符串，可以是多个
  - sep：分隔符，默认空格
  - collapse：当有多个字符串时，使用 collapse 将字符串连接起来，通常需要配合sep=""使用
+ format(x, digits, nsmall, scientific, width, justify = c("left", "right", "centre", "none")) 
  - x：需要格式化的数值
  - digits：整数部分保留的位数
  - nsmall：小数部分保留的位数
  - scientific：是否使用科学计数法
  - width：字符串的长度，如果字符串长度小于 width，则会在字符串的两侧填充空格
  - justify：字符串的对齐方式，默认左对齐
    ```R
    # 显示 9 位，最后一位四舍五入
    result <- format(23.123456789, digits = 9)
    print(result)

    # 使用科学计数法显示
    result <- format(c(6, 13.14521), scientific = TRUE)
    print(result)

    # 小数点右边最小显示 5 位，没有的以 0 补充
    result <- format(23.47, nsmall = 5)
    print(result)

    # 将数字转为字符串
    result <- format(6)
    print(result)

    # 宽度为 6 位，不够的在开头添加空格
    result <- format(13.7, width = 6)
    print(result)

    # 左对齐字符串
    result <- format("Runoob", width = 9, justify = "l")
    print(result)

    # 居中显示
    result <- format("Runoob", width = 10, justify = "c")
    print(result)
    ```
+ nchar：统计字符串的长度
+ toupper() & tolower()：大小写转换
+ substr(x, start, stop)：截取字符串
  - x：需要截取的字符串
  - start：截取的起始位置
  - stop：截取的结束位置
+ gsub(pattern, replacement, x)：替换字符串
  - pattern：需要替换的字符串
  - replacement：替换后的字符串
  - x：需要替换的字符串
+ strsplit(x, split)：分割字符串
  - x：需要分割的字符串
  - split：分割符

### 因子factor
+ 因子是一种用于存储分类变量的数据类型，它可以将字符型变量转换为因子，并对其进行排序和编码。
  - 将字符变量转换为类别变量（因子），便于数据分类和统计
  - 因子的核心属性是水平(levels)，即因子的不同类别,对于因子取值、排序可通过参数控制
  - 有序or无序：类别有无高下之分
+ 创建：factor(x = character(), levels, labels = levels,
       exclude = NA, ordered = is.ordered(x), nmax = NA)
  - x：需要转换为因子的字符型向量
  - levels：因子的水平，即分类的类别
  - labels：因子的标签，即分类的名称
  - exclude：需要排除的值
  - ordered：是否有序
  - nmax：因子的最大水平数
  ```R
  # 定义顺序：低 -> 高
  education <- c("高中", "本科", "硕士", "博士")
  education_factor <- factor(education, ordered = TRUE, levels = c("高中", "本科", "硕士", "博士"))
  ```
+ 水平因子生成：gl(n, k, length = n*k, labels = seq_len(n), ordered = FALSE)
  - n：设置levels的数量
- - k：设置每个level的重复次数
  - length：设置因子的总长度，默认为 n*k
  - labels：设置因子的标签
  - ordered：设置因子是否有序，默认为 FALSE
  - **用于审查测试数据集**
### 数据框data.frame
+ 数据框：特殊的二维表，每一列数据类型一致，所有列列名唯一且等长。
+ 创建：data.frame(…, row.names = NULL, check.rows = FALSE,
           check.names = TRUE, fix.empty.names = TRUE,
           stringsAsFactors = default.stringsAsFactors())
  - 列向量，可以是任何类型（字符型、数值型、逻辑型），一般以 tag = value 的形式表示，也可以是 value。
  - row.names: 行名，默认为 NULL，可以设置为单个数字、字符串或字符串和数字的向量。
  - check.rows: 检测行的名称和长度是否一致。
  - check.names: 检测数据框的变量名是否合法。
  - fix.empty.names: 设置未命名的参数是否自动设置名字。
  - stringsAsFactors: 布尔值，字符是否转换为因子，factory-fresh 的默认值是 TRUE，可以通过设置选项（stringsAsFactors=FALSE）来修改。
+ 访问元素
  - df[[1]]: 访问数据框的第一列
  - head(data.frame)：查看数据框的前几行
  - tail(data.frame)：查看数据框的后几行
+ 常用函数
  - **df <- rbind(df, new_row)：将新行添加到数据框中**
  - str(data.frame)：查看数据框的结构
  - summry(data.frame)：查看数据框的摘要信息
  - data.frame(table\$name, table\$age)：提取数据框中某一列
  - table[1:2, ]：提取数据框中前两行
  - table$部门 <- c("运营","技术","编辑"):添加一列
  - cbind_rows(c1,c2,c3)：多个向量合并为数据框
#### R数据重塑
##### 数据框连接（类似表连接）
+ merge(x, y, by = intersect(names(x), names(y)),
      by.x = by, by.y = by, all = FALSE, all.x = all, all.y = all,
      sort = TRUE, suffixes = c(".x",".y"), no.dups = TRUE,
      incomparables = NULL, …)
  - x, y： 数据框
  - by, by.x, by.y：指定两个数据框中匹配列名称，默认情况下使用两个数据框中相同列名称。
  - all：逻辑值; all = L 是 all.x = L 和 all.y = L 的简写，L 可以是 TRUE 或 FALSE。
  - all.x：逻辑值，默认为 FALSE。如果为 TRUE, 显示 x 中匹配的行，即便 y 中没有对应匹配的行，y 中没有匹配的行用 NA 来表示。
  - all.y：逻辑值，默认为 FALSE。如果为 TRUE, 显示 y 中匹配的行，即便 x 中没有对应匹配的行，x 中没有匹配的行用 NA 来表示。
  - sort：逻辑值，是否对列进行排序。 
  - Natural join 或 INNER JOIN：如果表中有至少一个匹配，则返回行
  - Left outer join 或 LEFT JOIN：即使右表中没有匹配，也从左表返回所有的行
  - Right outer join 或 RIGHT JOIN：即使左表中没有匹配，也从右表返回所有的行
  - Full outer join 或 FULL JOIN：只要其中一个表中存在匹配，则返回行
##### melt() ：宽格式数据转化成长格式
+ **宽数据格式：每一列是一个变量，每一行是一条记录，长数据格式则相反**
+ 依赖
  ```R
  # 安装库，MASS 包含很多统计相关的函数，工具和数据集
  install.packages("MASS", repos = "https://mirrors.ustc.edu.cn/CRAN/") 
    
  #  melt() 和 cast() 函数需要对库 
  install.packages("reshape2", repos = "https://mirrors.ustc.edu.cn/CRAN/") 
  install.packages("reshape", repos = "https://mirrors.ustc.edu.cn/CRAN/") 
  ```
+ melt(data, ..., na.rm = FALSE, value.name = "value")
  - data：需要转换的数据框
  - ...,传递给其他函数的参数或来自于其他函数的参数
  - na.rm：是否删除缺失值
  - value.name：转换后数据框中值的列名
##### cast()：长格式数据转化成宽格式
+ dcast/acast(
  data,
  formula,
  fun.aggregate = NULL,
  ...,
  margins = NULL,
  subset = NULL,
  fill = NULL,
  drop = TRUE,
  value.var = guess_value(data)
)
  - dcast:返回数据框，acast:返回矩阵
  - data：需要转换的数据框
  - formula：重塑的数据的格式，类似 x ~ y 格式，x 为行标签，y 为列标签 。
  - fun.aggregate：聚合函数，用于对 value 值进行处理。
  - margins：变量名称的向量（可以包含"grand\_col" 和 "grand\_row"），用于计算边距，设置 TURE 计算所有边距。
  - subset：对结果进行条件筛选，格式类似 subset = .(variable=="length")。
  - drop：是否保留默认值。
  - value.var：后面跟要处理的字段。
## 数据结构
### if
```R
x <- c("google","runoob","taobao")

if("runoob" %in% x) {
   print("包含 runoob")
} else {
   print("不包含 runoob")
}
```
### switch
+ switch(expression, case1, case2, case3....)
  - switch 语句中的 expression 是一个常量表达式，可以是整数或字符串，如果是整数则返回对应的 case 位置值，如果整数不在位置的范围内则返回 NULL。
  - 如果匹配到多个值则返回第一个。
  - expression如果是字符串，则对应的是 case 中的变量名对应的值，没有匹配则没有返回值。
  - switch 没有默认参数可用
```R
you.like<-"runoob"
switch(you.like, google="www.google.com", runoob = "www.runoob.com", taobao = "www.taobao.com")

output:"www.runoob.com"
```
### for
+ break//跳出循环
+ **next//跳过本次循环**
+ repeat//循环直到条件不满足
```R
v <- c("Google","Runoob")
cnt <- 2

repeat {
   print(v)
   cnt <- cnt+1
   
   if(cnt > 5) {
      break
   }
}
```
+ while
+ for 
```R
for (i in 1:5) {
   print(i) 
}
```
## 函数
+ 定义
```R
function_name <- function(arg_1, arg_2, ...) {
    # 函数体
    # 执行的代码块
    return(output)
}
```
+ 调用:sum1 <- mysum(a,b)
  - 非顺序参数需要通过名称来传递
### 内置函数
+ str：查看数据结构
## R-TXT
+ read.table(file, header = FALSE, sep = "\t", quote = "\"", dec = ".", fill = TRUE, comment.char = "", ...)
  - file：文件路径
  - header：是否将第一行作为列名，默认为 FALSE
  - sep：分隔符，默认为 "\t"
  - quote：引用符，默认为 "\""
  - dec：小数点，默认为 "."
  - fill：如果为 TRUE，则行中缺失的值将被填充为 NA，默认为 TRUE
  - comment.char：注释字符，默认为 ""
  - 返回是数据框，可用ncol、nrow查看行列数
+ readLines(file, n = -1, warn = TRUE, skip = 0, sep = "\n", ok = TRUE, skipNul = FALSE)
  - file：文件路径
  - n：读取的行数，默认为 -1，表示读取所有行
  - warn：是否显示警告信息，默认为 TRUE
  - skip：跳过的行数，默认为 0
  - sep：行分隔符，默认为 "\n"
  - ok：是否读取成功，默认为 TRUE
  - skipNul：是否跳过空行，默认为 FALSE
  - 返回是字符向量，可用length查看行数
+ write.table(x, file, append = FALSE, quote = TRUE, sep = " ", eol = "\n", na = "NA", dec = ".", row.names = TRUE, col.names = TRUE, qmethod = c("escape", "double"), fileEncoding = "")
  - x：数据框
  - file：文件路径
  - append：是否追加到文件，默认为 FALSE
  - quote：是否引用，默认为 TRUE
  - sep：分隔符，默认为 " "
  - eol：行结束符，默认为 "\n"
  - na：缺失值，默认为 "NA"
  - dec：小数点，默认为 "."
  - row.names：是否写入行名，默认为 TRUE
  - col.names：是否写入列名，默认为 TRUE
  - qmethod：引用方法，默认为 "escape"
  - fileEncoding：文件编码，默认为 ""
+ writeLines(text, con = stdout(), sep = "\n", useBytes = FALSE)
  - text：字符向量
  - con：输出文件路径，默认为 stdout()
  - sep：行分隔符，默认为 "\n"
  - useBytes：是否使用字节，默认为 FALSE
  
## R-CSV
+ **CSV 文件最后一行需要保留一个空行，不然执行程序会有警告信息。**
+ read.csv(file, header = TRUE, sep = ",", quote = "\"", dec = ".", fill = TRUE, comment.char = "", ...)
  - file：文件路径
  - header：是否将第一行作为列名，默认为 TRUE
  - sep：分隔符，默认为 ","
  - quote：引用符，默认为 "\""
  - dec：小数点，默认为 "."
  - fill：如果为 TRUE，则行中缺失的值将被填充为 NA，默认为 TRUE
  - comment.char：注释字符，默认为 ""
  - 返回是数据框，可用ncol、nrow查看行列数
+ **subset(x,subset,select)**
  - x：数据框
  - subset：行过滤，eg：id > 2 && id < 5
  - select：列过滤，eg：c("id","name")
- write.csv(x, file, row.names = TRUE, col.names = TRUE, sep = ",", quote = TRUE, eol = "\n", na = "NA", dec = ".", ...)
  - x：数据框
  - file：文件路径
  - row.names：是否写入行名，默认为 TRUE
  - col.names：是否写入列名，默认为 TRUE
  - sep：分隔符，默认为 ","
  - quote：是否引用，默认为 TRUE
  - eol：行结束符，默认为 "\n"
  - **na：缺失值，默认为 "NA"**
  - dec：小数点，默认为 "."
## R-Excel
+ 配置
  ```R
  library(xlsx)
  ```
+ read.xlsx(filename,sheetIndex=1,startRow=1,startCol=1,rowNames=FALSE)
  - filename：文件路径
  - sheetIndex：读取的 sheet 页，默认为 1
  - startRow：开始行，默认为 1
  - startCol：开始列，默认为 1
  - rowNames：是否将第一列作为行名，默认为 FALSE
+ write.xlsx(x, file, sheetName = "Sheet1", startRow = 1, startCol = 1, row.names = FALSE, col.names = TRUE, append = FALSE, sheetRef = NULL)
  - x：数据框
  - file：文件路径
  - sheetName：sheet 页名，默认为 "Sheet1"
  - startRow：开始行，默认为 1
  - startCol：开始列，默认为 1
  - row.names：是否写入行名，默认为 FALSE
  - col.names：是否写入列名，默认为 TRUE
  - append：是否追加，默认为 FALSE
  - sheetRef：sheet 引用，默认为 NULL
## R-xml
+ 配置
  ```R
  library(XML)
  ```
+ 数据提取
  - xmlParse()：解析 XML 文件，可通过file = "file.xml"参数指定文件路径
  - xmlRoot()：获取 XML 文件的根节点
  - xmlSize()：获取 XML 文件的节点数
  - rootnode[[1] [2]]:获取根节点的第一个子节点和第二个子节点
  - xmlToList()：将 XML 文件转换为列表,ToDataFrame()：将列表转换为数据框
## R-JSON
+ 配置
  ```R
  library(rjson)
  ```
+ 数据提取
  - fromJSON()：将 JSON 字符串转换为 R 对象
  - JSON1[[1]]：获取 JSON 对象的第一个元素
  - JSON1[[2][[2]]]：获取 JSON 对象的第二个元素的第二个元素,[行标[列标]]
  - as.data.frame()：将 JSON 对象转换为数据框
## R-mysql
+ 配置
  ```R
  library(RMySQL)
  ```
  - 连接配置：mysqlconnection = dbConnect(MySQL(), user = 'root', password = '', dbname = 'test',host = 'localhost')

### 查看数据
+ dbListTables(mysqlconnection)
+ 数据提取
  - dbDriver()：创建数据库驱动
  - dbConnect()：连接数据库
  - dbListTables()：获取数据库中的表
  - dbReadTable()：读取表数据
  - dbWriteTable()：写入表数据
  - dbDisconnect()：断开数据库连接
  - dbClearResult()：清除结果集
  - dbRemoveTable()：删除表
  - dbGetQuery(mysqlconnection, "SELECT * FROM table_name")：执行 SQL 查询
    - 可选参数：StringsAsFactors：是否将字符串转换为因子，field.types：字段类型，encoding：编码格式，verbose：是否打印详细信息
  - dbSendQuery(mysqlconnection, "SELECT * FROM table_name")：发送 SQL 查询
    - 可选参数：batchSize：每次提取行数，maxRows：最大提取行数，encoding：编码格式，stringsAsFactors：是否将字符串转换为因子，verbose：是否打印详细信息
    - fetch()：获取查询结果，SendQuery()返回一个查询结果对象，fetch()从该对象中获取查询结果，而GetQuery()直接返回查询结果
    - sendQuery将查询发送到服务器执行，适合大数据处理，可分批提取查询结果


## R-绘图
+ 中文字体：
```R
# 载入 showtext
library(showtext);
# 第一个参数设置字体名称，第二个参数为字体库路径，同目录下，我们写字体库名就可以了
font_add("SyHei", "SourceHanSansSC-Bold.otf"); 


#加载字体
showtext_begin();
 
绘图code

# 去掉字体
showtext_end();
```
### 饼图绘制
#### 2D饼图
+ piepercent = paste(round(100*info/sum(info)), "%")：将info中的数值转换为百分比
+ pie(x, labels = names(x), edges = 200, radius = 0.8,
    clockwise = FALSE, init.angle = if(clockwise) 90 else 0,
    density = NULL, angle = 45, col = NULL, border = NULL,
    lty = NULL, main = NULL, …)
  - x：数值向量，表示每个扇形的比例
  - labels：字符向量，表示每个扇形的标签
  - edges：扇形的边数，默认为 200
  - radius：扇形的半径，默认为 0.8
  - clockwise：扇形是否按顺时针方向绘制，默认为 FALSE
  - init.angle：扇形的起始角度，默认为 0
  - density：扇形的密度，默认为 NULL
  - angle：扇形的旋转角度，默认为 45
  - col：扇形的颜色，默认为 NULL，"#ED1C24":红色，"#FF7F27":橙色，"#FFD302":黄色，"#009245":绿色，"#005984":蓝色，"#7E008E":紫色
  - border：扇形的边框颜色，默认为 NULL
  - lty：扇形的边框线型，默认为 NULL
  - main：图表的标题，默认为 NULL
  
+ 图片保存
  - png(file = "pie.png", width = 800, height = 600)以png保存图片
  - jpeg(file = "pie.jpg", width = 800, height = 600)以jpg保存图片
  - bmp(file = "pie.bmp", width = 800, height = 600)以bmp保存图片

#### 3D饼图
+ library(plotrix)
+ pie3D(x, labels = NULL, explode = NULL, group = 1,
    col = NULL, main = NULL, explode.labels = FALSE,
    label.pos = 0, label.font = 1, label.cex = 1,
    label.col = "black", label.bcol = "black", …)
  - x：数值向量，表示每个扇形的比例
  - labels：字符向量，表示每个扇形的标签
  - explode：扇形的爆炸距离，默认为 NULL
  - group：扇形的分组，默认为 1
  - col：扇形的颜色，默认为 NULL
  - main：图表的标题，默认为 NULL
  - explode.labels：是否爆炸扇形的标签，默认为 FALSE
  - label.pos：扇形标签的位置，默认为 0
  - label.font：扇形标签的字体，默认为 1
  - label.cex：扇形标签的字体大小，默认为 1
  - label.col：扇形标签的字体颜色，默认为 "black"
  - label.bcol：扇形标签的边框颜色，默认为 "black"


### 条形图绘制
+ barplot(H,xlab,ylab,main, names.arg,col=c("",""),beside,family='SimHei')
  - H：数值向量，表示每个条形的数值
  - xlab：x轴标签
  - ylab：y轴标签
  - main：图表标题
  - names.arg：条形标签
  - col：条形颜色
  - beside：是否将条形堆叠显示，默认为 FALSE
  - family：字体



### 折线图绘制
+ S4 函数的方法：curve(expr, from = NULL, to = NULL, n = 101, add = FALSE,
      type = "l", xname = "x", xlab = xname, ylab = NULL,
      log = NULL, xlim = NULL, …)
  - expr：要绘制的函数表达式
  - from：x轴的起始值，默认为 NULL
  - to：x轴的结束值，默认为 NULL
  - n：绘制的点的数量，默认为 101
  - add：是否将曲线添加到现有的图形中，默认为 FALSE
  - type：曲线的类型，默认为 "l"，即直线
  - xname：x轴的标签，默认为 "x"
  - xlab：x轴的标签，默认为 xname
  - ylab：y轴的标签，默认为 NULL
  - log：是否对 x 或 y 轴进行对数变换，默认为 NULL
  - xlim：x轴的范围，默认为 NULL
  - …：其他参数，如颜色、线型等
+ S3 函数的方法：plot(x, y = 0, to = 1, from = y, xlim = NULL, ylab = NULL, main = NULL,…)
  - x：x轴的值
  - y：y轴的值，默认为 0
  - to：y轴的结束值，默认为 1
  - from：y轴的起始值，默认为 y
  - xlim：x轴的范围，默认为 NULL
  - ylab：y轴的标签，默认为 NULL
  - main：图表的标题，默认为 NULL
  - …：其他参数，如颜色、线型等

#### 散点图绘制
+ plot(x, y, type="p", main, xlab, ylab, xlim, ylim, axes)
  - x：x轴的值
  - y：y轴的值
  - type：图形的类型，默认为 "p"，即散点图
    - p：点图 l：线图 b：同时绘制点和线 c：仅绘制参数 b 所示的线 o：同时绘制点和线，且线穿过点 h：绘制出点到横坐标轴的垂直线 s：阶梯图，先横后纵 S：阶梯图，先纵后竖 n： 空图
  - main：图表的标题，默认为 NULL
  - xlab：x轴的标签，默认为 NULL
  - ylab：y轴的标签，默认为 NULL
  - xlim：x轴的范围，默认为 NULL
  - ylim：y轴的范围，默认为 NULL
  - axes：是否显示坐标轴，默认为 TRUE
#### 散点图矩阵
+ 是一个大的图形方阵，研究多个变量两两之间的相关关系。
+ pairs(formula, data，main)
  - formula：公式，指定变量之间的关系
  - data：数据框，包含变量数据
  - main：图表的标题，默认为 NULL



