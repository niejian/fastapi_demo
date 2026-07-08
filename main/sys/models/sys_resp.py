import datetime
from typing import List

from main.base.camel_case_model import CamelCaseModel


class SysRoleResp(CamelCaseModel):
    id: int
    role_code: str
    role_name: str
    role_status: int
    role_start_time: datetime.datetime
    role_end_time: datetime.datetime
    create_time: datetime.datetime
    # model_config = ConfigDict(from_attributes=True)


class SysUserResp(CamelCaseModel):
    id: int
    username: str
    user_status: int
    roles: List[SysRoleResp] = []
    create_time: datetime.datetime
    # model_config = ConfigDict(from_attributes=True)


class SysUserRoleResp(CamelCaseModel):
    id: int
    user_id: int
    role_id: int
    user_role_status: int
    # model_config = ConfigDict(from_attributes=True)

class SysPermissionResp(CamelCaseModel):
    id: int
    permission_code: str
    permission_name: str
    permission_type: int
    permission_status: int
    permission_start_time: datetime.datetime
    permission_end_time: datetime.datetime
    permission_sort: int = 100
    permission_icon: str = "" # 非必填
    permission_url: str = "" # 非必填

"""
    角色权限
"""
class SysRolePermissionResp(CamelCaseModel):
    role_id: int
    permission_list: List[SysPermissionResp] = []

"""
    用户角色权限
"""
class SysUserRolePermissionsResp(CamelCaseModel):
    user_id: int
    role_permission_list: List[SysRolePermissionResp] = []
