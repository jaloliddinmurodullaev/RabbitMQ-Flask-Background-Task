import sys
import json
import pika

class Subscriber:
    def __init__(self, config):
        self.config = config
        self.connection = self.create_connection()

    def create_connection(self):
        credentials = pika.PlainCredentials(username=self.config['username'], password=self.config['password'])
        parameters  = pika.ConnectionParameters(host=self.config['host'], port=self.config['port'], credentials=credentials)
        connection  = pika.BlockingConnection(parameters=parameters)
        return connection
    
    def on_message_callback(self, channel, method, properties, body):
        binding_key = method.routing_key
        data = {
            "properties": properties,
            "body": json.loads(body)
        }
        # print(data)
        print("received new message for -" + binding_key)

    def setup(self):
        try:
            channel = self.connection.channel()
            channel.exchange_declare(exchange=self.config['exchange'], exchange_type='topic')
            channel.queue_declare(queue=self.config['queue_name'])
            channel.queue_bind(queue=self.config['queue_name'], exchange=self.config['exchange'], routing_key=self.config['binding_key'])
            channel.basic_consume(queue=self.config['queue_name'], on_message_callback=self.on_message_callback, auto_ack=True)
            print(" [*] Waiting for data for " + self.config['queue_name'] + ". To exit press CTRL+C")

            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
        except Exception as e:
            print(f" [*] Unknown error: {str(e)}")


    def __del__(self):
      self.connection.close()

config = {
    'username': 'guest',
    'password': 'guest',
    'host': 'localhost',
    'port': 5672,
    'exchange': 'my_exchange'
}

if len(sys.argv) < 3:
    print("Usage: " + __file__ + " <QueueName> <BindingKey>")
    sys.exit()
else:
    config['queue_name']  = sys.argv[1]
    config['binding_key'] = sys.argv[2]

    subscriber = Subscriber(config)
    subscriber.setup()



