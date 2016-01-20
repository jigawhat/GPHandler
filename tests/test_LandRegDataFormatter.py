import os
import shutil
import joblib
import numpy as np
from Utils import lontime_to_datetime64
from GPModel import GPModel
from DataLoader import DataLoader
from LandRegDataFormatter import LandRegDataFormatter

dataset = "landreg"
aid = 1000
loader = DataLoader(verbose=False)
params = loader.load_params_for_aid(dataset, aid)
params["logadj"] = 1.2
params["log_scaling"] = 7.0
train_data = loader.load_data_for_params(dataset, aid, params).sample(10)
# test_y = 
df_size = len(train_data)

def test_initialisation():
    formatter = LandRegDataFormatter(params)

    assert formatter.logadj == params["logadj"]
    assert formatter.log_scaling == params["log_scaling"]

def test_format_X_y_for_empty_dataset():
    formatter = LandRegDataFormatter(params)
    result = formatter.format_X_y(train_data[train_data.index < lontime_to_datetime64(1900.0)])

    assert result == None

def test_format_X_y():
    formatter = LandRegDataFormatter(params)
    X, y, var = formatter.format_X_y(train_data)

    assert np.shape(X)[0] == df_size
    assert np.shape(y)[0] == df_size
    assert var > 0.0 and var < 1e12

def test_format_X_daterange():
    formatter = LandRegDataFormatter(params)
    request = {
        "date_range": [2010, 2012, 12],
        "property_type": "F",
        "estate_type": "L"
    }
    X = formatter.format_X(request)

    assert np.shape(X)[0] == 25

def test_format_X_dates_array():
    formatter = LandRegDataFormatter(params)
    request = {
        "dates": [ 2015.0, 2015.5, 2016.0, 2016.5 ],
        "property_type": "F",
        "estate_type": "L"
    }
    X = formatter.format_X(request)

    assert np.shape(X)[0] == 4

# def test_format_y_sigma():
#     formatter = LandRegDataFormatter(params)
#     price_pred, sigma = formatter.format_y_sigma(test_y, test_sigma)

#     assert np.shape(price_pred

