from typing import  Union, Literal
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from app.schemas.base_schema import BaseSchema

class ErrorDetail(BaseSchema):
    message: str = Field(..., description="Detailed error message")
    code: int = Field(..., description="HTTP status code of the error")
    details: Union[dict, list] | None = Field(
        default=None,
        description="Additional error details, can be dict or list"
    )

class ErrorResponse(BaseSchema):
    success: Literal[False] = Field(default=False, description="Always false for error responses")
    error: ErrorDetail = Field(..., description="Detailed error information")

    @classmethod
    def json_response(
        cls,
        message: str,
        code: int,
        details: Union[dict, list] | None = None
    ) -> JSONResponse:
        return JSONResponse(
            status_code=code,
            content=cls(
                error=ErrorDetail(message=message, code=code, details=details)
            ).model_dump()
        )

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": {
                    "message": "Invalid data",
                    "code": 400,
                    "details": {"field": "script"}
                }
            }
        }
