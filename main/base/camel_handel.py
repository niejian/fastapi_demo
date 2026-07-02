# _*_ utf-8 _*_
# @time: 2026/7/1 星期三 
# @author: nj
# @file: camel_handel 驼峰处理
# @project: fastapi_demo

# 将下划线转换为驼峰
def to_camel(string: str):
    strs = string.split("_")
    return strs[0] + "".join([s.title() for s in strs[1:]])

