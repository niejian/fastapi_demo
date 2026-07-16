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
* 将项目需要的包整合到`requirements.txt`
```shell
 pip freeze > requirements.txt
```
* 从`requirements.txt`中安装包
```shell
pip install -r requirements.txt
```
* `uvicorn run:app ` 命令
1. `uvicorn（命令本身）`
这是 Uvicorn ASGI 服务器的入口命令。它负责启动一个高性能的异步服务器进程，监听网络请求，并将请求转交给你的 Python 代码处理。

2. `run（文件/模块名）`
这部分指定了包含应用代码的 Python 文件。它代表当前目录下的 run.py 文件。

关键规则：不要写 .py 后缀。Uvicorn 采用 Python 的模块导入语法，所以写 run 而不是 run.py。

路径规则拓展：

如果文件在子文件夹中，用点号分隔，例如 src.main:app 代表 src/main.py 文件。

本质上是让 Uvicorn 去执行 from run import app。

3. `:`（分隔符）
这是一个固定的分隔符，用来隔开`文件模块`和`变量名`。它的作用就是告诉 Uvicorn：“前面的部分是文件路径，后面的部分是文件中具体的变量名”。

4. app（应用实例变量名）
这部分指定了在 `run.py` 文件中，`FastAPI` 应用实例的具体变量名称。
<b>在 run.py 文件中，你必须有一个名为 app 的变量，它是 FastAPI() 类的实例。</b>
Uvicorn 会执行类似于 from run import app 的操作，拿到这个实例后，开始处理请求。