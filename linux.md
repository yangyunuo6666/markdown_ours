[toc]
***

# 操作系统及技巧
1.	操作系统是软件用来帮助用户调度硬件工作。
2. shell（外壳）：保护内核，充当用户与内核沟通的角色。
3. shell远程连接时ping不通Linux，用ccleaner清理注册表即可。
3. 出现虚拟机CPU被禁用，可能是iOS文件损坏，重下即可。
4. 技巧：
   + 虚拟机快照：保存虚拟机当前状态，可还原的保存的状态。
    * 还原：快照管理器->选择快照->转到。
   + 系统更新：yum update 
5. 常用命令
   + clear：清屏
   + ALT+Ctrl+T：打开Ubuntu终端
   + tail -n 500 hive.log//查看日志最后500行
   + tail -n 500 | grep "ERROR" hive.log//查看日志最后500行中包含ERROR的行
6. /dev/null：是Linux文件系统中的一个文件，被称为黑洞，所有写入该文件的内容都会被自动丢弃
## Windows与Linux的文件互传
+ 前提Linux已经安装shell服务（openssh-server）。**当root用户无法连接时建议连接登录使用的用户或其他用户**
+ 使用前提是在连接linux的远程工具上使用（建议使用Xshell），需要下载lrzsz（yum install -y lrzsz）
+ 使用rz命令：回车后直接选择对应文件即可。
+ 使用sz命令：从linux上传输文件到windows上，sz传输时需要指定目录内传输的文件名，弹出页面后选择存放路径即可 

***
# vi/vim编辑器,文本处理
+ vim是vi的高级模式，**vim +10 1.txt跳转到文件开头后的第10行**。
+ 滚屏命令：Ctrl+U/L（前滚后滚半屏）
+ 翻页命令：Ctrl+F/B（前翻后翻）
+ **复制粘贴**，进入插入模式后再进行粘贴，否则会遇到第一i才开始粘贴的情况，导致粘贴内容不完整。
## vi的配置文件
+ vi ~/.vimrc
+ syn on #代码高亮
+ set nu #显示行号
+ set autoindent #自动缩进
+ set smartindent #智能缩进，更据代码语法较为推荐。
+ set ruler #显示光标
+ set undolevels=200 #undo的最大次数
+ set incsearch #快速查找单词
+ set ignorecase #忽略大小写
+ set hlsearch #高亮搜索结果
+ set background=bark #设置背景为bark
+ set  noerrorbells #出错不发警报
+ set tabstop=4 #设置宽度
+ set backup #设置自动备份(nobackup不启用)
+ set backupext = .bak #设置备份文件后缀
+ set backupdir = ./ #设置备份路径
## 文本处理工具
+ cut [opt] filename//文本切割
  - -f n:指定切割后提取第N列(分割后会形成多列)
  - //cut -d " " -f 3-:以空格为分隔符，取第三列到最后一列
  - -d 指定切割分隔符
  - //cut -d " " -f 1:以空格为分隔符，取第一列
  - -c n:指定切割后取第N列
+ awk [opt] '/pattern/{action}' filename//文件逐行读入处理
  + //默认以空格为分隔符，分割文件pattern:匹配模式，action:处理命令
  -  eg:awk -F : '/^root/{print $7}' /etc/passwd//匹配以root开头的行打印第7列
  - -F: 指定分隔符
  - -v : 赋值一个用户变量
  + awk 内置变量
    - NF:切割后的列数
    - NR:已读总行号
    - FILENAME:当前文件名

## 三种模式的使用
|序号|	vi编辑器的应用|	
|:--|:--|
|Esc|命令模式|
|u|撤销操作|
|G|调到最后一行|
|yy|复制光标所在行|
|nyy|复制n行|
|p|粘贴|
|hkjk|方向键|
|L|移到行首|
|$|移到行尾|
|A|行尾追加|
|dd|删除一行|
|ndd|删除N行|
|np|撤销上次的dd命令，最多9次|
|ndd|从光标所在位置删除n行|
|.|重复操作|
|编辑模式|	a/i|
|末线模式	|在命令模式下打一个:|
|	:wq |保存退出|
|	:q! |强制退出|

1. 在 vim 中
**: 执行vim本身的命令
:! 执行外部 命令**
外部 指的是 vim应用外面
也就是 shell环境中的命令
***


 
# 基础知识
## 软件包管理
### 内网安装时依赖包来源
+ 网站：Packages For Linux and Unix
  - 通过search：筛选可用依赖
### rpm命令(centerOS)
+ rpm -q  //查询安装信息
+ -a：查询所有已安装的软件包
  - rpm -qa | grep "mysql" //查询mysql相关的软件包
+ rpm -i //安装
  - 安装可能的问题：重复安装、文件冲突（部分已安装）、依赖关未解决。
  - -v：显示详细信息
  - -h：以#显示进度
  - sudo rpm -ivh mysql-community-server-5.7.28-1.el7.x86_64.rpm
+ rpm -e //卸载文件
  - --nodeps //强制卸载eg:sudo rpm -e --nodeps mysql
  
