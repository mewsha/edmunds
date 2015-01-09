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

    
    def requestInformation(self, query):
        """query the edmund's website for auto information"""
        """query should include anything  in the URI which is """
        """after the site and before the response formatting"""
        # build URI based on examples on edmunds.com
        jsonInfo = ""
        try:
            uri = "%s%s%s" % (edmunds.fullsite, query, edmunds.appendQ)
            print "Getting: %s information" % (query)
            response = urllib2.Request(uri)
            carData = urllib2.urlopen(response)
            jsonInfo = carData.read()
        except (urllib2.HTTPError, Exception) as e:
            print "An Exception occured: {0}: {1}".format(type(e), e)
        return jsonInfo


    def getMakeJson(self, make):
        """Returns json information about a given manufacturer"""
        make = str(make).replace(" ", "-")
        return self.requestInformation(make)


    def getModelYearJson(self,make,model,year):
        """Returns json one year's information for a given make, model and year"""
        make = str(make).replace(" ", "-")
        model = str(model).replace(" ", "-")
        year = str(year)
        query = "%s/%s/%s" % (make, model, year)
        return self.requestInformation(query)


    def getPackageJson(self, styleid):
        """Returns json information for a given style id number"""
        styleid = str(styleid).replace(" ", "-")
        query = "styles/%s/engines" % (str(styleid))
        return self.requestInformation(query)


    def printMakeInfo(self, makeDict):
        """Prints formatted model information"""
        idNum = makeDict['id']
        name = makeDict['name']
        models = makeDict['models']
        print "Make ID (%d)" % (idNum)
        print "\t%s has %d model(s)" % (name, len(models))
        for model in models:
            name = model['name']
            years = model['years']
            print "\t%s created for %d year(s)" % (name, len(years))
            for year in years:
                print "\t\t(%d) %d" % (year['id'], year['year'])
        
            
    def printModelInfo(self,modelDict):
        """Prints formatted model information"""
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


    def printEngine(self, engine):
        categories = ['id', 'code', 'name', 'equipmentType', 'size', \
            'configuration', 'fuelType', 'horsepower', 'torque', \
            'totalValves', 'type', 'compressorType', 'cylinder', \
            'displacement', 'compressionRatio']

        stats = {}
        for stat in categories:
            try: value = engine[stat]
            except (KeyError): value = 'undefined'
            stats[stat] = value

        try: stats['valvCyl'] = stats['totalValves']/stats['cylinder']
        except (TypeError): stats['valvCyl']='N/A'

        print ("({idNum})  STANDARD  {energy}({fuel}) {name}  "
                "{config}{cyl}  {size}L({disp}kL)").format(idNum=stats['id'], \
                energy=stats['type'], fuel=stats['fuelType'], \
                name=stats['name'], config=stats['configuration'], \
                cyl=stats['cylinder'], size=stats['size'], \
                disp=stats['displacement'])

        print ("{hp} hp  {valvCyl} valve/cyl  "
                "{torq} pound/sqinch").format(hp=stats['horsepower'], \
            valvCyl=stats['valvCyl'], torq=stats['torque'])


    def returnStandardEngine(self,enginesDict):
        engines = enginesDict["engines"]
        for engine in engines:
            avail = engine['availability']
            if(avail=="STANDARD"):
                return engine
        return None


    def printEngineInfo(self, enginesDict):
        """Prints Standard package information, engine info"""
        try:
            engine = self.returnStandardEngine(enginesDict)
            if (engine is None):
                raise RuntimeError("No standard engine for this style")
            self.printEngine(engine)
        except (RuntimeError, Exception) as e:
            print "Exception when printing engine information"
            print type(e), e


    def printEnginesSideBySide(self, engine1Dict, engine2Dict):
        """Prints two engine's information side by side for comparison"""
        try:

            
            engine1 = self.returnStandardEngine(engine1Dict)
            if (engine1 is None):
                raise RuntimeError("No standard engine for style 1")
            engine2 = self.returnStandardEngine(engine2Dict)
            if (engine2 is None):
                raise RuntimeError("No standard engine for style 2")

            categories = ['id', 'type', 'fuelType', 'configuration',\
                'cylinder', 'size', 'displacement', 'horsepower', \
                'totalValves', 'torque']
            catDict = {}

            for stat in categories:
                try: e1 = str(engine1[stat])
                except (KeyError): e1 = 'unlisted'
                try: e2 = str(engine2[stat])
                except (KeyError): e2 = 'unlisted'
                catDict[stat] = (e1, e2)
            underline = "\033[4m"
            noformat = "\033[0m"
            print "{0}Comparsion{1}".format(underline, noformat).center(60)
            print "{0:20s}{1:20s}{2}".format(" ", "Engine 1", "Engine 2")
            for label, value in catDict.iteritems():
                print "{0:20s}{1:20s}{2}".format(label.upper(), value[0], value[1]) 

        except (RuntimeError, Exception) as e:
            print "Exception when printing engine information"
            print type(e), e

    def printPackageInfo(self,enginesDict):
        """Prints formatted engine + package information"""
        engines = enginesDict["engines"]
        for engine in engines:
            avail = engine['availability']
            if(avail=="STANDARD"):
                self.printEngine(engine)
            else: #availability is OPTIONAL
                options = engine['options']
                for o in options:
                    optId = o['id']
                    optAvail = o['availability']
                    optName = o['name'] 
                    try: optDesc = o['description']
                    except (KeyError): optDesc = "No package description"
                    print "({0}) Options for {1} model(s) {2}\n{3}".format(optId,\
                        optAvail, optName, optDesc)

                    attr = o['attributes']
                    for a in attr:
                        print "{0}- {1} ".format(a['name'], a['value'])
            print "\n"
    

    def jsonHook(self,dct):
        """hook to convert json data to dictonary"""
        return dct
            

    def formatJSON(self, jsondata):
        """Turns incoming json data into a python usable diconary"""
        data = ""
        try:
            if(jsondata is None or jsondata == ""):
                raise RuntimeError("There is no json data to decode")
            else:
                data = json.loads(jsondata, object_hook=self.jsonHook)
        except Exception as e:
            print "An exception occured in formatJSON: %s" % (e)
        return data
