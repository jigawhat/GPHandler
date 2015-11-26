'''
This class abstracts the pulling of information off of the RabbitMQ queue
'''

import pika
import json

# Timeout for resending messages on the queue
# If no ack is recieved from a worker
timeout = 0 # TODO: change based on average times 

class RabbitPuller(object):
    def __init__(self, username, password, host, queue_name, process_request):
        # Call back to process request
        self.process_function = process_request
        
        # Credentials for RabbitMQ and connection
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials, heartbeat_interval=timeout))
        self.channel = connection.channel()
        # Sets up queue (creates it if needed) connection
        self.channel.queue_declare(queue=queue_name)
        
        # Sets messages to pile up queue instead of assigning
        self.channel.basic_qos(prefetch_count=1)
        # Setting the callback for the queue
        self.channel.basic_consume(self.on_request, queue=queue_name)

    def on_request(self, ch, method, props, body):
        # Response from processing request
        response = self.process_function(json.loads(body))

        # Deals with reply to RabbitMQ return queue
        if(props != None and props.reply_to != None):
            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id = props.correlation_id),
                             body=json.dumps(response))

        ch.basic_ack(delivery_tag = method.delivery_tag)
        
    def start(self):
        self.channel.start_consuming()