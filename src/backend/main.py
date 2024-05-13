from fastapi import FastAPI
import joblib
import sys
import os

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from src.constants import OUT_MODEL
import pandas as pd
random_forest = joblib.load(OUT_MODEL)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# disable CORS 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
  return {"message": "Hello World!"}

# make a prediction based on the input features, where you get the features in the request body. Also save the prediction in the database.
@app.post("/predict/")
async def predict(features: schemas.PredictionCreate, db: Session = Depends(get_db)):
  features = [features['feature']]
  prediction = random_forest.predict(features)
  # now save the prediction in the database
  crud.save_prediction(db, features, prediction[0])
  return {"prediction": prediction[0]}

# make a prediction based on the date that is passed as a parameter in the URL. The date should be in the format YYYY-MM-DD.
# make a prediction with the model for all the location_ids(which there are 6 of) and return the predictions in the response.
@app.get("/predict/{date}", response_model=dict)
async def predict_date(date: str, db: Session = Depends(get_db)):
  predictions = []
  missing = []
  df = pd.DataFrame(columns=['location_id', 'day_of_week', 'dela_prost_dan', 'RR', 'SS', 'TG', 'month', 'pretocnost_7d', 'pretocnost_3d'])
  for i in range(0, 6):
    # get from database the predictions for the given date for all the location_ids(0 to 5)
    predictions = crud.get_predictions_by_date(db, date, i)
    # if predictions is empty then continue

    if not predictions:
      missing.append(i)
      continue
    print("fdfsafsds", predictions[0].day_of_week)
    # create an empty dataframe
    
    # create a new row with the prediction values
    new_row = {
      'location_id': i,
      'day_of_week': predictions[0].day_of_week,
      'dela_prost_dan': predictions[0].free_day,
      'RR': predictions[0].rr,
      'SS': predictions[0].ss,
      'TG': predictions[0].tg,
      'month': predictions[0].month,
      'pretocnost_7d': predictions[0].pretocnost_7,
      'pretocnost_3d': predictions[0].pretocnost_3
    }

    new_df = pd.DataFrame(new_row, index=[0])
    print("new_df", new_df)

    # append the new row to the dataframe
    print(df.columns, new_df.columns)
    df = pd.concat([df, new_df], ignore_index=True)

  print("the df +++++++++++++++++", df)
  df.to_csv("df.csv", index=False)
  df = pd.read_csv("df.csv")
  print("this is df", df)
  final_predictions = random_forest.predict(df)
  final_predictions = final_predictions.tolist()
  # add to final_predictions the missing location_ids with the value 3
  for i in missing:
    final_predictions = list(final_predictions)
    final_predictions.insert(i, 3)
  print("final_predictions", final_predictions)
  # return the predictions
  return {"predictions": final_predictions}