import sys
import time
import json
import joblib
import random
import os.path
import numpy as np
import matplotlib.pyplot as plt
from DataLoader import DataLoader
from Utils import datetime64_to_lontime

model_save_path = "modelsaves_backup/"
loader = DataLoader(verbose=False)

def get_gp_model(dataset, aid, filename_suffix):
    path = model_save_path + dataset + "/" + str(aid) + filename_suffix + "/gp_model.pkl"
    while not os.path.isfile(path):
        print "gp model file missing: " + path
        time.sleep(3)
    return joblib.load(path)

dataset = "landreg"
typs = [("F", "D"), ("F", "F"), ("F", "S"), ("F", "T"),
        ("L", "D"), ("L", "F"), ("L", "S"), ("L", "T")]


total, within_5, within_10, within_20 = 0, 0, 0, 0

aids = [int(round(random.random() * 5425)) for x in range(1000)]

print "Getting stats"

for aid in aids:

    area_data = loader.load_data_for_aid(dataset, aid)
    test_data = area_data.sample(1)
    gp_model = get_gp_model(dataset, aid, "")

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
        for i in range(len(test_y)):
            err = abs(test_y[i] - pred_y[i])
            if err <= 0.05 * test_y[i]:
                within_5 += 1
            if err <= 0.1 * test_y[i]:
                within_10 += 1
            if err <= 0.2 * test_y[i]:
                within_20 += 1
            total += 1

print "Finished!"
print total
print within_5
print within_10
print within_20

    


#     \mathbf{x} \mapsto y = f(\mathbf{x}), 

# f(\mathbf{x}) \sim  GP(\mathbb{E}[f(\mathbf{x})], k(\mathbf{x}, \mathbf{x}'))

# k(\mathbf{x},\mathbf{x}') = \mathbb{E}[(f(\mathbf{x})-\mathbb{E}[f(\mathbf{x})])(f(\mathbf{x}')-\mathbb{E}[f(\mathbf{x}')])]


