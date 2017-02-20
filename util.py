import sys

# simple wrapper for logging to stdout on heroku
def log(message):
    print str(message)
    sys.stdout.flush()