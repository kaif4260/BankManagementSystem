from typing import Generic, Optional, TypeVar, List

from pydantic import BaseModel, Field, EmailStr

T = TypeVar("T")

# Login


class Login(BaseModel):
    username: str
    password: str

# Register

class Register(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone_number: str

    first_name: str
    last_name: str

class ResponseSchema(BaseModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional [T] = None

# Token

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str