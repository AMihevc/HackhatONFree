from pydantic import BaseModel
from datetime import datetime

class PredictionBase(BaseModel):
    date: datetime
    location_id: int
    day_of_week: int
    free_day: bool
    month: int
    pretocnost_7: int
    pretocnost_3: int
    pretocnost_q: int

class Predictions(PredictionBase):
    id: int
    final_prediction: int

    class Config:
        orm_mode = True

class PredictionCreate(PredictionBase):
    pass
