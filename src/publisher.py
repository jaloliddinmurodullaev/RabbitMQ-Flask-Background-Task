import json
import pika

class Publisher:
    def __init__(self, config):
        self.config = config

    def create_connection(self):
        max_tries = 3
        tried = 0
        
        while tried < max_tries:
            try:
                credentials = pika.PlainCredentials(self.config['username'], self.config['password'])
                parameters  = pika.ConnectionParameters(host=self.config['host'], port=self.config['port'], credentials=credentials)
                connection  = pika.BlockingConnection(parameters)

                print(" [x] Connection established ...")
                break
            except Exception as e:
                connection = None
                print(f" [x] Error while connecting: {str(e)}")

            tried += 1

        return connection
    
    def publish(self, key, message):
        connection = self.create_connection()

        if connection is not None:
            try:
                channel = connection.channel()

                channel.exchange_declare(exchange=self.config['exchange'], exchange_type='topic')
                channel.basic_publish(exchange=self.config['exchange'], routing_key=key, body=json.dumps(message))
                print(" [x] Sent message %r for %r" % (message, key))
            except Exception as e:
                print(f" [x] Unknown error: {str(e)}")
        else:
            print(f" [x] Couldn't establish a connection. Try again")

config = {
    'username': 'guest',
    'password': 'guest',
    'host': 'localhost',
    'port': 5672,
    'exchange': 'my_exchange'
}

publisher = Publisher(config=config)
publisher.publish('email.new', config)


