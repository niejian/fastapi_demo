# _*_ utf-8 _*_
# @time: 2026/7/2 星期四 
# @author: nj
# @file: sys_dao
# @project: fastapi_demo
import datetime
from typing import List, Optional

from sqlalchemy import func, join, select, and_
from sqlalchemy.orm import Session

from main.base.logger import logger
from main.base.page import Page
from main.sys.models.models import SysPermission, SysRolePermission, SysUser, SysUserRole, SysRole
from main.sys.models.sys_req import CreateUserReq
from main.sys.models.sys_resp import SysPermissionResp, SysRolePermissionResp, SysUserResp, SysUserRolePermissionsResp


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

        # 第一种方法：给返回对象的每个字段赋值
        # user_resp = SysUserResp(
        #     id=user.id,
        #     user_status=user.user_status,
        #     username=user.username,
        #     create_time=user.create_time,
        #     roles=roles
        # )
        # 第2种方法：将 user_resp 转换为 Pydantic Schema
        user_resp = SysUserResp.model_validate(user)

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
    
    def get_user_role_permissions(self, session: Session, user_id: int) -> SysUserRolePermissionsResp:
        role_results = session.execute(select(SysRole.id, SysPermission)
                                       .join(SysRolePermission, SysPermission.id == SysRolePermission.permission_id)
                                       .join(SysUserRole, SysRolePermission.role_id == SysUserRole.role_id)
                                       .join(SysUser, SysUserRole.user_id == SysUser.id)
                                       .where(
                                           and_(
                                               SysUser.id == user_id,
                                               SysRole.role_status == 1,
                                               SysUserRole.user_role_status == 1,
                                               SysPermission.permission_status == 1
                                           )
                                       )
                                )
        results = role_results.all()
        if results is None or len(results) == 0:
            return []
        user_role_permission = SysUserRolePermissionsResp(
            user_id=user_id,
            role_permission_list=[]
        )
        role_permissions_dict = {}
        # 先用字典存储相同role_id的权限列表
        for result in results:
            role_id = result[0]
            permission = result[1]
            if role_id in role_permissions_dict:
                role_permissions_dict[role_id].append(SysPermissionResp.model_validate(permission))
            else:
                role_permissions_dict[role_id] = [SysPermissionResp.model_validate(permission)]
        # 将字典转换为 SysRolePermissionResp 对象并添加到 user_role_permission 中
        for role_permission_dict in role_permissions_dict.items():
            user_role_permission.role_permission_list.append(SysRolePermissionResp(
                role_id=role_permission_dict[0],
                permission_list=role_permission_dict[1]
            ))
        # user_role_permission.role_permission_list.append(role_permissions_dict)
        
        # for role_id, permissions in role_permissions_dict.items():
        #     if role_id not in [role_permission.role_id for role_permission in user_role_permission.role_permission_list]:
        #         user_role_permission.role_permission_list.append(SysRolePermissionResp(
        #             role_id=role_id,
        #             permission_list=[SysPermissionResp.model_validate(permission)]
        #         ))
        #     else:
        #         for role_permission in user_role_permission.role_permission_list:
        #             if role_permission.role_id == role_id:
        #                 role_permission.permission_list.append(SysPermissionResp.model_validate(permission))
        #                 break

            # 检查是否已经存在该角色
            # for role_permission in user_role_permission.role_permission_list:
            #     if role_permission.role_id == role_id:
            #         role_permission.permission_list.append(SysPermissionResp.model_validate(permission))
            #         break
            #     else:
            #         role_permission.role_permission_list.append(SysRolePermissionResp(
            #             role_id=role_id,
            #             permission_list=[SysPermissionResp.model_validate(permission)]
            #         ))

        # user_role_permission = SysUserRolePermissionsResp(
        #     user_id=user_id,
        #     role_permission_list=[SysRolePermissionResp(
        #         role_id=role[0],
        #         permission_list=[SysPermissionResp.model_validate(role[1])] # 可以有部分字段缺失
        #     ) for role in role_permissions]
        # )
        # 
        logger.info(f"获取用户角色权限成功: {user_role_permission}")
        return user_role_permission


        
        
        


