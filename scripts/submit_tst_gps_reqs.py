from GPRequester import submit_gp_request

ev_areas = [
    "1671_logadj",
    # "1663_logadj",
    # "1653",
    # "1649_logadj",
    # "1632_logadj",
    # "1502",
    # "833_logadj",
    # "745_logadj",
    # "1719_logadj",
    # "1723_logadj",
    # "1726",
    # "1732_logadj",
    # "1773",
    # "1783",
    # "1802",
    # "1804",
    # "1816_logadj",
    # "1862_logadj",
    # "1873",
    # "1877",
    # "1889_logadj",
    # "1893",
    # "1899_logadj",
    # "1983_logadj",
    # "1984",
    # "1988_logadj",
    # "1990",
    # "1991",
    # "1996_logadj",
    # "2000_logadj"
]

for i in range(len(ev_areas)):
    aid_strs = ev_areas[i].split("_") 
    aid = int(aid_strs[0])

    request = {
        "dataset": "zoopla_sales",
        "id": str(aid),
    }
    if len(aid_strs) >= 2:
        request["params"] = {
            'logadj': 1.2,
            'filename_suffix': '_logadj'
        }
    submit_gp_request(request)
