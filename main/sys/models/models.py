from typing import Optional
import datetime

from sqlalchemy import DateTime, Integer, String, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class SysAttribute(Base):
    __tablename__ = 'sys_attribute'
    __table_args__ = {'comment': '属性定义表'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    attribute_name: Mapped[str] = mapped_column(String(32, 'utf8mb4_unicode_ci'), nullable=False, comment='属性名称')
    attribute_code: Mapped[str] = mapped_column(String(32, 'utf8mb4_unicode_ci'), nullable=False, comment='属性编码')
    attribute_type: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'STRING'"), comment='属性类型：STRING/INT/BOOLEAN/DATE')
    attribute_status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='状态：1=启用，0=禁用')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    attribute_desc: Mapped[Optional[str]] = mapped_column(String(64, 'utf8mb4_unicode_ci'), comment='属性描述')


class SysPermission(Base):
    __tablename__ = 'sys_permission'
    __table_args__ = {'comment': '权限表, 存储菜单/按钮/接口权限等信息'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    permission_name: Mapped[str] = mapped_column(String(32, 'utf8mb4_unicode_ci'), nullable=False, comment='权限名称')
    permission_desc: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False, comment='权限描述')
    permission_code: Mapped[str] = mapped_column(String(32, 'utf8mb4_unicode_ci'), nullable=False, comment='权限编码')
    permission_type: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='权限类型：1=菜单，2=按钮，3=接口')
    parent_id: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"), comment='父级ID，0表示顶级')
    permission_sort: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"), comment='排序号')
    permission_status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='权限状态：1=启用，0=禁用')
    permission_start_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, comment='生效开始时间')
    permission_end_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, comment='生效结束时间')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间')
    permission_url: Mapped[Optional[str]] = mapped_column(String(128, 'utf8mb4_unicode_ci'), comment='菜单URL或接口路径')
    menu_seq: Mapped[Optional[str]] = mapped_column(String(128, 'utf8mb4_unicode_ci'), comment='菜单序列号；1.123.12')
    permission_icon: Mapped[Optional[str]] = mapped_column(String(64, 'utf8mb4_unicode_ci'), comment='菜单图标')


class SysPermissionAttributeRule(Base):
    __tablename__ = 'sys_permission_attribute_rule'
    __table_args__ = {'comment': '权限属性规则表'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    permission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    attribute_id: Mapped[int] = mapped_column(Integer, nullable=False)
    operator: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False, comment='操作符：EQ/NEQ/GT/GTE/LT/LTE/IN/CONTAINS')
    expected_value: Mapped[str] = mapped_column(String(128, 'utf8mb4_unicode_ci'), nullable=False, comment='期望值')
    rule_status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


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


class SysRoleAttributeRule(Base):
    __tablename__ = 'sys_role_attribute_rule'
    __table_args__ = {'comment': '角色属性规则表'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(Integer, nullable=False)
    attribute_id: Mapped[int] = mapped_column(Integer, nullable=False)
    operator: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False, comment='操作符：EQ/NEQ/GT/GTE/LT/LTE/IN/CONTAINS')
    expected_value: Mapped[str] = mapped_column(String(128, 'utf8mb4_unicode_ci'), nullable=False, comment='期望值')
    rule_status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class SysRolePermission(Base):
    __tablename__ = 'sys_role_permission'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(Integer, nullable=False)
    permission_id: Mapped[int] = mapped_column(Integer, nullable=False)
    role_permission_status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    create_code: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False)
    update_code: Mapped[str] = mapped_column(String(16, 'utf8mb4_unicode_ci'), nullable=False)


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


class SysUserAttribute(Base):
    __tablename__ = 'sys_user_attribute'
    __table_args__ = {'comment': '用户属性值表'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    attribute_id: Mapped[int] = mapped_column(Integer, nullable=False)
    attribute_value: Mapped[str] = mapped_column(String(128, 'utf8mb4_unicode_ci'), nullable=False, comment='属性值')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


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
