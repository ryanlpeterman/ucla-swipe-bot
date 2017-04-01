import urllib2
import json
import datetime
import csv
import time

def test_func():
    # Need to acquire a more lasting access token
    access_token = "EAAP7YKc9WqsBAGxS8GZCihlqy6NS2yeZCONKyXcwgPB3sa7tlhd8fkOF0Ep5oteD23iWANYuStmr2FrVDWKVbtt0SxpTuSRsMfQwcjk5T9qSfWVQfGapdNWGFJqYW2Wy8759tfRnHB3rJbhBpVsVOLaEkTEZBkZD"
    group_id = '478176852260001'
    scrapeFacebookGroupFeedData(group_id, access_token)

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

    scrape_interval = 7200 # Change this to adjust scrape time interval
    since_time = str(int(time.time() - scrape_interval))
    until_time = str(int(time.time()))
    # construct the URL string
    base = "https://graph.facebook.com/v2.3"
    node = "/" + group_id + "/feed"
    # Add or subtract from parameters to customize return data
    parameters = "/?fields=created_time,from,message&since=%s&until=%s&access_token=%s" % (since_time, until_time, access_token)
    url = base + node + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    print json.dumps(data, indent=4, sort_keys=True)

if __name__ == '__main__':
    scrapeFacebookGroupFeedData(group_id, access_token)
