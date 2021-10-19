from datetime import date, datetime, time
from typing import List, Optional

from pydantic import BaseModel


class UserLocation(BaseModel):
    token: str
    location: str

    class Config:
        orm_mode: True
