from typing import List
from sqlalchemy import schema
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.sql.elements import and_

from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.schema import Column
import models
from schemas import mosque_timings, user_locations


def get_mosque_timings(db: Session, location: List[str]):
    return db.query(models.MosqueTimings).filter(models.MosqueTimings.location == location).first()


def get_all(db: Session):
    return db.query(models.MosqueTimings).all()


def add_mosque_timings(db: Session, mosque_timings: mosque_timings.MosqueTimings):
    db_mosque_timings = models.MosqueTimings(**mosque_timings.dict())
    db.add(db_mosque_timings)
    db.commit()
    db.refresh(db_mosque_timings)
    return db_mosque_timings


def update_mosqueTimings(db: Session, mosque_timings: models.MosqueTimings, updates: mosque_timings.MosqueTimings):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(mosque_timings, key, value)
    db.commit()

def add_location(db: Session, user_location: user_locations.UserLocation):
    db_user_location = models.UserLocation(**user_location.dict())
    db.add(db_user_location)
    db.commit()
    db.refresh(db_user_location)
    return db_user_location


def get_user_locaitons(token: str, db: Session):
    return db.query(models.MosqueTimings).join(models.UserLocation).filter(models.UserLocation.token == token).all()

def deleteMosqueTimings(db: Session):
    all_mosque_timings = db.query(models.MosqueTimings).first()
    db.delete(all_mosque_timings)
    db.commit()

def deleteUserLocation(db: Session, user_location: user_locations.UserLocation):
    user_location = db.query(models.UserLocation).filter(and_(models.UserLocation.token.__eq__(user_location.token), models.UserLocation.location.__eq__(user_location.location))).first()
    db.delete(user_location)
    db.commit()


    