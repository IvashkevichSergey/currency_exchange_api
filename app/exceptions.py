from fastapi import HTTPException
from starlette import status


class ExternalAPIException(HTTPException):
    """Exception that occurred when external currency API do not respond"""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code,
                         detail=f"An exception occurred while processing the request. {detail}")
