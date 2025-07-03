from pydantic import BaseModel

class BaseDTO(BaseModel):
    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
    }