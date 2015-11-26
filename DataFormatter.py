import numpy as np
from Utils import datetime64_to_tinynoised_lontime

# Approx. lat, lng units for london elevation
lat_100m = 0.000900
lng_100m = 0.001450

class DataFormatter(object):

    def __init__(self, params):
        # Load params we need for formatting data
        self.p_mappings = params["property_type_mappings"]
        self.e_mappings = params["estate_type_mappings"]
        self.p_mappings["U"] = float('NaN')
        self.e_mappings["U"] = float('NaN')
        self.max_n_samples = params["max_n_samples"]
        self.min_n_samples = params["min_n_samples"]
        self.price_zero_val = params["price_zero_val"]
        self.price_scaling_factor = params["price_scaling_factor"]

    def input_dataframe_to_X_y(self, dataframe):
        # Check we have some data in the dataframe
        if(len(dataframe) < 1 or len(dataframe) < self.min_n_samples):
            return None

        # Format price data (y)
        prices = dataframe['price'].values.ravel()
        y = (prices - self.price_zero_val) * self.price_scaling_factor

        # Format date, property type and estate type data (X)
        dates = np.atleast_2d(map(datetime64_to_tinynoised_lontime, dataframe.index.values)).T
        p_types = np.atleast_2d(map(lambda x: self.p_mappings[x], dataframe['property_type'])).T
        e_types = np.atleast_2d(map(lambda x: self.e_mappings[x], dataframe['estate_type'])).T
        X = np.concatenate((dates, p_types, e_types), axis=1)
        return X, y

    def format_input_X(self, X):
        years_range = X["end_date"] - X["start_date"]
        dates = np.atleast_2d([X["start_date"] + x for x in np.arange(0, years_range, 1.0/12)]).T
        return [[ date[0], self.p_mappings[X["property_type"]],
                           self.e_mappings[X["estate_type"]]] for date in dates]

    # Correct and format output prices
    def format_output_y_sigma(self, y, sigma):
        price_preds_gbp = map(lambda x: int(x), (y / self.price_scaling_factor) + self.price_zero_val)
        sigma_gbp = map(lambda x: int(x), sigma / self.price_scaling_factor)
        return list([price_preds_gbp, sigma_gbp])