### yum命令（centerOS）
+  yum install //安装文件
+  yum remove //卸载文件
+  yum list install //列出已安装的文件
+  yum search software //查找软件
+ 永久更换镜像源：
  - 备份:sudo cp -r /etc/yum.repos.d /etc/yum.repos.d.backup
  - 清除配置:sudo rm -f /etc/yum.repos.d/*.repo
  - 下载配置:sudo curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
  - 刷新:sudo yum clean all sudo yum makecache

## apt-get命令（Ubuntu）
+  apt-get install //安装文件
+  apt-get remove //卸载文件
+  apt-get list install //列出已安装的文件
+  apt-get search software //查找软件
+  -y //安装时自动确认
+  -f //修复依赖关系安装
+  -v //显示详细信息
+  -q //安静模式
+ **更换镜像**
  - 修改/etc/apt/sources.list文件，提前备份/etc/apt/sources.list文件
  - 修改为：
    ```
    deb http://mirrors.aliyun.com/ubuntu/ focal main restricted
    deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted
    deb http://mirrors.aliyun.com/ubuntu/ focal universe
    deb http://mirrors.aliyun.com/ubuntu/ focal-updates universe
    ```
  - 更新：sudo apt-get update
## **Linux快捷键**
+ Ctrl+C:终止当前进程
+ Ctrl+q:退出
+ Ctrl+L:清屏
+ cd - :返回上一次所在的目录

## **时间戳**
+ 时间戳：1970年1月1日0时0分0秒**0时区时间（UTC时间）**到现在的秒数，**注意需考虑时区**。
+ 截止现在：10位时间戳为秒，13位时间戳为毫秒。

## **多参数命令连用xargs命令,和管道命令** 
+ -n	指定每行最大的参数数量
+ -d	指定分隔符
+ 示例（删除所有以log结尾的文件）： find . -name "*.log" | xargs rm -f
+ 管道命令：将前一个命令的输出作为后一个命令的输入,eg:ls -l | grep "log"
## **输出命令echo与重定向**
+ 输出命令:echo "XXX",-e:识别转义字符
+ 重定向：>覆盖,>>追加,1.txt > 2.txt:用1的内容覆盖2的内容
##	**通配符（用于匹配信息的符号）**
+ *匹配0~n个字符 
+ ？任意个单个字符 
+ [0~9]匹配数字范围
+ [a~z]匹配字母范围[A~Z]匹配大写字母范围 
+ [a,b,c]或[abc]匹配abc任意一个 {abc}匹配abc中一个匹配不到报错 
+ [^abc]匹配除abc外任意一个
+ [a~z]*匹配任意个字母
## **正则表达式**
+ **通过regexp re使用，若正则表达式错误优先考虑是否有特殊字符需转义和运行环境对其影响**
+ .:匹配任意一个字符
+ ^:匹配字符串的开头
+ $:匹配字符串的结尾
+ *:匹配前一个字符0~n次
+ ?:匹配0~1个字符
+ \\:转义字符,匹配特殊字符
## **转义字符**：
+ \使反斜杠后一个变量变为字符串 
+ ‘’使单引号中都变为字符串 
+ “”保留变量属性不转义 
+ ``反引号执行其中命令返回结果（反引号在英文状态下按~）
##	**命令重命名与历史命令查看**：
+ history 查看历史命令
+ alias 查看当前已有的重命名命令。
+ alias 别名 = ‘原命令’（重命名命令）
+ unalias 别名（取消别名）
+ type md（查看md命令是否被使用）
+ 命令只是当时有用，将别名写入配置文件~/bashrc中后执行source/etc/bashrc命令使配置生效。
## **定时任务cronlab**
+ crontab -e 编辑定时任务,-l 查看, -r 删除N行
+ 定时任务文件：/etc/crontab
+ 定时任务日志：/var/log/cron
+ 任务：\*/1**** ls -l /home > /tmp/test.txt
  - 五个*号分别代表一个时间域：分钟 小时 日期 月份 星期几
  - 时间域内：不连续时间用逗号隔开，连续时间用-表示，不指定用*
  - */n:表示该时间域执行N次
+ 定时执行脚本：*/1**** /home/test.sh(需要提前chomd +x test.sh)
##  **\$**
   \$str表示变量可做赋值等，\$0表示脚本本身名字 \$1脚本第一个参数 \$n第n个参数 \$\$脚本运行的当前ID号 \$？最后命令运行的退出状态。
## 	**用户环境变量配置**
+(以加入自己的MySQL命令为例):在Linux中变量名一般大写，环境变量保存系统运行环境的变量。
+	Export 变量（改变环境变量，设置的是临时变量）、
+	修改配置文件/ect/profile
  编辑配置文件/ect/profile，在配置文件中加入配置语句：
  export PATH=$PATH:/usr/local/mysql/bin,在修改完文件后
  使用source /etc/profile命令,可以在不用重启系统的情况下使修改的内容you效
+ 修改其他配置文件
  - cd /etc/porfile.d//进入自定义配置文件目录，
   //当Linux启动时会遍历执行一个脚本profile，
   //该脚本会遍历执行/etc/profile.d/目录下的所有以sh结尾的脚本
  - vim my_env.sh,export PATH=$PATH:newpath
    //my_env.sh用于自定义环境变量，export设为全局
    //$PATH:newpath将字符串拼接到环境变量上
  - source /etc/profile
  - eg:
    #JAVA_HOME
    export JAVA_HOME=/opt/module/jdk1.8.0_212
    export PATH=$PATH:$JAVA_HOME/bin

## **中文输入法安装**
+ sudo apt-get install fcitx fcitx-bin fcitx-table-wubi fcitx-table-wbpy
+ im-config//开始配置，需要重启生效
+ fcitx//终端启动输入法

## 创建新用户
+ sudo useradd 用户名
+ sudo passwd 用户名，设置密码
+ sudo mkdir /home/用户名，设置用户主目录
+ usermod -g ceshizu uesr1 将用户user1的私有组设置为ceshizu
+ usermod -G ceshizu uesr1 将用户user1添加进组群ceshizu，并将改组设置为它的扩展组

## 三种办法禁用和恢复用户账户user1
+ root 用户输入下面两条命令即可禁用和恢复用户账户user1
   passwd  -l  user1
   passwd  -u  user1
+ root 用户输入下面两条命令即可禁用和恢复用户账户user1
   usermod  -L  user1
   usermod  -U  user1
+ root 用户去修改只读文件/etc/shadow,关于user1账户的passwd域的第一个字符前面加上一个“！”，达到禁用账户的目的，在需要恢复的时候只要删除字符“！”即可。

##	**Linux命令基础**
+	基础格式： 命令 [选项] [参数]
 *	选项：即命令选项，选项可组合短命令用- 长命令用- - 引导开始，ls命令可无选项（仅列出文件名），没有选项只执行基本功能。（-h查看帮助）
 *	参数：即命令处理对象，一般有默认参数。
+	命令输入：用tab键补全文件名，输入前几个后按tab无重复直接补全，有重复再按tab会列出重复的。   使用上下键查看最近输入命令，修改后可直接输入。
+	命令执行与中断
 *	Ctrl+C终断程序执行 ctrl+Z中断任务，将任务挂起 ctrl+D表示EOF(-1)用于输入参数之后表示结束
