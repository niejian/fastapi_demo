
import datetime
from hashlib import md5
import hashlib

from main.base.base_dao import transactional
from main.base.page import Page
from main.sys.dao.sys_dao import SysDao
from main.sys.models.sys_req import CreateUserReq
from main.sys.models.sys_resp import SysPermissionResp
from main.base.logger import logger

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
    
    def get_permissions_page(self, db, user_id: int, page_no: int=1, size: int=10)-> Page[SysPermissionResp]:
        logger.info(f"获取权限列表: user_id={user_id}, page_no={page_no}, size={size}")
        return self.sys_dao.get_permissions_page(db, user_id, page_no, size)
    