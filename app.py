import os
import json

import time
import atexit
import facebook_scraper

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import requests
from flask import Flask, request
from collections import defaultdict

# our modules
from util import log
import messenger_interface as fb
import database as db
import match as m

m.init()
app = Flask(__name__)

# The scheduler will only start after the first request. We need to include this
# because the debugger will naturally run two instances and this way we will
# only run one.
@app.before_first_request
def initialize():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=facebook_scraper.test_func,
        trigger=IntervalTrigger(seconds=5),
        id='scraping_job',
        name='Scraping the Facebook page every few hours',
        replace_existing=True)
    atexit.register(lambda: scheduler.shutdown())

# User Data Structure:
# { user_id:
#   { "is_buyer": bool, - False = seller
#     "when" : list(1, 2, 3) - contains each hour in military time that they are buying
#     "where": list("bplate", "deneve", "covel", "feast") - contains one or more dining halls
#     "price": int
#   }
# }

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

# endpoint for processing incoming messaging events
@app.route('/', methods=['POST'])
def webhook():

    data = request.get_json()
    # for testing
    log(data)

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                # the facebook ID of the person sending you the message
                sender_id = messaging_event["sender"]["id"]
                # the recipient's ID, which should be your page's facebook ID
                recipient_id = messaging_event["recipient"]["id"]

                # someone sent us a message
                if messaging_event.get("message"):
                    # skip message if its an emoji
                    if "text" not in messaging_event["message"]:
                        continue

                    message_text = messaging_event["message"]["text"]  # the message's text

                    # TODO: HANSEN - message_text is the input message from the user
                    # call your function on it
                    fb.send_message(sender_id, fb.setup_str("Hansen replace me bitch"))

                    # here is an example of what we want
                    # usr_dict = nlpfunction(message_text)
                    # matches = m.add_complete_user(usr_dict)

                    # send matches to each nig

    return "ok", 200

if __name__ == '__main__':
    app.run(debug=True)


