from GPRequester import submit_gp_request

# [2002, 2011, 2013, 2015, 2017]

for aid in [738]:
#for aid in [2506, 2513, 2516, 2519, 2520]:
    # request = {
    #     "dataset": "landreg",
    #     "id": str(aid)
    # }
    # submit_gp_request(request)
    request = {
        "dataset": "landreg",
        "id": str(aid),
        "params": {
            "logadj": 1.2,
            "log_scaling": 8.0,
            "save_json": 1.0,
            "filename_suffix": "_log8"
        }
    }
    submit_gp_request(request)
