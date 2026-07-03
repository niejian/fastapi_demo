
import datetime
from hashlib import md5
import hashlib

from main.base.base_dao import transactional
from main.sys.dao.sys_dao import SysDao
from main.sys.models.sys_req import CreateUserReq

class SysService:
    def __init__(self):
        self.sys_dao = SysDao()
    def get_user(self, db, user_id: int):
        return self.sys_dao.get_user(db, user_id)
    
    @transactional
    def create_user(self, db, user: CreateUserReq) -> int:
        user.password = hashlib.md5((user.password + "/qq123123").encode("utf-8")).hexdigest()
        user.userStatus = 1
        user.userStartTime = datetime.datetime.now()
        user.userEndTime = datetime.datetime.now() + datetime.timedelta(days=3650)
        id = self.sys_dao.create_user(db, user)
        return id
    