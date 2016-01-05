import joblib

model_save_path = "modelsaves/"

def get_gp_model(dataset, aid):
    return joblib.load(model_save_path + dataset + "/" + str(aid) + "/gp_model.pkl")

def get_predictions(request):
    gp_model = get_gp_model(request["dataset"], request["id"])
    return gp_model.predict(request)

area_id = "SW7" # Postcode prefix
area_id = 3247  # Grid square id

request = {
    "dataset": "landreg",
    "id": area_id,

    "date_range": [1995, 2019, 12], # (start, stop, year fraction)
    # OR
    "dates": [ 2015.0, 2015.5, 2016.0, 2016.5 ],
    # (date_range will be preferred over dates list if both are present)

    "property_type": "F",
    "estate_type": "L"
}

# Returns array of predictions and array of sigmas
price_preds, sigmas = get_predictions(request)

print len(price_preds)
