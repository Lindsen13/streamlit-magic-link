import uuid
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class User(BaseModel):
    """Class for User model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: Optional[str] = None
    is_verified: Optional[bool] = False
    is_payed_user: Optional[bool] = False
    additional_data: Optional[str] = None

class MagicLink(BaseModel):
    """Class for Magic Link model"""
    token: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    is_used: bool = False
    expiration_time: datetime = Field(default_factory=lambda: datetime.now() + timedelta(minutes=15))
