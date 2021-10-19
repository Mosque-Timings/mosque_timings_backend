from datetime import date, datetime, time
from typing import List, Optional

from pydantic import BaseModel


class MosqueTimings(BaseModel):
    location: str
    name: str
    updated: datetime
    fajr: time
    duhr: time
    asr: time
    maghrib: time
    isha: time
    friday: time

    class Config:
        orm_mode: True
