from GPRequester import submit_gp_request

for aid in [1027]:
#for aid in [2506, 2513, 2516, 2519, 2520]:
    # request = {
    #     "dataset": "landreg",
    #     "id": str(aid)
    # }
    # submit_gp_request(request)

    # request = {
    #     "dataset": "landreg",
    #     "id": str(aid),
    #     "params": {
    #         "logadj": 1.2,
    #         "log_scaling": 5.0,
    #     }
    # }

    request = {
            "dataset": "landreg",
            "id": str(aid),
            "params": {
                "filename_suffix": "_2013_logadj_sc11",
                "end_date": 2013,
                "logadj": 1.2,
                "log_scaling": 20.0
            }
        }

    submit_gp_request(request)
