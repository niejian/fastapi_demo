## 操作记录
### 生成数据库表model

```shell
sqlacodegen mysql+pymysql://root:123456@localhost:3306/rabac_demo --tables sys_permission,sys_attribute,sys_permission_attribute_rule,sys_role_attribute_rule,sys_role_permission,sys_user_attribute,sys_user_permission --outfile .\main\sys\models\models.py 
```
### 使用事务
在`service`层使用装饰器：`@transactional`
### 遇到问题
* 对象字段未初始化
给对象初始化值，否则在创建对象时，字段未初始化，会报错：
```
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
```

* Class 'main.sys.models.sys_req.CreateUserReq' is not mapped

```
session.add()方法要映射数据表，也就是通过sqlacodegen生成的model对象
```
* 使用装饰器`@transactional`，事务没生效
1. 装饰器内部是小不需要使用`session.begin()`,SQLAlchemy 的 Session 默认 autocommit=False，在第一次执行 SQL（如 add 或查询）时自动开始事务，无需手动 begin()。
2. Dao方法，数据增删改后，不需要用 ·session.commit()`, 如果该方法内部自己调用了 session.commit()，那么数据已被提前持久化，外层的回滚无法撤销。确保所有数据修改操作只有最外层事务装饰器执行提交，内部 DAO 只做 add、delete、flush，绝不 commit。

* 使用flush方法，报错'SysUser' object is not iterable
session.flush(sys_user)  # ❌ 错误！flush() 不接受参数

* http接口返回数据表对象处理
```python
# 处理数据表对象
permissions_items = [SysPermissionResp.model_validate(permission) for permission in permissions] if permissions else []

```
* http接口返回对象处理
 **返回对象字段可选，可以赋值默认值。设置的字段必须赋值**
    * 给对象的每个字段赋值
    ```python
    # 第一种方法：给返回对象的每个字段赋值
            user_resp = SysUserResp(
                id=user.id,
                user_status=user.user_status,
                username=user.username,
                create_time=user.create_time,
                roles=roles
            )
    ```
    * 通过`model_validate()`转换为对象
    ```python
        # 第2种方法：将 user_resp 转换为 Pydantic Schema
        user_resp = SysUserResp.model_validate(user)

    ```
* 按照不同的配置启动
确保各个文件跟run.py在同一目录下
```shell
# powershell中
$env:APP_ENV="dev"; fastapi dev run.py
```