"""
@Author:叶枫
@Time:2026/9/8
@Desc: 主入口
"""
import uvicorn

from project.config.config import settings
from project.utils.database import init_db_engine

if __name__ == "__main__":
    init_db_engine()
    uvicorn.run(
        "project.api.app:app",
        host=settings.app_host,
        port=settings.app_port,

    )
