# -*- coding: utf-8 -*-
"""
    $END$
    
    @Time : 2022/4/27 16:32
    @Author : noHairMan
    @File : env_name.py
    @Project : nhm-config
"""
import os.path

from nhm_config.env import EnvMapping
from nhm_config.manager import CONFIG_BASE_PATH

assert EnvMapping["DEVELOPMENT"] == {'config_path': os.path.join(CONFIG_BASE_PATH, "dev.ini")}
assert EnvMapping["PRODUCTION"] == {'config_path': os.path.join(CONFIG_BASE_PATH, "pro.ini")}