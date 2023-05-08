from typing import Dict, Optional, Union

from pydantic import BaseModel


class HTTP400BadRequestContent(BaseModel):
    code: str = "HTTP_400"
    msg: str = "Bad request"


class HTTP401UnauthorizedContent(BaseModel):
    code: str = "HTTP_401"
    msg: str = "Not authenticated"


class HTTP403ForbiddenContent(BaseModel):
    code: str = "HTTP_403"
    msg: str = "Not enough privileges"


class HTTP404NotFoundContent(BaseModel):
    code: str = "HTTP_404"
    msg: str = "Resource not found"


class HTTP409ConflictContent(BaseModel):
    code: str = "HTTP_404"
    msg: str = "Duplicate resource"


# HTTP Errors Response Schemas
# ############################
class HTTP400BadRequestResponse(BaseModel):
    content: Optional[HTTP400BadRequestContent] = HTTP400BadRequestContent()
    headers: Optional[Union[Dict[str, str], None]] = None


class HTTP401UnauthorizedResponse(BaseModel):
    content: Optional[HTTP401UnauthorizedContent] = HTTP401UnauthorizedContent()
    headers: Optional[Union[Dict[str, str], None]] = {"WWW-Authenticate": "Bearer"}


class HTTP403ForbiddenResponse(BaseModel):
    content: Optional[HTTP403ForbiddenContent] = HTTP403ForbiddenContent()
    headers: Optional[Union[Dict[str, str], None]] = None


class HTTP404NotFoundResponse(BaseModel):
    content: Optional[HTTP404NotFoundContent] = HTTP404NotFoundContent()
    headers: Optional[Union[Dict[str, str], None]] = None


class HTTP409ConflictResponse(BaseModel):
    content: Optional[HTTP409ConflictContent] = HTTP409ConflictContent()
    headers: Optional[Union[Dict[str, str], None]] = None
