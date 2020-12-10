#Librerías de flask y tweepy
from flask import jsonify

#Librerías propias
from modules.tweet import Tweet

class response:
    def getJson(pData):
        return jsonify({
            "status": "success",
            "message": "",
            "data": pData
        })
        
class chart:
    data = []
    label = ""
    chartLabels = []
    results = {};

    def setData(self, pData):
        self.data = pData

    def setLabel(self, pLabel):
        self.label = pLabel

    def setChartLabels(self, pChartLabels):
        self.chartLabels = pChartLabels

    def getResponse(self):
        self.results = {
            "data": self.data,
            "label": self.label,
            "chartLabels": self.chartLabels
        }
        return response.getJson(self.results)

class textList:
    data = []
    results = {}

    def setData(self, pData):
        self.data = pData

    def getResponse(self):
        self.results = {
            "data": self.data
        }
        return response.getJson(self.results)
