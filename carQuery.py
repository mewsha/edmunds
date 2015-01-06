#! /usr/lib/python

import edmunds as ed

class carQuery(object):

    def __init__(self):
        self.handler = ed.edmunds()


    def getYearInfo(self, make, model, year):
        try:
            jsonData = self.handler.getModelYearInfo(make, model,year)
            carInfo = self.handler.formatJSON(jsonData)
            self.handler.printModelInfo(carInfo)
        except Exception as e:
            print "An exception occured while getting year info"
            print e

        
    def getManufacturerInfo(self, maker):
        """Prints the models and years manufatured for a maker"""
        try:
            jsonData = self.handler.getMakeInfo(maker)
            makerInfo = self.handler.formatJSON(jsonData)
            self.handler.printMakeInfo(makerInfo)
        except Exception as e:
            print "An exception occured while getting manufacturer info"
            print e
		


		

