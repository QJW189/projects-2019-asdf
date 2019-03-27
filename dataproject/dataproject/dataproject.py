#Import relevant packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ipywidgets as widgets
import pydst
%matplotlib inline  #Display matplotlib graphs in notebook

#Define the language of DST used when collecting data
Dst = pydst.Dst(lang = 'da')

#Create a dictionary of columns to translate variables from DST to english
columns_dict = {}
columns_dict['REGION'] = 'Region'
columns_dict['ENHED'] = 'Unit'
columns_dict['KOEN'] = 'Sex'
columns_dict['INDKINTB'] = 'Income Interval'
columns_dict['TID'] = 'Year'
columns_dict['INDHOLD'] = 'Income'

#Collect data from DST using the pydst package
df = Dst.get_data(table_id = 'INDKFPP3', variables={'REGION':['*'],'ENHED':['118'], 'KOEN':['MOK'], 'INDKINTB':['000'], 'TID':['*']})

#Clean and structure data utilizing pandas functions
df.rename(columns = columns_dict, inplace = True)   #Translate the colums from danish to english by using the created dictionary, columns_dict
df.drop(columns = ['Unit', 'Sex', 'Income Interval'], inplace = True)   #Drop unnecessary comments
df['Region'] = df['Region'].replace({'Hele landet':'Denmark'})  #Rename 'Hele landet' to 'Denmark'
df = df.pivot(index = 'Region', columns = 'Year', values = 'Income')    #Use the pandas function pivot to reshape data
df = df.reindex(['Region Hovedstaden', 'Region Midtjylland', 'Region Nordjylland', 'Region Sjælland', 'Region Syddanmark', 'Denmark'], axis = 0)    #Change the order of the 'Region' variable

#Define a function to create a bar plot of the disposable by region and year
def income_figure_1(df, year):
    df[[year]].plot(kind = 'bar', color = '#193264', figsize = (8,5))   #Choose bar chart, color and figure size
    plt.xticks(rotation = 45, horizontalalignment= 'right') #Rotate the x-ticks and adjust the position to fit the figure
    plt.title('Disposible Income by region, 2016 prices', loc = 'left') #Create a title for the figure and left align it
    plt.ylabel('DKK')   #Set the y-label to DKK
    plt.xlabel('')  #Remove the x-label
    plt.ylim(100000, 300000)    #Set the y-axis intervals
    plt.show()

#Make the bar chart interactive by implementing ipywidgets
def income_history_1(df):
    widgets.interact(income_figure_1, 
    df = widgets.fixed(df),
    year = widgets.IntSlider(description = 'Year', min = 1987, max = 2017, value = 1987)    
    )   #Define the applied slider for the year variable of the bar chart income_figure_1 and set a description, min/max values and a start value            
income_history_1(df)


#Create a new bar chart where the y-axis is fixed to 'Denmark'
def income_figure_2(df, year):
    df[[year]].plot(kind = 'bar', color = '#193264' , figsize = (8,5))  
    plt.xticks(rotation = 45, horizontalalignment = 'right') 
    plt.title('Disposible Income by region, 2016 prices', loc = 'left') 
    plt.ylabel('DKK')   
    plt.xlabel('')  
    plt.ylim(0, df.loc['Denmark',year] * 2) #Fix the y-axis to 2 times the value of 'Denmark'
    plt.show()

#Make the bar chart interactive
def income_history_2(df):
    widgets.interact(income_figure_2, 
    df = widgets.fixed(df),
    year = widgets.IntSlider(description = 'Year', min = 1987, max = 2017, value = 1987)                 
    )  
income_history_2(df)

#Import data from DST
df_mw = Dst.get_data(table_id = 'INDKFPP3', variables = {'REGION':['000'],'ENHED':['118'], 'KOEN':['M', 'K'], 'INDKINTB':['000'], 'TID':['*']})

#Clean and structure data utilizing pandas functions
df_mw.rename(columns = columns_dict, inplace = True) #Translate the colums from danish to english by using the created dictionary, columns_dict
df_mw.drop(columns = ['Unit', 'Region', 'Income Interval'], inplace = True) #Drop unnecessary comments
df_mw['Sex'] = df_mw['Sex'].replace({'Mænd':'Men', 'Kvinder':'Women'})  #Rename the columns 'Mænd' and 'Kvinder' to 'Men' and 'Women'
df_mw = df_mw.pivot(index = 'Year', columns = 'Sex', values = 'Income') #Use the pandas function pivot to reshape data

#Create an index (1987 = 100) column for men and women
df_mw['Index_Men'] = (df_mw['Men']/df_mw.iloc[0,0]) * 100   #Create and index column for men utilizing the iloc function
df_mw['Index_Women'] = (df_mw['Women']/df_mw.iloc[0,1]) * 100 #Create and index column for women utilizing the iloc function

#Create a figure illustrating the development of disposable income over time for men and women
df_mw['Index_Men'].plot(color = '#193264', linewidth = 4, label = 'Men', figsize = (8,5))  #Set the color, linewidth, label and size of the figure                                               
df_mw['Index_Women'].plot(color = '#800000', linewidth = 4, label = 'Women') 
plt.title('Disposible Income by Sex, 1987 = 100', loc = 'left') #Create a title for the figure and left align it
plt.legend() #Include a legend in the figure
plt.show()