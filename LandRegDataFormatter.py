import math
import pandas as pd
import numpy as np
from Utils import datetime64_to_tinynoised_lontime
from DataFormatter import DataFormatter

class LandRegDataFormatter(DataFormatter):

    def __init__(self, params):
        self.logadj = float(params['logadj'])
        self.price_scaling_factor = 1e-5
        self.pt_map = {
            "F": [0, 0, 0],
            "T": [1, 0, 0],
            "S": [0, 1, 0],
            "D": [0, 0, 1]
        }
        self.et_map = {
            "L": 0,
            "F": 1
        }

    def format_X_y(self, df):
        # Check we have some data in the df
        if(len(df) < 1):
            return None

        # Return variance for 2003 onwards data
        y_2003 = df[df.index > np.datetime64('2003-01-01T00:00:00Z')]['price'].values.ravel()
        y_2003 = (map(lambda x: math.log(x, self.logadj), y_2003) if self.logadj else y_2003) * self.price_scaling_factor
        post_2003_variance = np.var(y_2003)

        # If dataframe contains more than 2000 entries, select a random sample of them,
        # but without removing any entries for rare property/estate types combinations
        max_datapoints = 1100 # Max datapoints for each property/estate type combination
        while(len(df) > 2000 and max_datapoints > 0):
            max_datapoints -= 100
            type_counts = df.groupby(('estate_type', 'property_type')).size()
            type_indexes = type_counts.index.values
            partitions = []
            for i in range(0, len(type_counts)):
                partition = df[(df['estate_type'].str[:] == type_indexes[i][0]) & \
                             (df['property_type'].str[:] == type_indexes[i][1])]
                if(len(partition) > max_datapoints):
                    partition = partition.sample(max_datapoints)
                partitions.append(partition)
            df = pd.concat(partitions)

        # Format dataframe into X, y input
        dates = np.atleast_2d(map(datetime64_to_tinynoised_lontime, df.index.values)).T
        p123 = map(self.map_property_type, df['property_type'])
        e1 = np.atleast_2d(map(self.map_estate_type, df['estate_type'])).T
        X = np.concatenate((dates, p123, e1), axis=1)
        y = df['price'].values.ravel()
        y = (map(lambda x: math.log(x, self.logadj), y) if self.logadj else y) * self.price_scaling_factor

        return X, y, post_2003_variance

    # Format input X
    def format_X(self, X):
        years_range = X["end_date"] - X["start_date"]
        dates = np.atleast_2d([X["start_date"] + x for x in np.arange(0, years_range, 1.0/12)]).T
        return [[ date[0], self.pt_map[X["property_type"]],
                           self.et_map[X["estate_type"]]] for date in dates]

    # Correct and format output prices
    def format_y_sigma(self, y, sigma):
        price_preds_gbp = map(lambda x: int(x), (y / self.price_scaling_factor))
        sigma_gbp = map(lambda x: int(x), sigma / self.price_scaling_factor)
        return list([price_preds_gbp, sigma_gbp])

    def map_property_type(self, p_type):
        return self.pt_map[p_type]
    def map_estate_type(self, e_type):
        return self.et_map[e_type]



