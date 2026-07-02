import datetime
from typing import List

from pydantic import ConfigDict

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
    roles: List[SysRoleResp] = None
    create_time: datetime.datetime
    # model_config = ConfigDict(from_attributes=True)


class SysUserRoleResp(CamelCaseModel):
    id: int
    user_id: int
    role_id: int
    user_role_status: int
    # model_config = ConfigDict(from_attributes=True)
