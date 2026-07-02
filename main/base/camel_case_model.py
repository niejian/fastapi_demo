# _*_ utf-8 _*_
# @time: 2026/7/1 星期三 
# @author: nj
# @file: camel_case_model
# @project: fastapi_demo
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from main.base.camel_handel import to_camel


class CamelCaseModel(BaseModel):
    model_config = ConfigDict(
        #  1. 生成别名：将 snake_case 转为 camelCase
        alias_generator=to_camel,
        # 2. 允许通过字段名（snake_case）或别名（camelCase）赋值
        populate_by_name=True,
        # 3. 支持从 ORM 对象读取数据（替代旧版的 orm_mode=True）
        from_attributes=True,
        # 时间格式化
        json_encoders={
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

    )
