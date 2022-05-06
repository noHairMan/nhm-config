# nhm-config

>   Author: noHairMan

***

### 一、项目简介

​	nhm-config 是一个配置管理模块，拓展了 python 标准库 configparser 的功能。自动检测环境变量选择对应环境的配置，当前只支持使用 ini 类型配置。支持多种类型的配置整合，放在项目的 extension 模块中，用户可通过 manager.add_extendsion 自由组合添加。当前 extension 中默认实现了 nacos 的整合，具体使用可参见以下示例。

***

### 二、项目文档

***

### 三、快速开始

1.   简单示例

     >   在当前项目运行目录下添加 configs/dev.ini 文件，配置demo如下:

     ```ini
     [env]
     env = development
     
     [base]
     debug = True
     
     [mysql]
     ```

     >   编写python代码，即可使用当前项目配置

     ```python
     from nhm_config import ConfigManager
     
     # 创建配置管理类对象
     manager = ConfigManager()
     
     # 获取布尔值类型参数
     debug = manager["base"]["debug"]
     print("debug: ", debug, type(debug))
     debug = manager["base"].get_boolean("debug")
     print("debug: ", debug, type(debug))
     
     # 获取不存在的参数，并传递不存在时候的默认值
     useless = manager["base"].get_boolean("useless")
     print("useless: ", useless, type(useless))
     helpful = manager["base"].get_boolean("helpful", True)
     print("helpful: ", helpful, type(helpful)
     ```

2.   使用自定义环境

     >   添加 configs/test.ini 文件

     ```ini
     [base]
     debug = false
     ```

     > 编写 python 代码，使用 test 配置文件
     >
     > **注：这里是在代码中指定使用 test 环境，生产环境请使用环境变量配置**

     ```python
     from nhm_config import ConfigManager, EnvMapping
     
     # 新增环境类型，添加完成后，自行增加 test.ini 文件
     class MyEnvMapping(EnvMapping):
         TEST = {
           "config_path": "test.ini"
         }
     
     # 设置环境变量名称为 $custom-env-name, 会从环境变量的值获取 $custom-env-name 的值，
     # 若要使用 test 环境的配置，可提前设置好，默认为: development
     manager = ConfigManager(env="test", env_name="custom-env-name", env_mapping=MyEnvMapping)
     print(manager["base"].get_boolean("debug"))
     ```

     > 两种方式设置环境的值

     - 代码中指定

         ```python
         manager = ConfigManager(env="test", env_name="custom-env-name", env_mapping=MyEnvMapping)
         ```

     - 通过环境变量设置

         ```shell
         # 设置当前环境变量
         custom-env-name=test
         # 打印结果是否设置成功
         echo $custom-env-name
         # test
         ```

     > 第一种代码中指定的方式一般只是测试的时候使用，生产环境请使用第二种方式：在环境变量中设置

3.   使用nacos拓展

     >   在 dev.ini 配置中添加nacos配置

     ```ini
     [nacos]
     server_addresses = http://192.168.2.43:8848
     namespace = a24a222f-6a1a-457d-90d0-9e7665f5eb77
     username = spider
     password = BG6KgemzwqZF9SD
     group = spider
     ignore_other_type: true
     ignore_decode_error: true
     ```

     -   group: 加载指定的group
     -   ignore_other_type: 当前在nacos中只支持解析json格式配置，是否忽略其他类型的配置的解析错误
     -   ignore_decode_error: 是否忽略解码nacos配置的错误，忽略时，发生

     >   编辑python代码，添加nacos拓展，添加拓展之后，会自动从对应配置文件中读取指定配置
     
     ```python
     from pprint import pformat
     
     from nhm_config.extensions.nacos import NacosConfigExtension
     from nhm_config import ConfigManager
     
     # 创建管理客户端，并添加拓展
     manager = ConfigManager(env="development")
     manager.add_extension(NacosConfigExtension)
     # 查看加载完成的配置
     print(pformat(manager.configs()))
     ```

---

### 四、Todo list

1.   待支持继承配置类时的配置方法，类似如下方式新增配置。

     ```python
     class Config(ConfigManager, metaclass=SubConfigMeta):
         THREAD_NUMBER = 4
         # kafka topic
         KAFKA_DATA_TOPIC = "patent-notice-change"
         # 待采集的任务队列
         REDIS_PROCESS_QUEUE_CHANGE = "patent:request:change"
     ```

---

### 五、注意事项

1.   配置项不区分大小写，存储时都会转换为大写。

     

