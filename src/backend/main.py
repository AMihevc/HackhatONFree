from fastapi import FastAPI
import joblib
import sys
import os
import requests
import aiohttp
import asyncio
from openai import OpenAI

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# from src.constants import OUT_MODEL
import pandas as pd
# random_forest = joblib.load(OUT_MODEL)

urls = ["https://www.vreme.si/api/1.0/location/?lang=sl&location=Ur%C5%A1lja%20gora",
        "https://www.vreme.si/api/1.0/location/?lang=sl&location=Letali%C5%A1%C4%8De%20Edvarda%20Rusjana%20Maribor",
        "https://www.vreme.si/api/1.0/location/?lang=sl&location=Celje",
        "https://www.vreme.si/api/1.0/location/?lang=sl&location=Topol",
        "https://www.vreme.si/api/1.0/location/?lang=sl&location=Nova%20Gorica"
        ]
ids = [{"kraj": "Uršlja gora", "id": 2619},
       {"kraj": "Edvarda Rusjana", "id": 1838},
       {"kraj": "Celje", "id": 2471},
       {"kraj": "Topol", "id": 2842},
       {"kraj": "Nova Gorica", "id": 1822}]

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
  response = requests.get("https://www.vreme.si/api/1.0/location/?lang=sl&location=Ljubljana").json()
#   print("the response:", response["forecast6h"]["features"][0]["properties"]["days"])
  days = response["forecast6h"]["features"][0]["properties"]["days"]
  desired_day = next((obj for obj in days if obj["date"] == "2024-05-15"), None) # the day for which we want the prediction
#   print("fdsfa", desired_day)
  part_of_desired_day = desired_day["timeline"] # here are up to 4 objects which represent part of the desired day
  print("part_of_desired_day", part_of_desired_day)
  return {"message": "fdsfa"}

# try 100 requests on the endpoint
@app.get("/test_rate/")
async def test_rate():
  for i in range(6):
    # check if the response is 200
    response = requests.get("https://www.vreme.si/api/1.0/location/?lang=sl&location=Ljubljana").json()
    print(f"{i} \t {response['forecast24h']}")
  return{"message": "fdsfa"}

async def make_api_call(url, session, order):
  async with session.get(url) as response:
    data = await response.json()
    # days = response["forecast6h"]["features"][0]["properties"]["days"]
    # TODO for now the date is hardcoded, we need to change it to be dynamic
    # desired_day = next((obj for obj in days if obj["date"] == "2024-05-15"), None) # the day for which we want the prediction
    # part_of_desired_day = desired_day["timeline"] # here are up to 4 objects which represent part of the desired day
    # print(f"URL: {url} (Order: {order}), Data: {data}")
    return data

# do the calls with tasks
async def get_loc_data():
  counter = 0
  # each task is a location(url)
  tasks = []
  async with aiohttp.ClientSession() as session:
    for url in urls:
      counter += 1
      task = asyncio.create_task(make_api_call(url, session, counter))
      tasks.append(task)
    await asyncio.gather(*tasks)
  # print(tasks[0].result()["forecast24h"]["features"])
  return tasks
  print("All tasks are done")

@app.get("/predict/{date}/")
async def predict(date: str):
  print("here")
  locations = await get_loc_data()
  # print("locations", locations[0].result())
  locations = [location.result() for location in locations]
  locations = [location["forecast6h"]["features"][0]["properties"]["days"] for location in locations]
  # now we have all the data for all the locations but just for the 6h
  # print("locations", locations[0]["forecast24h"]["features"])
  # features = [features['feature']]
  # prediction = random_forest.predict(features)
  # now save the prediction in the database
  # crud.save_prediction(db, features, prediction[0])
  # return {"prediction": prediction[0]}
  # in every location of locations only keep the desired date
  for i, location in enumerate(locations):
    desired_day = next((obj for obj in location if obj["date"] == date), None)
    locations[i] = desired_day
  # print("locations length", len(locations[0]))
  return locations

@app.get("/test_gpt/")
async def test_gpt():
  client = OpenAI(api_key="sk-proj-bzgRr2hFwrCnGFZX1VsWT3BlbkFJhF8GoNVWH2T5aWBdOdEn")

  conversation_history = [
      {"role": "system", "content": "Ste ekspert na področju poplav. Imate podatke, da je zelo velika verjetnost poplav v Ljubljani v naslednjih treh dneh."},
      {"role": "user", "content": "Ali bodo v naslednjih dneh kje v Sloveniji poplave?"}
      # Continue adding messages as the conversation progresses
  ]

  response = client.chat.completions.create(
      model="gpt-4",
      messages=conversation_history,
      # stream=True
  )

  # for chunk in response:
  #   print(chunk.choices[0].delta)
  print(response.choices[0].message)