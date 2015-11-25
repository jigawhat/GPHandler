'''
    Wires components together, and starts running the handler processsing jobs
'''

from RabbitPuller import RabbitPuller
from GPHandler import GPHandler

def test(request):
    print(request)

# gpr = GPRequester(ip, port, ...)

# ph = PredictionHandler(args , gpr)

prediction_queue_name = 'prediction_request_queue'
gp_queue_name = 'gp_request_queue'
username = 'aew13'
password = 'bubbler420'
host = '146.169.45.142'

gph = GPHandler()
p = RabbitPuller(username, password, host, gp_queue_name, gph.handle_request)

p.start()