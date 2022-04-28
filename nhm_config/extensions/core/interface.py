# -*- coding: utf-8 -*-
"""
    $END$
    
    @Time : 2022/4/27 18:28
    @Author : noHairMan
    @File : interface.py
    @Project : nhm-config
"""
from abc import ABC, abstractmethod


class ConfigExtensionAbc(ABC):
    """
    配置拓展接口，抽象基类
    """

    @abstractmethod
    def __init__(self, manager):
        """
        初始化
        """

    @abstractmethod
    def load_config(self):
        """
        加载对应配置

        :return: None
        """

