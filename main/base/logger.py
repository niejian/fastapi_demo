# _*_ utf-8 _*_
# @time: 2026/7/2 星期四 
# @author: nj
# @file: logger
# @project: fastapi_demo
import sys
from pathlib import Path
from loguru import logger
# 1. 定义日志文件存放路径
# 获取项目根路径


def get_project_root() -> Path:
    """从当前文件向上查找，直到找到 requirements.txt 所在的目录即为项目根"""
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "requirements.txt").exists():
            return parent
    return current


LOG_PATH = get_project_root() / "logs"
LOG_PATH.mkdir(exist_ok=True)

# 2. 移除 loguru 默认的配置（重要！）
logger.remove()

# 3. 配置控制台输出（带颜色，更美观）
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "<level>{message}</level>",
    level="INFO",
    colorize=True,
)

# 4. 配置文件输出（持久化存储，支持轮转和保留策略）
log_file = LOG_PATH / "app_{time:YYYY-MM-DD}.log"
logger.add(
    log_file,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    level="DEBUG",           # 文件里可以记录更详细的 DEBUG 信息
    rotation="00:00",        # 每天零点创建一个新文件
    retention="7 days",      # 只保留最近 7 天的日志
    compression="zip",       # 压缩旧日志以节省空间
)




# 导出 logger 实例供其他模块使用
__all__ = ["logger"]

