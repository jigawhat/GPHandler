import numpy as np
import matplotlib.pyplot as plt
from DataLoader import DataLoader
from GPRequester import submit_gp_request

loader = DataLoader()

def get_gp_model(dataset, aid):
    return joblib.load(model_save_path + dataset + "/" + str(aid) + "/gp_model.pkl")

def get_predictions(request):
    gp_model = get_gp_model(request["dataset"], request["id"])
    return gp_model.predict(request)

def test_gp_model_fold(dataset, aid, fold_year):
    params = loader.load_params_for_aid(dataset, aid)
    test_params["start_date"] = fold_year
    test_data = loader.load_data_for_params(dataset, aid, params)









test_params = params.copy()
    test_params["end_date"] = 3000
    