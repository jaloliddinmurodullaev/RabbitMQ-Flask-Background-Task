import os
from dotenv import load_dotenv
from flask import Blueprint
from .notifier import notify

load_dotenv()
blueprint = Blueprint("apis", __name__)

@blueprint.route("/api/send-email/")
def send_email():
    receivers = [
        'jaloliddinmurodullaev@gmail.com',
        'jaloliddinmurodullaev@gmail.com',
        'jaloliddinmurodullaev@gmail.com',
        'jaloliddinmurodullaev@gmail.com',
        'jaloliddinmurodullaev@gmail.com',
        'jaloliddinmurodullaev@gmail.com',
        'jaloliddinmurodullaev@gmail.com',
        'jaloliddinmurodullaev@gmail.com'
    ]

    print("-- DEBUG 0.0.0 --")

    response = notify(
        username  = os.getenv("USERNAME"), 
        password  = os.getenv("PASSWORD"),
        sender    = os.getenv("SENDER"),
        receivers = receivers
    )

    print("-- DEBUG 0.1.0 --")

    return response