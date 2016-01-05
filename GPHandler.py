import sys
import json
import joblib
import Utils
from GPModel import GPModel
from DataLoader import DataLoader
from LandRegDataFormatter import LandRegDataFormatter

model_save_path = "modelsaves/"

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
        # 
        dataset = str(req["dataset"])
        aid = str(req["id"])

        # Make aid an integer if it is a grid square id
        if not aid[0].isalpha():
            aid = int(float(aid))

        # Print processing message
        sys.stdout.write("\rProcessing GP request for area id = " + str(aid) + ", in dataset " + dataset + "...")
        sys.stdout.flush()

        # Get training data and params
        params = req["params"] if "params" in req else self.loader.load_params_for_aid(dataset, aid)
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

        
