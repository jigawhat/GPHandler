from GPRequester import submit_gp_request

for aid in range(2500, 2700):
    request = {
        "dataset": "landreg",
        "id": str(aid)
    }
    submit_gp_request(request)
