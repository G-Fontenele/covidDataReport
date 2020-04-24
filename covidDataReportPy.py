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
from tkinter import messagebox
import requests
import webbrowser
#from tempfile import NamedTemporaryFile


'''
The program is not generalized.
It only works from the dataset of the links below
'''

'''

Data came from:
    Brazil: https://covid.saude.gov.br/
    World: https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases

'''
#Run this on console if you want a new window with charts to be created
#%matplotlib qt
#Run this on console if you want charts inline
#%matplotlib inline




#list of colors I like
colors = ['blue','orange','green','cyan','olive','fuchsia','lime','darkorange','dimgray','darkred','orangered','olivedrab','gold','lightseagreen','darkslategrey','seagreen', 'deepskyblue','dodgerblue','chocolate','goldenrod']
def resetColors():
    colors = ['blue','orange','green','cyan','olive','fuchsia','lime','darkorange','dimgray','darkred','orangered','olivedrab','gold','lightseagreen','darkslategrey','seagreen', 'deepskyblue','dodgerblue','chocolate','goldenrod']

#This will clear the present figure you are using to plot in the moment
#each time the function is executed it closes a window
def clr():
    plt.close()
    resetColors()

# download the link of the data you want from humData
def refreshWorld():
    world.refreshData('dataCOVID.csv')

