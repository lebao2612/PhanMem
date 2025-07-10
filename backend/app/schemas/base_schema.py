from pydantic import BaseModel
# from app.utils import DictUtil
# from pydantic.alias_generators import to_camel

class BaseSchema(BaseModel):
    model_config = {
        "populate_by_name": True,  # cho phép khởi tạo bằng snake_case trong code
    }