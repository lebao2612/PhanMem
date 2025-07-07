from typing import Any, Callable
from functools import wraps
import httpx
import asyncio


class HandledException(Exception):
    def __init__(self, message: str, code: int = 400, details: Any = None):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(message)


def handle_exc(message_prefix: str = ""):
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except PermissionError as e:
                raise HandledException(f"{message_prefix}Permission denied: {e}", 403)
            except (FileNotFoundError, IsADirectoryError, NotADirectoryError) as e:
                raise HandledException(f"{message_prefix}File or directory error: {e}", 400)
            except (IOError, OSError) as e:
                raise HandledException(f"{message_prefix}I/O error: {e}", 500)
            except (httpx.RequestError, ConnectionError, TimeoutError) as e:
                raise HandledException(f"{message_prefix}Network error: {e}", 503)
            except (ValueError, TypeError, AttributeError, KeyError, IndexError) as e:
                raise HandledException(f"{message_prefix}Invalid input: {e}", 400)
            except (ZeroDivisionError, ArithmeticError, OverflowError) as e:
                raise HandledException(f"{message_prefix}Math error: {e}", 400)
            except RuntimeError as e:
                raise HandledException(f"{message_prefix}Runtime error: {e}", 500)
            except asyncio.TimeoutError as e:
                raise HandledException(f"{message_prefix}Async timeout: {e}", 504)
            except Exception as e:
                raise HandledException(f"{message_prefix}Unexpected error: {e}", 500)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except PermissionError as e:
                raise HandledException(f"{message_prefix}Permission denied: {e}", 403)
            except (FileNotFoundError, IsADirectoryError, NotADirectoryError) as e:
                raise HandledException(f"{message_prefix}File or directory error: {e}", 400)
            except (IOError, OSError) as e:
                raise HandledException(f"{message_prefix}I/O error: {e}", 500)
            except (httpx.RequestError, ConnectionError, TimeoutError) as e:
                raise HandledException(f"{message_prefix}Network error: {e}", 503)
            except (ValueError, TypeError, AttributeError, KeyError, IndexError) as e:
                raise HandledException(f"{message_prefix}Invalid input: {e}", 400)
            except (ZeroDivisionError, ArithmeticError, OverflowError) as e:
                raise HandledException(f"{message_prefix}Math error: {e}", 400)
            except RuntimeError as e:
                raise HandledException(f"{message_prefix}Runtime error: {e}", 500)
            except Exception as e:
                raise HandledException(f"{message_prefix}Unexpected error: {e}", 500)

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator
