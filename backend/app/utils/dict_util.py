import re
from typing import Any

class DictUtil:
    @staticmethod
    def camel_to_snake(name: str) -> str:
        """Chuyển tên từ camelCase sang snake_case"""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    @staticmethod
    def snake_to_camel(name: str) -> str:
        """Chuyển tên từ snake_case sang camelCase"""
        parts = name.split('_')
        return parts[0] + ''.join(x.title() for x in parts[1:])

    @staticmethod
    def normalize_keys(obj: Any) -> Any:
        """Chuyển tất cả key của dict từ camelCase sang snake_case (đệ quy)"""
        if isinstance(obj, dict):
            return {
                DictUtil.camel_to_snake(k): DictUtil.normalize_keys(v)
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [DictUtil.normalize_keys(i) for i in obj]
        else:
            return obj

    @staticmethod
    def denormalize_keys(obj: Any) -> Any:
        """Chuyển tất cả key của dict từ snake_case sang camelCase (đệ quy)"""
        if isinstance(obj, dict):
            return {
                DictUtil.snake_to_camel(k): DictUtil.denormalize_keys(v)
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [DictUtil.denormalize_keys(i) for i in obj]
        else:
            return obj