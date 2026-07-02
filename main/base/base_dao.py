# _*_ utf-8 _*_
# @time: 2026/7/2 星期四 
# @author: nj
# @file: base_dao
# @project: fastapi_demo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

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
