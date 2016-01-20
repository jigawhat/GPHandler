import sys
import time
import json
import joblib
import os.path
import numpy as np
from DataLoader import DataLoader
from Utils import datetime64_to_lontime

model_save_path = "modelsaves/"
loader = DataLoader()

def get_gp_model(dataset, aid, filename_suffix):
    path = model_save_path + dataset + "/" + str(aid) + filename_suffix + "/gp_model.pkl"
    while not os.path.isfile(path):
        time.sleep(3)
    return joblib.load(path)

typs = [("F", "D"),
        ("F", "F"),
        ("F", "S"),
        ("F", "T"),
        ("L", "D"),
        ("L", "F"),
        ("L", "S"),
        ("L", "T")]

ev_areas = [
    "1671_logadj",
    "1663_logadj",
    "1653",
    "1649_logadj",
    "1632_logadj",
    "1502",
    "833_logadj",
    "745_logadj",
    "1719_logadj",
    "1723_logadj",
    "1726",
    "1732_logadj",
    "1773",
    "1783",
    "1802",
    "1804",
    "1816_logadj",
    "1862_logadj",
    "1873",
    "1877",
    "1889_logadj",
    "1893",
    "1899_logadj",
    "1983_logadj",
    "1984",
    "1988_logadj",
    "1990",
    "1991",
    "1996_logadj",
    "2000_logadj"
]

ses = []

for i in range(len(ev_areas)):
    print "Area: " + ev_areas[i]
    aid_strs = ev_areas[i].split("_") 
    aid = int(aid_strs[0])
    fn_suffix = ("_" + aid_strs[1]) if len(aid_strs) >= 2 else ""

    gp_model = get_gp_model("landreg", aid, fn_suffix)
    area_data = loader.load_data_for_aid("landreg", aid)
    test_data = area_data.sample(34)

    # Add data and prediction plots for each property/estate type combination
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

print len(ses)
rmse = np.sqrt(sum(ses)/len(ses))
print rmse


