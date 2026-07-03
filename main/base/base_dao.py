# _*_ utf-8 _*_
# @time: 2026/7/2 星期四 
# @author: nj
# @file: base_dao
# @project: fastapi_demo
import functools

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from main.base.logger import logger

# class BaseDataSource:
#     data_base_url: str
#     engine = None
#     session = None
#
#     def __init__(self, data_base_url: str):
#         self.data_base_url = data_base_url
#         self.engine = create_engine(self.data_base_url, echo=True, future=True)
#         self.session = sessionmaker(self.engine, class_=Session, expire_on_commit=False)


# -------------------- 数据库配置 --------------------
# 请替换为你的 MySQL 连接信息
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/rabac_demo"

# engine = create_async_engine(DATABASE_URL, echo=True, future=True)
engine = create_engine(DATABASE_URL, echo=True, future=True)
# AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


# FastAPI 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def transactional(func):
    """
    事务装饰器，要求被装饰函数的第一个参数为 Session 对象，
    或者在 kwargs 中包含 'session' 键。
    发生异常时回滚，否则提交。
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, Session):
                session = arg
                break
         # 2. 若未获取到，检查第一个位置参数是否为 Session 实例
        if session is None and args :
            session = args[0]
        # 3. 若仍未获取到，抛出异常
        if session is None:
            logger.error("数据库未初始化，未获取到session对象")
            raise ValueError("No SQLAlchemy Session found in arguments.")

        try:
            # 默认 autocommit=False，在第一次执行 SQL（如 add 或查询）时自动开始事务，无需手动 begin()。
            # session.begin()  # 开始事务
            logger.info(f"开始事务: {func.__name__}")
            result = func(*args, **kwargs)
            session.commit()
            logger.info(f"提交事务: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"数据库事务异常：{e}")
            logger.error(f"回滚事务: {func.__name__}")
            session.rollback()
            raise e
        finally:
            session.close()
    return wrapper