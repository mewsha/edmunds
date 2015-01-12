#! /usr/lib/python

import urllib2
import json

class RequestInformation(object)

	"""Class to query apis for edmunds"""

    protocol = 'https://'
    apiKey = '&api_key=7ac6ee6c6jer4xj23warkxzt'


    def __init__(self):
        pass

    
    def requestInformation(self, query):
        """Query the edmund's website for auto information.
        The Query should include anything in the URI which is 
        after the site and before the api key, including the ?
        and the resFormat, but no prefixed /. 
        
        eg. 
        https://api.edmunds.com/api/vehicle/v2/query?fmt=json&api_key=#

        Returns: json
        """
        # build URI based on examples on edmunds.com
        jsonInfo = ""
        try:
            uri = "%s%s%s" % (edmunds.fullsite, query, edmunds.apiKey)
            response = urllib2.Request(uri)
            carData = urllib2.urlopen(response)
            jsonInfo = carData.read()
        except (urllib2.HTTPError, Exception) as e:
            print "An Exception occured: {0}: {1}".format(type(e), e)
        return jsonInfo
