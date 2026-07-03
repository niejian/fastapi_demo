import datetime

from pydantic import BaseModel


class CreateUserReq(BaseModel):
    username: str=None
    password: str=None
    userStatus: int=1
    userEndTime: datetime.datetime=None
    userStartTime: datetime.datetime=datetime.datetime.now()
    createTime: datetime.datetime=datetime.datetime.now()
    updateTime: datetime.datetime=datetime.datetime.now()
    createCode: str="admin"
    updateCode: str="admin"


