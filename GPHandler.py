import sys
import json
import joblib
import Utils
from GPModel import GPModel
from DataLoader import DataLoader
from LandRegDataFormatter import LandRegDataFormatter

model_save_path = "modelsaves/"
# Use "local" or "remote" data source
data_source = "local" 

class GPHandler(object):

    def __init__(self):
        self.datasets = {}
        self.area_dbs = {}
        self.loader = DataLoader()

        config_file = open('data_config.json')                       
        config = json.load(config_file)

        data_file = str(config["london_data"][data_source]) 

        print("Using London data source: %s" % data_source)
        print("Loading London data from: %s" % data_file)

        self.datasets["landreg"] = self.loader.load_dataset(data_file)
        self.area_dbs["grid_squares"] = self.loader.load_csv("grid_squares_db.csv", index_col="id")
        self.area_dbs["postcode_areas"] = self.loader.load_csv("postcode_areas_db.csv", index_col="postcode")
    
    # Handle request (make sure it's a GP request)
    def handle_request(self, request):
        status = self.check_request(request)
        if(status != 200):
            return status
        return self.handle_gp_request(request)

    # Handle a GP request
    def handle_gp_request(self, req):

        dataset = str(req["dataset"])
        aid = str(req["id"])

        sys.stdout.write("\rProcessing GP request for area id = " + aid + ", in dataset " + dataset + "...")
        sys.stdout.flush()

        is_postcode = aid[0].isalpha()
        db = "postcode_areas"
        if not is_postcode:
            aid = int(aid)
            db = "grid_squares"

        # Get training data and params
        params = req["params"] if "params" in req else self.area_dbs[db].loc[aid].to_dict()
        train_data = self.load_data_for_params(dataset, db, aid, params)
        
        # Create and fit gp model
        gp_model = GPModel(LandRegDataFormatter(params))
        final_kernel = gp_model.fit(params, train_data)

        # Store gp model
        Utils.create_folder(model_save_path)
        Utils.create_folder(model_save_path + dataset)
        Utils.create_folder(model_save_path + dataset + "/" + str(aid), overwrite=True)
        joblib.dump(gp_model, model_save_path + dataset + "/" + str(aid) + "/gp_model.pkl")

        # Store final kernel params back into areas db
        # self.area_dbs[db].set_value(aid, 'final_kernel', final_kernel)
        # self.area_dbs[db].to_csv(db + "_db.csv")

        sys.stdout.write("\rAwaiting GP Requests.                                    ")
        sys.stdout.flush()

        # Return ok response
        return self.status_response(200, "Gaussian process generated.")

    # Load dataset
    def load_data_for_params(self, dataset, db, aid, params):
        if(db == "postcode_areas"):
            return self.loader.load_data_for_postcode(self.datasets[dataset], aid)
        else:
            # Request is for a grid square
            lat, lng, size = float(params['lat']), float(params['lng']), float(params['size'])
            return self.loader.load_data_for_lat_lng_size(self.datasets[dataset], lat, lng, size)

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

        
