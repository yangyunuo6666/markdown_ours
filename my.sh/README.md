# 若直接复制脚本内容,粘贴时需要进入插入模式后再进行粘贴，否则会遇到第一个i才开始粘贴的情况，导致粘贴内容不完整。
+ 路径：/home/atguigu/bin
+ -bash: /home/atguigu/bin/xcall.sh: /bin/bash^M: 坏的解释器: 没有那个文件或目录
  - 有可能是因为在windows下编辑的文件，用隐藏的回车符
  - 使用 vim 编辑器转换格式
    用vim打开脚本文件：vim /home/atguigu/bin/xcall.sh 。
    进入命令模式（按Esc键），然后执行命令 :set ff=unix ，将文件格式转换为 Unix 格式（去除多余回车符）。
    保存并退出（:wq ）