#Tk inter app 
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        #creat the master
        self.parent = parent
        self.configureWindow(parent)
        self.msg = 1

        
    #The window was designed in order to be placed in the side of the screen,
    #that´s why it´s so thin
    # Window configuration: all buttons and labels
    def configureWindow(self, master):
        #Color of the background
        self.configuredColor = 'white'
        #Font of the title
        self.configuredFonte = 'Raleway'
        
        #Title of the root window
        master.title('COVID-19 Analysis')
        master.resizable(0,0)

        #It opens in the superior left side
        master.geometry('200x740+0+0')
        master.configure(bg=self.configuredColor)
    
        #Creation of two frames that will be placed the other frames
        self.bigFrame1 = tk.Frame(master, bg=self.configuredColor)
        self.bigFrame2 = tk.Frame(master, bg=self.configuredColor)
        
        self.frame1 = tk.Frame(self.bigFrame1, bg=self.configuredColor)
        
        #Frame 1 - country selction
        self.lb1 = tk.Label(self.frame1, text='Select Country to Plot', bg = self.configuredColor)
        self.lb2 = tk.Label(self.frame1, text='Confirmed Cases x Time', bg = self.configuredColor)
        self.scrollbar = tk.Scrollbar(self.frame1, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.frame1, yscrollcommand=self.scrollbar.set, highlightcolor=random.choice(colors), bg=self.configuredColor)
        self.listbox.insert(tk.END, *world.data['Country/Region'].drop_duplicates())
        self.scrollbar.config(command=self.listbox.yview)
        self.lb1.pack(fill=tk.BOTH)
        self.lb2.pack(fill=tk.BOTH)
        #self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(fill=tk.BOTH, expand=1)
        self.plotCountryButton = tk.Button(self.frame1, text="Plot Country", command=self.plotCountryCommand)
        self.plotCountryButton.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        self.frame3 = tk.Frame(self.bigFrame2, bg=self.configuredColor)
        
        #Frame 3
        self.lbBrasil = tk.Label(self.frame3, text='Plot Brazil Data: Bar Chart', bg = self.configuredColor)
        self.buttonBarRegion = tk.Button(self.frame3, text='Plot By Region', command = self.plotBarChartRegion)
        self.buttonBarState = tk.Button(self.frame3, text='Plot By State', command = self.plotBarChartState)
        self.lbBrasil.pack(side = tk.TOP, fill=tk.BOTH)
        self.buttonBarRegion.pack(side = tk.LEFT, fill=tk.BOTH)
        self.buttonBarState.pack(side = tk.RIGHT, fill=tk.BOTH)
        
        self.frame4 = tk.Frame(self.bigFrame2, bg=self.configuredColor)
        
        '''
        The listbox does not have a scrollbar itself,
        I decided to let just the scroll of the mouse or the dash movement
        There is a problem once one of the scrollbar(when placed) it moves the other one
        '''
        #Frame 4
        self.lbStateListbox = tk.Label(self.frame4, text='Select State to Plot', bg = self.configuredColor)
        self.stateScrollbar = tk.Scrollbar(self.frame4, orient=tk.VERTICAL)
        self.stateListbox = tk.Listbox(self.frame4, yscrollcommand=self.stateScrollbar.set, highlightcolor=random.choice(colors), bg=self.configuredColor)
        self.stateListbox.insert(tk.END, *br.data['estado'].drop_duplicates())
        self.scrollbar.config(command=self.stateListbox.yview)
        self.lbStateListbox.pack(fill=tk.BOTH)
        #self.stateScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stateListbox.pack(fill=tk.BOTH, expand=1)
        self.stateSelected = self.stateListbox.curselection()
        self.plotStateButton = tk.Button(self.frame4, text="Plot State "+str(self.stateSelected), command=self.plotStateCommand)
        self.plotStateButton.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        
        self.frame5 = tk.Frame(self.bigFrame2, bg=self.configuredColor)
        
        #Frame 5
        self.clearButton = tk.Button(self.frame5, text="Clear chart", command=self.clearAll)
        
        self.clearButton.pack(side = tk.BOTTOM, fill=tk.BOTH, pady = 5)

        self.title = tk.Label(self.bigFrame1, text='COVID-19 REPORT', font='Raleway 15 bold', bg = self.configuredColor)
        self.title.pack()
        self.bigFrame1.pack(padx = 4, pady = 5)
        self.bigFrame2.pack(padx = 4, pady = 5)
        
    

        #Date refresh and show updates
        self.dateLabel = tk.Label(self.frame5, text="Last update - US format", bg=self.configuredColor)
        self.dateLabel1 = tk.Label(self.frame5, text="World Data", bg=self.configuredColor)
        self.dateLabel2 = tk.Label(self.frame5, text=world.getDate(), bg=self.configuredColor)
        self.dateLabel3 = tk.Label(self.frame5, text="Brasil Data", bg=self.configuredColor)
        brDate = br.getDate()
        self.dateLabel4 = tk.Label(self.frame5, text=brDate, bg=self.configuredColor)
        
        self.dateLabel.pack(fill=tk.BOTH)
        self.dateLabel1.pack(fill=tk.BOTH)
        self.dateLabel2.pack(fill=tk.BOTH)
        self.dateLabel3.pack(fill=tk.BOTH)
        self.dateLabel4.pack(fill=tk.BOTH)
        

        self.title.pack()
        self.frame1.pack()
        #self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()
        self.frame5.pack(fill = tk.BOTH, padx = 1, pady =5)


        
        self.closeButton = tk.Button(master, text="Close", command=master.quit)
        self.closeButton.pack(side=tk.LEFT, padx = 2, fill=tk.BOTH, expand=1, pady=2)
        self.msgButton = tk.Button(master, text="Disable MSG BOX", command=self.desMsg)
        self.msgButton.pack(side=tk.RIGHT, padx = 2, fill=tk.BOTH, expand=1, pady=2)
        
        
    #This will plot the country selected on matplotlib figure
    def plotCountryCommand(self):
        index = self.listbox.curselection()
        country = world.data['Country/Region'].drop_duplicates().iloc[index[0]]
        print(country+' was selected')
        world.plotCountry(country)
        if self.msg == 1:
            messagebox.showinfo('Confirmed Cases in '+str(country), str(country)+' has '+str(world.cases)+' confirmed cases of COVID-19.')
        return country
    
    #This is connected to brazilian data
    def plotStateCommand(self):
        index = self.stateListbox.curselection()
        state = br.data['estado'].drop_duplicates().iloc[index[0]]
        print(state+' was selected')
        br.plotState(state)
        return state
    
    #this will plot the region group by from Brazil
    def plotBarChartRegion(self):
        return br.plotBarChartBy('Region')
    
    def plotBarChartState(self):
        return br.plotBarChartBy('State')
    
    def getDataFrame(self, dataframe):
        br.dfWindow(dataframe)
        return

    '''    
    def closeWindow(self):
        master.quit
        
    def data(self):
        return
    
    def helpGuide(self):
        return

    '''
    def desMsg(self):
        self.msg += -1
        self.msg = abs(self.msg)
        if self.msg == 1:
            self.msgButton['text'] = 'Disable MSG BOX' #This msg is shown with the confirmed cases of each country
        else:
            self.msgButton['text'] = 'Enable MSG BOX' 

        return self.msg
    
    def clearAll(self):
        clr()

        
