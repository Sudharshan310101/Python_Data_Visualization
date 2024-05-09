#!/usr/bin/env python
# coding: utf-8

# <h1 align=center><font size = 5>Visualizing Immigration Trends to Canada with Regression Plots</font></h1>

#                                        Data Visalization Project - IV

# ## Table of Contents
# 
# <div class="alert alert-block alert-info" style="margin-top: 20px">
#     <ol>
#         <li><a href="#ref1">Downloading and Prepping Data</a></li>
#         <li><a href="#ref2">Regression Plots</a></li>
#     </ol>
# </div>

# # About the Data
# 
# Dataset: Immigration to Canada from 1980 to 2013 - [International migration flows to and from selected countries - The 2015 revision](http://www.un.org/en/development/desa/population/migration/data/empirical2/migrationflows.shtml) from United Nation's website
# 
# 
# The dataset compiles yearly records of international migrant movements as documented by destination countries. It encompasses both arrivals and departures, categorized by criteria such as birthplace, citizenship, or previous/next residency, applicable to both foreign nationals and citizens of the destination countries.

# <a id="ref1"></a> 
# # Downloading and Prepping Data 

# In[1]:


import numpy as np 
import pandas as pd 
from PIL import Image # converting images into arrays


# In[2]:


df_can = pd.read_excel('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Canada.xlsx',
                       sheet_name='Canada by Citizenship',
                       skiprows=range(20),
                       skipfooter=2)


# In[3]:


df_can.head()


# In[4]:


print(df_can.shape)


# In[5]:


# Removing unnecessary columns
df_can.drop(['AREA','REG','DEV','Type','Coverage'], axis = 1, inplace = True)

# Renaming the columns so that they make sense
df_can.rename (columns = {'OdName':'Country', 'AreaName':'Continent','RegName':'Region'}, inplace = True)

# for sake of consistency, making column labels of type string
df_can.columns = list(map(str, df_can.columns))

# setting the country name as index - useful for quickly looking up countries using .loc method
df_can.set_index('Country', inplace = True)

# adds total column
df_can['Total'] =  df_can.sum (axis = 1)

# years that will be used
years = list(map(str, range(1980, 2014)))
print ('data dimensions:', df_can.shape)


# <a id="ref2"></a> 
# # Regression Plots 

# In[6]:


get_ipython().run_cell_magic('capture', '', "%matplotlib inline\n\nimport matplotlib as mpl\nimport matplotlib.pyplot as plt\n\nmpl.style.use('ggplot') # optional: for ggplot-like style\n\n!pip install seaborn \nimport seaborn as sns\n\nprint ('Matplotlib version: ', mpl.__version__)\nprint('Seaborn installed and imported!')")


# Creating a dataframe that stores that total number of landed immigrants to Canada per year from 1980 to 2013.

# In[7]:


# Using sum() method to get the total population per year
df_tot = pd.DataFrame(df_can[years].sum(axis=0))

# changing the years to type float (useful for regression later on)
df_tot.index = map(float, df_tot.index)

# resetting the index to put in back in as a column in the df_tot dataframe
df_tot.reset_index(inplace=True)

# renaming columns
df_tot.columns = ['year', 'total']

df_tot.head()


# In[8]:


plt.figure(figsize=(15, 10))

sns.set(font_scale=1.5)
sns.set_style('whitegrid')

ax = sns.regplot(x='year', y='total', data=df_tot, color='green', marker='+', scatter_kws={'s': 200})
ax.set(xlabel='Year', ylabel='Total Immigration')
ax.set_title('Total Immigration to Canada from 1980 - 2013')


# Creating a scatter plot with a regression line to visualize the total immigration from Denmark, Sweden, and Norway to Canada from 1980 to 2013.

# In[9]:


df_countries = df_can.loc[['Denmark', 'Norway', 'Sweden'], years].transpose()

# create df_total by summing across three countries for each year
df_total = pd.DataFrame(df_countries.sum(axis=1))

# reset index in place
df_total.reset_index(inplace=True)

# rename columns
df_total.columns = ['year', 'total']

# change column year from string to int to create scatter plot
df_total['year'] = df_total['year'].astype(int)

# define figure size
plt.figure(figsize=(15, 10))

# define background style and font size
sns.set(font_scale=1.5)
sns.set_style('whitegrid')

# generate plot and add title and axes labels
ax = sns.regplot(x='year', y='total', data=df_total, color='green', marker='+', scatter_kws={'s': 200})
ax.set(xlabel='Year', ylabel='Total Immigration')
ax.set_title('Total Immigrationn from Denmark, Sweden, and Norway to Canada from 1980 - 2013')


