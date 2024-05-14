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
import pandas as pd
import datetime
random_forest = joblib.load("models/model_rf")

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
  # print("part_of_desired_day", part_of_desired_day)
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
  # print("here")
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

  df = pd.DataFrame(columns=['station_id', 'padavine_klicina_00', 'temperatura_avg_00', 'veter_hitrost_00', 'veter_sunki_00',
                                           'padavine_klicina_06', 'temperatura_avg_06', 'veter_hitrost_06', 'veter_sunki_06',
                                           'padavine_klicina_12', 'temperatura_avg_12', 'veter_hitrost_12', 'veter_sunki_12',
                                           'padavine_klicina_18', 'temperatura_avg_18', 'veter_hitrost_18', 'veter_sunki_18',
                                           'month'])
  ffmax_val_mean = 0
  count = 0
  for i, location in enumerate(locations):
    new_row = {
      'station_id': ids[i]["id"],
      'padavine_klicina_00': location["timeline"][0]["tp_acc"],
      'temperatura_avg_00': location["timeline"][0]["t"],
      'veter_hitrost_00': location["timeline"][0]["ff_val"],
      'veter_sunki_00': location["timeline"][0]["ffmax_val"],
      'padavine_klicina_06': location["timeline"][1]["tp_acc"],
      'temperatura_avg_06': location["timeline"][1]["t"],
      'veter_hitrost_06': location["timeline"][1]["ff_val"],
      'veter_sunki_06': location["timeline"][1]["ffmax_val"],
      'padavine_klicina_12': location["timeline"][2]["tp_acc"],
      'temperatura_avg_12': location["timeline"][2]["t"],
      'veter_hitrost_12': location["timeline"][2]["ff_val"],
      'veter_sunki_12': location["timeline"][2]["ffmax_val"],
      'padavine_klicina_18': location["timeline"][3]["tp_acc"],
      'temperatura_avg_18': location["timeline"][3]["t"],
      'veter_hitrost_18': location["timeline"][3]["ff_val"],
      'veter_sunki_18': location["timeline"][3]["ffmax_val"],
      'month': str(int(location["date"].split("-")[1]))
    }
    # check value is None or empty, if not then add zero
    if new_row["veter_sunki_00"] is None or new_row["veter_sunki_00"] == "":
      new_row["veter_sunki_00"] = 0
    ffmax_val_mean += int(new_row["veter_sunki_00"])

    if new_row["veter_sunki_06"] is None or new_row["veter_sunki_06"] == "":
      new_row["veter_sunki_06"] = 0
    ffmax_val_mean += int(new_row["veter_sunki_06"])

    if new_row["veter_sunki_12"] is None or new_row["veter_sunki_12"] == "":
      new_row["veter_sunki_12"] = 0
    ffmax_val_mean += int(new_row["veter_sunki_12"])

    if new_row["veter_sunki_18"] is None or new_row["veter_sunki_18"] == "":
      new_row["veter_sunki_18"] = 0
    ffmax_val_mean += int(new_row["veter_sunki_18"])
    ffmax_val_mean = ffmax_val_mean / 4

    new_row["veter_sunki_00"] = ffmax_val_mean
    new_row["veter_sunki_06"] = ffmax_val_mean
    new_row["veter_sunki_12"] = ffmax_val_mean
    new_row["veter_sunki_18"] = ffmax_val_mean
    ffmax_val_mean = 0
    # chech if any of the values is None or empty
    # for key, value in new_row.items():
    #   if value == None or value == "":
    #     count += 1
    #     new_row[key] = 0
    #     print("key", key, i)

    


    new_df = pd.DataFrame(new_row, index=[0])

    df = pd.concat([df, new_df], ignore_index=True)
  
  # print("the df +++++++++++++++++", df)

  final_predictions = random_forest.predict(df)
  final_predictions = final_predictions.tolist()
  # print("final_predictions", final_predictions)
  # df.to_csv("df.csv", index=False)
  # df = pd.read_csv("df.csv")
  # print(locations[0]["date"])
  # get today date
  today = datetime.date.today()

  response = {
    "urslja": final_predictions[0],
    "maribor": final_predictions[1],
    "celje": final_predictions[2],
    "topol": final_predictions[3],
    "nova_gorica": final_predictions[4],
    "context": 'You are an expert in floods. You have data for a probabilty of floods in five different locations in Slovenia. Values of the predictions are between 0 and 2.' +
    ' 0 means no floods, 1 means low probability of floods, 2 means high probability of floods. The values are as follows: Uršlja gora: ' + str(final_predictions[0]) + ', Maribor: ' +
    str(final_predictions[1]) + ', Celje: ' + str(final_predictions[2]) + ', Topol: ' + str(final_predictions[3]) + ', and Nova Gorica: ' + str(final_predictions[4]) +
    ' and the values are for date: ' + locations[0]["date"] + '. and today is: ' + str(today) + '.'
  }
  return response

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