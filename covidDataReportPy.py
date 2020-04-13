# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 15:42:59 2020

@author: gonca
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import random



#Run this on console if you want a new window with charts to be created
#%matplotlib qt
#Run this on console if you want charts inline
#%matplotlib inline

#list of colors I like
colors = ['blue','orange','green','cyan','olive','fuchsia','lime','darkorange','dimgray','darkred','orangered','olivedrab','gold','lightseagreen','darkslategrey','seagreen', 'deepskyblue','dodgerblue','chocolate','goldenrod']
def resetColors():
    colors = ['blue','orange','green','cyan','olive','fuchsia','lime','darkorange','dimgray','darkred','orangered','olivedrab','gold','lightseagreen','darkslategrey','seagreen', 'deepskyblue','dodgerblue','chocolate','goldenrod']

def clr():
    plt.close()
    resetColors()
    
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
    
    def color(self, lis):
        color = random.choice(colors)
        colors.remove(color)
        if len(colors) == 0:
            resetColors()    
        return color
    
    def configureChart(self, chart, country, color=''):
        color = self.color(colors)
        plt.title('Confirmed Cases of COVID-19')
        plt.xlabel('Date')
        plt.ylabel('Confirmed Cases')
        self.chart = chart.plot(grid= True, subplots=True, figsize=(12, 9), label=country, color=color)
        plt.legend(loc='best')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        return self.chart
        
    def plotCountry(self, country):
        dataCountry = self.findDataOf(country)
        self.configureChart(dataCountry, country)
        plt.show()
        
    def compareCountryPlot(self, country_1, country_2):
        dataCountry1 = self.findDataOf(country_1)
        dataCountry2 = self.findDataOf(country_2)
        color_1 = self.color(colors)
        color_2 = self.color(colors)
        self.configureChart(dataCountry1, country_1, color_1)
        self.configureChart(dataCountry2, country_2, color_2)
        plt.show()


class Brasil(Data):        
    def readDataFrom(self, file):
        data = pd.read_csv(file, sep=';', encoding='ISO-8859-1')
        return data
    
    def groupBy(self, by_Region_or_State):
        by = by_Region_or_State
        dic = {'Region':'regiao','State':'estado'}
        a = self.data.groupby(dic[by])['casosNovos','obitosNovos'].sum()
        a.columns = ['Confirmed cases','Deaths']
        return a
    
    def plotBarChartBy(self, by_Region_or_State, in_same_chart=True):
        if in_same_chart == True:
            sp = False
        else:
            sp = True
        by = by_Region_or_State
        df = self.groupBy(by)
        color_1 = color(colors)
        color_2 = color(colors)
        chart = df.plot.bar(title=('COVID-19 by brazilian ' + by), grid = True, subplots=sp, color=(color_1,color_2))
        plt.legend(loc='best')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()
        
    def findDataOf(self, state, region=''):
        regionData = self.data[self.data['estado'].str.contains(state)]
        del regionData['obitosNovos']
        del regionData['casosNovos']
        del regionData['estado']
        if region == '':
            del regionData['regiao']
        cases = regionData['casosAcumulados'].iloc[-1]
        print ('Number of confirmed cases in ' + str(state) + ' is ' + str(cases))
        return regionData
    
    '''
    def configureChart(self, chart, state, color='orangered'):
        fig = plt.figure()
        plt.rcParams['figure.figsize'] = (15,12)
        del chart['obitosAcumulados']
        plt.title('Cases of COVID-19 in '+ str(state))
        plt.xlabel('Date')
        plt.ylabel('Confirmed Cases')
        dates = []
        for item in chart['data']:
            item = str(item)
            dates.append(item)
        print (dates)
        plt.xticks(range(len(dates)), dates)
        #plt.plot(dates, chart['casosAcumulados'])
        chart.plot()
        #chart.plot(grid= True, subplots=True, figsize=(12, 9), label=state, color=color)
        plt.legend(loc='best')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
    '''


    def configureChart(self, chart, state, color='orangered'):
        dates = []
        for item in chart['data']:
            item = str(item)
            dates.append(item)
        dates = [datetime.strptime(x, '%d/%m/%Y') for x in dates]
        print(dates)
        self.chart = chart.plot(xticks=dates, grid= True, subplots=True, figsize=(12, 9), label=state, color=color)
        plt.legend(loc='best')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        return self.chart
    
    def plotState(self, state):
        dataState = self.findDataOf(state)
        self.configureChart(dataState, state)
        #self.chart.set_xticklabels(dataState['data'])
        #plt.plot(dataState['data'],dataState['casosAcumulados'])
        plt.show()
        
        
world = Data('dataCOVID.csv')
br = Brasil('dataBrasil.csv')


#setlimitdate
#https://covid.saude.gov.br/
        