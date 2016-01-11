import os
import sys
import time
import json
import joblib
import shutil
import numpy as np
from DataLoader import DataLoader
from Utils import datetime64_to_lontime, lontime_to_datetime64
from GPRequester import submit_gp_request
from Plot3d import plot_predictions

model_save_path = "modelsaves/"
loader = DataLoader()

def get_gp_model(dataset, aid, filename_suffix):
    path = model_save_path + dataset + "/" + str(aid) + filename_suffix + "/gp_model.pkl"
    while not os.path.isfile(path):
        time.sleep(3)
    return joblib.load(path)


typs = [("F", "D"), ("F", "F"), ("F", "S"), ("F", "T"),
        ("L", "D"), ("L", "F"), ("L", "S"), ("L", "T")]

dataset = "landreg"
folds = [2013, 2012, 2011]
log_scales = [0.0, 1.6666666, 2.0, 3.3333333, 4.0, 7.0, 10.0, 15.0, 20.0]

min_year = 1995
max_year = 2019
granularity = float(1)/float(12)
steps = (max_year-min_year)*12 + 1
t = [(min_year + x * granularity) for x in range(0, steps)]

for aid in [1923]:

    area_data = loader.load_data_for_aid(dataset, aid)

    paths = []
    for fold in folds:
        for i in range(len(log_scales)):
            fn_suffix = "_" + str(fold) + "_" + ("normal" if i == 0 else ("logadj_sc" + str(i)))
            request = {
                "dataset": dataset,
                "id": str(aid),
                "params": {
                    "filename_suffix": fn_suffix,
                    "end_date": fold,
                    "logadj": 0.0 if i == 0 else 1.2,
                    "log_scaling": log_scales[i]
                }
            }
            path = model_save_path + dataset + "/" + str(aid) + fn_suffix + "/gp_model.pkl"
            if not os.path.isfile(path):
                submit_gp_request(request)
                paths.append(path)

    # for path in paths:
    #     if os.path.isfile(path):
    #         os.remove(path)
    time.sleep(1)
    i = 0
    while any(map(lambda x: not os.path.isfile(x), paths)):
        i += 10
        time.sleep(10)
        print i
    time.sleep(1)

    results = None
    gp_models = {}
    for lsi in range(len(log_scales)):
        plls, ses = [], []
        gp_models[lsi] = {}
        for fold in folds:
            fn_suffix = "_" + str(fold) + "_" + ("normal" if lsi == 0 else ("logadj_sc" + str(lsi)))
            gp_model = get_gp_model(dataset, aid, fn_suffix)
            test_data = area_data[(area_data.index >= lontime_to_datetime64(float(fold))) & \
                                  (area_data.index < lontime_to_datetime64(float(fold + 3)))]
            for et, pt in typs:
                test_data_for_type = test_data[(test_data['property_type']==pt) & \
                                               (test_data['estate_type']==et)]
                if len(test_data_for_type) < 1:
                    continue
                test_x_list = map(datetime64_to_lontime, test_data_for_type.index.values)
                test_x = np.atleast_2d(test_x_list).T
                test_y = test_data_for_type['price'].values.ravel()
                request = {
                    "dates": test_x_list,
                    "property_type": pt,
                    "estate_type": et
                }
                pred_y, sigmas = gp_model.predict(request)
                for i in range(len(test_x)):
                    se = (test_y[i] - pred_y[i]) ** 2
                    ses.append(se)
                    s = sigmas[i] ** 2
                    pll = (-1/2 * np.log(2 * np.pi * s)) - (se / (2 * s))
                    plls.append(pll)
        rmse = np.sqrt(sum(ses)/len(ses))
        mpll = np.mean(plls)
        res = np.array([[lsi, mpll, rmse]])
        results = res if lsi == 0 else np.concatenate(results, res)
    
    max_mpll_i = np.argmax(results[:, 1])
    min_rmse_i = np.argmin(results[:, 2])

    max_rmse_i = np.argmax(results[:, 2])
    min_mpll_i = np.argmin(results[:, 1])

    print
    print "Max mpll: " + str(results[max_mpll_i])
    print "Min rmse: " + str(results[min_rmse_i])
    print 
    print "Max rmse: " + str(results[max_rmse_i])
    print "Min mpll: " + str(results[min_mpll_i])
    print

    graph_res_is = [ max_mpll_i, min_rmse_i, max_rmse_i, min_mpll_i ]

    for i in graph_res_is:
        for fold in folds:
            lsi = results[i][0]
            area_data_flats = area_data[(area_data["property_type"]=="F") & (area_data["estate_type"]=="L")]
            data_x = np.atleast_2d(map(datetime64_to_lontime, area_data_flats.index.values)).T
            data_y = area_data_flats['price'].values.ravel()
            request = {
                "dates": t,
                "property_type": "F",
                "estate_type": "L"
            }
            fn_suffix = "_" + str(fold) + "_" + ("normal" if lsi == 0 else ("logadj_sc" + str(lsi)))
            gp_model = get_gp_model(dataset, aid, fn_suffix)
            pred_y, sigmas = gp_model.predict(request)
            name = dataset + "_" + str(aid) + fn_suffix
            plot_predictions(pred_y, sigmas, t, datapoints=(data_x, data_y), name=name, vert_line_x=float(fold))

