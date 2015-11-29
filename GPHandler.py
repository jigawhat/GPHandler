import Utils
import json
import joblib
from GPModel import GPModel
from DataLoader import DataLoader
from DataFormatter import DataFormatter

model_save_path = "modelsaves/"

class GPHandler(object):

    def __init__(self):
        self.loader = DataLoader()
        self.datasets = {}
        self.datasets["landreg"] = self.loader.load_dataset("http://www.doc.ic.ac.uk/project/2015/362/g1536201/aew13/GPHandler/london-data.csv")
    
    def handle_request(self, request):
        self.check_request(request)
        return self.handle_gp_request(request)

    def handle_gp_request(self, req):
        area = req["area"]
        dataset = req["dataset"]
        model = req["model"]
        
        # Get model parameters from model_parameters.json
        with open('model_parameters.json') as model_params_file:
            all_model_params = json.load(model_params_file)
        params = all_model_params[dataset][model]

        # Format input X data
        dataframe_for_area = self.loader.load_data_for_area(self.datasets[dataset], area)
        data_formatter = DataFormatter(params)
        X, y = data_formatter.input_dataframe_to_X_y(dataframe_for_area)

        # Create and fit gp model
        gp_model = GPModel(X, y, params, data_formatter)

        # Store gp model
        Utils.create_folder(model_save_path)
        Utils.create_folder(model_save_path + dataset)
        Utils.create_folder(model_save_path + dataset + "/" + model)
        Utils.create_folder(model_save_path + dataset + "/" + model + "/" + area, overwrite=True)
        joblib.dump(gp_model, model_save_path + dataset + "/" + model + "/" + area + "/gp_model.pkl")

        # Return ok response
        return self.status_response(200, "Gaussian process generated.")

    
    def status_response(self, num, message):
        return { "status":num, "message": message }
            
    def check_request(self, req):
        if("dataset" not in req):
            print("err")
            
        if("model" not in req):
            print("err")    
        
        if("area" not in req):
            return self.status_response(402, "No area given in gaussian process request")    
            
        dataset = str(req["dataset"])
        
        model = str(req["model"])

        if(dataset != "landreg"):
            return self.status_response(400, "Unknown dataset '" + dataset + "'.")
        
        # Check model exists
        with open('model_parameters.json') as model_params_file:                            
            all_model_params = json.load(model_params_file)
        
        models_for_dataset = all_model_params[dataset]
        if(not model in models_for_dataset):
            return self.status_response(401, "Unknown model '" + model + "' for dataset '" + dataset + "'.")

        
