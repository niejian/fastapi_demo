import datetime

from pydantic import ConfigDict
from sqlalchemy import DateTime, Integer, String, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from main.base.base_dao import Base


class SysRole(Base):
    __tablename__ = 'sys_role'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    role_desc: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    role_code: Mapped[str] = mapped_column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    role_status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    role_start_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    role_end_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    create_code: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False)
    update_code: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False)
    model_config = ConfigDict(from_attributes=True)  # 转化为json



class SysUser(Base):
    __tablename__ = 'sys_user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    password: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    user_status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    user_start_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    user_end_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    create_code: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False)
    update_code: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False)


class SysUserPermission(Base):
    __tablename__ = 'sys_user_permission'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    permission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_permission_status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    create_code: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False)
    update_code: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False)


class SysUserRole(Base):
    __tablename__ = 'sys_user_role'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_role_status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    create_code: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False)
    update_code: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False)
