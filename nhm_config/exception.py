# -*- coding: utf-8 -*-
"""
    自定义异常模块
    
    @Time : 2022/4/27 15:50
    @Author : noHairMan
    @File : exception.py
    @Project : nhm-config
"""


class NhmConfigException(Exception):
    """
    异常基类
    """


class NhmConfigExtensionException(NhmConfigException):
    """
    拓展异常基类
    """


class BaseInfoException(Exception):
    def __init__(self, error: str):
        self.__error = error

    @property
    def error(self):
        return self.__error

    def __str__(self):
        return f"当前错误对象: {self.error}"


class NoEnvError(NhmConfigException, BaseInfoException):
    """
    未获取到对应配置文件
    """
    def __str__(self):
        return f"此环境配置不存在: {self.error}"


class NoConfigFileError(NhmConfigException, BaseInfoException):
    """
    未获取到对应配置文件
    """
    def __str__(self):
        return f"当前配置文件不存在: {self.error}"


class ConfigTypeError(NhmConfigException):
    """
    配置类型转换错误
    """