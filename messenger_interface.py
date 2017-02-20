from util import log
import os
import json
import requests

# sends given json object to facebook api
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

    return r.status_code

# returns json object containing str payload
def setup_str(msg):
    return {"text":msg}

# sets up payload for location question
def init_location():
    message_obj = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type":"generic",
                "elements":[
                    {
                        "title": "Pick Dining Halls",
                        "subtitle" : "Swipe right to navigate. When you are done adding dining halls, press 'Done'.",
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Done",
                                "payload": "GOTO:TIME"
                            }
                        ]

                    },{
                        "title": "Bruin Plate",
                        "subtitle" : "The healthy option at UCLA!",
                        "image_url" : "http://bruinplate.hhs.ucla.edu/img/Home_Slide3_new.jpg",
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Add",
                                "payload": "ADD:BPLATE"
                            }
                        ]
                    },{
                        "title": "De Neve",
                        "subtitle" : "The hearty option if you are looking for shorter lines!",
                        "image_url" : "http://graphics.dailybruin.com/reg2013/img/ae/thumb/grub.jpg",
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Add",
                                "payload": "ADD:DENEVE"
                            }
                        ]
                    },{
                        "title": "Feast",
                        "subtitle" : "Asian cuisine that hits the spot!",
                        "image_url" : "http://feast.hhs.ucla.edu/wp-content/uploads/2011/09/IMG_9542_SS1.jpg",
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Add",
                                "payload": "ADD:FEAST"
                            }
                        ]
                    },{
                        "title": "Covel",
                        "subtitle" : "Dining hall if you're feeling antisocial!",
                        "image_url" : "http://www.ucla.edu/img/content-images/campus-life-housing-02.jpg",
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Add",
                                "payload": "ADD:COVEL"
                            }
                        ]
                    }
                ]
            }
        }
    }

    return message_obj

# setsup buyer question to send to user
def init_user():
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
                                "payload": "BUYER:TRUE"
                            },{
                                "type": "postback",
                                "title": "Seller",
                                "payload": "BUYER:FALSE"
                            }
                        ]
                    }
                ]
            }
        }
    }

    return message_obj
