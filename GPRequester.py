import pika
import json

gp_queue_name = 'gp_request_queue'
username = 'aew13'
password = 'bubbler420'
host = '146.169.45.142'
timeout = 0

credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials, heartbeat_interval=timeout))
channel = connection.channel()
channel.queue_declare(queue=gp_queue_name)

def submit_gp_request(request):
    channel.basic_publish(exchange='', routing_key=gp_queue_name, body=json.dumps(request))


