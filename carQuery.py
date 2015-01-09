#! /usr/lib/python

import edmunds as ed

class carQuery(object):

    def __init__(self):
        self.handler = ed.edmunds()


    def getStyleInfo(self, make, model, year):
        try:
            jsonData = self.handler.getModelYearJson(make, model,year)
            carInfo = self.handler.formatJSON(jsonData)
            self.handler.printModelInfo(carInfo)
        except Exception as e:
            print "An exception occured while getting year info"
            print e

        
    def getManufacturerInfo(self, maker):
        """Prints the models and years manufatured for a maker"""
        try:
            jsonData = self.handler.getMakeJson(maker)
            makerInfo = self.handler.formatJSON(jsonData)
            self.handler.printMakeInfo(makerInfo)
        except Exception as e:
            print "An exception occured while getting manufacturer info"
            print type(e), e


    def getPackageInfo(self, styleId):
        try:
            jsonData = self.handler.getPackageJson(styleId)
            packageInfo = self.handler.formatJSON(jsonData)
            self.handler.printPackageInfo(packageInfo)
        except Exception as e:
            print "An exception occured while getting package info"
            print type(e), e 

    def getEngineInfo(self, styleId):
        try:
            jsonData = self.handler.getPackageJson(styleId)
            packageInfo = self.handler.formatJSON(jsonData)
            self.handler.printEngineInfo(packageInfo)
        except Exception as e:
            print "An exception occured while getting engine info"
            print type(e), e 
        

    def compareEngines(self, style1id, style2id):
        """compares engines for two cars"""
        try:
            jsonData1 = self.handler.getPackageJson(style1id)
            jsonData2 = self.handler.getPackageJson(style2id)
            engine1data = self.handler.formatJSON(jsonData1)
            engine2data = self.handler.formatJSON(jsonData2)
            self.handler.printEnginesSideBySide(style1id=engine1data, style2id=engine2data)
        except Exception as e:
            print "An exception occured while comparing engines"
            print type(e), e
        

