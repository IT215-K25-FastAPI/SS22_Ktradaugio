from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.database import init_db
from app.routers import auth, account, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="TrustBank Digital API", lifespan=lifespan)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "ERROR", "detail": str(exc.detail)},
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "VALIDATION_ERROR", "detail": "Dữ liệu đầu vào sai định dạng"},
    )


@app.exception_handler(Exception)
def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_SERVER_ERROR", "detail": "Đã xảy ra lỗi hệ thống không xác định"},
    )


app.include_router(auth.router)
app.include_router(account.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "TrustBank Digital API đang hoạt động."}
