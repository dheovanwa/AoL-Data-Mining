import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from statistics import mean
import csv

df = pd.read_csv("./coordinates_with_dates.csv")
dates = df.iloc[:, 0].values
latitudes = df.iloc[:, 1].values
longitudes = df.iloc[:, 2].values

weathers = []

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"

for i in range(len(dates)):
	print(f"Data ke-{i+2}")
	params = {
		"latitude": latitudes[i],
		"longitude": longitudes[i],
		"start_date": f"{dates[i]}",
		"end_date": f"{dates[i]}",
		"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "precipitation", "rain", "surface_pressure", "cloud_cover", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_100m", "wind_direction_10m", "wind_gusts_10m", "soil_moisture_0_to_7cm", "soil_moisture_7_to_28cm"],
		"timezone": "Asia/Bangkok"
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = mean(hourly.Variables(0).ValuesAsNumpy())
	hourly_relative_humidity_2m = mean(hourly.Variables(1).ValuesAsNumpy())
	hourly_dew_point_2m = mean(hourly.Variables(2).ValuesAsNumpy())
	hourly_precipitation = mean(hourly.Variables(3).ValuesAsNumpy())
	hourly_rain = mean(hourly.Variables(4).ValuesAsNumpy())
	hourly_surface_pressure = mean(hourly.Variables(5).ValuesAsNumpy())
	hourly_cloud_cover = mean(hourly.Variables(6).ValuesAsNumpy())
	hourly_et0_fao_evapotranspiration = mean(hourly.Variables(7).ValuesAsNumpy())
	hourly_vapour_pressure_deficit = mean(hourly.Variables(8).ValuesAsNumpy())
	hourly_wind_speed_10m = mean(hourly.Variables(9).ValuesAsNumpy())
	hourly_wind_speed_100m = mean(hourly.Variables(10).ValuesAsNumpy())
	hourly_wind_direction_10m = mean(hourly.Variables(11).ValuesAsNumpy())
	hourly_wind_gusts_10m = mean(hourly.Variables(12).ValuesAsNumpy())
	hourly_soil_moisture_0_to_7cm = mean(hourly.Variables(13).ValuesAsNumpy())
	hourly_soil_moisture_7_to_28cm = mean(hourly.Variables(14).ValuesAsNumpy())

	weathers.append([
		hourly_temperature_2m,
		hourly_relative_humidity_2m,
		hourly_dew_point_2m,
		hourly_precipitation,
		hourly_rain,
		hourly_surface_pressure,
		hourly_cloud_cover,
		hourly_et0_fao_evapotranspiration,
		hourly_vapour_pressure_deficit,
		hourly_wind_speed_10m,
		hourly_wind_speed_100m,
		hourly_wind_direction_10m,
		hourly_wind_gusts_10m,
		hourly_soil_moisture_0_to_7cm,
		hourly_soil_moisture_7_to_28cm,
	])

with open("cuaca.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["temperature_2m", "relative_humidity_2m", "dew_point_2m", "precipitation", "rain", "surface_pressure", "cloud_cover", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_100m", "wind_direction_10m", "wind_gusts_10m", "soil_moisture_0_to_7cm", "soil_moisture_7_to_28cm"])
    for row in weathers:
        writer.writerow(row)