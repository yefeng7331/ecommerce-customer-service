"""
@Author:叶枫
@Time:2026/9/8
@Desc:配置文件
        模块作用：加载环境变量，解析YAML文件，管理配置参数
"""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# import os
#
# from dotenv import load_dotenv
#
# load_dotenv()
# os.getenv("LLM_MODEL")

# 1. 加载.env文件路径

## 获取相对路径
ENV_DIR = Path(__file__).parents[2]
ENV_FILE = ENV_DIR / ".env"


# 2.使用pydantic-settings方式读取配置
# 第一步 创建类，继承BaseSettings
# 第二步 使用封装好的方法读取env文件的内容

class Settings(BaseSettings):
    # SettingsConfigDict有返回值，使用变量接受，变量名称固定的,必须为model_config
    model_config = SettingsConfigDict(
        # 文件路径
        env_file=ENV_FILE,
        # 编码方式
        env_file_encoding="utf-8",
        # 配置文件中的属性和类中的属性可以不一致
        extra="ignore"

    )

    # 和配置文件对应属性名称，不区分大小写

    LLM_MODEL: str = None

    llm_api_key: str
    llm_base_url: str

    # 数据库
    database_url: str

    # 商城API
    commerce_api_base_url: str

    # 服务器
    app_host: str
    app_port: int

# 初始化（创建）对象
settings = Settings()

if __name__ == "__main__":
    print(settings.database_url)
    print(settings.app_port)
