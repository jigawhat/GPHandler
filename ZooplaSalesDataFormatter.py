import math
import pandas as pd
import numpy as np
from Utils import datetime64_to_tinynoised_lontime
from DataFormatter import DataFormatter

class ZooplaSalesDataFormatter(DataFormatter):

    def __init__(self, params):
        self.logadj = float(params['logadj'])
        self.price_scaling_factor = 1e-6
        self.log_scaling = 10.0
        if 'log_scaling' in params:
            self.log_scaling = float(params['log_scaling'])
        self.pt_map = {
            "F": [0, 0, 0],
            "T": [1, 0, 0],
            "S": [0, 1, 0],
            "D": [0, 0, 1]
        }

    def format_X_y(self, df):
        # Check we have some data in the df
        if(len(df) < 1):
            return None

        # If dataframe contains more than 2000 entries, remove excess data from those
        # property/estate type combinations with the most entries (thus preserving the
        # data for rarer property/estate type combinations). Starting with a max number
        # of datapoints for each type combination of 1050, take random samples of these
        # bloated type combinations, lowering the max datapoints by 50 each
        # iteration, until we have less than 2000 datapoints overall
        max_datapoints = 1100
        while(len(df) > 2000 and max_datapoints > 0):
            max_datapoints -= 50
            type_counts = df.groupby(('property_type', 'num_bathrooms', 'num_bedrooms', 'num_floors', 'num_recepts')).size()
            type_indexes = type_counts.index.values
            partitions = []
            for i in range(0, len(type_counts)):
                partition = df[(df['property_type'].str[:] == type_indexes[i][0]) & \
                               (df['num_bathrooms'].str[:] == type_indexes[i][1])
                               (df['num_bedrooms'].str[:] == type_indexes[i][2])
                               (df['num_floors'].str[:] == type_indexes[i][3])
                               (df['num_recepts'].str[:] == type_indexes[i][4])]
                if(len(partition) > max_datapoints):
                    partition = partition.sample(max_datapoints)
                partitions.append(partition)
            df = pd.concat(partitions)

        # Format dataframe into X, y input
        dates = np.atleast_2d(map(datetime64_to_tinynoised_lontime, df.index.values)).T
        p123 = map(lambda x: self.pt_map[x], df['property_type'])
        n_bath = np.atleast_2d(map(float, df['num_bathrooms'])).T
        n_bed = np.atleast_2d(map(float, df['num_bedrooms'])).T
        n_flo = np.atleast_2d(map(float, df['num_floors'])).T
        n_rec = np.atleast_2d(map(float, df['num_recepts'])).T
        X = np.concatenate((dates, p123, n_bath, n_bed, n_flo, n_rec), axis=1)
        y = df['price'].values.ravel()
        self.price_scaling_factor = 0.3 / np.mean(y)
        if self.logadj:
            self.price_scaling_factor *= self.log_scaling
        y = y * self.price_scaling_factor
        if self.logadj:
            y = np.vectorize(lambda x: math.log(x, self.logadj))(y)

        # Return variance for 2003 onwards data
        y_2003 = df[df.index > np.datetime64('2003-01-01T00:00:00Z')]['price'].values.ravel()
        y_2003 = y_2003 * self.price_scaling_factor
        if self.logadj:
            y_2003 = np.vectorize(lambda x: math.log(x, self.logadj))(y_2003)
        post_2003_variance = np.var(y_2003)

        return X, y, post_2003_variance

    # Format input X
    def format_X(self, params):
        X = []
        if "date_range" in params:
            start, stop, step_fraction = map(float, params["date_range"])
            X = np.linspace(start, stop, ((stop-start)*step_fraction) + 1)
        else:
            X = map(float, params["dates"])
        X = np.atleast_2d(X).T
        pt_arr = np.atleast_2d([self.pt_map[params["property_type"]]] * len(X))
        n_bath = np.atleast_2d([float(params["num_bathrooms"])] * len(X)).T
        n_bed = np.atleast_2d([float(params["num_bedrooms"])] * len(X)).T
        n_flo = np.atleast_2d([float(params["num_floors"])] * len(X)).T
        n_rec = np.atleast_2d([float(params["num_recepts"])] * len(X)).T
        return np.concatenate((X, pt_arr, n_bath, n_bed, n_flo, n_rec), axis=1)

    # Correct and format output prices
    def format_y_sigma(self, y, sigma):
        if self.logadj:
            y = self.logadj ** y
            sigma = self.logadj ** sigma
        price_preds_gbp = np.vectorize(lambda x: int(x))(y / self.price_scaling_factor)
        sigma_gbp = np.vectorize(lambda x: int(x))(sigma / self.price_scaling_factor)
        return price_preds_gbp, sigma_gbp



