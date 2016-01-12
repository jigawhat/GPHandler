import sys
import time
import json
import joblib
import os.path
import numpy as np
# import mpld3
# from mpld3 import plugins
import matplotlib.pyplot as plt
from DataLoader import DataLoader
from Utils import datetime64_to_lontime

model_save_path = "modelsaves/"
pred_save_path = "predsaves/"
loader = DataLoader(verbose=False)

# Define some CSS to control our custom labels
css = """
html
{
  font-family:Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
  color: #ffffff;
  background-color: #000000;
}
"""

def get_gp_model(dataset, aid, filename_suffix):
    path = model_save_path + dataset + "/" + str(aid) + filename_suffix + "/gp_model.pkl"
    while not os.path.isfile(path):
        time.sleep(3)
    return joblib.load(path)

def plot_predictions(price_preds, sigmas, dates, datapoints=None, name="", vert_line_x=None):
    price_preds, sigmas, t = np.asarray(price_preds), np.asarray(sigmas), np.asarray(dates)
    fig = plt.figure()
    # fig.set_size_inches(18, 11)
    fig.subplots_adjust(left=0.17, bottom=0.05, right=0.95, top=0.95)
    pred_plot = plt.plot(t, price_preds, color='red', ls='-', lw=1, label="Price Prediction")

    if(datapoints != None):
        d_dates, d_prices = datapoints
        data_plot = plt.plot(d_dates, d_prices, 'x', color='blue', ls='', label="Price Data")

    if(vert_line_x != None):
        vert_line_plot = plt.axvline(vert_line_x, color='r', linestyle='--')

    plt.fill(np.concatenate([t, t[::-1]]),
             np.concatenate([(price_preds - 1.9600 * sigmas),
                             (price_preds + 1.9600 * sigmas)[::-1]]),
             alpha=.15, fc='#000000', ec='None', label='95% confidence interval')
    # plt.title("Price vs. Time")
    plt.ylabel('Price (' + u"\xA3" + ')')
    fig.savefig("graphs/p_vs_t_" + str(name) + ".png")
    # tooltip = plugins.PointLabelTooltip(pred_plot[0], labels=map(str, list(price_preds)))
    # plugins.connect(fig, tooltip)
    # plugins.connect(fig, plugins.Reset(), plugins.Zoom(), plugins.BoxZoom(), tooltip)
    # plt.show()
    plt.close('all')

form = [("F", "D", "Freehold Detached", 'r', '--', 2, 'x'),
        ("F", "F", "Freehold Flats", 'g', '--', 2, 'o'),
        ("F", "S", "Freehold Semi-detached", 'c', '--', 2, 'x'),
        ("F", "T", "Freehold Terraces", 'b', '--', 2, 'x'),
        ("L", "D", "Lease Detached", 'r', '-', 1, 'o'),
        ("L", "F", "Lease Flats", 'g', '-', 1, '+'),
        ("L", "S", "Lease Semi-detached", 'c', '-', 1, 'o'),
        ("L", "T", "Lease Terraces", 'b', '-', 1, 'o')]

def plot_all(dataset, aid, fn_suffix):

    #gp_model = get_gp_model(dataset, aid, fn_suffix)
    predictions = None
    predictions_file = open(pred_save_path + dataset + "/" + str(aid) + fn_suffix + '.json')                       
    predictions = json.load(predictions_file)
    area_data = loader.load_data_for_aid(dataset, aid)

    fig = plt.figure()
    # fig.set_size_inches(18, 11)
    fig.subplots_adjust(left=0.17, bottom=0.05, right=0.95, top=0.95)
    plots = []

    # Get dates for prediction line generation
    min_year = 1995
    max_year = 2019
    granularity = float(1)/float(12)
    steps = (max_year-min_year)*12 + 1
    t = [(min_year + x * granularity) for x in range(0, steps)]

    # Add data and prediction plots for each property/estate type combination
    for et, pt, label, col, linestyle, linewidth, ico  in form:
        preds = predictions[pt][et]
        price_pred, sigma = np.asarray(preds["price_preds"]), np.asarray(preds["sigmas"])
        area_data_for_type = area_data[(area_data['property_type']==pt) & \
                                       (area_data['estate_type']==et)]
        d_dates = np.atleast_2d(map(datetime64_to_lontime, area_data_for_type.index.values)).T
        d_prices = area_data_for_type['price'].values.ravel()
        dot_style = col + ico
        line_col = col
        if(line_col == 'g'):
            line_col = '#00FF00'
        pred_plot, = plt.plot(t, price_pred, color=line_col, ls=linestyle, lw=linewidth, label=label + " Prediction")
        data_plot, = plt.plot(d_dates, d_prices, dot_style, ls='', label=label)
        plots.append(pred_plot)
        plots.append(data_plot)
        plt.fill(np.concatenate([t, t[::-1]]),
                 np.concatenate([(price_pred - 1.9600 * sigma),
                                 (price_pred + 1.9600 * sigma)[::-1]]),
                 alpha=.15, fc=col, ec='None', label='95% confidence interval')

    # Draw graph
    plt.legend(handles=plots, loc="upper left", fontsize=10)
    plt.title("Price vs. Time")
    plt.ylabel('Price (' + u"\xA3" + ')')
    fig.savefig('graphs/p_vs_t_' + str(aid) + fn_suffix + "_.png")
    # mpld3.show()
    plt.close('all')

# first = int(float(sys.argv[1])) if(len(sys.argv) > 1) else 0
# last = int(float(sys.argv[2])) if(len(sys.argv) > 2) else 0
# fn_suffix = sys.argv[3] if(len(sys.argv) > 3) else ""

# min_year = 1995
# max_year = 2019
# granularity = float(1)/float(12)
# steps = (max_year-min_year)*12 + 1
# dates = [(min_year + x * granularity) for x in range(0, steps)]

# for aid in range(first, last + 1):
#     predictions_file = open(pred_save_path + "landreg" + "/" + str(aid) + fn_suffix + '.json')                       
#     predictions = json.load(predictions_file)
#     plot_predictions(predictions["F"]["L"]["price_preds"], predictions["F"]["L"]["sigmas"], dates, name="yes", vert_line_x=2016.0)
