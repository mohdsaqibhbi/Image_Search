import sys

import uvicorn
from exceptions.api import APIBaseException
from fastapi import FastAPI
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from globals import (
    APP_NAME,
    api_description,
    api_root_path,
    api_summary,
    api_version,
    log,
)
from middleware.error_handler import CatchRuntimeErrorMiddleware
from routers import core
from schema.api import APIHealthCheckResponse

app = FastAPI(
    root_path=api_root_path,
    title=APP_NAME,
    summary=api_summary,
    description=api_description,
    version=api_version,
)
app.add_middleware(CatchRuntimeErrorMiddleware)
app.include_router(core.router)

log.info_print(f"{APP_NAME} API Started, and is Ready to Serve Requests!")

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    
    endpoint = request.url.path
    log.error_print_tb(
        f"\nValidation Error Occurred in Request Payload for Endpoint: {endpoint} \n",
        custom_dimensions={
            "statusCode": 422,
            "method": request.method,
        },
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )
    
@app.exception_handler(APIBaseException)
async def api_internal_exception_handler(
    request: Request, exc: APIBaseException
) -> JSONResponse:
    
    status_code = exc.status_code
    log.error_print_tb(
        exc.message,
        custom_dimensions={
            "statusCode": status_code,
            "method": request.method,
        },
    )
    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.message},
    )
    
@app.exception_handler(Exception)
async def unknown_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    
    log.error_print_tb(
        "Unknown Error Occurred",
        custom_dimensions={
            "statusCode": 500,
            "method": request.method,
        },
    )
    line_no = sys.exc_info()[2].tb_lineno
    
    err = f"Error : {sys.exc_info()[0]}. {sys.exc_info()[1]}, line: {line_no}"
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Unknown Error Occurred. Error: {err}"},
    )

@app.get(
    "/health",
    summary="API Health Check",
    description="Check API Health, returns 200 if healthy.",
)
async def health_check() -> APIHealthCheckResponse:
    return APIHealthCheckResponse(message=f"{APP_NAME} API is Healthy")


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, workers=1)
