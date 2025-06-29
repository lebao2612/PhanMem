from typing import Optional, Union, Literal
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

class ErrorDetail(BaseModel):
    message: str = Field(..., description="Detailed error message")
    code: int = Field(..., description="HTTP status code of the error")
    details: Optional[Union[dict, list]] = Field(
        default=None,
        description="Additional error details, can be dict or list"
    )

class ErrorResponse(BaseModel):
    success: Literal[False] = Field(default=False, description="Always false for error responses")
    error: ErrorDetail = Field(..., description="Detailed error information")

    @classmethod
    def json_response(
        cls,
        message: str,
        code: int,
        details: Optional[Union[dict, list]] = None
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
