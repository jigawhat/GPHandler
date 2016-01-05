import json
import pandas as pd
from Utils import lontime_to_datetime64

# Use "local" or "remote" data source
data_source = "local" 

# Approx. lat, lng units for london elevation
lat_100m = 0.000900
lng_100m = 0.001450

class DataLoader(object):

    # Initialise by loading in postcode co-ordinates csv (used for area search)
    def __init__(self):
        self.datasets = {}
        self.area_dbs = {
            "landreg": {}
        }

        print("Using data source: %s" % data_source)
        data_config_file = open('data_config.json')                       
        data_config = json.load(data_config_file)
        coord_data_file = str(data_config["coord_data"][data_source])
        landreg_data_file = str(data_config["landreg_data"][data_source])

        print("Loading coord data from: %s" % coord_data_file)
        self.coord_data = pd.read_csv(coord_data_file)

        print("Loading London Land Registry data from: %s" % landreg_data_file)
        self.datasets["landreg"] = self.load_dataset(landreg_data_file)

        print("Loading model parameters databases")
        self.area_dbs["landreg"]["grid_squares"] = pd.read_csv("grid_squares_db.csv", index_col="id")
        self.area_dbs["landreg"]["postcode_areas"] = pd.read_csv("postcode_areas_db.csv", index_col="postcode")

    # Loads a csv dataset, assuming it has labeled columns date, price
    def load_dataset(self, csv_path):
        dataset = pd.read_csv(csv_path, parse_dates=['date'], index_col=['date'])
        dataset['price'] = dataset['price'].astype(int)
        return dataset

    # Load data for an area id
    def load_data_for_aid(self, dataset, aid):
        aid, _ = self.normalise_area_id_and_get_db_name(aid)
        params = self.load_params_for_aid(dataset, aid)
        return self.load_data_for_params(dataset, aid, params)

    # Load params for an area id
    def load_params_for_aid(self, dataset, aid):
        aid, db = self.normalise_area_id_and_get_db_name(aid)
        return self.area_dbs[dataset][db].loc[aid].to_dict()

    # Load data for given params
    def load_data_for_params(self, dataset, aid, params):
        aid, db = self.normalise_area_id_and_get_db_name(aid)
        df = None
        if(db == "postcode_areas"):
            df = self.load_data_for_postcode(dataset, aid)
        else:
            # Request is for a grid square
            lat, lng, size = float(params['lat']), float(params['lng']), float(params['size'])
            df = self.load_data_for_lat_lng_size(dataset, lat, lng, size)
        # Select data within given start and end dates (if given)
        if("start_date" in params):
            df = df[df.index >= lontime_to_datetime64(float(params["start_date"]))]
        if("end_date" in params):
            df = df[df.index < lontime_to_datetime64(float(params["end_date"]))]
        return df

    # Get subset of data for a postcode prefix
    def load_data_for_postcode(self, dataset, pc):
        if(pc[-1:] != ' '):
            pc = pc + ' '
        return self.datasets[dataset][(self.datasets[dataset]['postcode'].str[:len(pc)] == pc)]

    # Get subset of data for a given grid square
    def load_data_for_grid_square(self, dataset, aid):
        params = self.load_params_for_aid(dataset, aid)
        return self.load_data_for_params(dataset, aid, params)

    # Get subset of data for given lat, lng, size
    def load_data_for_lat_lng_size(self, dataset, lat, lng, size):
        size_100m = 1.0 * size / 100.0
        size_lat = lat_100m * size_100m
        size_lng = lng_100m * size_100m
        lat_min = float(lat) - (size_lat / 2.0)
        lng_min = float(lng) - (size_lng / 2.0)
        pcs = self.coord_data[(self.coord_data['long'] >= lng_min) & (self.coord_data['long'] < lng_min + size_lng) &
                               (self.coord_data['lat'] >= lat_min) & (self.coord_data['lat'] < lat_min + size_lat)]['postcode']
        return self.datasets[dataset].query("postcode == " + str(list(pcs)))

    # Normalise area id and get db name
    def normalise_area_id_and_get_db_name(self, aid):
        if self.is_postcode(aid):
            return aid, "postcode_areas"
        return int(float(aid)), "grid_squares"

    # Return whether the given area id is a postcode (otherwise it's a grid square id)
    def is_postcode(self, aid):
        return str(aid)[0].isalpha()