#Top class of the data analysis
#this one should derivate the other classes
#like the brazilian one
class Data:
    def __init__(self, file):
        self.data = self.readDataFrom(file)
        
    def refreshData(self, fileName, url='https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv'):
        print('Beginning file download with requests of world data from ' + str(url))

        self.url = url
        r = requests.get(self.url) #module requests, get data from a website, link on the entry opf function
        
        with open(fileName, 'wb') as f:
            f.write(r.content)

        # Retrieve HTTP meta-data
        print(r.status_code)
        print(r.headers['content-type'])
        print(r.encoding)
        
        world = Data('dataCOVID.csv')

        
    #get the last date that was ploted on a graph
    def getDate(self):
        dfList = self.data.columns.values.tolist()
        date = dfList[-1]
        print ('In US Format: mm/dd/yyyy')
        return date
        
    def readDataFrom(self, file):
        #methods from pandas
        data = pd.read_csv(file, sep=',', encoding='ISO-8859-1')
        #Delete the columns that we have no interest
        del data['Lat'] 
        del data['Long']
        del data['Province/State']
        return data
        
    #find all data of the country you want, creting a time line basically
    def findDataOf(self, country):
        regionData = self.data[self.data['Country/Region'].str.contains(country)] #Get data which contains the country
        del regionData['Country/Region'] #No need anymore
        regionData = regionData.sum(axis=0)
        self.cases = regionData.iloc[-1] #get the last number of the list
        print ('Number of confirmed cases in ' + str(country) + ' is ' + str(self.cases))
        return regionData
    
    #Used in order to not repeat colors of the list of colors I Chose
    def color(self, lis):
        if len(colors) == 0:
            resetColors()  #If there is no colors to select anymore, it will reset the list
        color = random.choice(colors)
        colors.remove(color)
        return color
    
    #This configure the chart for most of the functions
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
        dataCountry = self.findDataOf(country) #use functions already defined
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
        

    def viewDf(self):
        self.data.to_html('f.html')
        webbrowser.open('f.html')



    #Experiment funcion to plot logxlog chart of the confirmed cases by the new cases per day
    #The results did not go as expected but can be mascared by a function just for analysis purpose
    def logPlot(self, country):
        i=0
        newCases = []
        dataCountry = self.findDataOf(country)
        print ('dataC size is ' + str(dataCountry.size))
        length = dataCountry.size - 1
        #get the number of daily new cases by iteration
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
        plt.yscale('log') #changes the scale to log on y axis
        plt.xscale('log') #the same for x
        plt.grid(True)
        plt.plot(dataCountry, newCases)
        plt.show()

