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

# returns json object containing time prompt payload
def setup_time():
    message_obj = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type":"generic",
                "elements":[
                    {
                        "title": "Pick Times",
                        "subtitle" : "Swipe right to navigate. Add as many time periods as you like.",
                        "image_url" : "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Icons8_flat_clock.svg/2000px-Icons8_flat_clock.svg.png"
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Done Adding Times",
                                "payload": "GOTO:DONE"
                            }
                        ]
                    },{
                        "title": "Breakfast Times",
                        "subtitle" : "Can you wake up in time?",
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Add 8-9am",
                                "payload": "TIME:8"
                            },{
                                "type": "postback",
                                "title": "Add 9-10am",
                                "payload": "TIME:9"
                            },{
                                "type": "postback",
                                "title": "Add 10-11am",
                                "payload": "TIME:10"
                            }
                        ]
                    },{
                        "title": "Lunch Times",
                        "subtitle" : "Pick times for lunch",
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Add 11am-12pm",
                                "payload": "TIME:11"
                            },{
                                "type": "postback",
                                "title": "Add 12-1pm",
                                "payload": "TIME:12"
                            },{
                                "type": "postback",
                                "title": "Add 1-2pm",
                                "payload": "TIME:1"
                            }
                        ]
                    },{
                        "title": "Dinner Times",
                        "subtitle" : "Pick times for dinner",
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Add 5-6pm",
                                "payload": "TIME:17"
                            },{
                                "type": "postback",
                                "title": "Add 6-7pm",
                                "payload": "TIME:18"
                            },{
                                "type": "postback",
                                "title": "Add 7-8pm",
                                "payload": "TIME:19"
                            }
                        ]
                    }
                ]
            }
        }
    }

    return message_obj

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
                                "title": "Done Adding Halls",
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
                                "title": "Add Bplate",
                                "payload": "HALL:BPLATE"
                            }
                        ]
                    },{
                        "title": "De Neve",
                        "subtitle" : "The hearty option if you are looking for shorter lines!",
                        "image_url" : "http://graphics.dailybruin.com/reg2013/img/ae/thumb/grub.jpg",
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Add De Neve",
                                "payload": "HALL:DENEVE"
                            }
                        ]
                    },{
                        "title": "Feast",
                        "subtitle" : "Asian cuisine that hits the spot!",
                        "image_url" : "http://feast.hhs.ucla.edu/wp-content/uploads/2011/09/IMG_9542_SS1.jpg",
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Add Feast",
                                "payload": "HALL:FEAST"
                            }
                        ]
                    },{
                        "title": "Covel",
                        "subtitle" : "Dining hall if you're feeling antisocial!",
                        "image_url" : "http://www.ucla.edu/img/content-images/campus-life-housing-02.jpg",
                        "buttons" : [
                            {
                                "type": "postback",
                                "title": "Add Covel",
                                "payload": "HALL:COVEL"
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
