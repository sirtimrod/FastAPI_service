import re
import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr
from pydantic import validator


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModels(BaseModel):
    class Config:
        """tells pydentic to convert even non dict odj to json"""

        orm_mode = True


class ShowUser(TunedModels):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr

    @validator("name")
    def validate_name(cls, value):
        pass

    @validator("surname")
    def validate_surname(cls, value):
        pass
