# -*- coding: utf-8 -*-
"""
    $END$
    
    @Time : 2022/4/27 17:58
    @Author : noHairMan
    @File : nacos.py
    @Project : nhm-config
"""
import json
from json import JSONDecodeError

from nacos import NacosClient

from nhm_config.exception import NhmConfigExtensionException, BaseInfoException
from nhm_config.extensions.core.base import BaseConfigExtension
from nhm_config.logger import get_logger
from nhm_config.manager import ConfigManager, DictSection


class NacosExtensionException(NhmConfigExtensionException):
    """
    nacos拓展异常基类
    """


class NotSupportNacosConfigType(NacosExtensionException, BaseInfoException):
    """
    不支持的nacos的配置类型，请使用json格式
    """

    def __str__(self):
        return f"当前不支持的配置类型: {self.error['type']}, data-id: {self.error['dataId']}, group: {self.error['group']}"


class NacosConfigDecodeError(NacosExtensionException, BaseInfoException):
    """
    nacos配置解码错误，无法从指定类型文件中提取配置项
    """

    def __str__(self):
        return f"当前配置文件解码错误: data-id: {self.error['dataId']}, group: {self.error['group']}"


class NacosConfigExtension(BaseConfigExtension):
    __logger = get_logger("NacosConfigExtension")

    def __init__(self, manager: ConfigManager):
        super(NacosConfigExtension, self).__init__(manager)
        self.__manager = manager

    def load_config(self):
        """
        加载nacos配置
        """
        nacos_config = self.__manager["nacos"]
        nacos_client = NacosClient(
            server_addresses=nacos_config.get("server_addresses"),
            namespace=nacos_config.get("namespace"),
            username=nacos_config.get("username"),
            password=nacos_config.get("password")
        )
        configs = nacos_client.get_configs(group=nacos_config.get("group"))
        ignore_other_type = nacos_config.get_boolean("ignore_other_type")
        ignore_decode_error = nacos_config.get_boolean("ignore_decode_error")
        for data in configs["pageItems"]:
            if data["type"] != "json":
                if not ignore_other_type:
                    raise NotSupportNacosConfigType(data)
                self.__logger.warning(NotSupportNacosConfigType(data))
                continue
            try:
                config = json.loads(data["content"])
            except JSONDecodeError:
                if not ignore_decode_error:
                    raise NacosConfigDecodeError(data)
                self.__logger.warning(NacosConfigDecodeError(data))
                continue
            self.__manager[data["dataId"]] = DictSection(data["dataId"], config)
