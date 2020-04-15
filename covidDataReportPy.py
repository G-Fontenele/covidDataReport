# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 15:42:59 2020

@author: gonca
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import random
import tkinter as tk
import requests

'''

Data came from:
    Brazil: https://covid.saude.gov.br/
    World: https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases

'''
#Run this on console if you want a new window with charts to be created
#%matplotlib qt
#Run this on console if you want charts inline
#%matplotlib inline



world = Data('dataCOVID.csv')
br = Brasil('dataBrasil.csv')

#list of colors I like
colors = ['blue','orange','green','cyan','olive','fuchsia','lime','darkorange','dimgray','darkred','orangered','olivedrab','gold','lightseagreen','darkslategrey','seagreen', 'deepskyblue','dodgerblue','chocolate','goldenrod']
def resetColors():
    colors = ['blue','orange','green','cyan','olive','fuchsia','lime','darkorange','dimgray','darkred','orangered','olivedrab','gold','lightseagreen','darkslategrey','seagreen', 'deepskyblue','dodgerblue','chocolate','goldenrod']

def clr():
    plt.close()
    resetColors()

def refreshWorld():
    world.refreshData('dataCOVID.csv')
   
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configureWindow(parent)
        

        
    def configureWindow(self, master):
        master.title('COVID-19 Analysis')

        #master.geometry('1300x650+10+10')
        master.configure(bg='white')
        
        self.frame1 = tk.Frame(master, bg='white')
        
        #Frame 1 - country selction
        self.lb1 = tk.Label(self.frame1, text='Select Country to Plot', bg = 'white')
        self.lb2 = tk.Label(self.frame1, text='Confirmed Cases x Time', bg = 'white')
        self.scrollbar = tk.Scrollbar(self.frame1, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.frame1, yscrollcommand=self.scrollbar.set, highlightcolor=random.choice(colors), bg='white')
        self.listbox.insert(tk.END, *world.data['Country/Region'])
        self.scrollbar.config(command=self.listbox.yview)
        self.lb1.pack(fill=tk.BOTH)
        self.lb2.pack(fill=tk.BOTH)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(fill=tk.BOTH, expand=1)
        self.plotCountryButton = tk.Button(self.frame1, text="Plot Country", command=self.plotCountryCommand)
        self.plotCountryButton.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        
        self.frame2 = tk.Frame(master, bg='white')
        
        #Frame 2
        self.lbCountryTitle = tk.Label(self.frame2, text='Country', bg = 'white')
        self.lbCountry = tk.Label(self.frame2, text='', bg = 'white')
        self.lbCasesTitle = tk.Label(self.frame2, text='Confirmed Cases', bg = 'white')
        self.lbCases = tk.Label(self.frame2, text='', bg = 'white')
        self.clearButton = tk.Button(self.frame2, text="Clear Chart", command=self.clearAll)

        
        self.lbCountryTitle.pack(side = tk.TOP, fill=tk.BOTH)
        self.lbCountry.pack(side = tk.TOP, fill=tk.BOTH)
        self.lbCasesTitle.pack(side = tk.TOP, fill=tk.BOTH)
        self.lbCases.pack(side = tk.TOP, fill=tk.BOTH)
        self.clearButton.pack(side = tk.BOTTOM, fill=tk.BOTH)
        
        self.frame1.pack(side=tk.LEFT)
        self.frame2.pack(side=tk.RIGHT)

        '''
        self.close_button = tk.Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.label = tk.Label(master, text="Choose an option of the above to plot a chart")
        self.label.pack()
        ''' 
  
    def plotCountryCommand(self):
        index = self.listbox.curselection()
        country = world.data['Country/Region'].iloc[index[0]]
        print(country+' was selected')
        world.plotCountry(country)
        self.lbCountry['text'] = country
        self.lbCases['text'] = world.cases
        return country
    
    def clearAll(self):
        clr()
        self.lbCountry['text'] = 'Cleared'
        self.lbCases['text'] = ''
        
        
class Data:
    def __init__(self, file):
        self.data = self.readDataFrom(file)
        
    def refreshData(self, fileName, url='https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv'):
        print('Beginning file download with requests of world data from ' + str(url))

        self.url = url
        r = requests.get(self.url)
        
        with open(fileName, 'wb') as f:
            f.write(r.content)

        # Retrieve HTTP meta-data
        print(r.status_code)
        print(r.headers['content-type'])
        print(r.encoding)
        
        
    def getDate(self):
        dfList = self.data.columns.values.tolist()
        date = dfList[-1]
        print ('In US Format: mm/dd/yyyy')
        return date
        
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
        self.cases = regionData.iloc[-1]
        print ('Number of confirmed cases in ' + str(country) + ' is ' + str(self.cases))
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

    def logPlot(self, country):
        i=0
        newCases = []
        dataCountry = self.findDataOf(country)
        print ('dataC size is ' + str(dataCountry.size))
        length = dataCountry.size - 1
        while i < (length):
            dailyNewCases = dataCountry.iloc[i+1] - dataCountry.iloc[i]
            print (dailyNewCases)
            newCases.append(dailyNewCases)
            i += 1
        print (newCases)
        color = self.color(colors)
        dataCountry.drop(dataCountry.tail(1).index,inplace=True)
        plt.title('Logaritm scale Cases x New Cases')
        plt.xlabel('New Cases')
        plt.ylabel('Confirmed Cases')
        plt.yscale('log')
        plt.xscale('log')
        plt.grid(True)
        plt.plot(dataCountry, newCases)
        plt.show()

class Brasil(Data):        
    def readDataFrom(self, file):
        data = pd.read_csv(file, sep=';', encoding='ISO-8859-1')
        return data

    def getDate(self):
        dfList = self.data['data']
        date = dfList.iloc[-1]
        print ('In international Format')
        return date
    
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

    def configureChartForCurve(self, chart, state, color=''):
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(8,3), gridspec_kw={'wspace':.2})
        color = self.color(colors)
        dates = []
        for item in chart['data']:
            item = str(item)
            dates.append(item)
        ax1.plot(dates,chart['casosAcumulados'])
        ax2.plot(dates,chart['obitosAcumulados'])
        
        fig.suptitle('COVID-19 Analysis - ' + str(state), fontsize=16)
        
        
        ax1.set_title('Cases of COVID-19 in '+ str(state))
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Confirmed Cases')
        
        #ax1.legend(loc='best')
        ax1.grid(True)
        
        ax2.set_title('Deaths of COVID-19 in '+ str(state))
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Deaths')

        #ax2.legend(loc='best')
        ax2.grid(True)
        
        locator=ticker.MaxNLocator(prune='both', nbins=5)
        ax1.xaxis.set_major_locator(locator)
        ax2.xaxis.set_major_locator(locator)
        
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()

        return fig
    
    def plotState(self, state):
        dataState = self.findDataOf(state)
        self.configureChartForCurve(dataState, state).show()
        


'''
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)

    root.call('wm', 'attributes', '.', '-topmost', '1')
    root.mainloop()
'''  

#setlimitdate
#https://covid.saude.gov.br/
        