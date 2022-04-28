# -*- coding: utf-8 -*-
"""
    $END$

    @Time : 2022/4/27 17:58
    @Author : noHairMan
    @File : base.py
    @Project : nhm-config
"""

from nhm_config.extensions.core.interface import ConfigExtensionAbc


class BaseConfigExtension(ConfigExtensionAbc):
    """
    配置拓展基类
    """

    def __init__(self, manager): ...

    def load_config(self): ...
