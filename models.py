from datetime import date, datetime
from sqlalchemy import Boolean, Float, Column, ForeignKey, Integer, String, DateTime, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.schema import PrimaryKeyConstraint

from database import Base


class MosqueTimings(Base):
    __tablename__ = "mosque_timings"

    location = Column(String, primary_key=True)
    name = Column(String)
    updated = Column(DateTime)
    fajr = Column(Time)
    duhr = Column(Time)
    asr = Column(Time)
    maghrib = Column(Time)
    isha = Column(Time)
    friday = Column(Time)

class UserLocation(Base):
    __tablename__ = "user_locations"
    __table_args__ = (
        PrimaryKeyConstraint('token', 'location'),
    )
    token = Column(String)
    location = Column(String, ForeignKey('mosque_timings.location'))


# class UserMosques(Base):
#     pass
