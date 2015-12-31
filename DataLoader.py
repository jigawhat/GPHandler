import json
import pandas as pd

# Use "local" or "remote" data source
data_source = "local" 

# Approx. lat, lng units for london elevation
lat_100m = 0.000900
lng_100m = 0.001450

class DataLoader(object):

    # Initialise by loading in postcode co-ordinates csv (used for area search)
    def __init__(self):
        config_file = open('data_config.json')                       
        config = json.load(config_file)
        data_file = str(config["coord_data"][data_source]) 

        print("Using coord data source: %s" % data_source)
        print("Loading coord data from: %s" % data_file)
        
        self.coord_data = pd.read_csv(data_file)

    # Loads a csv into a dataframe
    def load_csv(self, csv_path, **kwargs):
        return pd.read_csv(csv_path, **kwargs)

    # Loads a csv dataset, assuming it has labeled columns date, price
    def load_dataset(self, csv_path):
        dataset = pd.read_csv(csv_path, parse_dates=['date'], index_col=['date'])
        dataset['price'] = dataset['price'].astype(int)
        return dataset

    # Get subset of data for a postcode prefix
    def load_data_for_postcode(self, data, pc):
        if(pc[-1:] != ' '):
            pc = pc + ' '
        return data[(data['postcode'].str[:len(pc)] == pc)]

    # Get subset of data for given lat, lng, size
    def load_data_for_lat_lng_size(self, data, lat, lng, size):
        size_100m = 1.0 * size / 100.0
        size_lat = lat_100m * size_100m
        size_lng = lng_100m * size_100m
        lat_min = float(lat) - (size_lat / 2.0)
        lng_min = float(lng) - (size_lng / 2.0)
        pcs = self.coord_data[(self.coord_data['long'] >= lng_min) & (self.coord_data['long'] < lng_min + size_lng) &
                               (self.coord_data['lat'] >= lat_min) & (self.coord_data['lat'] < lat_min + size_lat)]['postcode']
        return data.query("postcode == " + str(list(pcs)))
