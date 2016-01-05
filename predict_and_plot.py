import sys
import joblib
import numpy as np
import matplotlib.pyplot as plt
from DataLoader import DataLoader
from Utils import datetime64_to_lontime

area_id = sys.argv[1] if(len(sys.argv) > 1) else "SW5"
fn_suffix = sys.argv[2] if(len(sys.argv) > 2) else ""

model_save_path = "modelsaves/"
loader = DataLoader()

def get_gp_model(dataset, aid, filename_suffix):
    return joblib.load(model_save_path + dataset + "/" + aid + filename_suffix + "/gp_model.pkl")

# def get_predictions(gp_model, request):
#     filename_suffix = request["filename_suffix"] if "filename_suffix" in request else ""
#     gp_model = get_gp_model(request["dataset"], request["id"], filename_suffix)
#     return gp_model.predict(request)

form = [("F", "D", "Freehold Detached", 'r', '--', 2, 'x'),
        ("F", "F", "Freehold Flats", 'g', '--', 2, 'o'),
        ("F", "S", "Freehold Semi-detached", 'c', '--', 2, 'x'),
        ("F", "T", "Freehold Terraces", 'b', '--', 2, 'x'),
        ("L", "D", "Lease Detached", 'r', '-', 1, 'o'),
        ("L", "F", "Lease Flats", 'g', '-', 1, '+'),
        ("L", "S", "Lease Semi-detached", 'c', '-', 1, 'o'),
        ("L", "T", "Lease Terraces", 'b', '-', 1, 'o')]

def predict_and_plot_all(dataset, aid, fn_suffix):

    gp_model = get_gp_model(dataset, aid, fn_suffix)
    price_preds, sigmas = [], []

    fig = plt.figure()
    fig.set_size_inches(20, 12, forward=False)
    plots = []

    for typ in form:
        et, pt = typ[:2]

    

    # Load datapoints to plot
    area_data = loader.load_data_for_aid("landreg", aid)
    area_data_for_type = area_data[(area_data['property_type']==request["property_type"]) & \
                                   (area_data['estate_type']==request["estate_type"])]
    d_dates = np.atleast_2d(map(datetime64_to_lontime, area_data_for_type.index.values)).T
    d_prices = area_data_for_type['price'].values.ravel()

    # Load x values (dates) to plot predictions for
    X = []
    if "date_range" in request:
        start, stop, step_fraction = map(float, request["date_range"])
        X = np.linspace(start, stop, ((stop-start)*step_fraction) + 1)
    else:
        X = map(float, request["dates"])
    X = np.atleast_2d(X).T

    # Draw graph
    pred_plot, = plt.plot(X, price_preds, color="b", label="Price prediction")
    data_plot, = plt.plot(d_dates, d_prices, "x", ls='', label="Price data")
    plt.fill(np.concatenate([X, X[::-1]]),
             np.concatenate([(price_preds - 1.9600 * sigmas),
                             (price_preds + 1.9600 * sigmas)[::-1]]),
             alpha=.25, fc="b", ec='None', label='95% confidence interval')
    plt.legend(handles=[pred_plot], loc="upper left")
    plt.title("Price vs. Time")
    plt.ylabel('Price')
    fig.savefig('graphs/price_vs_time_' + aid + request["filename_suffix"] + ", " + \
                request["property_type"] + ", " + request["estate_type"] + ", " + \
                str(ll) + ", " + str(kernel) + "_.png")
    plt.show()



request = {
    "dataset": "landreg",
    "id": area_id,
    "date_range": [1995, 2019, 12],
    "property_type": "F",
    "estate_type": "L",
    "filename_suffix": fn_suffix
}

(price_preds, sigmas), ll, kernel = get_predictions(request)
plot_predictions(request, price_preds, sigmas, ll, kernel)


