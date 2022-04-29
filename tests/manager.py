# -*- coding: utf-8 -*-
"""
    $END$
    
    @Time : 2022/4/27 15:37
    @Author : noHairMan
    @File : manager.py
    @Project : nhm_config
"""
from pprint import pformat

from nhm_config.env import EnvMapping
from nhm_config.extensions.nacos import NacosConfigExtension
from nhm_config.manager import get_config, ConfigManager


def test_get_config_parser():
    config = get_config(env="production")
    return config


def test_config_manager():
    class MyEnvMapping(EnvMapping):
        # DEVELOPMENT = {
        #     "config_path": "dev.ini",
        # }
        # PRODUCTION = {
        #     "config_path": "pro.ini",
        # }
        TEST = {
            "config_path": "test.ini"
        }

    manager = ConfigManager(env="development", env_mapping=MyEnvMapping)
    print(manager["base"]["DEBUG"])
    print(manager["base"]["debug1"])
    breakpoint()
    assert manager["nacos"].get_string("namespace") == "a24a222f-6a1a-457d-90d0-9e7665f5eb77"
    assert manager["base"].get_boolean("debug") is True
    assert manager["base"].get("no_such_key", 123) == 123
    assert manager["no_such_key"].get("no_such_key") is None
    assert manager["no_such_key"]["no_such_key"] is None
    manager.add_extension(NacosConfigExtension)
    print(pformat(manager.configs()))


# assert test_get_config_parser() is not None
assert test_config_manager() is None