+ **命令参数传递**：命令1 | xargs 命令2：将命令1的输出作为命令2的参数
## 日期命令
+ date : 显示当前时间
  - %Y : 年,%m : 月, %d : 日, %H : 时, %M : 分, %S : 秒, 
  - -d "num days ago" : 显示num天前的日期
  - -s "YYYY-MM-DD HH:MM:SS" : 设置日期
  - %s : 时间戳
## **Linux的文件知识**
### 特点：
   + 文件名支持265个字符，大小写敏感。
   + 任何软件和I/O设备都被视为文件
   + 没有盘符，不同硬件分块挂载在目录下。 
   +  Linu无拓展符，机器不识别但可给用户提示文件类型
### 类型：
   + 普通文件(-)：红黑(rar) 绿色(exe)
   + 目录文件(D/d)：存放文件名及其信息。
   + 链接文件(l)：指向真实文件的链接。
   + 设备文件(B/C)：位于/dev目录下。
   + 管道文件(P)：用于进程信息传递。
### 权限
#### 字母法
+ r w x s(执行文件的用户暂时拥有文件所有权)
#### 数字法
+ 以八进制数表示，0(无权限) 1(x) 2(w) 4(r)，权限相加后得一个数子，三个数字为一组依次表示文件属主u、同组用户(g)、其他用户(o)的权限。


+ drwxr-xr-x(其中的为文件类型，rwx为文件所有者权限，r-x为所以组权限，r-x为其他用户权限)x(eXecute，执行)
+ 1.**简介普通文件的rwx权限**
r(Read，读取)：对文件而言，具有读取文件内容的权限；
w(Write,写入)：对文件而言，具有新增、修改文件内容的权限；
x(eXecute，执行)：对文件而言，具有执行文件的权限。

+ **简介目录的rwx权限**
r(Read，读取)：拥有此权限表示可以读取目录结构列表，也就是说可以查看目录下的文件名和子目录名。
w(Write,写入)：拥有此权限表示具有更改该目录结构列表的权限。
x(eXecute，执行)：拥有目录的x权限表示用户可以进入该目录成为工作目录。

+ **简介目录w权限**
w(Write,写入)：拥有此权限表示具有更改该目录结构列表的权限。
1.在该目录下新建新的文件或子目录。
2.删除该目录下已经存在的文件或子目录。
3.将该目录下已经存在的文件或子目录进行重命名。
4.转移该目录内的文件或子目录的位置。
### /etc/passwd文件。
+ 该文件保存用户帐户信息。
+ 该文件的每一行保存一个用户的数据。
+ 用户数据按域以冒号分割。
+ 每一行的格式如下：
username：password:uid:gid:userinfo:home:shell
### /etc/group文件。
+ 该文件保存组账户的信息。
+ 该文件的每一行保存一个组群的数据。
+ 组群数据按域以冒号分割。
+ 每一行的格式如下：
group_name:group_password:group_id:group_members

# 文件目录和软件管理命令
## chmod命令，更改权限
+ 
  - chmod命令用于改变文件/目录的访问权限；
  - chmod命令有两种用法，一种是包含字母和操作符表达式的文字设定法；另一种是包含数字的数字设定法。
+ chomd [who] [+|-|=] [mode] + filename
  - [who]: u:文件属主 g:同组用户  a:所有用户  o:其他用户
  - [mode]: r w x(执行) s(执行文件者有文件拥有者的权限)
  - 操作符：+添加权限、-减少、=重新赋给权限

## umask命令，更改默认权限
+ umask： 显示文件或目录的默认权限，
+ umask 数字：设置默认权限，数字为补码，以888-X后可得实际权限，文件创建时不可有可执行权限故最高为6，路径最高为7


## chown命令，更改属主
+ chown [option] [user/group] filename //
  - option：-R递归更改  -v显示过程
  - user/group：更改到的属主，**也可一起修改newgroup:newuser**
  - filename：支持通配符

## **cd命令：更换当前路径**
 + cd 路径(进入该目录)
 + linux的：
    * linux的文件结构为树形结构，所有的目录挂在根目录上。
    * 打开终端后自动进入用户目录(/home/用户名)
 + 特殊的目录
   -   ~家目录 
   -  	.当前目录
   -   ..上一级目录
   -   **cd - :返回上一次进入的目录**
   -   cd ../..返回上上级目录
   -   cd -P:进入连接文件的源文件路径
   -   ${sys:username}：获取用户名,root/${sys:username}用户目录
## **dirname命令**，获取文件路径
+ dirname /etc/sysconfig/network-scripts/ifcfg-ens33
  - 输出：/etc/sysconfig/network-scripts
## **basename命令**，获取文件名
+ basename /etc/sysconfig/network-scripts/ifcfg-ens33
  - 输出：ifcfg-ens33

## gzip/bzip/zip命令，文件压缩

### gzip
+ gzip 压缩
+ gunzip 解压缩 ，删除原文件
+ zcat 解压缩并输出到stdout，不删除原文件
+ 选项：
  - -r:递归压缩
  - -level:设置压缩率
  - -f:强制压缩
  - -c：将压缩和解压缩的结果输出到stdout
  - -n：保留原文件名和时间戳
  - -N：不保留原文件名和时间戳
  - -t：测试压缩文件是否损坏
  - -v：显示执行过程
  - -V：显示版本信息
  - -q：不显示警告信息
  - -a：使用ASCLL编码
  - -S：更改压缩后文件后缀

### bzip
+ bzip2 压缩
+ bunzip2 解压缩 ，删除原文件
+ bzcat 解压缩并输出到stdin，不删除原文件
+ bz2recover 修复并解压缩
+ 选项：
  - -d：解压缩
  - -level:设置压缩率
  - -z/f:强制压缩
  - -c：将压缩和解压缩的结果输出到stdout
  - -k：保留原始文件
  - -t：测试压缩文件是否损坏
  - -L：显示版本和授权信息
  - -V：显示版本信息
  - -s：减少内存的使用

### zip命令
+ zip:压缩
+ unzip:解压缩
## **tar命令，文件打包**
+ 选项
  - cvf:创建新备份、显示执行过程、指定需要的原文件
  - z:压缩算法选择gzip
  - j:压缩算法选择bzip
  - C：指定压缩后保存的位置
  - x:解压缩
  - t:列出文件内容。
  - f:指定压缩文件名，必须放在最后。
