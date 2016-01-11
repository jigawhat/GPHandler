from GPRequester import submit_gp_request

for aid in range(1921, 1931):
#for aid in [2506, 2513, 2516, 2519, 2520]:
    request = {
        "dataset": "zoopla_sales",
        "id": str(aid)
    }
    submit_gp_request(request)
    request = {
        "dataset": "zoopla_sales",
        "id": str(aid),
        "params": {
            'logadj': 1.2,
            'filename_suffix': '_logadj'
        }
    }
    submit_gp_request(request)
