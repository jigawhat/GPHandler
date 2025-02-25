import json
import joblib
import Utils
import numpy as np
from GPModel import GPModel
from DataLoader import DataLoader
from LandRegDataFormatter import LandRegDataFormatter
from ZooplaSalesDataFormatter import ZooplaSalesDataFormatter
# from Plot3d import plot_predictions, plot_all

model_save_path = "modelsaves/"
pred_save_path = "predsaves/"
property_types = ["F", "T", "S", "D"]
estate_types = ["F", "L"]

class GPHandler(object):

    def __init__(self):
        self.loader = DataLoader(verbose=False)
    
    # Handle request (make sure it's a GP request)
    def handle_request(self, request):
        status = self.check_request(request)
        if(status != 200):
            return status
        # return self.status_response(500, "Request cancelled")
        return self.handle_gp_request(request)

    # Get training params and data for a given GP request
    def get_params_and_data(self, request):
        dataset, aid = request["dataset"], request["id"]
        params = self.loader.load_params_for_aid(dataset, aid)
        if params == None:
            print "Params not found for area id: " + str(aid) + ", using SW7 params..."
            params = self.loader.load_params_for_aid(dataset, "SW7")
            print params
        if "params" in request:
            for param in request["params"]:
                params[param] = request["params"][param]
        return params, self.loader.load_data_for_params(dataset, aid, params)

    # Handle a GP request
    def handle_gp_request(self, request):
        dataset = str(request["dataset"])
        aid = str(request["id"])

        # Make aid an integer if it is a grid square id
        if not aid[0].isalpha():
            aid = int(float(aid))

        # Get params and data for request
        params, train_data = self.get_params_and_data(request)
        n = len(train_data)
        if n < 20:
            print "n less than 20, for aid: " + str(aid)
            return self.status_response(405, "n less than 20 for aid: " + str(aid))

        # Print processing message
        Utils.sys_print("\rProcessing GP request for area id = " + str(aid) + \
                        ", n = " + str(n) + ", in dataset " + dataset + "...")
        
        # Create and fit gp model
        data_formatter = ZooplaSalesDataFormatter(params) if dataset == "zoopla_sales" else LandRegDataFormatter(params)
        gp_model = GPModel(data_formatter)
        gp_model.fit(params, train_data)
        final_kernel = gp_model.gpr.kernel_

        # Store gp model
        filename_suffix = params["filename_suffix"] if "filename_suffix" in params else ""
        Utils.create_folder(model_save_path)
        Utils.create_folder(model_save_path + dataset)
        Utils.create_folder(model_save_path + dataset + "/" + str(aid) + filename_suffix, overwrite=True)
        joblib.dump(gp_model, model_save_path + dataset + "/" + str(aid) + filename_suffix + "/gp_model.pkl")

        # Generate predictions and plot/save to json
        # Get dates for prediction line generation
        min_year = 1995
        max_year = 2019
        granularity = float(1)/float(12)
        steps = (max_year-min_year)*12 + 1
        dates = [(min_year + x * granularity) for x in range(0, steps)]

        # Request from zoopla data

        # request = {
        #     "dates": dates,
        #     "property_type": "F",
        #     "num_bathrooms": 0,
        #     "num_bedrooms": 2,
        #     "num_recepts": 0,
        #     "num_floors": 0,
        # }
        # plot_data = train_data[(train_data["property_type"]=="F")]

        # Request from landreg data

        # request = {
        #     "dates": dates,
        #     "property_type": "F",
        #     "estate_type": "L"
        # }
        # plot_data = train_data[(train_data["property_type"]=="F") & (train_data["estate_type"]=="L")]
        # plot_t = np.atleast_2d(map(Utils.datetime64_to_tinynoised_lontime, plot_data.index.values)).T
        # plot_y = plot_data['price'].values.ravel()
        # price_preds, sigmas = gp_model.predict(request)
        # name = dataset + "_" + str(aid) + filename_suffix
        # plot_predictions(price_preds, sigmas, dates, datapoints=(plot_t, plot_y), name=name)

        # Request from landreg for all type combinations predictions json

        if "save_json" in params and float(params["save_json"]):
            p_json = {}
            for pt in property_types:
                p_json[pt] = {}
                for et in estate_types:
                    request = {
                        "dates": dates,
                        "property_type": pt,
                        "estate_type": et
                    }
                    price_preds, sigmas = gp_model.predict(request)
                    price_preds = list(price_preds)
                    sigmas = list(sigmas)
                    p_json[pt][et] = {
                        "price_preds": price_preds,
                        "sigmas": sigmas
                    }

            Utils.create_folder(pred_save_path)
            Utils.create_folder(pred_save_path + dataset)
            path = pred_save_path + dataset + "/" + str(aid) + filename_suffix + ".json"
            with open(path, 'w') as outfile:
                json.dump(p_json, outfile)

        # plot_all(dataset, aid, filename_suffix)

        # TODO: Store final kernel params back into areas db

        Utils.sys_print("\rAwaiting GP Requests.                                                       ")

        # Return ok response
        return self.status_response(200, "Gaussian process generated.")

    # Returns a status response object for a given status number and message
    def status_response(self, num, message):
        return { "status": num, "message": message }
            
    # Checks a given request to make sure it's a GP request
    def check_request(self, req):
        if("dataset" not in req):
            print("Error 402: Request missing dataset")
            return self.status_response(402, "No dataset given in gaussian process request")   
            
        if("id" not in req):
            print("Error 403: Request missing id")
            return self.status_response(403, "No id given in gaussian process request")
            
        dataset = str(req["dataset"])
        if(dataset != "landreg" and dataset != "zoopla_sales"):
            print("Error 404: Unknown dataset")
            return self.status_response(404, "Unknown dataset '" + dataset + "'.")

        return 200

        
