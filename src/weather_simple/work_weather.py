import pandas as pd
from glob import glob
from datetime import datetime
from tqdm import tqdm
from pathlib import Path


DATA = "/d/hpc/projects/FRI/tp1859/weather/data2/data_id*.csv"
DATA_OUT = "/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_out"

DATA_STATIONS_INFO = "/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/stations_info.pkl"

STOLPCI_LONG = {
    'valid': 'datetime',
    't': "temperatura",
    'p': "povprečen zračni tlak (hPa)",
    'rh': "povprečna relativna vlaga (%)",
    'ff': "hitrost vetra",
    'dd': "smer vetra",
    'veter_sunki': "maksimalna hitrost vetra (m/s)",
    'rr': "količina padavin",
    'g_sunrad': "povprečen energijski tok globalnega sevanja (W/m2)",
    'di_sunrad': "povprečen energijski tok difuznega sevanja (W/m2)",
    'uvb': "UVB (mW/m2)",
}

STOLPCI_SHORT = {
    'valid': 'datetime',
    't': "temperatura_avg",
    'p': "tlak_avg",
    'rh': "rel_vlaga_avg",
    'ff': "veter_hitrost",
    'dd': "veter_smer",
    'veter_sunki': "veter_sunki",
    'rr': "padavine_klicina",
    'g_sunrad': "energ_tok_global_avg",
    'di_sunrad': "energ_tok_difuz_avg",
    'uvb': "uvb",
}


DATE_FROM = "2018-01-01"

DATE_TO = "2022-12-31"

# KOROSKA STATIONS
# STATIONS_TO_USE = ["2620", "2845", "1839", "2666", "2654", "2631", "2619"]
# OUT_MACRO_REGION_STATIONS = "koroska_stations"

# STATIONS_TO_USE = ["1838"]
# OUT_MACRO_REGION_STATIONS = "maribor_stations"

# STATIONS_TO_USE = ["2842"]
# OUT_MACRO_REGION_STATIONS = "ljubljana_stations"

# STATIONS_TO_USE = ["2471"]
# OUT_MACRO_REGION_STATIONS = "celje_stations"

STATIONS_TO_USE = ["1824"]
OUT_MACRO_REGION_STATIONS = "nova_gorica_stations"

df_stations = pd.read_pickle(DATA_STATIONS_INFO)
print(df_stations.head())


df_all = pd.DataFrame()

for csv_path in tqdm(glob(DATA), desc="Processing stations"):
    path = Path(csv_path)

    station_id_path = path.parts[-1].strip(".csv").split("-")[-1]
    if station_id_path not in STATIONS_TO_USE:
        continue
    
    df = pd.read_csv(csv_path)

    print(f"Reading: {csv_path}")

    if df.empty:
        continue

    station_id = df["id"].unique()[0]
    assert len(df["id"].unique()) == 1
    
    if str(station_id) not in STATIONS_TO_USE:
        continue

    df.drop(columns=["Unnamed: 0", "id"], inplace=True)

    # drop rows that contain 20:00 at the end of valid column
    # only 00 and 30 contain all data
    remove_based_on_time_list = ["20:00", "10:00", "40:00", "50:00"]
    for time in remove_based_on_time_list:
        df = df[~df["valid"].str.endswith(time)]

    # get datetime from formated string
    df["valid"] = pd.to_datetime(df["valid"], format="%Y-%m-%d %H:%M:%S")

    print(f"Reading: {csv_path}")

    # rename columns
    df.rename(columns=STOLPCI_SHORT, inplace=True)

    # take only data from DATE_FROM onwards
    df = df[df["datetime"] >= DATE_FROM]
    df = df[df["datetime"] < DATE_TO]

    
    # drop "veter_smer"
    df.drop(columns=["veter_smer", "energ_tok_global_avg", "energ_tok_difuz_avg", "uvb"], inplace=True)

    # for every 6 h intervals get new df
    # average temperatura_avg, tlak_avg  rel_vlaga_avg  veter_hitrost  energ_tok_global_avg  energ_tok_difuz_avg  uvb
    # sum padavine_klicina
    # max veter_sunki
    df_6h = pd.DataFrame()
    df_6h["padavine_klicina"] = df.resample("6h", on="datetime").sum()["padavine_klicina"]
    df_6h["veter_sunki"] = df.resample("6h", on="datetime").max()["veter_sunki"]

    for column in ["temperatura_avg", "tlak_avg", "rel_vlaga_avg", "veter_hitrost"]:
        df_6h[column] = df.resample("6h", on="datetime").mean()[column]

    print(df_6h.head())

    # get all dates in list 
    dates = df_6h.index.date
    # get unique dates
    dates = sorted(list(set(dates)))

    # add row for each unique day
    for date in dates:
        df_row_to_add = pd.DataFrame()
        
        df_row_to_add["station_id"] = [station_id]
        df_row_to_add["date"] = [date]

        # for time 00, 06, 12, 18 add columns to df_row_to_add
        for time in ["00:00", "06:00", "12:00", "18:00"]:
            dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            # df_row_to_add["datetime"] = [dt]
            # get data for that datetime
            hour_str = time.split(":")[0]
            
            # padavine
            df_row_to_add[f"padavine_klicina_{hour_str}"] = df_6h.loc[dt, "padavine_klicina"]

            # temperatura
            df_row_to_add[f"temperatura_avg_{hour_str}"] = df_6h.loc[dt, "temperatura_avg"]

            # tlak
            df_row_to_add[f"tlak_avg_{hour_str}"] = df_6h.loc[dt, "tlak_avg"]
            # TODO: add min max tlak

            # veter_hitrost
            df_row_to_add[f"veter_hitrost_{hour_str}"] = df_6h.loc[dt, "veter_hitrost"]

            # veter_sunki
            df_row_to_add[f"veter_sunki_{hour_str}"] = df_6h.loc[dt, "veter_sunki"]


        # add month number
        df_row_to_add["month"] = dt.month

        # exit()


        # print(df_row_to_add.head())

        df_all = pd.concat([df_all, df_row_to_add], ignore_index=True)

        # exit()
        # print(df_row_to_add.head())


df_all.to_csv(f"{DATA_OUT}/{OUT_MACRO_REGION_STATIONS}.csv", index=True)
df_all.to_pickle(f"{DATA_OUT}/{OUT_MACRO_REGION_STATIONS}.pkl")

    # print("Station id", station_id)
    # print(df.head(10))
    # print(df.columns)

    # for column print max, min average vals
    # for column in df.columns:
    #     print(f" {column} : max: {df[column].max()}, min: {df[column].min()}, avg: {df[column].mean()}")

    # drop "Unnamed: 0" column