+ 其他：
  - tar -tf etc.tar | more //查看压缩包的内容


 
## 其他
+ tar -xzvf  压缩包的路径  -C 目标路径
+ Linux中的补全建： Tab
+ **tree**列出一个文件夹下的所有子文件夹和文件（以树形结构来进行列出）
+  输入su然后输入root密码可切换到root用户。
+ 关机命令：
  - 重启命令：reboot, init 6, systemctl reboot
  - 关机命令：poweroff, init 6, systemctl poweroff
+ 注销用户命令：logout，退出控制台命令：exit
+ Showdown命令：（-t在改变runlevel之前告诉init多久后关机 -r重启 -k发送警告给登录者 -h关机后关电 -f重启时忽略fsck -F重启时强迫fsck -time设定关机前的时间）showdown -h 20:54
+ Haltreboot命令（就是调用showdown -h）：
-n防止sync系统的调用 -w写wtmp记录 -d不写wtmp记录 -f不调用showdown而关机 -I关机前断网 -p默认选项
+ init命令
  七个级别，init 0关机 init 6 重启

##  ls命令（查看当前目录下的文件）
+ -a:查看所有文件
+ -h:(通常与L连用),将文件大小通过我们容易观察的单位显示
+ -l :以列表形式展示文件
+ -R:递归显示所有文件
##  **显示文件内容(cat，more，less，tail)：**
+ cat：显示文件，也可用来合并文件cat 1.txt 2.txt >12.txt。
+ more：按enter或space进入下一行，P&C清屏，**S可压缩多行空白行为一行**，f显示文件名和行数。q:退出
+ less(**部分加载适合大文件的查看**):Page Up 上翻页 Page Down下翻页,q:退出
+ head：显示文件头（前）10行，head -n 5 filename显示前5行
+ tail:显示文件尾（后）10行，tail -n 5 filename显示后5行
## 文件内容查询grep "str"  filename
+ i(比较时不区分大小写) c(只显示匹配行数) v(反向匹配) x(完全匹配) n(输出前加上行号)
## **文件查询(find、whereis、locate)**
### find [option] path:
   - -a(and),-o(or)
   - -user (查找属主为user的文件,find /home/ -user root)
   - -name(支持通配符,find /home/ -name *.txt) 
   - -Inname(匹配字符串的链接文件可用通配符) 
   - -type	查找某一类型的文件。
   - -print	find 命令将匹配的文件输出到标准输出
   - -exec	find 命令对匹配的文件执行该参数所给出的 shell 命令
### whereis 文件名：只能搜索二进制文件（-b），man 帮助文件（-m）和源代码文件（-s）
+ which：，我们**通常使用 which 来确定是否安装了某个指定的程序**，因为它只从 PATH 环境变量指定的路径中去搜索命令并且返回第一个搜索到的结果
### locate filename(db 快速查询):
   - 使用 locate 命令查找文件会通过查询 /var/lib/mlocate/mlocate.db 
      数据库来检索信息。 数据库也不是实时更新的，
      updatedb 命令来更新数据库。 刚添加的文件，
      可能会找不到，需要手动执行一次 updatedb 命令 ,
      注意这个命令也不是内置的命令。
      在部分环境中需要手动安装，然后执行更新。
      sudo apt-get update
      sudo apt-get install locate
      sudo updatedb
  - 支持通配符,locate *.txt
  - -r:支持正则表达式,locate -r ".*\.txt"
  - -i:忽略大小写,locate -i *.txt
## rm命令，删除文件
+ rm [file_dir] 
  - -r递归删除文件路径 
  - -i/f:删除前询问/不询问 
## touch命令，创建文件
+ touch 文件名   创建文件，一次性可以创建多个文件，名称用空格隔开
## mv命令，文件移动和重命名
+ mv src dest
  - 当地二个数据为文件名时，为重命名。
  - -i可提示移动 
  - -f不询问移动
## cp、rsync、scp命令，文件复制、远程复制、远程同步
+ cp src dest
  - -a保留一切 
  - -d复制时保留链接 
  - -i/f:复制前询问/不询问 
  - -p复制修改时间和权限 
  - -r递归复制 
  - -l链接文件
  - cp defualt.txt defualt.txt.bak//备份文件
  - cp defualt.txt.bak defualt.txt//备份还原
+ scp src $user@$host:$pdir//远程复制文件
  - -r 递归复制目录
  - -p 保留修改时间和权限
+ rsync src $user@$host:$pdir//远程同步文件
  - a 递归复制目录 
  - v 显示执行过程

## mkdir文件路径的创建和删除 
+ mkdir(必须有其父目录的w权限)
  - -p递归创建 
  - -v显示创建 
  - -m设置权限也可用chmod命令
+ rmdir -p递归删除
+ **多分支目录创建：mkdir -p dir1/{dir2,dir3,dir4},注意大括号内不能有空格**

## In 文件链接命令
+ ls -li 查看文件inode(索引节点)
+ 硬链接(直接链接到源文件)：ln scr_file link_name
+ 软链接(类似快捷方式)：ln -s scr_file link_name

## grep命令,文件内容匹配。
+ -i	忽略大小写的不同，所以大小写视为相同
+ -r	递归搜索eg：grep -r "main()".
+ -v	反向选择，打印不匹配的行
+ -n 显示匹配行号
+ -c	计算找到‘搜寻字符串’（即 pattern）的次数
+ eg：grep "root" /etc/passwd --color=auto(--color=auto为颜色)
## 文件处理命令
### sort命令
+ m:若相同则合并文件
+ f:忽略大小写
+ d:按字典序排列，非字典符忽略
+ b:忽略前导空白字符。
+ r:逆序输出结果

### unip命令，删除文件中重复行
+ d/u:只(不)显示重复行
+ c:显示每行出现次数

### **wc命令 ，统计**
+ -c	统计字节数
+ -l	统计行数eg：wc -l c.txt
+ -w  统计行数
  
### comm [选项] 文件 1 文件 2 ，比较已排序文件。
+ -1不输出文件 1 特有的行
+ -2不输出文件 2 特有的行
+ -3不输出文件 1，2 特有的行
### diff [option] file1 file2,比较文件无需已排序。
+ -b 忽略空格
+ -r 递归处理，file换位dir


