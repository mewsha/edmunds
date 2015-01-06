#! /usr/lib/python
import urllib2
import json

class edmunds(object):


    protocol = 'https://'
    resFormat = '?fmt=json'
    apiKey = '&api_key=7ac6ee6c6jer4xj23warkxzt'
    site = 'api.edmunds.com/api/vehicle/v2/'
    fullsite = protocol + site
    appendQ = resFormat + apiKey


    def __init__(self):
		pass

    
    def getInformation(self, query):
		"""query the edmund's website for auto information"""
		# build URL based on examples on edmunds.com
		jsonInfo = ""
		try:
			url = "%s%s%s" % (edmunds.fullsite, query, edmunds.appendQ)
			print "Getting: %s information" % (query)
			response = urllib2.Request(url)
			carData = urllib2.urlopen(response)
			jsonInfo = carData.read()
		except Exception as e:
			print "An Exception occured: %s" % e
		return jsonInfo


    def getMakeInfo(self, make):
		"""Returns json information about a given manufacturer"""
		return self.getInformation(make)
   


    def getModelYearInfo(self,make,model,year):
		"""Returns json one year's information for a given make, model and year"""
		query = "%s/%s/%s" % (str(make), str(model), str(year))
		return self.getInformation(query)


    def printModelInfoDump(self, carDict):
		"""dumps model information, not pretty"""
		for key,value in carDict.iteritems():
			if (key == 'styles'):
				for style in value:
					for skey, sval in style.iteritems():
						if(skey == 'submodel'):
							print skey, sval['body']
						else:
							print skey, sval
			else:	
				print key,value


    def printMakeInfo(self, makeDict):
		"""Prints Maker information in neat form"""
		idNum = makeDict['id']
		name = makeDict['name']
		models = makeDict['models']
		print "Make ID (%d)" % (idNum)
		print "\t%s has %d model(s)" % (name, len(models))
		for model in models:
			name = model['name']
			years = model['years']
			print "\t%s was created for %d year(s)" % (name, len(years))
			for year in years:
				print "\t\t(%d) %d" % (year['id'], year['year'])
	    
		    
    def printModelInfo(self,modelDict):
		"""Prints model information in neat form"""
		idNum = modelDict['id']
		year = modelDict['year']
		styles = modelDict['styles']
		print "Model ID (%d)" % (idNum)
		print "\t%d has %d style(s)" % (year,len(styles))
		for style in styles:
			sid = style['id']
			name = style['name']
			submodel = style['submodel']
			modelname = submodel['modelName']
			trim = style['trim']
			print "\t%s %s, %s (%d)" % (trim,modelname,name,sid)


    def jsonHook(self,dct):
		"""hook to convert json data to dictonary"""
		return dct
		    

    def formatJSON(self, jsondata):
		"""Turns incoming json data into a python usable diconary"""
		data = ""
		try:
			if(jsondata != ""):
				data = json.loads(jsondata, object_hook=self.jsonHook)
			else:
				print "There is no json data to decode. Please check your URL"
		except Exception as e:
			print "An exception has occured: %s" % (e)
		return data
