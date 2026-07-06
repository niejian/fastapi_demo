# _*_ utf-8 _*_
# @time: 2026/7/2 星期四 
# @author: nj
# @file: sys_dao
# @project: fastapi_demo
import datetime
from typing import Optional

from sqlalchemy import func, join, select, and_
from sqlalchemy.orm import Session

from main.base.logger import logger
from main.base.page import Page
from main.sys.models.models import SysPermission, SysRolePermission, SysUser, SysUserPermission, SysUserRole, SysRole
from main.sys.models.sys_req import CreateUserReq
from main.sys.models.sys_resp import SysPermissionResp, SysUserResp, SysRoleResp, SysUserRoleResp


class SysDao:

    def get_user(self, session: Session, user_id: int) -> Optional[SysUserResp]:
        result = session.execute(select(SysUser).where(SysUser.id == user_id, SysUser.user_status == 1))
        user = result.scalar_one_or_none()
        if user is None:
            return None
        logger.info(f"获取到用户信息: {user} --userId:{user_id}")
        # 连表查询，获取用户角色
        role_results = session.execute(select(SysRole)
        .join(SysUserRole, SysRole.id == SysUserRole.role_id)
        .where(
            and_(
                SysUserRole.user_id == user_id,
                SysRole.role_status == 1,
                SysUserRole.user_role_status == 1)))
        roles = role_results.scalars().all()
        if roles is None or len(roles) == 0:
            user.roles = []
            return user
        logger.info(f"获取到角色信息: {roles=}")

        # 3. 将每个角色 ORM 转换为 Pydantic Schema
        # roles_resp = [SysRoleResp.model_validate(role) for role in roles] if roles else []

        # 给返回对象的每个字段赋值
        user_resp = SysUserResp(
            id=user.id,
            user_status=user.user_status,
            username=user.username,
            create_time=user.create_time,
            roles=roles
        )

        return user_resp
    
    # 创建用户

    def create_user(self, session: Session, user: CreateUserReq) -> int:
        sys_user = SysUser(
            username=user.username,
            password=user.password,
            user_status=user.userStatus,
            user_start_time=user.userStartTime,
            user_end_time=user.userEndTime,
            create_code=user.createCode,
            update_code=user.updateCode,
            create_time=datetime.datetime.now(),
            update_time=datetime.datetime.now(),
        )
        session.add(sys_user)
        # 自己调用了 session.commit()，那么数据已被提前持久化，
        # 外层的回滚无法撤销。确保所有数据修改操作只有最外层事务装饰器执行提交，内部 DAO 只做 add、delete、flush，
        # session.commit()
        session.flush()  # 将对象持久化到数据库，但不提交事务，确保 sys_user.id 可用
        logger.info(f"创建用户成功: {sys_user}")
        return sys_user.id
    
    def get_permissions_page(self, session: Session, user_id: int,
                            page_no: int=1, size: int=10) -> Page[SysPermissionResp]:
        offset = (page_no - 1) * size
        result = session.execute(select(SysPermission)
        .join(SysRolePermission, SysPermission.id == SysRolePermission.permission_id)
        .join(SysUserRole, SysRolePermission.role_id == SysUserRole.role_id and SysUserRole.user_id == user_id)
        .where(
            and_(
                SysUserRole.user_id == user_id,
                SysPermission.permission_status == 1,
                SysUserRole.user_role_status == 1)).offset(offset).limit(size))
        permissions = result.scalars().all()
        if permissions is None or len(permissions) == 0:
            return Page(items=permissions, total=0, page_no=page_no, size=size)
        #  获取总数
        total_result = select(func.count()).select_from(SysPermission).join(
            SysRolePermission, SysPermission.id == SysRolePermission.permission_id).join(
                SysUserRole, SysRolePermission.role_id == SysUserRole.role_id and SysUserRole.user_id == user_id
                ).where(
            and_(
                SysUserRole.user_id == user_id,
                SysPermission.permission_status == 1,
                SysUserRole.user_role_status == 1))
        total = session.execute(total_result).scalar_one()
        # logger.info(f"获取权限列表成功: {permissions}")

        permissions_items = [SysPermissionResp.model_validate(permission) for permission in permissions] if permissions else []
        
        page = Page(items=permissions_items, total=total, page_no=page_no, size=size)
        return page
        
        


