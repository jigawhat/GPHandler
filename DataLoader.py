import json

import re
import pandas as pd

# Use "local" or "remote" data source
data_source = "remote" 

class DataLoader(object):

    # Initialise by loading in postcode co-ordinates csv (used for area search)
    def __init__(self):
        config_file = open('data_config.json')                       
        config = json.load(config_file)

        data_file = str(config["coord_data"][data_source]) 

        print("Using data source: %s" % data_source)
        print("Loading data from: %s" % data_file)
        
        self.coord_data = pd.read_csv(data_file)

    # Loads a csv dataset, assuming it has labeled columns date, price, estate_type
    def load_dataset(self, csv_path):
        dataset = pd.read_csv(csv_path, parse_dates=['date'], index_col=['date'])
        dataset = dataset[(dataset['estate_type'].str[:] != "U")]
        dataset['price'] = dataset['price'].astype(int)
        return dataset

    # Get subset of data for a given area (postcode or co-ordinates string)
    # Assumes data has column 'postcode'
    def load_data_for_area(self, data, area):
        # Check if area is a lat_lng_size and not a postcode (first character is a non-letter)
        if(re.compile(r'^[a-zA-Z]').match(area[0]) == None):
            return self.load_data_for_lat_lng(data, area)
        # Return data for the postcode
        return data[(data['postcode'].str[:len(area)] == area)]

    # Get subset of data for given lat_lng_size string
    def load_data_for_lat_lng(self, data, lat_lng_size):
        latlng_str = lat_lng_size   .split(" ")
        side_len_metres_over_100 = float(latlng_str[2]) / 100.0
        side_len_lat = lat_100m * side_len_metres_over_100
        side_len_lng = lng_100m * side_len_metres_over_100
        lat_min = float(latlng_str[0]) - (side_len_lat / 2.0)
        lng_min = float(latlng_str[1]) - (side_len_lng / 2.0)
        pcs = self.coord_data[(self.coord_data['long'] >= lng_min) & (self.coord_data['long'] < lng_min + side_len_lng) &
                          (self.coord_data['lat'] >= lat_min) & (self.coord_data['lat'] < lat_min + side_len_lat)]['postcode']
        return data.query("postcode == " + str(list(pcs)))
