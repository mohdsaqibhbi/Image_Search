import sys

from fastapi import Request, status
from fastapi.responses import JSONResponse
from globals import log
from starlette.middleware.base import BaseHTTPMiddleware


class CatchRuntimeErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            log.error_print_tb(f"Internal Server Error: {exc}")
            line_no = sys.exc_info()[2].tb_lineno
            err = f"Error : {sys.exc_info()[0]}. {sys.exc_info()[1]}, line: {line_no}"
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": f"Internal Server Error: {err}"},
            )
