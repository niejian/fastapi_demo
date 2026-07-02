# _*_ utf-8 _*_
# @time: 2026/6/18 星期四 
# @author: nj
# @file: items
# @project: fastapi_demo
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
    # 添加了以下参数，则该路由组下的所有路由都会添加该参数
    # dependencies=[Depends(get_query_token)],
    # 添加了以下参数，则该路由组下的所有路由都会添加该参数
    # responses={418: {"description": "I'm a teapot"}},
    # 添加了以下参数，则该路由组下的所有路由都会添加该参数
)


@router.get("/")
def list_items():
    return [{"name": "Foo"}, {"name": "Bar"}, {"name": "Baz"}, {"name": "Qux"}]

@router.get("/{item_id}")
def read_item(item_id: int, name: str = None):
    return {"item_id": item_id}