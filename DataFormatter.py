import numpy as np

# Approx. lat, lng units for london elevation
lat_100m = 0.000900
lng_100m = 0.001450

class DataFormatter(object):

    def __init__(params):
        # Load params we need for formatting data
        self.property_type_mappings = params["property_type_mappings"]
        self.estate_type_mappings = params["estate_type_mappings"]
        self.max_n_samples = params["gp_params"]["max_n_samples"]
        self.price_zero_val = params["price_zero_val"]
        self.price_scaling_factor = params["price_scaling_factor"]

    def input_dataframe_to_X_y(dataframe):
        # Check we have some data in the dataframe
        if(len(dataframe) < 1 or len(dataframe) < self.max_n_samples):
            return None

        # Format price data (y)
        prices = dataframe['price'].values.ravel()
        y = (prices - self.price_zero_val) * self.price_scaling_factor

        # Format date, property type and estate type data (X)
        dates = np.atleast_2d(map(Utils.datetime64_to_tinynoised_lontime, dataframe.index.values)).T
        p_types = np.atleast_2d(map(lambda x: Utils.map_property_type(x, params["property_type_mappings"]), dataframe['property_type'])).T
        e_types = np.atleast_2d(map(lambda x: Utils.map_estate_type(x, params["estate_type_mappings"]), dataframe['estate_type'])).T
        X = np.concatenate((dates, p_types, e_types), axis=1)

    def output_y_sigma_to_prices_sigma_list(y, sigma):
        price_preds_gbp = map(lambda x: int(x), (y / self.price_scaling_factor) + self.price_zero_val)     # Correct prices
        sigma_gbp = map(lambda x: int(x), sigma / self.price_scaling_factor)

        return list([price_pred_gbp, sigma_gbp])
