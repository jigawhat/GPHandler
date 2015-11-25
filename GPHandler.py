import Utils
import json
import joblib
from GPModel import GPModel
from DataLoader import DataLoader
from DataFormatter import DataFormatter

model_save_path = "modelsaves/"

class GPHandler(object):
    def __init__(self):
        print("Initialising...")
        self.loader = DataLoader()
        self.landreg_data = self.loader.load_dataset("london-data.csv")
    
    def handle_request(request):
        check_request(request)
        #if(request["type"] == "graph"):
        return handle_gp_request(request)

    def handle_gp_request(request):
        area = req["area"]  
        
        # Get model parameters from model_parameters.json
        with open('model_parameters.json') as model_params_file:
            all_model_params = json.load(model_params_file)
        params = all_model_params[dataset_name][model_name]

        # Format input X data
        dataframe_for_area = DataLoader.load_data_for_area(self.landreg_data, area)
        data_formatter = DataFormatter(params)
        X, y = data_formatter.input_dataframe_to_X_y(dataframe_for_area)

        # Create and fit gp model
        gp_model = GPModel(X, y, params)

        # Store gp model
        Utils.create_folder(model_save_path)
        Utils.create_folder(model_save_path + dataset)
        Utils.create_folder(model_save_path + dataset + "/" + model_name)
        Utils.create_folder(model_save_path + dataset + "/" + model_name + "/" + postcode, overwrite=True)
        joblib.dump(gp_model, model_save_path + dataset + "/" + model_name + "/" + postcode + "/gp_model.pkl")

        return None

    
    def status_response(num, message):
        return { "status":num, "message": message }
            
    def check_request(req):
        if("datatset" not in req):
            print("err")
            
        if("model" not in req):
            print("err")    
        
        if("area" not in req):
            return status_response(402, "No area given in prediction request")    
            
        dataset = str(req["dataset"])
        
        model = str(req["model"])

        if(dataset != "landreg"):
            return status_response(400, "Unknown dataset '" + dataset + "'.")
        
        # Check model exists
        with open('model_parameters.json') as model_params_file:                            
            all_model_params = json.load(model_params_file)
        
        models_for_dataset = all_model_params[dataset]
        if(not model in models_for_dataset):
            return status_response(401, "Unknown model '" + model + "' for dataset '" + dataset + "'.")

        
