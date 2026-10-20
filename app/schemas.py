
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegistrationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    college: str | None = Field(default=None, max_length=150)
    department: str | None = Field(default=None, max_length=150)


class RegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    college: str | None
    department: str | None
    registered_at: datetime
