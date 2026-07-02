# _*_ utf-8 _*_
# @time: 2026/7/2 星期四 
# @author: nj
# @file: sys_routes
# @project: fastapi_demo
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from main.base.base_dao import get_db
from main.base.base_resp import BaseResp
from main.sys.dao.sys_dao import SysDao
from main.sys.models.sys_resp import SysUserResp

router = APIRouter(
    prefix="/sys",
    tags=["sys"],
    responses={404: {"description": "Not found"}},
    # 添加了以下参数，则该路由组下的所有路由都会添加该参数
    # dependencies=[Depends(get_query_token)],
    # 添加了以下参数，则该路由组下的所有路由都会添加该参数
    # responses={418: {"description": "I'm a teapot"}},
    # 添加了以下参数，则该路由组下的所有路由都会添加该参数
)

sysDao = SysDao()


@router.get("/user/{user_id}", response_model=BaseResp)
def get_user(user_id: int, db: Session = Depends(get_db)):
    result = sysDao.get_user(db, user_id)
    if result:
        return BaseResp.success(data=result)
    return BaseResp.fail(-1, "获取用户信息失败")


