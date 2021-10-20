from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/series/", response_model=schemas.Series)
def create_series(series: schemas.SeriesCreate, db: Session = Depends(get_db)):
    db_series = crud.get_series_by_id(db, SeriesInstanceUID=series.SeriesInstanceUID)
    if db_series:
        raise HTTPException(status_code=400, detail="Series already exists")
    return crud.create_series(db=db, series=series)


@app.get("/series/", response_model=List[schemas.Series])
def read_series(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    series = crud.get_series(db, skip=skip, limit=limit)
    return series
