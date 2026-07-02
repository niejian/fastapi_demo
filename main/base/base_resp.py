# _*_ utf-8 _*_
# @time: 2026/7/1 星期三 
# @author: nj
# @file: base_resp
# @project: fastapi_demo
from typing import TypeVar
from pydantic import ConfigDict

from main.base.camel_case_model import CamelCaseModel

T = TypeVar('T')


class BaseResp(CamelCaseModel):
    code: int
    msg: str
    data: T = None

    # model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def success(data: T = None) -> 'BaseResp':
        return BaseResp(code=200, msg="success", data=data)

    @staticmethod
    def fail(code: int, msg: str) -> 'BaseResp':
        return BaseResp(code=code, msg=msg, data=None)


