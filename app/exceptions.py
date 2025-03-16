from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from .utils import error_response

async def custom_exception_handler(request: Request, exc: Exception):
    """
    Custom exception handler to format API error responses.
    """
    if isinstance(exc, StarletteHTTPException):
        return error_response(message=exc.detail, status_code=exc.status_code)
    
    return error_response(message="An unexpected error occurred.", status_code=500)
