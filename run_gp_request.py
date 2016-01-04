import pika
import json
import joblib

# model_path = "modelsaves/landreg/release/SE8 4A/gp_model.pkl"

gp_queue_name = 'gp_request_queue'
username = 'aew13'
password = 'bubbler420'
host = '146.169.45.142'
timeout = 0

request = {
    'dataset': 'landreg',
    'id': 3247,
    # The params dictionary below is only used for testing different params -
    # it's not needed for getting predictions for an area
    # 'params': {
    #     'start_date': 1990,
    #     'end_date': 2013,
    #     'filename_suffix': "_test_1",
    #     'alpha_var_multiplier': 0.0,
    #     'dataset': 'landreg',
    #     'id': 3247.0,
    #     'lat': 51.53476,
    #     'lng': -0.18132,
    #     'logadj': 1.5,
    #     'n': 1097.0,
    #     'n_restarts_optimiser': 3.0,
    #     'rbf_ls_init': 70.0,
    #     'rbf_ls_lb': 0.1,
    #     'rbf_ls_ub': 1000.0,
    #     'rq_a_init': 0.01,
    #     'rq_a_lb': 0.01,
    #     'rq_a_ub': 100.0,
    #     'rq_ls_init': 0.1,
    #     'rq_ls_lb': 0.1,
    #     'rq_ls_ub': 100.0,
    #     'size': 357.0,
    #     'wk_var_mult_lb': 0.49,
    #     'wk_var_mult_ub': 0.51
    # }
}

credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials, heartbeat_interval=timeout))
channel = connection.channel()
channel.queue_declare(queue=gp_queue_name)


channel.basic_publish(exchange='', routing_key=gp_queue_name, body=json.dumps(request))

