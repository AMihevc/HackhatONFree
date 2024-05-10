import requests
import hjson
import json
from pprint import pprint
import pandas as pd
from datetime import datetime
import os
import time
from tqdm import tqdm
import glob

"""
Program to scrape ARSO weather data for all automatic stations for a predefined date range and save it to files.
Data should be in 30 minute intervals.
"""


os.makedirs("data", exist_ok=True)

DATE_FR = "2022-01-01"
DATE_TO = "2024-05-10"

VARS_TO_GET = "12,26,21,15,23,24"
URL_INITIAL = f"https://meteo.arso.gov.si/webmet/archive/locations.xml?d1={DATE_FR}&d2={DATE_TO}&type=4&%20lang=si"

URL_GREEN = f"https://meteo.arso.gov.si/webmet/archive/data.xml?lang=si&vars={VARS_TO_GET}&group=halfhourlyData0&type=halfhourly&id={{id_station}}&d1={{date_from}}&d2={{date_to}}"


def get_json_like(url, load_offline=False):
    if load_offline:
        with open("data.json", "r", encoding="utf-8") as f:
            data = f.read()
        return json.loads(data)
    
    # print("GET:", url)

    try:
        response = requests.get(url)
        resp = response.text

        AFTER = "AcademaPUJS.set("
        BEFORE = ")]]></pujs>"
        data = resp[resp.find(AFTER) + len(AFTER):resp.find(BEFORE)].strip()
        data = data.encode('latin-1').decode('utf-8')

        json_like = hjson.loads(data)
        with open("data.json", "w", encoding="utf-8") as f:
            text = json.dumps(json_like, indent=2, ensure_ascii=False)
            f.write(text)

    except Exception as e:
        print("Error for GET:", url)
        print(e)
        print("RESPONSE TEXT:")
        print(resp)

    # print(json_like)
    return json_like



def get_df_from_station_res(dt_from, dt_to, station_id, dt_format="%Y-%m-%d"):
    # get station data for a certain date range
    url_station = URL_GREEN.format(
        id_station=station_id.strip("_"),
        date_from=dt_from.strftime(dt_format),
        date_to=dt_to.strftime(dt_format),
    )
    station_data = get_json_like(url_station, load_offline=False)

    station_params = station_data["params"]
    # print(station_params)

    # dict of {param : long column name} pairs
    params_dict = {
        key : param["l"]
        for key, param
        in station_params.items()
    }

    # dict of {param key : all param data} pairs
    params_dict_invert = {
        param["name"] : {
            "key" : key,
            **param
        }
        for key, param
        in station_params.items()
    }

    assert len(station_data["points"]) == 1
    station_points = station_data["points"][station_id]

    df = pd.DataFrame(station_points).transpose()
    df.index = df.index.str.strip("_")  # index strip _
    df.index = pd.to_numeric(df.index)  # index to number

    # get datetime from weird formated string
    inx_first = df.index[0]  # first index
    df.index = df.index - inx_first  # index is now minutes
    # dt_from = datetime.strptime(DATE_FR, "%Y-%m-%d")
    df.index = df.index.map(lambda x: dt_from + pd.Timedelta(minutes=x))
    
    # rename columns from param key to long name
    df.rename(columns=params_dict, inplace=True)  # rename columns
    df.sort_index(inplace=True)  # sort by index

    return df


initial = get_json_like(URL_INITIAL)
stations = initial["points"].keys()
# stations = ["_2626"]

# get data for all stations
for station_id in tqdm(stations, desc="Stations"):
    dir_out = f"data/{station_id}"
    os.makedirs(dir_out, exist_ok=True)

    station = initial["points"][station_id]
    # # ['name', 'lon', 'lat', 'alt', 'type']
    # print(station["name"], station["lon"], station["lat"], station["alt"], station["type"])
    with open(f"{dir_out}/station.json", "w", encoding="utf-8") as f:
        text = json.dumps(station, indent=2, ensure_ascii=False)
        f.write(text)

    # print(station_data)

    # date_from = "DATE_FR"
    # date_to = DATE_TO

    # get one month pairs between 2 dates
    fmt = "%Y-%m-%d"
    date_from = datetime.strptime(DATE_FR, fmt)
    date_to = datetime.strptime(DATE_TO, fmt)
    dt_month_beginings = pd.date_range(date_from, date_to, freq="MS")
    dt_month_ends = pd.date_range(date_from, date_to, freq="ME")
    date_ranges_list = list(zip(dt_month_beginings, dt_month_ends))
    # print(dt_month_beginings)
    # print(dt_month_ends)

    # df_all = None

    for date_from, date_to in tqdm(date_ranges_list, desc="Getting data"):
        # date_from = date_from.strftime(fmt)
        # date_to = date_to.strftime(fmt)
        # print(date_from, date_to)
        
        station_id_stripped = station_id.strip('_')
        filepath_out = f"{dir_out}/{station_id_stripped}_{date_from.strftime('%Y-%m')}"
        if os.path.exists(f"{filepath_out}.pkl"):
            continue

        df = get_df_from_station_res(date_from, date_to, station_id)

        # print(df.columns.tolist())
        if not df.columns.tolist():
            print(f"Empty data for {date_from.strftime('%Y-%m')}")
            time.sleep(0.5)
            continue

        df.to_pickle(f"{filepath_out}.pkl")
        df.to_csv(f"{filepath_out}.csv", index=True)

        time.sleep(1)


    # merge all to one file
    df_all = None
    for file in glob.glob(f"{dir_out}/{station_id_stripped}*.pkl"):
        df = pd.read_pickle(file)
        if df_all is None:
            df_all = df
        else:
            df_all = pd.concat([df_all, df])

    df_all.sort_index(inplace=True)  # sort by index
    df_all.to_pickle(f"{dir_out}/_all.pkl")
    df_all.to_csv(f"{dir_out}/_all.csv", index=True)

    # print(df_all.columns)
    # print(df_all)


# https://meteo.arso.gov.si/webmet/archive/data.xml?lang=si&vars=12,26,21,15,23,24&group=halfhourlyData0&type=halfhourly&id=2626&d1=2023-02-01&d2=2023-02-28&nocache=lw0fkiah3x2hzwg540o
# https://meteo.arso.gov.si/webmet/archive/data.xml?lang=si&vars=12,26,21,15,23,24&group=halfhourlyData0&type=halfhourly&id=2626&d1=2022-04-01&d2=2022-05-01&nocache=lw0isq3v9t19aho2h1
# https://meteo.arso.gov.si/webmet/archive/data.xml?lang=si&vars=12,26,21,15,23,24&group=halfhourlyData0&type=halfhourly&id=2626&d1=2023-04-01&d2=2023-05-01&nocache=lw0iqex7d2jbmotb1yw