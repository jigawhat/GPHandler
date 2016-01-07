from GPRequester import submit_gp_request

for aid in range(2500, 2523):
#for aid in [2506, 2513, 2516, 2519, 2520]:
    request = {
        "dataset": "landreg",
        "id": str(aid)
    }
    submit_gp_request(request)
