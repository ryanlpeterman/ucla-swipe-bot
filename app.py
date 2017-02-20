import os
import json

import requests
from flask import Flask, request
from collections import defaultdict

from util import log
import messenger_interface as fb

app = Flask(__name__)

# User Data Structure:
# { user_id:
#   { "buyer": bool, - False = seller
#     "when" : set(1, 2, 3) - contains each hour in military time that they are buying
#     "where": set("bplate", "deneve", "covel", "feast") - contains one or more dining halls
#   }
# }

# User has not filled out all fields yet
incomplete_data = defaultdict(dict)
# User has fully filled out fields and we can match on this data
final_data = defaultdict(dict)

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

                    # TODO: temporarily starts data request save on begin msg send
                    #       change to on "get started" button press instead later
                    if message_text.lower() == "begin":
                        fb.send_message(sender_id, fb.init_user())
                    else:
                        fb.send_message(sender_id, fb.setup_str("Got a message!"))

                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    payload = messaging_event["postback"]["payload"]
                    handle_payload(sender_id, payload)

    return "ok", 200

# handles payload string from postback
# payloads are in the form
#   <action>:<value>
# i.e.
#   set:buyer
#   init:buyer
def handle_payload(uid, payload):
    log("Received postback payload from {id}: {load}".format(id=uid, load=payload))

    action, value = payload.split(":")

    if action == "HALL":
        add_hall(uid, value)

    elif action == "BUYER":
        set_buyer(uid, value)

        # if we have no dining hall data
        if "where" not in incomplete_data[uid]:
            fb.send_message(uid, fb.init_location())

    # TODO: Convert to NLP to prompt user for time data
    elif action == "TIME":
        add_time(uid, int(value))

    # use this postback action to resend prompts
    elif action == "GOTO":
        if value == "TIME":
            fb.send_message(uid, fb.setup_time())
        elif value == "HALL":
            fb.send_message(uid, fb.init_location())
        elif value == "DONE":
            usr = incomplete_data[uid]

            # user gave complete data
            if "when" in usr and "where" in usr and "buyer" in usr:
                # add object to complete dict
                complete_data[uid] = incomplete_data[uid]
                del incomplete_data[uid]

                fb.send_message(uid, fb.setup_str("Great! I will try my best to match you and let you know if I find someone!"))
                log(complete_data)

            else:
                fb.send_message(uid, fb.setup_str("I don't have the complete information necessary to match you, please fill out the following forms"))

                if "where" not in usr:
                    fb.send_message(uid, fb.init_location())
                if "when" not in usr:
                    fb.send_message(uid, fb.setup_time())
                if "buyer" not in usr:
                    fb.send_message(uid, fb.init_user())

    else:
        log("Received unhandled payload: {load}".format(load=payload))

# TODO: Replace these functions and the global objects with a proper database
def is_user_complete(uid):
    usr = incomplete_data[uid]
    return ()

def set_buyer(uid, buyer_str):
    incomplete_data[uid]["buyer"] = (buyer_str == "buyer")
    log("USER: {id} was set to {buyer}".format(id=uid, buyer=buyer_str))

def add_hall(uid, hall):
    if "where" in incomplete_data[uid]:
        incomplete_data[uid]["where"].add(hall)

    # no locations set yet
    else:
        incomplete_data[uid]["where"] = set([hall])

    log("Added location {hall} to user {id}".format(hall=hall, id=uid))

def add_time(uid, hour):
    if "when" in incomplete_data[uid]:
        incomplete_data[uid]["when"].add(hour)

    # no locations set yet
    else:
        incomplete_data[uid]["when"] = set([hour])

    log("Added time {hour} to user {id}".format(hour=hour, id=uid))

if __name__ == '__main__':
    app.run(debug=True)