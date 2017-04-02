import urllib2
import json
import datetime
import csv
import time
import app
import language

def test_func():
    # 60 day access token, need to figure out long-term solution
    access_token = "EAACEdEose0cBAOvKzF2WNLgPpaZC8IetUoQKOz3nCTEhbCv5S1EqxlzL3R2BVByEvTXhugZBQPh6ZBkVWlxJaeDTPHYpcR8o69SCU2P5Cax5DzY3ZCX2d0DRxwbjaBuk8xOkbDfdIdZBSWBOwyHJT2XbFJZBb4IZCGHfcch0R89K0vcsVA5oMTLzZA95mJstlQQZD"
    # SwipeSwap Group ID Number
    group_id = '478176852260001'
    new_JSON_posts = scrapeFacebookGroupFeedData(group_id, access_token)
    list_of_extracted_data = []
    list_of_posts = new_JSON_posts['data']
    for post in list_of_posts:
        name = ""
        uid = ""
        message = ""
        for attribute, value in post.iteritems():
            if attribute == "from":
                uid = value['id']
                name = value['name']
            if attribute == "message":
                message = value
        list_of_extracted_data.append( (name, message, uid) )
        # print "\nName: " + name + "\nMessage: " + message
    for element in list_of_extracted_data:
        final_post_data_dict = language.process_language(element[0], element[1], element[2])
        print final_post_data_dict
        #print element[0], element[1]
    # make a call to handle_payload in app.py

def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while not success:
        try:
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)

            print "Error for URL %s: %s" % (url, datetime.datetime.now())

    return response.read()

def scrapeFacebookGroupFeedData(group_id, access_token):

    scrape_interval = 345600 # Change this to adjust scrape time interval
    since_time = str(int(time.time() - scrape_interval))
    until_time = str(int(time.time()))
    # construct the URL string
    base = "https://graph.facebook.com/v2.8"
    node = "/" + group_id + "/feed"
    # Add or subtract from parameters to customize return data
    parameters = "/?fields=created_time,from,message&since=%s&until=%s&access_token=%s" % (since_time, until_time, access_token)
    url = base + node + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))
    # print json.dumps(data, indent=4, sort_keys=True)
    return data

if __name__ == '__main__':
    scrapeFacebookGroupFeedData(group_id, access_token)
