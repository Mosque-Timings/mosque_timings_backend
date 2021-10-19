from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.param_functions import Body, Query
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
import crud
import models
from schemas import mosque_timings, user_locations
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


allowed_origins = ['*']

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_all(db=Depends(get_db)):
    return crud.get_all(db=db)


@app.post('/mosque-timings/')
async def get_checks(location: List[str], db: Session = Depends(get_db)):
    return crud.get_mosque_timings(db=db, location=location)


@app.post('/new/')
async def add_mosque_timings(mosque_timings: mosque_timings.MosqueTimings, db: Session = Depends(get_db)):
    return crud.add_mosque_timings(db=db, mosque_timings=mosque_timings)


@app.post('/new-user-location/')
async def add_device_location(user_location: user_locations.UserLocation, db=Depends(get_db)):
    return crud.add_location(db=db, user_location=user_location)


@app.post('/delete-user-location/')
async def add_device_location(user_location: user_locations.UserLocation, db=Depends(get_db)):
    return crud.deleteUserLocation(db=db, user_location=user_location)


@app.get("/user-locations/")
async def user_locations(token: str = Query(...), db=Depends(get_db)):
    return crud.get_user_locaitons(db=db, token=token)


@app.put("/update/")
def update_checks(mosque_timings: mosque_timings.MosqueTimings, db: Session = Depends(get_db)):
    existing_item = crud.get_mosque_timings(
        db=db, location=mosque_timings.location)
    if existing_item is None:
        crud.add_mosque_timings(db=db, mosque_timings=mosque_timings)
    else:
        crud.update_mosqueTimings(
            db=db, mosque_timings=existing_item, updates=mosque_timings)

        # send_notification(title='CheckUp Done', body='Car checkup for today is done')

    return mosque_timings


@app.post("/delete/")
async def delete(db=Depends(get_db)):
    # crud.deleteMosqueTimings(db=db)
    crud.deleteUserLocation(db=db)
    return 'deleted'
