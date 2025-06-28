from typing import Generic, TypeVar, Literal, Optional
from pydantic import BaseModel, Field

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    success: Literal[True] = Field(default=True, description="Always True")
    data: Optional[T] = Field(default=None, description="Payload data")
