#! /usr/lib/python
import urllib2
import json

class edmunds(object):
    """Class to query the vehicle api for edmunds"""

    protocol = 'https://'
    resFormat = 'fmt=json'
    apiKey = '&api_key=7ac6ee6c6jer4xj23warkxzt'
    site = 'api.edmunds.com/api/vehicle/v2/'
    fullsite = protocol + site


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


    def getMakeJson(self, make):
        """Years and Models of given manufacturer's vehicles

        Returns: json
        """
        make = str(make).strip()
        make = make.replace(" ", "-")
        query = "{make}?{resFmt}".format(make=make, resFmt=edmunds.resFormat)
        print("Getting {make} info:").format(make=make)
        return self.requestInformation(query)


    def getModelYearJson(self,make,model,year):
        """
        Package information for a given make, model and year

        Returns: json
        """
        make = str(make).strip()
        make = make.replace(" ", "-")
        model = str(model).strip()
        model = model.replace(" ", "-")
        year = str(year).strip()
        query = "{make}/{model}/{year}?{resFmt}".format(make=make,\
                model=model, year=year, resFmt=edmunds.resFormat)
        print("Getting {make} {model} {year} info:").format(make=make, \
                                                           model=model,\
                                                           year=year)
        return self.requestInformation(query)

    def getVinDecoded(self,vin):
        """
        Decode Vin number into a make, model, style 
        and other useful information.

        Returns: json
        """
        vin = str(vin).strip()
        vin = vin.replace(" ", "-")
        query = ("vins/{vin}?{resFmt}").format(vin=vin,\
                 resFmt=edmunds.resFormat)
        
        print("Getting {vin} info:").format(vin=vin)
        return self.requestInformation(query)

    def getTMVPrice(self, styleid, condition, mileage, zipcode):
        """
        Returns the estimated true market value for a car with it's
        styleid, condition, number of miles and sale location. 

        Returns: json
        """
        styleid = str(styleid).strip()
        styleid = styleid.replace(" ", "-")
        condition = str(styleid).strip()
        styleid = styleid.replace(" ", "-")
                styleid = str(styleid).strip()
        styleid = styleid.replace(" ", "-")
                styleid = str(styleid).strip()
        styleid = styleid.replace(" ", "-")
               

    def getPackageJson(self, styleid):
        """
        Information for a given style id number

        Returns: json
        """
        styleid = str(styleid).strip()
        styleid = styleid.replace(" ", "-")
        query = "styles/{idNum}/engines?{resFmt}".format(\
                idNum=styleid, resFmt=edmunds.resFormat)
        return self.requestInformation(query)


    def printMakeInfo(self, makeDict):
        """
        Prints formatted model information

        Returns: None
        """
        idNum = makeDict['id']
        name = makeDict['name']
        models = makeDict['models']
        print "Make ID (%d)" % (idNum)
        print "\t%s has %d model(s)" % (name, len(models))
        #Extract out the model information and print each
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
        #Extract the style information and print each style
        for style in styles:
            sid = style['id']
            name = style['name']
            submodel = style['submodel']
            modelname = submodel['modelName']
            trim = style['trim']
            print "\t%s %s, %s (%d)" % (trim,modelname,name,sid)


    def printStandardEngine(self, engine):
        """Prints information about an engine"""
        categories = ['id', 'code', 'name', 'equipmentType', 'size', \
                    'configuration', 'fuelType', 'horsepower', \
                    'torque', 'totalValves', 'type', 'compressorType', \
                    'cylinder', 'displacement', 'compressionRatio']
        #Extract out the engine statistics 
        stats = {}
        for stat in categories:
            try: 
                value = engine[stat]
            except (KeyError, Exception): 
                value = 'undefined'
            stats[stat] = value
        #Calculate the number of valves per cylinder
        try: 
            stats['valvCyl'] = stats['totalValves']/stats['cylinder']
        except (TypeError, Exception): 
            stats['valvCyl']='N/A'
        print ("({idNum})  STANDARD  {energy}({fuel}) {name}  "
                "{config}{cyl}  {size}L({disp}kL)").format(\
                idNum=stats['id'], energy=stats['type'], \
                fuel=stats['fuelType'], name=stats['name'], \
                config=stats['configuration'], cyl=stats['cylinder'],\
                size=stats['size'], disp=stats['displacement'])
        print ("{hp} hp  {valvCyl} valve/cyl {torq} pound/"
                "sqinch").format(hp=stats['horsepower'], \
                valvCyl=stats['valvCyl'], torq=stats['torque'])
        print ("code: {code}").format(\
                code=stats['code'])


    def returnStandardEngine(self,enginesDict):
        """Extracts the standard engine information from package dict"""
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
            self.printStandardEngine(engine)
        except (RuntimeError, Exception) as e:
            print "Exception when printing engine information"
            print type(e), e


    def printEnginesSideBySide(self, **packagesDicts):
        """Prints two engine's information side by side"""
        try:
            # get each style's engine information
            engines = []
            styleIds = packagesDicts.keys()
            for style in styleIds:  
                engine = self.returnStandardEngine(packagesDicts[style])
                if (engine is None):
                    print ("No engine information found for engine "
                            "{0}").format(style)
                    engine = {'style':'notFound '+ style}
                else:
                    engine['style'] = style
                engines.append(engine)

            categories = ['style', 'id', 'type', 'fuelType', 'configuration',\
                'cylinder', 'size', 'displacement', 'horsepower', \
                'totalValves', 'torque']
            data = {x:[] for x in categories}
            
            #Pull out stats which are important for comparison into dict
            for label in categories:
                stats = [] 
                for engine in engines:
                    try: value = engine[label]
                    except (KeyError): value = 'unlisted'
                    stats.append(value)
                data[label] = stats

            #print out the stats for all styles, side by side
            underline = "\033[4m"
            noformat = "\033[0m"
            print "{0}Comparsion{1}".format(underline, noformat).center(60)
            for label, stats in data.iteritems():
                line = "{0:20s}".format(label.upper())
                for stat in stats:
                    line = line + "{0:20s}".format(str(stat))
                print line

        except (RuntimeError, Exception) as e:
            print "Exception when printing engine information"
            print type(e), e


    def printPackageInfo(self,enginesDict):
        """Prints formatted engine + package information"""
        engines = enginesDict["engines"]
        for engine in engines:
            avail = engine['availability']
            if(avail=="STANDARD"):
                self.printStandardEngine(engine)
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
    

    def printVinInfo(self, vinDict):
        """Prints information inside a vin dictionary"""
        try:
            vin = vinDict['vin']
            print "Vin: {0}".format(vin)
            make = vinDict['make']['name']
            model = vinDict['model']['name']
            print "{0} {1}".format(make, model)
            epaClass = vinDict['categories']['EPAClass']
            market = vinDict['categories']['market']
            size = vinDict['categories']['vehicleSize']
            style = vinDict['categories']['vehicleStyle']
            print " {0} {1}, {2} {3}".format(size, style, market, epaClass)
            mpg = vinDict["MPG"]
            print "MPG: city-{0} highway-{1}".format(mpg['city'],mpg['highway'])
            trans = vinDict["transmission"]['transmissionType']
            print "Transmission: {0}".format(trans)
            try:
                self.printStandardEngine(vinDict['engine'])
            except (KeyError, Exception):
                print "No engine information listed."
        except (Exception) as e:
            print "An exception occured printing vin information"
            print type(e), e

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
