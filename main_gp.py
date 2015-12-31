'''
    Wires components together, and starts running the handler processsing jobs
'''
import sys
import json

from RabbitPuller import RabbitPuller
from GPHandler import GPHandler

# First argument is type of configuration
if(len(sys.argv) > 1):
    option = sys.argv[1]
else:
    option = "test"

# Load configuration options
config_file = open('config.json')                       
config = json.load(config_file)

print("Attempting to load configuration option: %s" % option)
print("Using RabbitMQ server on: %s" % str(config[option]["host"]))
print("Accessing queue with username: %s" % str(config[option]["username"]))
print("Using password: %s" % str(config[option]["password"]))


prediction_queue_name = str(config["queue_names"]["pred"])
gp_queue_name = str(config["queue_names"]["gp"])

username = str(config[option]["username"])
password = str(config[option]["password"])
host = str(config[option]["host"])

gph = GPHandler()
p = RabbitPuller(username, password, host, gp_queue_name, gph.handle_request)

sys.stdout.write("Awaiting GP Requests.                             ")
sys.stdout.flush()

p.start()
