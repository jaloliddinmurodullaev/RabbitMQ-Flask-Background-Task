from .email_sender import EmailSender
from .rabbitmq import RabbitMQConnection

TEMPLATE = "Subject: Welcome\n\nThis is a message from smtp server"

def notify(username, password, sender, receivers, message=TEMPLATE):
    queue = RabbitMQConnection(username='guest', password='guest')
    queue.connect()
    try:
        server = EmailSender()
        server.start()
        server.login(username=username, password=password)
        for receiver in receivers:
            print('sent')
            server.send_mail(sender=sender, receiver=receiver, message=message)

        response = {
            "status": "success",
            "message": "success",
            "count": 10,
            "sent": 10,
        }
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e),
            "count": 10,
            "sent": 0
        }
    finally:
        server.exit()

    return response



