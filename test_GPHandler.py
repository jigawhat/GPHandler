import os
import shutil
from GPHandler import GPHandler

model_save_path = "modelsaves/"
pred_save_path = "predsaves/"
gph = GPHandler()


def test_loading_params_and_data():
    request = {
        "dataset": "landreg",
        "id": 1000,
        "params": {
            "logadj": 1.2,
            "log_scaling": 7.0
        }
    }
    params, data = gph.get_params_and_data(request)
    assert params["log_scaling"] == 7.0
    assert len(data) > 0

def test_check_request_that_should_pass():
    request = {
        "dataset": "landreg",
        "id": 1000,
        "params": {
            "logadj": 1.2,
            "log_scaling": 7.0
        }
    }
    status = gph.check_request(request)
    assert status == 200

def test_check_request_that_should_fail():
    request = {
        "dataset": "dsfknsl",
        "id": 1000
    }
    status = gph.check_request(request)
    assert status != 200

def test_handling_gp_request_and_saving_json():
    request = {
        "dataset": "landreg",
        "id": 1000,
        "params": {
            "logadj": 1.2,
            "log_scaling": 7.0,
            "filename_suffix": "_test_GPHandler_gp_model",
            "save_json": 1
        }
    }
    model_path = model_save_path + "landreg/1000_test_GPHandler_gp_model"
    json_path = pred_save_path + "landreg/1000_test_GPHandler_gp_model.json"

    response = gph.handle_gp_request(request)
    assert response["status"] == 200
    assert os.path.isfile(model_path + "/gp_model.pkl")
    assert os.path.isfile(json_path)

    if os.path.exists(model_path):
        shutil.rmtree(model_path)

    if os.path.isfile(json_path):
        os.remove(json_path)