# 进程管理
+ 进程：进程是操作系统进行资源分配和调度的基本单位。每个进程都有自己的地址空间、文件描述符、环境变量等。
## 系统调用与进程基础
### 系统调用
+ 内核态与用户态
  - 内核态：运行操作系统内核代码的态，具有最高权限
  - 用户态：运行用户程序代码的态，权限较低。
  - **通过系统调用由用户态切换到内核态执行中断操作**
  - 普通程序在用户态下执行，内核态用于处理中断和系统调用
+ 常见的系统调用：
  - 1号:exit():终止进程
  - 2号:fork():创建子进程
  - 3号:read():从文件描述符中读取数据
  - 4号:write():向文件描述符中写入数据
  - 5号:open():打开文件
+ 每个系统调用由系统调用号唯一标识，内核维护系统调用表，
  表中的元素是系统调用函数的入口地址，号为偏移量。
+ 系统调用分类：进程管理、文件操作、设备管理、内存管理、进程通信、信息维护。
+ 内核函数查找：sys_call_table系统调用表中查找。
### 进程树
+ Linux所有进程构成了树形结构,根为0号进程。
  - 0号进程:系统启动时由内核创建,是所有进程的祖先。
  - 1号进程(init进程):由0号进程创建,负责系统初始化
    (**由内核态的kernel_init函数完成**),
    完成后execve函数加载并执行init程序(内核态信息不变，覆盖用户态信息)
    最后经过一系列内核操作切换到用户态的init进程,
    负责进程管理，系统服务，创建和管理部分内核线程
### **exec函数族与fork 函数(创建子进程)**
+ exec函数族：加载新程序覆盖当前进程空间，执行新程序。
  - execl、execv、 execve、execlp、exeecvp、fexecvp
+ pid_t fork(void);//一次调用两次返回
  //子进程返回0，父进程返回子进程的pid，出错返回-1。
+ 创建的子进程为父进程的副本，共享代码和数据，但拥有独立的进程空间。
+  
```
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();
    if (pid == -1) {
        // fork 失败
        perror("fork");
        return 1;
    } else if (pid == 0) {
        // 子进程,相当于子程序，处理代码
        if (execve("/bin/ls", NULL, NULL) < 0){
          //使用exce函数加载新程序
            printf("exec eorr!\n");
            exit(1);
        } 
    } else {
        // 父进程，父进程继续执行，处理代码
        printf("This is the parent process, PID: %d, Child PID: %d\n", getpid(), pid);
        wait(NULL); // 等待子进程结束
    }
    return 0;
}
```
### 进程的状态
+ 运行状态：进程正在执行，处于运行状态。
+ 就绪状态：进程已处于准备运行状态，即进程获得了除CPU以外的所有必要资源，一旦得到CPU资源，便可立即执行。
+ 阻塞（封锁）状态：进程正在等待某一事件而暂停执行，如等待某资源为可用或等待IO操作完成。
### 进程类型：
+ 交互进程：由shell启动的进程，如ps、top等。可在前台或后台运行。
+ 批处理进程：和终端无联系，是一个进行序列。
+ 守护进程：系统启动时的进程，并在后台运行。
### 进程的工作模式
+ 用户模式：如运行的是程序，则该进程处于用户模式。
+ 内核模式：如用户程序执行中出现了系统调用或发生了中断事件，需要运行操作系统的核心程序，则该进程处于内核模式。
## 守护进程（后台运行）
+ 守护进程是一种独立于控制终端并且周期性地执行某种任务或等待处理某些发生的事件。
+ 启动的方法
  - 在引导系统时启动的进程，在系统引导过程中运行，在系统关闭时终止。一般存放在/etc/rc.d中。
  - 手动输入shell提示符。
  - 使用crond守护进程启动，存放在/var/spool/cron/crontabs目录，中为需要周期执行的命令。
  - 使用at命令，定时执行。
### at命令(仅执行一次的定时任务)
+ 格式：at [-f file] time
+ 参数：
  - -f：指定命令从某个文件中读取数据。
  - -V：显示版本信息。
  - -q：使用指定队列，合法的队列名为"a-z"或A~Z。a队列是默认队列。
  - -m: 指定任务执行后的邮件通知。
  - -d：删除一个或多个任务。
  - -l: 列出指定队列中的所有任务。
  - -v:显示执行时间。
  - -c: 显示指定任务的详细内容到标准输出。
  - 时间：指定任务执行的时间，格式为"HH:MM 月.日.年(最后两位)"。

以下是一个at命令的示例：

```
at 12:00 -f -m "test task" "ls"
这个命令会在12:00执行"ls"命令，并显示任务执行后的结果。同时，任务描述信息为"test task"。

需要注意的是，at命令执行的任务需要用引号括起来，以确保命令的完整性。此外，at命令执行的任务需要具有可执行权限，否则会无法执行。
```
### batch命令，空闲时执行。
+ 格式：batch  [-V] [-q queue] [-f file] [-mv] [-time]
+ 参数参考at命令，但一般不指定时间。

## 进程查询与终止
### 进程查询
+ pstree [opt]//以树状图显示进程
  - p:显示进程PID
  - u:显示进程所属用户
+ ps -aux //查询所有进程
  - a:显示所有进程，包括其他用户的进程。
  - u:以用户为主的格式来显示进程状态。
  - x:显示没有控制终端的进程。
  - ps -aux | grep XXX//查询特定XXX进程
+ top [opt]//实时显示进程状态
  - -d 秒数:指定top命令的刷新时间间隔，单位为秒。
  - -p PID:指定要显示的进程ID。
  - i :忽略闲置和僵死进程。
  - 交互式输入命令：
    - u + username:查看指定用户进程 
    - P:以CPU使用率排序，默认
    - M:以内存使用率排序
    - N:以PID排序
    - q:退出top命令
    - k PID:终止PID号进程
### 进程终止
+ kill [option] PID
  - 9:强行结束进程
+ killall processname//结束所有同名进程,消耗资源，支持通配符

