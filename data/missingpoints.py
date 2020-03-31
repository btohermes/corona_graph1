import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

#df = pd.read_csv('map1_points_not_removed_v1_hermes.csv')

def drop_missplaced_points (df):

    # Importing and plotting the cities shapefile
    gdf = gpd.read_file("shapes_files/shapes_europe/Europe.shp")
    gdf.plot(cmap='OrRd', figsize = (15,10))
    plt.xlim(xmax = -6, xmin = -10)
    plt.ylim(ymax = 42.5, ymin = 36.5)

    # Changes the MULTIPOLYGON to Polygons
    gs = gdf.explode()
    gs_portugal = gs.loc[gs['ORGN_NAME'] == 'Portugal',:]

    #Locate just Portugal
    gs_portugal_part = gs_portugal.iloc[34:35,:]
    gs_portugal_shape = gs_portugal_part['geometry'][0]

    #Remove missplaced points:
    drop_rows = []

    for i in range(df.shape[0]):
        inside_region = Point(df['Longitude'][i], df['Latitude'][i]).within(gs_portugal_shape)
        if (inside_region == False):
            drop_rows.append(i)
    df = df.drop(drop_rows)

    return df


