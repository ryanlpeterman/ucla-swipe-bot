import os
import sys
import json

import requests
from flask import Flask, request
from collections import defaultdict

app = Flask(__name__)

# User Data Structure:
# { user_id:
#   { "buyer": bool, - False = seller
#     "begin": <beginning time>,
#     "end": <ending time> - integer on the hour
#     "where": set("bplate", "deneve", "covel", "feast") - contains one or more dining halls
#   }
# }

# User has not filled out all fields yet
incomplete_data = defaultdict(dict)
# User has fully filled out fields and we can match on this data
final_data = defaultdict(dict)

dining_halls = ["bplate", "deneve", "feast", "covel"]

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

                if messaging_event.get("message"):  # someone sent us a message
                    # skip message if its an emoji
                    if "text" not in messaging_event["message"]:
                        continue
                    message_text = messaging_event["message"]["text"]  # the message's text

                    # TODO: temporarily starts data request save on begin msg send
                    #       change to on "get started" button press instead later
                    if message_text.lower() == "begin":
                        init_user(sender_id)
                    else:
                        obj = {"text": "Got a message!"}
                        send_message(sender_id, obj)

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
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

    if action == "init":
        log("Handle Init with payload: {load}".format(load=payload))
        handle_init(uid, value)
    elif action == "set":
        log("TODO: implement setting finalized data")
    else:
        log("Received unhandled payload: {load}".format(load=payload))

# handles initializing incomplete data in init flow
def handle_init(uid, value):
    if value == "buyer" or value == "seller":
        incomplete_data[uid]["buyer"] = (value == "buyer")
        init_location(uid)

    elif value in dining_halls:
        if incomplete_data[uid]["where"]:
            incomplete_data[uid]["where"].add(value)

        # no locations set yet
        else:
            incomplete_data[uid]["where"] = set([value])

        # TODO: figure out better way of doing this loop
        # all dining halls or picked none
        if len(incomplete_data[uid]["where"]) == 4:
            # init_begin()
            print "TODO: get times now"
        else:
            init_location(uid)
    else:
        #TODO: Handle storing when
        print "TODO: store when"

# sends a templated question to recipient asking if buyer or seller
def init_user(recipient_id):
    log("init:buyer from {recipient}".format(recipient=recipient_id))

    message_obj = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type":"generic",
                "elements":[
                    {
                        "title": "Let's get started!",
                        "subtitle": "Are you a buyer or a seller?",
                        "buttons":
                        [
                            {
                                "type": "postback",
                                "title": "Buyer",
                                "payload": "init:buyer"
                            },{
                                "type": "postback",
                                "title": "Seller",
                                "payload": "init:seller"
                            }
                        ]
                    }
                ]
            }
        }
    }

    send_message(recipient_id, message_obj)

# sends a templated question to recipient asking for which dining halls they prefer
def init_location(recipient_id):
    log("init:location from {recipient}".format(recipient=recipient_id))

    message_obj = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type":"list",
                "top_element_style":"compact",
                "elements":[
                    {
                        "title": "Which dining halls are you buying/selling at?\nBruin Plate",
                        "buttons":
                        [
                            {
                                "type": "postback",
                                "title": "Add",
                                "payload": "init:bplate"
                            }
                        ]

                    },{
                        "title": "Feast",
                        "buttons":
                        [
                            {
                                "type": "postback",
                                "title": "Add",
                                "payload": "init:feast"
                            }
                        ]

                    },{
                        "title": "De Neve",
                        "buttons":
                        [
                            {
                                "type": "postback",
                                "title": "Add",
                                "payload": "init:deneve"
                            }
                        ]

                    },{
                        "title": "Covel",
                        "buttons":
                        [
                            {
                                "type": "postback",
                                "title": "Add",
                                "payload": "init:covel"
                            }
                        ]

                    }
                ]
            }
        }
    }

    send_message(recipient_id, message_obj)

def send_message(recipient_id, message_obj):

    log("sending message to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": message_obj
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

# simple wrapper for logging to stdout on heroku
def log(message):
    print str(message)
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True)