# Linux服务管理与网络管理
## Linux服务管理
+ systemctl [opt] servicename(centerOS7后用systemctl
  - start:启动服务
  - stop:停止服务
  - restart:重启服务
  - status:查看服务状态
  - reload:重新加载服务配置
  - enable:设置服务开机自启
  - disable:关闭服务开机自启
  - list-units:列出所有服务
+ 永久设置服务chconfig
  - chconfig list:列出所有服务
  - chconfig -level 5 servicename on/off:设置服务在特定级别自启
  - chconfig servicename on/off:设置服务开机自启,在所有运行级别
## Linux网络管理
+ 安装：sudo yum install -y nc
### 查看网络状态
+ netstat [opt] //查看网络状态
  - a:显示所有连接和监听端口。
  - n:以数字形式显示地址和端口号。
  - p:显示进程ID和进程名。
  - tlinp:显示TCP、UDP和ICMP协议的连接和监听端口。
### 开启虚拟机网络
+ 登录root用户
+ ifconfig -a 查看使用的网卡，一般为ens33
+ ifup ens33 激活链接，一般默认为DHCP模式
+ 打开虚拟网络编辑器，新建VMnet8设置为nat模式设置子网IP。
+ 启动并设Windows下的虚拟网卡VMnet8设置为自动获取IP，也可固定IP、掩码、网关DNS。
### 固定IP(需要重启)
+ vi /etc/sysconfig/network-scripts/ifcfg-ens33
  - ONBOOT=yes
  - BOOTPROTO=static
  - IPADDR=192.168.1.100
  - NETMASK=网关
  - DNS1=域名解析器
### 更改用户主主机名
+ //临时修改 hostnamectl set-hostname new-hostname
+ vi /etc/sysconfig/network
  - 127.0.1.1   new-hostname
+ 更改Linu域名映射：
  - /etc/hosts
  - 127.0.0.1   localhost
+ 修改Windows的hosts文件：
  - C:\Windows\System32\drivers\etc\hosts(复制到桌面修改后替换)


## **用户与组管理命令**
### whoaim 命令，查看当前登录用户。
+ -u 显示用户登录时间。
+ who am i :显示当前所有登录用户。
### useradd 命令，添加用户。
+ -c	指定描述性信息
+ -d	指定用户主目录 ,-d /home/newuser  
+ -e	指定帐号失效时间
+ -g	指定用户所属组
+ -G	指定用户所属的附加组
+ -p 	指定用户密码
+ -s 指定用户登录Shell,-s /bin/bash
+ -r	创建系统用户
### passwd 命令，修改密码。
+ -l	锁定帐号
+ -u	解锁帐号
+ -d	使账号无密码
+ -f	强迫用户下次登录时修改密码
### usermod 命令，修改用户。
+ -c	修改用户描述信息
+ -d	修改用户主目录
+ -e	修改用户失效时间
+ -g	修改用户所属组
+ -G	修改用户所属的附加组
+ -l	修改用户名
+ -L	锁定用户密码
+ -U	解锁用户密码
+ -s	修改用户登录Shell
### userdel 命令，删除用户。
+ -r	删除用户主目录  
+ -f	强制删除用户
### id 命令，查看用户信息。
+ -u	显示用户UID
+ -g	显示用户GID
### 提权命令：sudo ll /root
+ 显示root目录。
+ 操作：vi /etc/sudo,末行添加：user1 ALL=(ALL) ALL
+ Ubuntu：vi /etc/sudoers
### groupadd 命令，添加组。
+ -g	指定组ID
+ -o	创建一个系统组
### groupdel 命令，删除组。

# 磁盘管理命令
## 磁盘基础知识
+ 所有的硬件设备都映射到一个文件系统，swap分区可提供虚拟内存。
+ 设备类型：
  - IDE设备：前缀hd,编号为abcd...
  - SCSI设备，前缀sd,编号为abcd...
+ 硬盘分区：
  - 最多有4个主分区（以数字编号1234），含拓展分区，拓展分区中可以逻辑分区（编号以5开始）。
+ **磁盘配额的准备工作**
  - 需要先创建磁盘配额文件，aquota.grp和aquota.user。
  - 使用quotacheck命令可自动创建磁盘配额文件。(eg:quotacheck -avgu)
  - quotacheck命令选项：
    - -a:扫描/etc/mtab中所有挂载的文件系统。
    - -u:计算各个用户占用的目录和文件数目，并创建aquota.user文件。
    - -g:计算各个组占用的目录和文件数目，并创建aquota.grp文件。
    - -v:互动模式。
    - -b:备份旧的配额文件。
### 对用户或用户组进行磁盘限制
+ 软限制：用户在文件系统可拥有的最大磁盘空间和最大文件数量，在某个宽限范围可暂时超过限制。
+ 硬限制：用户可拥有的最大磁盘空间和最大文件数量，绝对不可超过这个限制。
### 磁盘配额命令edquota
+ -g:组配额
+ -u:用户配额
+ -p:对磁盘配额设置进行复制。
+ -t:对文件系统进行软限制。
+ eg:
  - 设置用户配额：edquota -u user
```
/dev/sda5:block in use:0,limits(soft=0,hard=0)
#soft:磁盘容量软限制，单位为B。
#hard:磁盘容量硬限制，单位为B。
inodes in use:0,limits(soft=0,hard=0)
#soft:文件数量软限制，单位为个。
#hard:文件数量硬限制，单位为个。
```
## 磁盘挂载/卸载命令
### mount命令，临时挂载命令。
+ mount [-t type] sdb path
  - type 为文件系统个格式（ext4、vfat、ntfs）
  - device 设备名
  - dir 为挂载点
### 永久挂载磁盘(启动时自动挂载)
+ vim etc/fstab
+ 新增记录：sdb path
### umount命令，卸载命令
+ umount [device/dir]
## 查看磁盘分区，统计磁盘使用情况
+ mount 显示磁盘挂载信息
+ fdisk -l 查看磁盘分区信息
+ df 查看磁盘情况(-h以KB、MB、GB为单位显示)
+ du [opt] dir 查看目录占用情况
  - -h:以KB、MB、GB为单位显示
  - -s:显示总计
  - -a:显示所有文件和目录大小
  - -c:显示明细和总计
  - --max-depth=1:显示目录下第一层文件大小
## fdisk path：进行磁盘手动分区，和格式化
+ fdisk dir //开始分区
  - m:选择命令。
  - n:新增分区
  - d:删除分区
  - p:显示已有分区信息
  - q:退出
  - t:设置分区号
  - u:改变空间大小显示方式
  - w:保存
  - x:进入专家模式
+ mkfs 分区格式化
  - mkfs -t type device [block_size]
    * type 格式化后的类型
    * device 为设备名
    * [block_size] 设备大小为可选参数
  - mkswap dir //将dir格式化为swap分区
## 查看用户（组）使用情况：quota
+ quota -u user3查看用户3的磁盘使用情况。
## **统计文件数**
+ ls -l | grep "^-" | wc -l //统计当前目录下文件数
+ ls -lR | grep "^-" | wc -l //统计当前目录及子目录下文件数
+ ls -lR | grep "^d" | wc -l//统计当前目录下目录数


# liunux 编程
## 编译与运行
+ gcc -o hello.c hello.out
+ ./hello.out //运行程序(需要可执行权限)
## 调试
+ gcc -g hello.c -o hello.out //编译时加入调试信息
+ list 1.c //查看源码
  - list 1,10 //查看第1行到第10行的源码
  - list sum //查看sum函数的源码
  - list XXX.c:sum // 查看XXX.c文件中sum函数的源码
### 调试相关
+ list 1.c //查看源码
+ gdb -q hello.out //-q跳过版权信息进行调试
+ run(r) //运行程序，开始调试
+ next(n) //单步执行
  - next 10 //执行10步
+ step(s) //执行下一步，进入函数体
  - step 10 //执行10步
+ bt://查看函数调用栈
+ print var(p var) //打印变量值,
+ quit//退出调试器
+ break 10 //在第10行设置断点
  - break 10 if i==5 //在第10行设置条件断点
  - break sort //在sort函数处设置断点
+ delete 1(d 1) //删除第1个断点
  - delete //删除所有断点
+ info breakpoints(info b) //查看所有断点
+ continue //继续执行
+ print sum //打印sum的值
  - print/x sum //以16进制打印sum的值
  - print/t sum //以2进制打印sum的值
  - print/o sum //以8进制打印sum的值

# **shell编程**
## 格式：
  - #!/bin/bash开头指定脚本解释器，但soure命令可使其在当前shell中执行。
  - 脚本需要有可执行权限：chmod +x my1.sh
## 脚本的执行与传参:
+ 在子shell执行脚本
  - 先增加权限，再执行：./my1.sh
  - sh my1.sh直接执行。
+ 在当前shell中执行脚本(**可改变当前环境中的变量**)
  - source my1.sh
  - . my1.sh
+ 传参：./my1.sh var1 var2
+ 其他
  - nohup XXX.sh &//后台执行脚本
  - 2>&1：表示将错误重定向到标准输出上(0：标准输入，1:标准输出，2:标准错误输出)
  - 组合使用：nohup  [xxx命令]> file  2>&1 &，表示将xxx命令运行的结果输出到file中，并保持命令启动的进程在后台运行。
## shell的特殊字符
+ 单引号：单引号中所有的字符都为普通字符。
+ 双引号：双引号中所有的字符除了\$、\、`之外都为普通字符。(美元，反引号，反斜杠)
+ 倒引号：倒引号中的内容为命令，且可以正常执行。
## 变量（不可以以数字开头，定义变量两侧不可有空格）：
  - 系统变量(输入set即可显示)：
    - **$HOME：当前用户主目录**
    - **$PWD：当前工作目录**
    - **$USER：当前用户**
    - $PATH：命令的搜索路径
    - **$SHELL：当前用户shell类型**
    - $LANG：当前用户语言环境
    - $PS1：主提示符
    - $PS2：次提示符
    - $UID：当前用户的UID
    - $LOGNAME：当前用户的登录名
    - $MAIL：当前用户的邮件存放目录
    - $PWD：当前工作目录
    - $SHLVL：当前shell的运行级别
    - $HOSTNAME：当前主机名
  - 用户自定义变量：
    - 定义变量：变量名=变量值（不可有空格）
    - 定义字符变量： a=“hello world”//中间有空格时需要用引号括起来。
    - 定义数组：declare -a my_array //定义了一个名为my_array的数组。访问和C一样。
    - 撤销变量：unset 变量名
    - 声明静态变量（不可撤销）：readonly 变量名
  - **设置环境变量,后可在所有脚本使用**(先进入/ect/project)：
   - 基本语法：
    - 定义变量：export 变量名=变量值
    - source /etc/profile配置文件名(刷新环境变量)
    - echo $变量名(查看环境变量)
 - 特殊变量：
  - 语法：
    - $$ ：当前进程的进程号
    - $！：后台运行的最后一个进程号
    - $？：最后一次执行的命令返回状态,echo $?可查看返回值。
    - $# : 传递给脚本的参数个数,通常用于循环判断参数的个数是否正确。
    - "$*" ：传递给脚本的所有参数，$*把所有参数看成一个整体。
    - //for i in $*,遍历输入所有参数，每个参数作为独立的一个数据保存在数组中。
    - //for i in "$*",for仅仅循环一次,所有参数为一个整体。
    - "$@" ：传递给脚本的所有参数，$@把每个参数区分对待。
### 变量的使用：
+ 使用变量前需要加上$符号。
+ 在字符串中使用变量需要有大括号括起来再加$符号。
+ 对变量重新赋值时=两边不可有空格。
+ 列式计算： $(($i%5)) == 0
#### 数组的使用与定义
+ 使用
  - 定义数组：a = (1 2 3)
  - 访问数组元素：${a[0]}
  - 更改一个数组元素：a[0] = 100
  - 删除一个数组元素：unset a[0]
  - 增加一个数组元素：a[3] = 100
+ 声明 declare
  - -a：声明数组
  - -i：声明整型
  - -x：声明环境变量
  - -f: 声明函数 
  - -r: 声明只读变量。


## 输入输出：
### 输入：
  - 命令的引用：
   - a=`date` <=> a=$(date) #将date命令执行的结果赋给a
  - 位置参数变量：
   - 作用：读入命令行输入信息。
   - 基本语法：
    - $n：n为数字，$0表示命令本身，$1-$9表示第1到第9个参数，大于10用大括号表示，如${10}
    - $*：所有参数，$@所有参数，与$*作用相同，但$*是单个字符串，而$@是数组。
    - $#：参数个数
    - $@:所有参数将每个参数作为独立的一个数据保存在数组中。
  - read 命令：读取控制台输入，交互式输入。
   - read -p "请输入用户名：" //指定输入提示符为"请输入用户名："
   - read -t 10 //指定等待输入的时间，过时不候。
   - read -p “请输入一个数字” N1 //将输入的值赋给变量N1
### 输出：
 - echo "XXX"//输出XXX字符串
 - echo -e "XXX"//输出XXX字符串，且-e执行转义字符。
 - echo "resl=$res"
 - -n：不换行输出。
## 运算符与逻辑符：
+ 基本语法
  - 格式："$((表达式))" "$[表达式]" "expr m + n//需要将结果赋给其他变量需要，用反引号括起来。
+ 逻辑符：
  - -a ：逻辑与
  - -o ：逻辑或
  - !：逻辑非
  
## 循环与条件
+ **条件判断式**（[ “OK” = “OK” ]）：
  - 数值比较（**不可使用>=需要拆开为 >  -o ==**）：
    - -eq：等于则为真。
    - -ne：不等于则为真。   
    - -gt：大于则为真。
    - -ge：大于等于则为真。
    - -lt：小于则为真。
    - -le：小于等于
  - 字符串比较：
    - =：等于则为真。
    - !=：不等于则为真。
    - -z：字符串长度为0则为真。
    - -n：字符串长度不为0则为真。
  - 文件比较：
    - -e：文件存在则为真。
    - -r：文件存在且可读
    - -w：文件存在且可写
    - -x：文件存在且可执行
    - -s：文件存在且非空
    - -d：文件存在且为目录
    - -f：文件存在且为普通文件
    - -c：文件存在且为字符型特殊文件
    - -b：文件存在且为块特殊文件
    - -p：文件存在且为命名管道
+ 条件判断式的注意：
  - 条件判断式与中括号两边必须有空格。
  - **判断式中的变量名必须需要加美元符号（$）**
+ if条件判断（非空为真）：
  - if基本语法(**条件判断式与中括号两边必须有空格**)：    
```
if [ 条件判断式 ]
then
    程序
fi
```
```
if [ 条件判断式 ]
then
    程序
else
    程序
fi
```
```
if [ 条件判断式 ]
then
    程序
elif [ 条件判断式 ]
then
    程序
fi
```
+ case条件判断（**case的判断式必须是一个字符串**）：  
```
case $变量名 in
    "值1")
        程序
        ;;
    "值2"
        程序
        ;;
    *)
        程序
        ;;
