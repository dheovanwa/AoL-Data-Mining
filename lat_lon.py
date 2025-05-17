import pandas as pd
import requests
import csv

from requests.structures import CaseInsensitiveDict
df = pd.read_csv('./prov.csv')

prov = df.iloc[:, 0].values
kab_kota = df.iloc[:, -1].values

lat_lon = []

for i in range(len(prov)):
    address = f"{prov[i]}, {kab_kota[i]}"

    url = f"https://api.geoapify.com/v1/geocode/search?text={address}&apiKey=21a55303fd2e4e869ee4f0d73ee667ee"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)
    data = resp.json()

    latitude = data["features"][0]["geometry"]["coordinates"][1]
    longitude = data["features"][0]["geometry"]["coordinates"][0]

    print(f"data ke-{i+2}: {latitude}, {longitude}")
    lat_lon.append([latitude, longitude])


with open("coordinates.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Latitude", "Longitude"])
    for row in lat_lon:
        writer.writerow(row)