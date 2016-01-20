import os
import shutil
import joblib
from GPModel import GPModel
from DataLoader import DataLoader
from LandRegDataFormatter import LandRegDataFormatter

dataset = "landreg"
aid = 1000
loader = DataLoader(verbose=False)
params = loader.load_params_for_aid(dataset, aid)
train_data = loader.load_data_for_params(dataset, aid, params)
data_formatter = LandRegDataFormatter(params)

def test_fit_and_predict_gp_model():

    gp_model = GPModel(data_formatter)
    gp_model.fit(params, train_data)

    request = {
        "dates": [ 2015.0, 2015.5, 2016.0, 2016.5 ],
        "property_type": "F",
        "estate_type": "L"
    }
    price_preds, sigmas = gp_model.predict(request)

    assert price_preds[0] > 0.0 and price_preds[0] < 1e12
    assert sigmas[0] > 0.0 and sigmas[0] < 1e12

    request = {
        "date_range": [2010, 2012, 12],
        "property_type": "T",
        "estate_type": "F"
    }
    price_preds, sigmas = gp_model.predict(request)

    assert price_preds[0] > 0.0 and price_preds[0] < 1e12
    assert sigmas[0] > 0.0 and sigmas[0] < 1e12


