import urllib2
import json
import datetime
import csv
import time
import app

def test_func():
    # 60 day access token, need to figure out long-term solution
    access_token = "EAACEdEose0cBAO80bNUePh8rWYLLfKT8Fnp946JUoT2qE6Sl9qsJt3FCxpociUojX8lo3bFRoN9PUM31UNIbvGZCq7gPFSPohHrImcD5yxEgBr0jkje82gn7IDkvvmmdGPEZCb7TPB1NlYzx1RTZAzyksBxLqviIA4bhsbqPr6ZCyJpO54G23czUhJO5cHUZD"
    # SwipeSwap Group ID Number
    group_id = '478176852260001'
    new_JSON_posts = scrapeFacebookGroupFeedData(group_id, access_token)
    list_of_extracted_data = []
    list_of_posts = new_JSON_posts['data']
    for post in list_of_posts:
        name = ""
        message = ""
        for attribute, value in post.iteritems():
            if attribute == "from":
                name = value['name']
            if attribute == "message":
                message = value
        list_of_extracted_data.append( (name, message) )
        print "\nName: " + name + "\nMessage: " + message
    #for element in list_of_extracted_data:
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
    print json.dumps(data, indent=4, sort_keys=True)
    return data

if __name__ == '__main__':
    scrapeFacebookGroupFeedData(group_id, access_token)
