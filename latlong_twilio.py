#! /usr/bin/env python
"""
Usage: %s <lat> <lon>

From lat-lon location, returns a list of venues using the Foursquare API
"""

import sys
import os
import httplib2
import foursquare
import twilio

# Twilio REST API version
API_VERSION = '2010-04-01'

# Twilio AccountSid and AuthToken
ACCOUNT_SID = 'AC02e6fc5f949b4c1b01645d52faad168b'
ACCOUNT_TOKEN = 'd72f5917a17f3c4f4504f1c3ff2e8cbb'

# Outgoing Caller ID previously validated with Twilio
CALLER_ID = '6504540072';

# Create a Twilio REST account object using your Twilio account ID and token
account = twilio.Account(ACCOUNT_SID, ACCOUNT_TOKEN)

def usage():
    sys.stdout.write( __doc__ % os.path.basename(sys.argv[0]))

def call_list(URL):
    # 1. Initiate a new outbound call to 415-555-1212
    #    uses a HTTP POST
    d = {
        'From' : CALLER_ID,
        'To' : '347-266-0830',
        'Url' : URL,
        }
    try:
        print account.request('/%s/Accounts/%s/Calls' % \
                                  (API_VERSION, ACCOUNT_SID), 'POST', d)
    except Exception, e:
        print e
        print e.read()

def make_locs(lat,lon,lim):
    # get nearby locs from foursquare
    f = foursquare.Api()
    x = f.get_venues(lat,lon,l=lim)
    r = twilio.Response()
    g = r.append(twilio.Gather(numDigits=1))
    j = 1
    for i in x['groups'][0]['venues']:
        g.append(twilio.Say("%s %s" % (repr(j), i['name'])))
        j += 1
    r.append(twilio.Redirect())
    return r
    # resp = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"
    # resp += "<Response>\n"
    # j = 1
    #     resp += ("<Say>%s %s</Say>\n" % (repr(j),i['name']))
    #     j += 1
    # resp += "</Response>"
    # resp = resp.replace('&','and')
    # return resp

if __name__ == "__main__":

    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    lat = sys.argv[1]
    lon = sys.argv[2]
    lim = 9

    locs = make_locs(lat,lon,lim)

    fh = open('/var/www/locs.xml','w')
    fh.write(repr(locs))
    fh.close()

    print locs
    call_list('http://cs.maxsobell.com/locs.xml')
