from typing import List, Optional

from pydantic import BaseModel


class SeriesBase(BaseModel):
    SeriesInstanceUID: str
    PatientID: str
    PatientName: str
    StudyInstanceUID: str
    InstancesInSeries: int


class SeriesCreate(SeriesBase):
    pass


class Series(SeriesBase):

    class Config:
        orm_mode = True
