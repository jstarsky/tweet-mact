import os
import numpy as np
import pandas as pd
import glob
from geojson import Point, Feature, LineString, Polygon



def dir_os_db(wdir="db", os_system="WIN"):
    if os_system == "WIN":
        db_folder = "%s\\%s\\" % (os.getcwd(), wdir)
        db_csv = glob.glob("%s*.csv" % db_folder)
    elif os_system == "OSX":
        db_folder = "%s/%s/" % (os.getcwd(), wdir)
        db_csv = glob.glob("%s*.csv" % db_folder)
    else:
        db_folder = "%s/%s/" % (os.getcwd(), wdir)
        db_csv = glob.glob("%s*.csv" % db_folder)
    return db_csv

def classifier_search_tweets_loc():

    type_os = 'OSX'

    db_csv = dir_os_db(wdir="db_input", os_system=type_os)

    _search_tweets_loc = []

    for db in db_csv:
        try:
            df = pd.read_csv(db)
            list_counter_NEG = []
            list_counter_POS = []

            for index, row in df.iterrows():
                try:
                    coordinates_lon = float(row['LONGITUD'])
                    coordinates_lat = float(row['LATITUD'])

                    _db_csv = dir_os_db(wdir="db", os_system=type_os)

                    _counter_NEG = 0
                    _counter_POS = 0

                    for _db in _db_csv:
                        try:
                            _df = pd.read_csv(_db)

                            for index, row in _df.iterrows():
                                try:
                                    _coordinates_lon = float(row['_search_loc_lon'])
                                    _coordinates_lat = float(row['_search_loc_lat'])

                                    if float(coordinates_lon) == float(_coordinates_lon) and \
                                            float(coordinates_lat) == float(_coordinates_lat):

                                        if row['label'] == "NEG":
                                            _counter_NEG += 1
                                        elif row['label'] == "POS":
                                            _counter_POS += 1


                                except Exception as e:
                                    print(e, "-------")

                        except Exception as e:
                            print(e)

                    list_counter_NEG.append(_counter_NEG)
                    list_counter_POS.append(_counter_POS)

                except Exception as e:
                    print("%s: this search tweets has not localization" % e)

            series_counter_NEG = pd.Series(list_counter_NEG)
            series_counter_POS = pd.Series(list_counter_POS)

            df['counter_NEG'] = series_counter_NEG.values
            df['counter_POS'] = series_counter_POS.values
            print(df['counter_NEG'])
            df.to_csv(db, index=False)

        except Exception as e:
            print(e)

    db_csv = dir_os_db(wdir="db", os_system=type_os)

    _tweets_with_locations = []
    _tweets_without_locations = []


if __name__ == "__main__":
    classifier_search_tweets_loc()
