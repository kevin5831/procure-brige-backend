from fastapi.responses import JSONResponse
from fastapi import HTTPException

def success_response(message: str = "", data: dict = None, status_code: int = 200):
    """
    Returns a standardized success response.
    """
    return JSONResponse(
        content={
            "status": True,
            "message": message,
            "data": data
        },
        status_code=status_code
    )

def error_response(message: str = "An error occurred", status_code: int = 400, errors: dict = None):
    """
    Returns a standardized error response.
    """
    return JSONResponse(
        content={
            "status": False,
            "message": message,
            "data": errors
        },
        status_code=status_code
    )

