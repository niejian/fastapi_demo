# _*_ utf-8 _*_
# @time: 2026/7/2 星期四 
# @author: nj
# @file: sys_routes
# @project: fastapi_demo
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from main.base.base_dao import get_db
from main.base.base_resp import BaseResp
from main.sys.models.sys_req import CreateUserReq
from main.sys.service.sys_service import SysService
from main.base.logger import logger

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

sys_service = SysService()


@router.get("/user/{user_id}", response_model=BaseResp)
def get_user(user_id: int, db: Session = Depends(get_db)):
    result = sys_service.get_user(db, user_id)
    if result:
        return BaseResp.success(data=result)
    return BaseResp.fail(-1, "获取用户信息失败")

@router.get("/user/create/{user_name}/{user_password}", response_model=BaseResp)
def create_user(user_name: str, user_password: str, db: Session = Depends(get_db)):
    if user_name == '' or user_name is None:
        return BaseResp.fail(-1, "用户名不能为空")
    if user_password == '' or user_password is None:
        return BaseResp.fail(-1, "密码不能为空")
    # CreateUserReq = {
    #     "username": user_name,
    #     "password": user_password
    # }
    create_user_req = CreateUserReq(
        username=user_name,
        password=user_password
    )
    user_id = sys_service.create_user(db, create_user_req)
    if user_id and user_id > 0:
        return BaseResp.success(data={"id": user_id})
    return BaseResp.fail(-1, "创建用户失败")

@router.get("/user/permissions/{user_id}/{page_no}/{size}", response_model=BaseResp)
def get_permissions_page(user_id: int, page_no: int, size: int, db: Session = Depends(get_db)):
    page = sys_service.get_permissions_page(db, user_id, page_no, size)
    if page:
        return BaseResp.success(data=page)
    return BaseResp.fail(-1, "获取权限列表失败")

@router.get("/user/role_permissions/{user_id}", response_model=BaseResp)
def get_user_role_permissions(user_id: int, db: Session = Depends(get_db)):
    try:
        result = sys_service.get_user_role_permissions(db, user_id)
        return BaseResp.success(data=result)
    except Exception as e:
        logger.error(f"获取用户角色权限列表异常：{e}")
        return BaseResp.fail(-1, "获取用户角色权限列表失败")



