import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException, RequestValidationError
from app.exceptions import HandledException

# Cấu hình logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def register_error_handlers(app: FastAPI):
    @app.exception_handler(HandledException)
    async def handle_service_error(request: Request, exc: HandledException):
        return JSONResponse(
            status_code=exc.code,
            content={"error": exc.message, "code": exc.code}
        )

    @app.exception_handler(FastAPIHTTPException)
    async def handle_http_exception(request: Request, exc: FastAPIHTTPException):
        logger.warning(f"HTTPException: {exc.detail} (status: {exc.status_code})")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "code": exc.status_code}
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "Dữ liệu không hợp lệ hoặc thiếu trường bắt buộc",
                "code": 422,
                "details": exc.errors(),
            },
        )

    @app.exception_handler(404)
    async def handle_404(request: Request, exc):
        return JSONResponse(
            status_code=404,
            content={"error": "Tài nguyên không tồn tại hoặc đường dẫn sai", "code": 404}
        )

    @app.exception_handler(405)
    async def handle_405(request: Request, exc):
        return JSONResponse(
            status_code=405,
            content={"error": "Phương thức HTTP không được hỗ trợ", "code": 405}
        )

    @app.exception_handler(Exception)
    async def handle_exception(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "Lỗi hệ thống, vui lòng thử lại sau", "code": 500}
        )