esac
```
+ 循环（exit 100终止程序返回100，可通过$?获得）
  - for循环1：
```
for in "$*"
do 
    程序
done
```
 - for循环2,注意中间的空格
```
for (( 初始值; 条件判断式; i++ ))
do
    程序
done
```
  - while循环：
```
while [ 条件判断式 ]
do
    程序
done
```
  - until循环(条件为假时，终止循环)：
```
until [ 条件判断式 ]
do
    程序
done
```
## 函数
### 系统函数
+ basename:获取文件名
  eg: basename dir/fiel.txt
+ dirname:获取文件绝对路径
  eg: dirname /home/abc/fiel.txt//输出/home/abc
+ 
### 自定义函数(必须先定义才可调用)
#### 语法
```
function 函数名(){
    程序
}
```
#### 调用
```
函数名 参数1 参数2 
```
#### 设置为任何地方都可调用
+ 设置为全局变量
```
source 文件名
```
+ 设置为当前shell环境
+ 实验
```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pwd.h>
#include <sys/types.h>
#include <sys/utsname.h>
#include <sys/wait.h> 

#define MAX_CMD_PRARM 100
#define MAX_HOSTNAME_LEN 100
#define MAX_PATH_LEN 1000
 
typedef struct
{
    char *arg[MAX_CMD_PRARM];
    int argNum;
} cmdArgV;
 
