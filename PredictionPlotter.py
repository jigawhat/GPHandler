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
    return joblib.load(model_save_path + dataset + "/" + str(aid) + filename_suffix + "/gp_model.pkl")

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
    area_data = loader.load_data_for_aid(dataset, aid)

    fig = plt.figure()
    fig.set_size_inches(20, 12, forward=False)
    plots = []
    date_range = [1995, 2019, 12]
    request = {
        "dataset": dataset,
        "id": aid,
        "date_range": date_range,
        "filename_suffix": fn_suffix
    }

    # Load x values (dates) to plot predictions for
    start, stop, step_fraction = map(float, date_range)
    t = np.atleast_2d(np.linspace(start, stop, ((stop-start)*step_fraction) + 1)).T

    # Add data and prediction plots for each property/estate type combination
    for typ in form:
        et, pt, label, col, linestyle, linewidth, ico = typ
        request["property_type"] = pt
        request["estate_type"] = et
        price_pred, sigma = gp_model.predict(request)
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
                 alpha=.2, fc=col, ec='None', label='95% confidence interval')

    # Draw graph
    plt.legend(handles=plots, loc="upper left")
    plt.title("Price vs. Time")
    plt.ylabel('Price')
    fig.savefig('graphs/p_vs_t_' + str(aid) + fn_suffix + ", " + \
                str(round(gp_model.gpr.log_marginal_likelihood_value_)) + ", " + str(gp_model.gpr.kernel_) + "_.png")
    #plt.show()
    plt.close('all')


predict_and_plot_all("landreg", 2500, "")


