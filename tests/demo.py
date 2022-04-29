# -*- coding: utf-8 -*-
"""
    $END$
    
    @Time : 2022/4/28 16:15
    @Author : noHairMan
    @File : demo.py
    @Project : nhm-config
"""


def demo1():
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
    print("helpful: ", helpful, type(helpful))


def demo2():
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


def demo3():
    from pprint import pformat

    from nhm_config.extensions.nacos import NacosConfigExtension
    from nhm_config import ConfigManager

    manager = ConfigManager(env="development")
    manager.add_extension(NacosConfigExtension)
    print(pformat(manager.configs()))


if __name__ == '__main__':
    # demo1()
    demo3()
