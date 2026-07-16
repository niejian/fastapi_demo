#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2026-07-16 11:07:07
# @Author  : xxyyzz
# @Link    : base_config
# @Version : 0.0.1
# @Desc    : 基础配置

import os

from pydantic_settings import BaseSettings, SettingsConfigDict

env = os.getenv("APP_ENV", "dev")
env_file = f".env.{env}"  # 自动拼出 .env.dev 或 .env.prod

class BaseConfig(BaseSettings):
    """
    基础配置类
    """
    debug: bool = True
    db_host: str = "localhost1"
    db_port: int = 33061
    db_user: str = "root1"
    db_password: str = "1234561"
    db_name: str = "rabac_demo"
    zk_str: str = "localhost" #zookeeper://192.168.240.15:2181?backup=192.168.240.15:2182,192.168.240.15:2183

    zk_timeout: int = 10

    def get_db_url(self) -> str:
        """
        获取数据库连接 URL
        """
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"


    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"
    

    model_config = SettingsConfigDict(
        env_file=env_file, 
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        )

base_config = BaseConfig()