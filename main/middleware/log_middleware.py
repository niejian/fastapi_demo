# _*_ utf-8 _*_
# @time: 2026/7/2 星期四 
# @author: nj
# @file: log_middleware
# @project: fastapi_demo
import time
from urllib.request import Request

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from main.base.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        try:
            # 记录请求开始时间
            start_time = time.time()

            # 提取请求信息
            client_ip = request.client.host
            method = request.method
            url = request.url.path

            # 记录请求日志
            logger.info(f"Request: {method} {url} from {client_ip}")

            # 处理请求
            response = await call_next(request)

            # 计算耗时
            process_time = time.time() - start_time

            # 记录响应日志
            logger.info(
                f"Response: {method} {url} "
                f"status={response.status_code} "
                f"time={process_time:.3f}s "
                f"from {client_ip}"
            )

            # 在响应头中添加处理时间（可选）
            response.headers["X-Process-Time"] = str(process_time)
            return response
        except Exception as exc:
            # 记录异常日志（可复用上面的 logger）
            logger.exception(f"Middleware caught exception: {exc} - Path: {request.url.path}")
            # 返回一个友好的错误响应
            return JSONResponse(
                status_code=500,
                content={"code": 500, "message": "服务器内部错误", "data": None}
            )
