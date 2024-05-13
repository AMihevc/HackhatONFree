from sqlalchemy.orm import Session
import models, schemas

#create a new prediction
def create_prediction(db: Session, prediction: schemas.PredictionBase):
    db_prediction = models.Prediction(**prediction.model_dump())
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

# return all predictions
def get_predictions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Prediction).offset(skip).limit(limit).all()

# return a a prediction by location_id
def get_prediction_by_location_id(db: Session, location_id: int):
    return db.query(models.Prediction).filter(models.Prediction.location_id == location_id).first()

# save a prediction
def save_prediction(db: Session, prediction: schemas.PredictionBase, final_prediction: int):
    db_prediction = models.Prediction(**prediction.model_dump(), final_prediction=final_prediction)
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

# get predictions by date
def get_predictions_by_date(db: Session, date: str, location_id: int):
    return db.query(models.Prediction).filter(models.Prediction.date == date, models.Prediction.location_id == location_id).all()