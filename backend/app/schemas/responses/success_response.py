from typing import Generic, TypeVar, Literal
from pydantic import Field
from app.schemas.base_schema import BaseSchema
T = TypeVar("T")

class SuccessResponse(BaseSchema, Generic[T]):
    success: Literal[True] = Field(default=True, description="Always True")
    data: T | None = Field(default=None, description="Payload data")
