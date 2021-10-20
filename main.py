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


@app.get("/mosques/")
async def get_all(db=Depends(get_db)):
    return crud.get_all_mosques(db=db)


@app.get("/mosques/timings/")
async def get_all(db=Depends(get_db)):
    return crud.get_all_mosques_timings(db=db)


@app.post('/mosques/new/')
async def add_mosque_timings(mosque_timings: mosque_timings.MosqueTimings, db: Session = Depends(get_db)):
    return crud.add_mosque_timings(db=db, mosque_timings=mosque_timings)


@app.put("/mosques/update/")
def update_mosque_timings(mosque_timings: mosque_timings.MosqueTimings, db: Session = Depends(get_db)):
    existing_item = crud.get_mosque_timings(
        db=db, location=mosque_timings.location)
    if existing_item is None:
        crud.add_mosque_timings(db=db, mosque_timings=mosque_timings)
    else:
        crud.update_mosqueTimings(
            db=db, mosque_timings=existing_item, updates=mosque_timings)

        # send_notification(title='CheckUp Done', body='Car checkup for today is done')

    return mosque_timings


@app.get("/user/locations/")
async def get_user_locations(token: str = Query(...), db=Depends(get_db)):
    return crud.get_user_locaitons(db=db, token=token)


@app.post('/user/locations/new/')
async def new_device_location(user_location: user_locations.UserLocation, db=Depends(get_db)):
    return crud.add_location(db=db, user_location=user_location)


@app.post('/user/locations/delete/')
async def delete_device_location(user_location: user_locations.UserLocation, db=Depends(get_db)):
    return crud.delete_user_location(db=db, user_location=user_location)


@app.post("/all/delete/")
async def delete(db=Depends(get_db)):
    # crud.deleteMosqueTimings(db=db)
    crud.deleteUserLocation(db=db)
    return 'deleted'
