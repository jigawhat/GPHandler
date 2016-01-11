from GPRequester import submit_gp_request

for aid in range(168, 169):
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
            'filename_suffix': '_full_alphas_1.0'
        }
    }
    submit_gp_request(request)
