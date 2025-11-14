[toc]

# markdown 语法
##### 无法打开侧边预览，重启软件（重启电脑）
##  一、标题的使用
使用 # 表示标题，其中 # 号必须在行首，##二级标题。
#### 二、粗体与斜体
用一对*括起来为斜体，两对为粗体，三对为又粗又斜体，先选中后可直接在两端同时添加\*符号。
##  三、分割线的使用
使用三个以上及以上的***或---，独占一行。
##  四、文字上划线表示删除
用两个~为一边括起来，可在文字上划线。
##  五、超链接与图片写法
第一个方括号为链接名（图片介绍），后紧接一个()写链接。而图片前加一个！即可。
##  六、列表
6.1.无序列表：使用‘-’ ‘+’ ‘*’表示无序列表，可嵌套。
6.2.有序列表：<数字.两个空格>
##  七、区块
markdown区块是在段落开头使用 “>”，依然是紧跟空格，可嵌套使用，如“>>”表示第一区块内的又一区块。
##  八、代码插入
+ 一行用单引号括起来，多行用三个为一组单引号括起来, 在第一组单引号可加标识表示是什么代码。
  - eg:
  ```
  hello world
  ```
  - eg：Java
  ```java
  public class HelloWorld {
      public static void main(String[] args) {
          System.out.println("Hello, World!");
      }
  }
  ```
##  九、表格
每排单元格要用| 分开 表头与内容用 — 分开，加:可以实现左对齐，右对齐，居中。不加则默认为左对齐,注意符号要用英文。
eg：
“|  表头   | 表头  | 表头 | 表头 |
| :---  | ---:  | :--: | ---- |
| 单元格  | 单元格 |单元格|单元格|
| 单元格  | 单元格 |单元格|单元格|”

|  表头   | 表头  | 表头 | 表头 |
| :---  | ---:  | :--: | ---- |
| 单元格  | 单元格 |单元格|单元格|
| 单元格  | 单元格 |单元格|单元格|
***
##  十、标签
1.  不在 Markdown 涵盖范围之内的标签，都可以直接在文档里面用 HTML 撰写。
<h1>一级标题</h1>
<h2>二级标题</h2> 
<h3>三级标题</h3>
<p>段落标签</p>

2.  hgroup标签主要作用是用来为标题分组，可以将一组相关的标题放到hgroup里面。
+  第一em标签的样式是斜体，而strong标签的样式是加粗
+  第二em标签是强调语义的，而strong标签是强调内容的
+  q标签和blockquote标签都是引用，不同的是q标签是短引，用而blockquote标签是长引用会换行的。
+  br标签的作用是，强制换行，它是一个自结束标签。
+  hr标签就是给页面加一个分割线,这个del标签就是删除标签
+  center标签的作用就是剧中，把文字啊图片啊啥的全部居中到页面中间
+  div标签是用来布局的，并没有语义，只是一个区块。
+  **span标签，没有语义，一般用来包裹文字,让文字更好被选中。（也可用反引号引起来）**
+  b是加粗
##  十一、上传文件
查看->终端
git add markdown-help.md
git commit -m "newfile"
git branch -M main
git push -u origin main（-f强制推送）
443错误：git config --global --unset http.proxy
        git config --global --unset https.proxy
        \<font color='red'> C </font>
## 十二、数学公式插入
+ $d(x,y)=\sqrt{\sum_{i=1}^{n}(x_i-y_i)^2}$
+ 在Markdown中写数学公式主要有两种方式：行内公式和行间公式
  - 行内公式（行内插入）
    - 用一对美元符号`$`将公式括起来，公式会在文本行内显示。例如，\$ a^2 + b^2 = c^2 \$，显示效果：$ a^2 + b^2 = c^2 $ 
  - 行间公式（独占一行）
    - 用一对双美元符号`$$`将公式括起来，公式会单独占一行并居中显示。例如：
    ```
    $$
    \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
    $$
    ```
    显示为：
    $$
    \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
    $$

