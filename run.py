#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2026-07-06 08:58:30
# @Author  : xxyyzz
# @Link    : debug
# @Version : 1.0.0
# desc: 本地main方法启动,debug

from fastapi import FastAPI
import uvicorn

from main.base.base_config import base_config
from main.middleware.log_middleware import LoggingMiddleware
from main.sys.routes import sys_routes


app = FastAPI()
# 统一注册所有路由
# app.include_router(user_route.router)
app.include_router(sys_routes.router)
# 添加日志组件
app.add_middleware(LoggingMiddleware)


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/config")
async def show_config():
    return {
        "db_host": base_config.db_host,
        "db_user": base_config.db_user,
        "db_name": base_config.db_name,
    }

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)

