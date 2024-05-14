import pandas as pd


# OUT_MACRO_REGION_STATIONS = "koroska_stations"
# OUT_MACRO_REGION_STATIONS = "maribor_stations"
# OUT_MACRO_REGION_STATIONS = "ljubljana_stations"
# OUT_MACRO_REGION_STATIONS = "celje_stations"
OUT_MACRO_REGION_STATIONS = "nova_gorica_stations"
locations_counter = 5
macro_locations = ["koroska_stations", "maribor_stations", "ljubljana_stations", "celje_stations", "nova_gorica_stations"][:locations_counter]

DATA_OUT = f"/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_out/{OUT_MACRO_REGION_STATIONS}.pkl"
DATA_OUT_CLEAN = f"/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_out/{OUT_MACRO_REGION_STATIONS}_clean.pkl"
DATA_OUT_CLEAN_FINAL_ZENODO = f"/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_out/all_clean_zenodo"

DATA_OUT_TRAIN_X = f"/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_out/all_macro_train_X.pkl"
DATA_OUT_TRAIN_X_CSV = f"/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_out/all_macro_train_X.csv"
DATA_OUT_TRAIN_Y = f"/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_out/all_macro_train_y.pkl"
DATA_OUT_TRAIN_Y_CSV = f"/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_out/all_macro_train_y.csv"

# remove "_stations"
macro_location = OUT_MACRO_REGION_STATIONS[:-9]
data_visina_macro = f"/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_visina/data_{macro_location}.csv"


df = pd.read_pickle(DATA_OUT)

# df date column to datetime
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

print(df.head())
print(df.columns)

# # print unique for station_id
# print(df["station_id"].unique())

# impute missing values for all NaN values in each column


# drop all Null columns
# print columns that are all null
# print(df.columns[df.isnull().all()])
columns_remove = ['tlak_avg_00', 'tlak_avg_06', 'tlak_avg_12', 'tlak_avg_18']
df = df.drop(columns=columns_remove)


# aggregate by month and impute missing values for each column

for month_i in range(1, 13):
    for time in ["00", "06", "12", "18"]:
        for col in ["padavine_klicina", "temperatura_avg", "veter_hitrost", "veter_sunki"]:
            col_name = f"{col}_{time}"
            # print(col_name)
            # print(df[col_name].isnull().sum())
            df[col_name] = df[col_name].fillna(df.groupby("month")[col_name].transform("mean"))


# aggregate by date and average all columns
for time in ["00", "06", "12", "18"]:
    for col in ["padavine_klicina", "temperatura_avg", "veter_hitrost"]:
        col_name = f"{col}_{time}"
        df[col_name] = df.groupby("date")[col_name].transform("mean")

    col_name = f"veter_sunki_{time}"
    df[col_name] = df.groupby("date")[col_name].transform("max")


# use only one station_id from first unique station_id
df = df[df["station_id"] == df["station_id"].unique()[0]]




df_visina = pd.read_csv(data_visina_macro, sep=";")
print(df_visina.head())

# Datum to datetime
df_visina["Datum"] = pd.to_datetime(df_visina["Datum"], format="%d.%m.%Y")
# rename to date
df_visina.rename(columns={"Datum": "date", "pretok (m3/s)": "pretok_m3s"}, inplace=True)

# merge with df based on date
df = pd.merge(df, df_visina, on="date", how="left")


# todo: remove date, station_id
df = df.drop(columns=["date"])


# 5 quantiles semaphore for pretok_m3s ->  pretok_m3s_q column
# TODO: uporabi poplavne dogodke, da dolocis boljše mejne vrednosti
N_QUANT = 21
df["pretok_m3s_q"] = pd.qcut(df["pretok_m3s"], N_QUANT, labels=False, duplicates="drop")


# pretok_m3s_q 20 to -3
# pretok_m3s_q 10-19 to -2
# pretok_m3s_q 0-9 to -1
df["pretok_m3s_q"] = df["pretok_m3s_q"].map(lambda x: -3 if x >= 20 else (-2 if x >= 10 else -1))

df["pretok_m3s_q"] = df["pretok_m3s_q"]*-1 -1


df.to_pickle(DATA_OUT_CLEAN)

# OUT_MACRO_REGION_STATIONS = "ljubljana_stations"
# OUT_MACRO_REGION_STATIONS = "celje_stations"
# OUT_MACRO_REGION_STATIONS = "nova_gorica_stations"

df_all = pd.DataFrame()
for macro_loc in macro_locations:
    macro_path = "/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_out/{}_clean.pkl".format(macro_loc)
    df_tmp = pd.read_pickle(macro_path)
    df_all = pd.concat([df_all, df_tmp], ignore_index=True)

print(df_all.head())

df = df_all


# this is final data for zenodo upload
df.to_pickle(f"{DATA_OUT_CLEAN_FINAL_ZENODO}.pkl")
df.to_csv(f"{DATA_OUT_CLEAN_FINAL_ZENODO}.csv")



print(df.head())
print(df["pretok_m3s_q"].unique())
print(df["pretok_m3s_q"].value_counts())

y = df["pretok_m3s_q"]
X = df.drop(columns=["pretok_m3s", "pretok_m3s_q"])

y.to_pickle(DATA_OUT_TRAIN_Y)
X.to_pickle(DATA_OUT_TRAIN_X)

y.to_csv(DATA_OUT_TRAIN_Y_CSV)
X.to_csv(DATA_OUT_TRAIN_X_CSV)


# df = pd.read_excel(DATA_POPLAVE)
# print(df.head())
