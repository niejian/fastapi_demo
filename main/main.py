# # _*_ utf-8 _*_
# # @time: 2026/6/18 星期四 
# # @author: nj
# # @file: main
# # @project: fastapi_demo
# import uvicorn
# from fastapi import FastAPI

# from main.middleware.log_middleware import LoggingMiddleware
# from main.sys.routes import sys_routes

# app = FastAPI()
# # 统一注册所有路由
# # app.include_router(user_route.router)
# app.include_router(sys_routes.router)
# # 添加日志组件
# app.add_middleware(LoggingMiddleware)


# @app.get("/")
# def root():
#     return {"message": "Hello World"}

