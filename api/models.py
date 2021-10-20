from sqlalchemy import Column, Integer, String

from .database import Base


class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    SeriesInstanceUID = Column(String, unique=True, nullable=False)
    PatientID = Column(String, nullable=False)
    PatientName = Column(String, unique=True, nullable=False)
    StudyInstanceUID = Column(String, nullable=False)
    InstancesInSeries = Column(Integer, nullable=False)
