# Imports, Path for DB and API URL

import json
import sqlite3
import requests
import numpy as np
import pandas as pd
from pathlib import Path

BASE_URL = "https://api.open-meteo.com/v1/forecast"
DB_PATH = Path("../Data/DB/AERO.db")


# ________________________________________________________________________________________________________________________________________________________
# City names and coordinates

latlong = {"London":[51.50, -0.12],"New York": [40.71, -74.00],"Tokyo": [35.67, 139.65],"Sydney": [-33.86, 151.20],"Reykjavik": [64.14, -21.89]}
cities = ["London", "New York", "Tokyo", "Sydney", "Reykjavik"]


# _________________________________________________________________________________________________________________________________________________________
# Data collection

data = []

for lat, long in latlong.values():
    resp = requests.get(f"{BASE_URL}?latitude={lat}&longitude={long}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&forecast_days=3").json()
    resp["city"] = [n for n, l in latlong.items() if l == [lat, long]][0]
    data.append(resp)
    

rows = []

for di in data:
    city = di["city"]
    hourly = di["hourly"]

    times = hourly["time"]
    temps = hourly["temperature_2m"]
    hums  = hourly["relative_humidity_2m"]
    winds = hourly["wind_speed_10m"]

    for i in range(len(times)):
        rows.append({
            "city": city,
            "forecast_time": times[i],
            "temp_c": temps[i],
            "humidity": hums[i],
            "wind_kph": winds[i]
        })


# _________________________________________________________________________________________________________________________________________________________
# DB creation and data insertion

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute(
    """
    DROP TABLE IF EXISTS forecasts;
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS forecasts(
    id	INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    forecast_time TEXT,
    temp_c REAL,
    humidity INTEGER,
    wind_kph REAL
    );
    """
)


com_for_insert = """
    INSERT OR REPLACE INTO forecasts(city, forecast_time, temp_c, humidity, wind_kph)
    VALUES(:city, :forecast_time, :temp_c, :humidity, :wind_kph)
    """

cur.executemany(com_for_insert, rows)

conn.commit()


# ______________________________________________________________________________________________________________________________________________________________
# Pandas data reading

df = pd.read_sql("""SELECT * FROM forecasts""", conn)
conn.close()

groupt = df.groupby("city")["temp_c"].max()


# ______________________________________________________________________________________________________________________________________________________________

# Question 1
h_temp = groupt.max()
h_temp_city = groupt.idxmax()
print(f"Highest predicted tempreture in next 3 days has {h_temp_city} with tempreture of {h_temp:.2f}")

# Question 2
groupws = df.groupby("city")["wind_kph"].mean()
h_ws = groupws.max()
h_ws_city = groupws.idxmax()
print(f"Highest average wind speed in next 3 days has {h_ws_city} with speed of {h_ws:.2f}")

# Question 3
groupht = groupt = df.groupby("city")["temp_c"].max()
grouplt = groupt = df.groupby("city")["temp_c"].min()
temp_swing = {}

for city in cities:
    swing = groupht[city]-grouplt[city]
    temp_swing[city] = swing

h_ts = max(temp_swing.values())
h_ts_city = [city for city, swg in temp_swing.items() if swg == h_ts][0]
print(f"Highest tempreture swing in next 3 days has {h_ts_city} with speed of {h_ts:.2f}")

# Question 4
groupat = df.groupby("city")["temp_c"].mean()

for city in cities:
    avg_temp = groupat[city]
    print(f"Average predicted tempreture in {city} is {avg_temp:.2f}")
    
    
# Question 5
df["fog_rain_risk"] = np.ones(360)
df["fog_rain_risk"] = df["fog_rain_risk"].where(df["humidity"]>90, 0)

print(f"Count of rows with 90+% humidity is {df["fog_rain_risk"].sum()}")
df = df.drop("fog_rain_risk", axis=1)