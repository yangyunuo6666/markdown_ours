[toc]

***
# DataX
+ datax架构：以DataX框架为核心，将不同的数据源进行数据抽取和数据写入，当需要接入一个新的数据源的时候，只需要将此数据源对接到 DataX，便能跟已有的数据源做到无缝数据同步
  - Reader：数据采集模块，负责采集数据源的数据，将数据发送给Framework。
  - Writer：数据写入模块，负责不断向Framework取数据，并将数据写入到目的端。
  - Framework：用于连接reader和writer，作为两者的数据传输通道，并处理缓冲，流控，并发，数据转换等核心技术问题。

+ 运行原理：DataX 作业启动后，会通过 Job 管理器创建一个或多个 Task，每个 Task 负责一部分数据的同步工作。Task 又分为 TaskGroup，每个 TaskGroup 包含多个 Task。DataX 通过 TaskGroup 来实现并发，从而提高数据同步的效率。

+ **数据同步命令**：python /opt/module/datax/bin/datax.py /opt/module/datax/job/XXX.json
+ **查看配置文件模板命令**：python /opt/module/datax/bin/datax.py -r AXXreader -w BXXwriter
  - 从AXXreader读取数据，写入到BXXwriter
  - 支持mysql、hdfs、等
  - 配置文件起名：AXX2BXX.json（A to B）
+ 编写配置文件：/opt/module/datax/job/AXX2BXXX.json 
+ 使用配置文件生成脚本生成
  - 上传jar包
  - 修改配置文件
    ```properties
    datax-config-generator-1.0-SNAPSHOT-jar-with-dependencies.jar
    mysql.username=root
    mysql.password=root
    mysql.host=hadoop102
    mysql.port=3306
    hdfs.uri=hdfs://hadoop102:8020
    is.seperated.tables=0

    mysql.database.import=ad
    mysql.tables.import=base_complex,base_dic,base_organ,base_region_info,employee_info,express_courier,line_base_info,line_base_shift,truck_driver,truck_info,truck_model,truck_team
    import_out_dir=/opt/module/datax/job/import

    #mysql.database.export=tms_report
    #mysql.tables.export=
    #export_out_dir=/opt/module/datax/job/export
                                
    ```
    - 运行jar包生成配置：java -jar datax-config-generator-1.0-SNAPSHOT-jar-with-dependencies.jar
## Datax部署
+ [下载地址](http://datax-opensource.oss-cn-hangzhou.aliyuncs.com/datax.tar.gz)
+ [源码地址](https://github.com/alibaba/DataX)

+ 依赖关系
  - Linux、jdk1.8、Python2.6X

+ 安装：解压压缩包即可， tar -zxvf datax.tar.gz -C /opt/module/
  - 自检：cd /opt/module/datax/bin/; python datax.py /opt/module/datax/job/job.json
  - 编写配置文件：vim /opt/module/datax/job/stream2stream.json
    ```json
    {
        "job": {
            "content": [
                {
                    "reader": {
                        "name": "streamreader",
                        "parameter": {
                            "sliceRecordCount": 10,
                            "column": [
                                {
                                    "type": "long",
                                    "value": "10"
                                },
                                {
                                    "type": "string",
                                    "value": "hello，DataX"
                                }
                            ]
                        }
                    },
                    "writer": {
                        "name": "streamwriter",
                        "parameter": {
                            "encoding": "UTF-8",
                            "print": true
                        }
                    }
                }
            ],
            "setting": {
                "speed": {
                    "channel": 1
                }
            }
        }
    }   
    ```
+ 运行：python datax.py /opt/module/datax/job/stream2stream.json

## Datax使用(同步数据)
+ 1.编写配置文件，vim /opt/module/datax/job/AXX2BXXX.json
+ 2.运行：python datax.py /opt/module/datax/job/AXX2BXXX.json//将数据从AXX同步到BXXX

# Sqoop
































