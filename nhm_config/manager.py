# -*- coding: utf-8 -*-
"""
    $END$
    
    @Time : 2022/4/27 15:09
    @Author : noHairMan
    @File : manager.py
    @Project : nhm_config
"""
import os
from configparser import ConfigParser
from pprint import pformat
from typing import Type, Any

from nhm_config.env import EnvMapping
from nhm_config.exception import NoConfigFileError, NoEnvError, ConfigTypeError, NoSuchConfigException, \
    ConfigKeyMustBeStr
from nhm_config.extensions.core.interface import ConfigExtensionAbc
from nhm_config.logger import get_logger

CONFIG_BASE_PATH = os.path.join(os.getcwd(), "configs")

__logger = get_logger("ConfigManager")


class ConfigDict(dict):
    """
    配置类字典，为了自定义缺省异常定义
    """
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise ConfigKeyMustBeStr
        super(ConfigDict, self).__setitem__(key.upper(), value)

    def __missing__(self, key: str):
        if not key.isupper():
            return self[key.upper()]
        raise NoSuchConfigException(key)


class DictSection:
    """
    配置管理
    """

    def __init__(self, configs: dict = None):
        self.__config = ConfigDict(configs) if configs else ConfigDict()

    def __repr__(self):
        return str(self.__config)

    def get_integer(self, key: str, default=None) -> int:
        return cast(int, self.get(key, default or 0))

    get_int = get_integer

    def get_dict(self, key: str, default=None) -> dict:
        return cast(dict, self.get(key, default or {}))

    def get_boolean(self, key: str, default=None) -> bool:
        value = self.get(key, default or False)
        if isinstance(value, str):
            if value.lower().strip() in ("no", "off", "false", "0"):
                return False
        return cast(bool, value)

    get_bool = get_boolean

    def get_string(self, key: str, default=None) -> str:
        return cast(str, self.get(key, default or ""))

    get_str = get_string

    def get_list(self, key: str, default: Any = None) -> list:
        return cast(list, self.get(key, default or []))

    def get(self, key: str, default: Any = None) -> Any:
        return self.__config.get(key, default)

    def set(self, key: str, value: Any):
        self.__config[key] = value

    def __getitem__(self, item) -> Any:
        return self.__config[item]

    def __setitem__(self, key, value):
        self.set(key, value)


def load_config(parser: ConfigParser) -> dict:
    config = {}
    for section in parser.sections():
        item = DictSection()
        for option in parser.options(section):
            item[option] = parser.get(section, option)
        config[section] = item
    return config


def get_config(*, env: str = None, env_name: str = "NHM_ENV", env_mapping: Type[EnvMapping] = EnvMapping) -> dict:
    """
    使用标准库configparser解析ini文件

    :param env: 指定当前使用的环境项，当同时配置了 环境变量指定 和 指定此参数 时，优先使用此参数指定的环境项
    :type env: str
    :param env_name: 当前使用的环境变量名称
    :type env_name: str
    :param env_mapping: 配置文件项，如需新增多套环境配置，请继承实现此类
    :type env_mapping: Type[nhm_config.env.EnvMapping]
    :return: 所有ini配置文件中的配置项
    :rtype: dict
    """
    environment = env if env else os.environ.get(env_name) or "development"
    environment = environment.lower()

    parser = ConfigParser()
    environment_object = env_mapping.get(environment)
    if environment_object is None:
        raise NoEnvError(environment)
    if not os.path.exists(config_path := os.path.join(CONFIG_BASE_PATH, environment_object["config_path"])):
        raise NoConfigFileError(config_path)

    __logger.info(f"------ ConfigManager ------")
    __logger.info(f"当前环境: {environment}")
    __logger.info(f"配置文件: {config_path}")
    __logger.info(f"--------------------------")

    with open(config_path) as fh:
        parser.read_file(fh)
    return load_config(parser)


def cast(_type, value):
    try:
        return _type(value)
    except TypeError:
        raise ConfigTypeError


class ConfigManager:
    """
    配置管理类客户端
    """
    __logger = get_logger("ConfigManager")

    def __init__(self, env: str = None, env_name: str = "NHM_ENV", env_mapping: Type[EnvMapping] = EnvMapping):
        """
        初始化管理客户端，根据指定环境项从配置文件中加载配置，
        未指定环境项时，默认加载 development 环境

        :param env: same to method `get_config`
        :param env_name: same to method `get_config`
        :param env_mapping: same to method `get_config`
        """
        super(ConfigManager, self).__init__()
        self.__config = get_config(env=env, env_name=env_name, env_mapping=env_mapping)
        self.__logger.debug(pformat(self.__config))

    def get(self, key: str):
        return self.__config.get(key, DictSection())

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.__config[key] = value

    def configs(self):
        return self.__config

    def add_extension(self, extension_class: Type[ConfigExtensionAbc]):
        extension = extension_class(self)
        extension.load_config()
