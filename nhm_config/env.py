# -*- coding: utf-8 -*-
"""
    $END$
    
    @Time : 2022/4/27 16:21
    @Author : noHairMan
    @File : env_name.py
    @Project : nhm-config
"""


class EnvMeta(type):
    def __getitem__(self, item: str):
        return self.get(item)

    def get(self, item: str, default=None):
        return getattr(self, item.upper(), default)


class EnvMapping(metaclass=EnvMeta):
    """
    环境名称必须大写
    """
    DEVELOPMENT = {
        "config_path": "dev.ini",
    }

    PRODUCTION = {
        "config_path": "pro.ini",
    }