### 常用数学符号和语法
+ **上标和下标**：使用`^`表示上标，`_`表示下标。例如， x^2 表示$x^2$，x_i表示$x_i$
+ **分式**：使用`\frac{分子}{分母}`来表示分式。例如，\frac{1}{2}表示$\frac{1}{2}$。
+ **根式**：使用`\sqrt{}`表示根号，根号下的内容放在大括号内。例如，\sqrt{2}表示$\sqrt{2}$
+ **求和**：求和符号用`\sum`表示，上下限用`_{下限}^{上限}`表示。例如，\sum_{i=1}^{n} i : $\sum_{i=1}^{n} i$表示从1到$n$的求和，
+ **积分**:积分符号用`\int`表示，\int_{0}^{1} x^2 dx表示从0到1对$x^2$的积分$\int_{0}^{1} x^2 dx$。
  - 无穷数表示：用`\infty`表示无穷大,`-\infty`。例如，$\int_{-\infty}^{\infty} e^{-x^2} dx$表示从负无穷到正无穷对$e^{-x^2}$的积分$\int_{-\infty}^{\infty} e^{-x^2} dx$。
+ **希腊字母**：希腊字母可以通过在字母名称前加上反斜杠`\`来输入。例如，\alpha表示$\alpha$，\beta表示$\beta$，\pi表示$\pi$等，其他符号见末尾符号表。
+ **矩阵**：使用`\begin{matrix}...\end{matrix}`来表示矩阵，矩阵元素之间用`&`分隔，行与行之间用`\\`分隔。例如：

```
$$
\begin{matrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{matrix}
$$
```
表示一个3x3的矩阵:
$$
\begin{matrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{matrix}
$$

### 特殊字符转义
- 如果要在公式中显示美元符号`$`、反斜杠`\`等特殊字符，需要在其前面加上反斜杠进行转义。例如，要显示$x = \$5$，需要写成$x = \$5$。
### 不同系统字体库
+ Windows：C:\Windows\Fonts
+ Linux：/usr/share/fonts,可通过fc-list查看字体库
+ MAC: /System/Library/Fonts
# pycharm技巧
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
## 插件
+ 中文插件：setting->plugins->搜索chinese->install
## 键盘操作
+ 按shift+F6可打出省略号
+ 打开超级复制板：按下win+C 开启超级复制版，可复制不连续的内容后一起按下win+V粘贴。
+ win+shift+s：截屏
# 常用CMD（DOS）命令
+ win+R：打开运行
    - 输入cmd可打开控制台
    - notepad可打开记事本
    - taskmgr可打开任务管理器
+ dir：查看当前目录
+ cd：切换目录，注意切换磁盘分区时直接D:+enter
+ cls：清屏
+ exit//退出控制台
+ ipconfig：查看本机IP地址
+ ping：检测网络连通性
+ netstat：查看当前网络连接
+ net start：启动服务
+ net stop：停止服务
+ netstat -an |  more //查看当前网络连接并分页显示
   - 外部地址：有没有外部链接连到本地端口
   - 状态：listening正在监听， establ lshed已连接
+ netstat -an | findstr 9999 //查看9999端口
+ net -anb //查看网络连接并显示使用程序，需要管理员权限
+ tree:查看目录结构
+ md(mkdir):创建目录
+ rd:删除目录
+ del:删除文件
+ copy:复制文件
+ move:移动文件
+ ren:重命名文件
+ type:查看文件内容
+ find “XXX”//查找文件
+ echo:输出内容
  - echo %path%：查看环境变量
  - echo %JAVA_HOME%：查看JAVA_HOME环境变量
  - echo %CLASSPATH%：查看CLASSPATH环境变量
  - echo %HADOOP_HOME%：查看HADOOP_HOME环境变量
  - echo %HADOOP_CONF_DIR%：查看HADOOP_CONF_DIR环境变量
+ showdown:关机
+ at 22:00/everyday:M,T,W,TH,F,S,SU 1.bat//在星期一至星期日的22:00执行1.bat
  - at //查看定时任务
  - at ID delete//删除定时任务
# 批处理文件编写.bat(大小写不敏感)
+ @echo off//不显示盘符
+ pause//通常在末尾使用，暂停程序运行，用于观察结果
+ SET myVar=Hello//定义变量
+ set /a var1=1+2//斜杠a表示数学运算
+ ECHO %myVar%//输出变量
+ %N:接收用户输入参数
+ call 1.bat //调用1.bat
+ REM或:: //注释
+ 支持重定向符号>、>>，支持&&和||，支持管道符号|
+ exist:判断文件是否存在,
## 批处理之分支
+ IF EXIST myfile.txt (
    ECHO 文件存在
  ) ELSE (
      ECHO 文件不存在
  )
+ for /d in path do xxx ://遍历目录执行do后的命令
+ for /d %%a in (*) do @echo %%a//遍历当前目录,(\*)表示当前路径
+ for /r %%a in (*) do @echo %%a//遍历当前目录及其子目录

# git
+ **注意每次开发前先pull代码，保证当前为最新版本，合并分支时若你的版本低于远程版本会合并失败**
+ 代码托管平台：github、码云Gitee、gitlab：公司内网代码托管平台
+ git不能追踪到空目录解决：在该空目录下创建一个.gitkeep文件
## git项目
+ issuse：论坛用于讨论问题等
+ license：开源许可证
+ README:项目说明
  - eg:[模板](F:\Word-Markdown\Markdown-GitHub\Markdown\git仓库README模板.md)

+ 多模块项目结构
  ```
  parent
  |--通用module1  
  |--前端module2
  |--后端module3
  |--爬虫系统module4
  |--平台管理子系统module5
  ```
## 工具
+ [绘图Draw.io](https://app.diagrams.net/)
+ 
## 配置：
+ 系统用户级别：区分不同开发人员的身份
  - git config list:查看配置信息
  - git config- -global user.name yangyunuo6666
  - git config --global user.email goodMorning_pro@qq.com
  - 信息保存位置：~/.gitconfig文件
+ github协作
  - 仓库->settings->collaborators->添加协作者
+ ssh登录
  -  进入当前用户的家目录：cd ~
  -  删除.ssh目录：rm-rvf .ssh
  -  运行命令生成.ssh密钥目录：ssh-keygen-t rsa-C atguigu2018ybuq@aliyun.com 注意：这里-C这个参数是大写的C，连续回车三次
  - 复制id_rsa.pub文件内容，登录GitHub，点击用户头像→Settings→SSHandGPG keys ->  NewSSHKey：  输入复制的密钥信息
  -  回到Gitbash创建远程地址别名：git remote add origin_ssh git@github.com:atguigu2018ybuq/huashan.git
  -  推送文件进行测试
+ 配置git忽略文件：即无需git管理的文件
  - idea的配置文件等
  - 新建XXX.gitignore文件，添加需要忽略的文件名或文件夹名
    ```
    #Compiledclassfile
    *.class
    #Logfile
    *.log
    #BlueJfiles
    *.ctxt
    #MobileToolsforJava(J2ME)
    .mtj.tmp/
    # Package Files #
    *.jar
    *.war
    *.nar
    *.ear
    *.zip
    *.tar.gz
    *.rar
    # virtual machine crash logs, see http://www.java.com/en/download/help/error_hotspot.xml
    hs_err_pid*
    .classpath
    .project
    .settings
    target
    ```
  - 在~/.gitconfig 文件中引入上述文件
    ```
    [core]
      excludesfile = C:/Users/Lenovo/Java.gitignore
    ```
## git基础
+ 文件完整性：SHA-1哈希算法，任何文件一旦修改，其哈希值都会改变。
+ git保存版本的机制（快照流）：
  - Git 把数据看作是小型文件系统的一组快照。
  - 每次提交更新时Git都会对当前的全部文件制作一个快照并保存这个快照的索引。
  - 为了高效，如果文件没有修改，Git 不再重新存储该文件，而是只保留一个链接指向之前存储的文件
+ git结构：git status:查看状态
  - 工作区:git add file.txt
  - 暂存区:git commit -m "commit message"
  - 本地仓库:git push/pull
  - 远程仓库:git pull
+ 团队内部协作；
  - pull：从远程仓库拉取代码到本地仓库
    -  pull=fetch+merge
    -  gitfetch[远程库地址别名][远程分支名]
    -  gitmerge[远程库地址别名/远程分支名]
    -  gitpull[远程库地址别名][远程分支名]
  - push：将本地仓库的代码推送到远程仓库
  - clone：从远程仓库克隆代码到本地
+ 团队外部协作；
  - fork：从远程仓库克隆代码到新团队本地
  - pull request：将新团队的代码合并到原团队
  - merge：将新团队的代码审核通过后合并到原团队
+ 版本控制：
  - 使用多个分支同时推进多个开发任务，一个分支开发失败，不会对其他分支有任何影响。失败的分支删除重新开始即可。
  - 分支的切换：本质是切换HEAD指针指向的分支。
  - eg：master：主分支用于用户下载生成应用。hotfix：用于修复bug。feature_n：用于开发新功能，release_n：用于预发布分支，develop：用于日常开发分支。
  - 合并冲突解决：手动解决冲突，然后提交合并结果。

## git-idea 
+ 

## git命令 
+ git status ： 查看工作区、暂存区状态
+ git add [file name] ：将工作区的“新建/修改”添加到暂存区
+ git commit-m "commit message" [file name]：将暂存区的内容提交到本地库
+ git remote-v 查看当前所有远程地址别名
+ git remote add [别名] [远程地址] ：将远程仓库地址添加到本地
+ git push [别名] [分支名] ：将本地分支推送到远程仓库
+ git clone [远程地址] ：将远程仓库克隆到本地
+ git log：查看提交历史，空格：翻页，q：退出，b:向上翻页
  - --pretty=oneline：简洁显示提交历史
  - --oneline：简洁显示提交历史
  - --reflog：显示提交信息
+ 版本回退：
  - gitreset--hard a6ace91：回退到指定版本a6ace91
  - git reset--hard HEAD^：回退到上一个版本
  - git reset--hard HEAD~n：回退到上n个版本
    - --soft：仅在本地库回退，暂存区、工作区不变
    - --mixed：仅在本地库、暂存区回退，工作区不变
    - --hard：本地库、暂存区、工作区都回退
+ 删除文件并找回
  - 前提：删除前，文件存在时的状态提交到了本地库。
  - 操作：gitreset--hard[指针位置]
   - 删除操作已经提交到本地库：指针位置指向历史记录
   - 删除操作尚未提交到本地库：指针位置使用HEAD
+ 比较文件差异
  - gitdiff[文件名]
   - 将工作区中的文件和暂存区进行比较
  - gitdiff[本地库中历史版本][文件名]
   - 将工作区中的文件和本地库历史记录比较
  - 不带文件名比较多个文件
+ 分支操作：
  - git branch 分支名：创建分支
  - git branch -v:查看分支
  - git checkout 分支名：切换分支
  - git merge 分支名：合并分支
    - 切换到接受修改的分支（被合并，增加新内容）上 git checkout [被合并分支名]
    - ：执行merge命令 git merge [有新内容分支名]
  + 冲突解决
    第一步：编辑文件，删除特殊符号
    第二步：把文件修改到满意的程度，保存退出
    第三步：git add[文件名]
    第四步：git commit -m "日志信息"，注意：此时commit一定不能带具体文件名
## Git技巧
+ 网址前加KK可到镜像网站快速下载文件。
+ FastGitHub软件可提高Git访问速度。
+ README:项目说明文件

## gitlab
### gitlab部署


# Dev-c++技巧
+ 打开调试信息：
    + 编译器->编译选项->编译器设置->调试->调试信息
# VSCode技巧
+ shift+alt+向下：复制当前行到下一行

***
# 附录
## 符号表
| 符号 | Markdown语法 | 
|----|----|
| 小写希腊字母α | `$\alpha$` |
| 小写希腊字母β | `$\beta$` | 
| 小写希腊字母γ | `$\gamma$` | 
| 小写希腊字母δ | `$\delta$` | 
| 小写希腊字母ε | `$\epsilon$` | 
| 小写希腊字母ζ | `$\zeta$` | 
| 小写希腊字母η | `$\eta$` | 
| 小写希腊字母θ | `$\theta$` | 
| 小写希腊字母ι | `$\iota$` |
| 小写希腊字母κ | `$\kappa$` | 
| 小写希腊字母λ | `$\lambda$` | 
| 小写希腊字母μ | `$\mu$` |
| 小写希腊字母ν | `$\nu$` |
| 小写希腊字母ξ | `$\xi$` |
| 小写希腊字母π | `$\pi$` | 
| 小写希腊字母ρ | `$\rho$` | 
| 小写希腊字母σ | `$\sigma$` |
| 小写希腊字母τ | `$\tau$` | 
| 小写希腊字母υ | `$\upsilon$` |
| 小写希腊字母ϕ | `$\phi$` | 
| 小写希腊字母χ | `$\chi$` | 
| 小写希腊字母ψ | `$\psi$` | 
| 小写希腊字母ω | `$\omega$` | 
| 大写希腊字母Γ | `$\Gamma$` |
| 大写希腊字母Δ | `$\Delta$` |
| 大写希腊字母Θ | `$\Theta$` | 
| 大写希腊字母Λ | `$\Lambda$` |
| 大写希腊字母Ξ | `$\Xi$` |
| 大写希腊字母Π | `$\Pi$` |
| 大写希腊字母Σ | `$\Sigma$` | 
| 大写希腊字母Υ | `$\Upsilon$` |
| 大写希腊字母Φ | `$\Phi$` | 
| 大写希腊字母Ψ | `$\Psi$` |
| 大写希腊字母Ω | `$\Omega$` | 
| 正负号± | `$\pm$` |
| 乘号× | `$\times$` |
| 除号÷ | `$\div$` |
| 点乘⋅ | `$\cdot$` | 
| 星号∗ | `$\ast$` | 
| 圆圈运算符∘ | `$\circ$` | 
| 异或⊕ | `$\oplus$` | 
| 张量积⊗ | `$\otimes$` | 
| 圆卷积⊙ | `$\odot$` |
| 小于等于≤ | `$\leq$` |
| 大于等于≥ | `$\geq$` |
| 不等于≠ | `$\neq$` | 
| 约等于≈ | `$\approx$` |
| 恒等于≡ | `$\equiv$` | 
| 属于∈ | `$\in$` | 
| 不属于∉ | `$\notin$` |
| 子集⊂ | `$\subset$` | 
| 超集⊃ | `$\supset$` | 
| 子集或相等⊆ | `$\subseteq$` | 
| 超集或相等⊇ | `$\supseteq$` | 
| 求和符号∑ | `$\sum$` |
| 连乘符号∏ | `$\prod$` |
| 积分符号∫ | `$\int$` | 
| 无穷大∞ | `$\infty$` | 
| nabla算子∇ | `$\nabla$` | 
| 偏导数符号∂ | `$\partial$` |
| 根号$\sqrt{}$ | `$\sqrt{2}$` | 
| 分数$\frac{}{}$ | `$\frac{1}{2}$` |
