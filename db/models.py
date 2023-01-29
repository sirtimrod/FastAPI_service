import uuid
from sqlalchemy import (
    Column,
    Boolean,
    String,
)
from sqlalchemy.dialects.postgresql import UUID

from .db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid64)
    name = Column(String, nulable=False)
    surname = Column(String, nulable=False)
    email = Column(String, nulable=False, unique=True)
    is_active = Column(Boolean(), default=True)
