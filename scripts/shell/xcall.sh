#! /bin/bash
#xcall 后面跟着linux指令操作，可以同时对多个服务器节点同时执行相同指令
#，eg：xcall jps 
for i in  hadoop102 hadoop103 hadoop104
do
    echo --------- $i ----------
    ssh $i "$*"
done
