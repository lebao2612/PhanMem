import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException, RequestValidationError
from app.exceptions import HandledException
from app.schemas.responses import ErrorResponse

# Cấu hình logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def register_error_handlers(app: FastAPI):
    @app.exception_handler(HandledException)
    async def handle_service_error(request: Request, exc: HandledException):
        return ErrorResponse.json_response(
            message=exc.message,
            code=exc.code,
            details=exc.details
        )

    @app.exception_handler(FastAPIHTTPException)
    async def handle_http_exception(request: Request, exc: FastAPIHTTPException):
        logger.warning(f"HTTPException: {exc.detail} (status: {exc.status_code})")

        if isinstance(exc.detail, dict):
            return ErrorResponse.json_response(
                message=exc.detail.get("message", "Lỗi HTTP"),
                code=exc.status_code,
                details=exc.detail.get("details")
            )

        return ErrorResponse.json_response(
            message=str(exc.detail),
            code=exc.status_code
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        return ErrorResponse.json_response(
            message="Dữ liệu không hợp lệ hoặc thiếu trường bắt buộc",
            code=422,
            details=exc.errors()
        )

    @app.exception_handler(404)
    async def handle_404(request: Request, exc):
        return ErrorResponse.json_response(
            message="Tài nguyên không tồn tại hoặc đường dẫn sai",
            code=404,
            details={"url": str(request.url)}
        )

    @app.exception_handler(405)
    async def handle_405(request: Request, exc):
        return ErrorResponse.json_response(
            message="Phương thức HTTP không được hỗ trợ",
            code=405,
            details={"method": request.method, "url": str(request.url)}
        )

    @app.exception_handler(Exception)
    async def handle_exception(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return ErrorResponse.json_response(
            message="Lỗi hệ thống, vui lòng thử lại sau",
            code=500,
            details={"exception": str(exc)}
        )