#This is a derivated class from data
class Brasil(Data):        
    def readDataFrom(self, file):
        data = pd.read_csv(file, sep=';', encoding='ISO-8859-1')
        return data

    def getDate(self):
        dfList = self.data['data']
        date = dfList.iloc[-1]
        #The next steps are done in order to get the date with \\\
        date = str(date)
        print (date)
        #date = date[5:7]+'/'+date[8:10]+'/'+date[2:4]
        return date
    
    def viewDf(self, group = ''):
        if group == '':
            self.data.to_html('f.html')
        if group == 'State':
            self.groupBy('State').to_html('f.html')
        if group == 'Region':
            self.groupBy('Region').to_html('f.html')
        webbrowser.open('f.html')
        
    #Gets a group of the states or regions
    #In the future it may be able to get states per region
    #not done in this version
    def groupBy(self, by_Region_or_State):
        by = by_Region_or_State
        dic = {'Region':'regiao','State':'estado'}
        a = self.data.groupby(dic[by])['casosNovos','obitosNovos'].sum()
        a.columns = ['Confirmed cases','Deaths']
        return a
    
    #If you want to see the number of deaths separated from cases, try in_same_chart = False, or actually anything else other than True
    def plotBarChartBy(self, by_Region_or_State, in_same_chart=True):
        if in_same_chart == True:
            sp = False
        else:
            sp = True
        by = by_Region_or_State #defines if the bar chart is going to be ploted by region or brazilian state
        df = self.groupBy(by)
        color_1 = self.color(colors)
        color_2 = self.color(colors)
        chart = df.plot.bar(title=('COVID-19 by brazilian ' + by), grid = True, subplots=sp, color=(color_1,color_2))
        plt.legend(loc='best')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()
        
    def findDataOf(self, state, region=''):
        regionData = self.data[self.data['estado'].str.contains(state)]
        del regionData['obitosNovos'] #Not needed
        del regionData['casosNovos'] #Not needed
        del regionData['estado'] #Not needed
        if region == '': #See if you want some region specific
            del regionData['regiao']
        cases = regionData['casosAcumulados'].iloc[-1] #Gets the last number of cumulated cases
        print ('Number of confirmed cases in ' + str(state) + ' is ' + str(cases))
        return regionData

    def configureChartForCurve(self, chart, state):
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(8,3), gridspec_kw={'wspace':.2}) #Create a figure with two subplots
        color = self.color(colors)
        dates = [] #Create an empty list
        #Fulfill the list with all the dates
        for item in chart['data']:
            item = str(item)
            #item = item[5:7]+'/'+item[8:10]+'/'+item[2:4]
            dates.append(item)
        ax1.plot(dates,chart['casosAcumulados'])
        ax2.plot(dates,chart['obitosAcumulados'])
        
        #Title of the figure
        fig.suptitle('COVID-19 Analysis - ' + str(state), fontsize=16)
        
        #Configure the first chart
        ax1.set_title('Cases of COVID-19 in '+ str(state))
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Confirmed Cases')
        
        #ax1.legend(loc='best')
        ax1.grid(True)
        
        #Configure the second chart
        ax2.set_title('Deaths of COVID-19 in '+ str(state))
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Deaths')

        #ax2.legend(loc='best')
        ax2.grid(True)
        
        #This is used due to the fact there are a lot of dates, so we plot just nbins of then
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
STILL  NOT WORKING PO=ROPERLY
#Define menu class of the interface_______________________________________________________________
class Menu_system:
    def __init__(self, janela):
        self.frame = tk.Frame(janela)
        self.frame.pack()
        self.menu = tk.Menu(janela)
        
        self.menuArq = tk.Menu(self.menu)
        #self.menuArq.add_command(label='Open', command=Open)
        #self.menuArq.add_command(label='Save', command=Save)
        self.menuArq.add_command(label='Quit', command=MainApplication.closeWindow)
        self.menu.add_cascade(menu=self.menuArq, label='File')
        
        
        self.menuEdit = tk.Menu(self.menu)
        self.menuEdit.add_command(label='Clear', command=MainApplication.clearAll(MainApplication))
        #self.menuEdit.add_command(label='Disable MessageBox', command=MainApplication.desMsg(MainApplication))
        self.menu.add_cascade(menu=self.menuEdit, label='Edit')

        
        self.menuHelp = tk.Menu(self.menu)
        self.menuHelp.add_command(label='Program Data', command=MainApplication.data)
        self.menuHelp.add_command(label='Guide', command=MainApplication.helpGuide)
        self.menu.add_cascade(menu=self.menuHelp, label='Help')


        janela.config(menu=self.menu)       
'''
#App mainloop
if __name__ == "__main__":
    root = tk.Tk()
    #Creation of the dataframes of WorldData and BrasilData
    #It needs to be created here in order to the script work
    world = Data('dataCOVID.csv')
    br = Brasil('dataBrasil.csv')
    #The root window will always be toplevel
    #If you dont want it, just comment the next line
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.call('wm', 'attributes', '.', '-topmost', '1')
    #Uncomment to add the menu system Still not working properly
    #Menu_system(root)
    root.mainloop()

 

#setlimitdate
#https://covid.saude.gov.br/
        