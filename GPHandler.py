import sys
import json
import joblib
import Utils
from GPModel import GPModel
from DataLoader import DataLoader
from LandRegDataFormatter import LandRegDataFormatter

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

    # Handle a GP request
    def handle_gp_request(self, req):
        dataset = str(req["dataset"])
        aid = str(req["id"])

        # Make aid an integer if it is a grid square id
        if not aid[0].isalpha():
            aid = int(float(aid))

        # Print processing message
        sys.stdout.write("\rProcessing GP request for area id = " + str(aid) + ", in dataset " + dataset + "...")
        sys.stdout.flush()

        # Get training params and data
        params = self.loader.load_params_for_aid(dataset, aid)
        if params == None:
            return self.status_response(405, "Unknown area id: " + str(aid))
        if "params" in req:
            for param in req["params"]:
                params[param] = req["params"][param]
        train_data = self.loader.load_data_for_params(dataset, aid, params)
        
        # Create and fit gp model
        gp_model = GPModel(LandRegDataFormatter(params))
        gp_model.fit(params, train_data)
        final_kernel = gp_model.gpr.kernel_

        # Store gp model
        filename_suffix = params["filename_suffix"] if "filename_suffix" in params else ""
        Utils.create_folder(model_save_path)
        Utils.create_folder(model_save_path + dataset)
        Utils.create_folder(model_save_path + dataset + "/" + str(aid) + filename_suffix, overwrite=True)
        joblib.dump(gp_model, model_save_path + dataset + "/" + str(aid) + filename_suffix + "/gp_model.pkl")

        min_year = 1995
        max_year = 2019
        granularity = float(1)/float(12)
        steps = (max_year-min_year)*12 + 1
        dates = [(min_year + x * granularity) for x in range(0, steps)]

        p_json = []

        for pt in property_types:
            for et in estate_types:
                request = {
                    "dataset": "landreg",
                    "id": aid,
                    "dates": dates,
                    "property_type": pt,
                    "estate_type": et
                }
                price_preds, sigmas = gp_model.predict(request)
                price_preds = list(price_preds)
                sigmas = list(sigmas)
                p_dict = {
                    "property_type": pt,
                    "estate_type": et,
                    "price_preds": price_preds,
                    "sigmas": sigmas
                }
                p_json.append(p_dict)

        Utils.create_folder(pred_save_path)
        Utils.create_folder(pred_save_path + dataset)
        path = pred_save_path + dataset + "/" + str(aid) + filename_suffix + ".json"
        with open(path, 'w') as outfile:
            json.dump(p_json, outfile)


        # TODO: Store final kernel params back into areas db

        sys.stdout.write("\rAwaiting GP Requests.                                                       ")
        sys.stdout.flush()

        # Return ok response
        return self.status_response(200, "Gaussian process generated.")

    def status_response(self, num, message):
        return { "status": num, "message": message }
            
    def check_request(self, req):
        if("dataset" not in req):
            print("Error 402: Request missing dataset")
            return self.status_response(402, "No dataset given in gaussian process request")   
            
        if("id" not in req):
            print("Error 403: Request missing id")
            return self.status_response(403, "No id given in gaussian process request")
            
        dataset = str(req["dataset"])
        if(dataset != "landreg"):
            print("Error 404: Unknown dataset")
            return self.status_response(404, "Unknown dataset '" + dataset + "'.")

        return 200

        
