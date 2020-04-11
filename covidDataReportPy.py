# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 15:42:59 2020

@author: gonca
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Run this on console if you want a new window with charts to be created
#%matplotlib qt
#Run this on console if you want charts inline
#%matplotlib inline

class Data:
    def __init__(self, file):
        self.data = self.readDataFrom(file)
        
    def readDataFrom(self, file):
        data = pd.read_csv(file, sep=',', encoding='ISO-8859-1')
        del data['Lat']
        del data['Long']
        del data['Province/State']
        return data
        
    def findDataOf(self, country):
        regionData = self.data[self.data['Country/Region'].str.contains(country)]
        del regionData['Country/Region']
        regionData = regionData.sum(axis=0)
        cases = regionData.iloc[-1]
        print ('Number of confirmed cases in ' + str(country) + ' is ' + str(cases))
        return regionData
    
    def configureChart(self, chart, country, color='orangered'):
        #fig,chart = plt.figure()
        plt.rcParams['figure.figsize'] = (15,12)
        plt.title('Confirmed Cases of COVID-19')
        plt.xlabel('Date')
        plt.ylabel('Confirmed Cases')
        chart.plot(grid= True, subplots=True, figsize=(12, 9), label=country, color=color)
        plt.legend(loc='best')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()
        
    def plotCountry(self, country):
        dataCountry = self.findDataOf(country)
        self.configureChart(dataCountry, country)
        
    def compareCountryPlot(self, country_1, country_2):
        dataCountry1 = self.findDataOf(country_1)
        dataCountry2 = self.findDataOf(country_2)
        self.configureChart(dataCountry1, country_1, 'fuchsia')
        self.configureChart(dataCountry2, country_2, 'lime')


#setlimitdate
        