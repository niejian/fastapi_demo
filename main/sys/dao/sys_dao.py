# _*_ utf-8 _*_
# @time: 2026/7/2 星期四 
# @author: nj
# @file: sys_dao
# @project: fastapi_demo
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from main.base.logger import logger
from main.sys.models.models import SysUser, SysUserRole, SysRole
from main.sys.models.sys_resp import SysUserResp, SysRoleResp, SysUserRoleResp


class SysDao:

    def get_user(self, db: Session, user_id: int) -> Optional[SysUserResp]:
        result = db.execute(select(SysUser).where(SysUser.id == user_id, SysUser.user_status == 1))
        user = result.scalar_one_or_none()
        if user is None:
            return None
        logger.info(f"获取到用户信息: {user} --userId:{user_id}")
        # 连表查询，获取用户角色
        role_results = db.execute(select(SysRole)
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