void type_prompt(char *prompt)
{
    struct passwd *pwd;
    char hostname[MAX_HOSTNAME_LEN];
    char pathname[MAX_PATH_LEN];
    int length;
 
    pwd = getpwuid(getuid()); 
    char* path = getcwd(pathname, MAX_PATH_LEN); 
    gethostname(hostname, MAX_HOSTNAME_LEN); 
    sprintf(prompt, "%s@%s:%s# ", pwd->pw_name, hostname,path);
}
 
cmdArgV *getParsedCmd(char *input)
{
    cmdArgV *retV = (cmdArgV *)malloc(sizeof(cmdArgV));
    int i = 0;
    char *token = strtok(input, " ");
 
    while (token)
    {
        retV->arg[i++] = token;
        token = strtok(NULL, " ");
    }
    retV->arg[i] = NULL;
    retV->argNum = i;
    return retV;
}

int main(int argc, char *argv[])
{
    cmdArgV *cmdArg;
    char prompt[MAX_PATH_LEN];
    char input[MAX_PATH_LEN];

    while (1)
    { 
        type_prompt(prompt);
        printf("%s", prompt); 
        fgets(input, MAX_PATH_LEN, stdin); 
        input[strcspn(input, "\n")] = '\0'; 
        cmdArg = getParsedCmd(input); 
        
        if (!(strcmp(cmdArg->arg[0],"exit"))){
        	break;
		}else if(!(strcmp(cmdArg->arg[0],"cd"))){
            if (cmdArg->argNum > 1) {
                if (chdir(cmdArg->arg[1]) != 0) {
                    perror("chdir");
                }
            }				
		}else{
			int status;
			if (fork()==0){
				waitpid(-1,&status,0);
			}else{
				char  commd[MAX_CMD_PRARM]="/bin/";
				strcat(commd,cmdArg->arg[0]);
				printf("commd:%s",commd);	
				if(execve(commd,cmdArg->arg,NULL)<0){
					printf("execve error!\n");
					exit(-1);
				}
			}
		}
//        for (int i = 0; i < cmdArg->argNum; i++)
//        {
//            printf("%s\n", cmdArg->arg[i]);
//        }
   	 	free(cmdArg);
    }

    return 0;
}

```
