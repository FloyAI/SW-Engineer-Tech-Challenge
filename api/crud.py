from sqlalchemy.orm import Session

from . import models, schemas

def create_series(db: Session, series: schemas.SeriesCreate):
    db_series = models.Series(
        SeriesInstanceUID = series.SeriesInstanceUID,
        PatientID = series.PatientID,
        PatientName = series.PatientName,
        StudyInstanceUID = series.StudyInstanceUID,
        InstancesInSeries = series.InstancesInSeries
    )
    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    return db_series


def get_series(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Series).offset(skip).limit(limit).all()


def get_series_by_id(db: Session, SeriesInstanceUID: str):
    return db.query(models.Series).filter(
        models.Series.SeriesInstanceUID == SeriesInstanceUID
    ).first()
