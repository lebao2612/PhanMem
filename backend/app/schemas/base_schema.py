from pydantic import BaseModel
from app.utils import DictUtil

class BaseSchema(BaseModel):
    model_config = {
        "alias_generator": DictUtil.snake_to_camel,
        "validate_by_name": True,
    }