#@ Used from the week 30 mar
print("#===Stay Alert===#")

from datetime import datetime
import numpy as np
import pandas as pd
import json
import geopandas as gpd
import unidecode
import copy
from shapely.geometry import Point, Polygon

from missingpoints import drop_missplaced_points

FileName="map1_points_removed_v1.geojson"

data = pd.read_excel("raw_data/cases_complete_v1.xlsx")
data.drop("Unnamed: 0.1", axis=1, inplace=True)
data_geo = gpd.read_file("raw_data/concelhos.json")

#=== Declare functions ===#
def feature(data):
      """ This generates a dictionary of the feature to
      be put in the geojson
      """
      return {
          "type":"Feature",
          "properties":{
              "Data":"2020-03-18",
              "Type":data.ProvinceName,
              "Title":data.FreguesiaName,
            },
          "geometry":{
              "type":"Point",
              "coordinates":[
                  data.Longitude,
                  data.Latitude
              ],
          },
          "id": "ak0203bdgzrh"
      }

#=== Axiliar DataFrames and Lists===#
data_types = data.dtypes
data_shape = data.shape


#=== Separate the multiple cases ===#
# @ Rule: See the number of new cases for that region
# @ Create duplicated in new dataframe the first and second reccords are the original
# @ The others are random generated values  in order to simulate data everywhere
cases_manual_extended = []
for i, row in data.iterrows():
    nr_total_cases = row["Number of Infected"]
    for j in range(0,nr_total_cases):
        row_copy = copy.deepcopy(row)
        cases_manual_extended.append(row_copy)
        print(f"{len(cases_manual_extended)} reccord updated")

cases_sep = pd.DataFrame(cases_manual_extended)
#=== Randomize the points ===#
cases_sep['rand1'] = 0
cases_sep['rand2'] = 0
cases_sep.loc[cases_sep["ProvinceName"] != "HOSPITAL",'rand1'] = np.random.randint(-100,100,size=(cases_sep.loc[cases_sep["ProvinceName"] != "HOSPITAL",:].shape[0],)) / 3333
cases_sep.loc[cases_sep["ProvinceName"] != "HOSPITAL",'rand2'] = np.random.randint(-100,100,size=(cases_sep.loc[cases_sep["ProvinceName"] != "HOSPITAL",:].shape[0],)) / 3333
cases_sep["Longitude"] = cases_sep["Longitude"] + cases_sep["rand1"]
cases_sep["Latitude"] = cases_sep["Latitude"] + cases_sep["rand2"]


# Have to do this to make it work
cases_sep.to_csv('map1.csv')
#df = pd.read_csv('map1_points_not_removed_v1_hermes.csv')
cases_sep = pd.read_csv('map1.csv', low_memory=False)
cases_sep = drop_missplaced_points(cases_sep)
print('done')

# cases_sep.to_csv("file_friday_night_remove_point_water")
cases_manual_extended_separated_shape = cases_sep.shape
cases_manual_extended_separated_head = cases_sep.head()

features = []
for i, j in cases_sep.iterrows():
    print(i)
    features.append(feature(j))

print(f"Features length {len(features)}")

geoJSON_object = {
    "type": "FeatureCollection",
    "metadata": {
        "generated": 1584640843000
    },
    "features": features,
    "bbox":[
        -5.17,
        -42.7548,
        -2.76,
        179.7419,
        169.5996,
        617.35
    ]
}

geoJSON_string = json.dumps(geoJSON_object)
print(type(geoJSON_string))

with open(FileName, 'w', encoding='utf-8') as f:
    f.write(json.dumps(geoJSON_object))
print("Fini.")


# Remove the file we made tempereraly
import os
os.remove('map1.csv')


#===Write the Json only of the features===#
#
# features_json = json.dumps(features)
# with open(f"./feature_jsons/feature_v1.json", 'w', encoding='utf-8') as f:
#     f.write(features_json)
