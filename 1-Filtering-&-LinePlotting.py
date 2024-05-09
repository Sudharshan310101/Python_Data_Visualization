#!/usr/bin/env python
# coding: utf-8

# <h1 align=center><font size = 5>Filtering & Visualizing Immigration Trends to Canada With Line Plots</font></h1>

#                                        Data Visualization Project - I

# ## Table of Contents
# 
# <div class="alert alert-block alert-info" style="margin-top: 20px">
#     <ol>
#         <li><a href="#ref1">About the Data</a></li>
#         <li><a href="#ref2">Downloading and Prepping Data</a></li>
#         <li><a href="#ref3">Indexing and Selection</a></li>
#         <li><a href="#ref4">Data Exploration & Filtering</a></li>
#         <li><a href="#ref5">Visualizing Data With Line Plots</a></li>
#     </ol>
# </div>

# <a id="ref1"></a> 
# # About the Data 

# The Dataset: Immigration to Canada from 1980 to 2013

# Dataset Source: [International migration flows to and from selected countries - The 2015 revision](http://www.un.org/en/development/desa/population/migration/data/empirical2/migrationflows.shtml).
# 
# The dataset originates from the United Nations and provides yearly information on the movement of people across borders, specifically focusing on immigrants recorded by destination countries. It includes data on both incoming and outgoing migration, categorized by factors such as place of birth, citizenship, or previous/next residence for both foreign and domestic individuals. This updated dataset covers statistics from 45 different countries.

# <a id="ref2"></a> 
# ## Downloading and Prepping Data

# In[1]:


import numpy as np 
import pandas as pd 


# In[2]:


df_can = pd.read_excel('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Canada.xlsx',
                       sheet_name='Canada by Citizenship',
                       skiprows=range(20),
                       skipfooter=2)


# In[3]:


df_can.head()


# Getting the index and columns as lists

# In[4]:


get_ipython().run_cell_magic('capture', '', 'df_can.columns.tolist()\ndf_can.index.tolist()')


# In[5]:


df_can.shape    


# Removing a few unnecessary columns. 

# In[6]:


# note: in pandas axis=0 represents rows (default) and axis=1 represents columns.
df_can.drop(['AREA','REG','DEV','Type','Coverage'], axis=1, inplace=True)
df_can.head(2)


# Renaming the columns so that they make sense.

# In[7]:


df_can.rename(columns={'OdName':'Country', 'AreaName':'Continent', 'RegName':'Region'}, inplace=True)
df_can.columns


# In[8]:


df_can['Total'] = df_can.sum(axis=1)


# Checking for null values in the data set:

# In[9]:


get_ipython().run_cell_magic('capture', '', 'df_can.isnull().sum()')


# Viewing a quick summary of each column:

# In[10]:


df_can.describe()


# <a id="ref3"></a> 
# ## Indexing and Selection (slicing)

# Filtering data by country for the years: 1980 - 1985.

# In[11]:


df_can[['Country', 1980, 1981, 1982, 1983, 1984, 1985]]


# In[12]:


# setting index to be by 'country' 
df_can.set_index('Country', inplace=True)


# In[13]:


df_can.head(3)


# In[14]:


# to remove the name of the index column
df_can.index.name = None


# <a id="ref4"></a> 
# # Data Exploration & Filtering

# #### Viewing the number of immigrants from Japan for years 1980 to 1985

# In[15]:


print(df_can.loc['Japan'])


# In[16]:


# for year 2013
print(df_can.loc['Japan', 2013])


# In[17]:


#for years 1980 to 1985
print(df_can.loc['Japan', [1980, 1981, 1982, 1983, 1984, 1984]])


# Converting the following column names into strings: '1980' to '2013'.

# In[18]:


df_can.columns = list(map(str, df_can.columns))


# Creating a variable that will make it easy to call upon the full range of years:

# In[19]:


years = list(map(str, range(1980, 2014)))


# #### Filtering Data By Continent

# In[20]:


#create the condition boolean series
condition = df_can['Continent'] == 'Asia'
print(condition)


# In[21]:


#passing condition into the dataFrame
df_can[condition]


# #### Filtering Data By Continent & Region

# In[22]:


df_can[(df_can['Continent']=='Asia') & (df_can['Region']=='Southern Asia')]


# Reviewing changes made so far.

# In[23]:


print('data dimensions:', df_can.shape)
print(df_can.columns)
df_can.head(2)


# <a id="ref5"></a> 
# # Visualizing Data With Line Plots

# #### Plotting a line graph of immigration from Haiti

# In[24]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib as mpl
import matplotlib.pyplot as plt


# In[25]:


mpl.style.use(['ggplot']) # optional: for ggplot-like style


# In[26]:


haiti = df_can.loc['Haiti', years] # passing in years 1980 - 2013 to exclude the 'total' column
haiti.head()


# In[27]:


haiti.index = haiti.index.map(int) #changing the index values of Haiti to type integer for plotting


# In[28]:


haiti.plot(kind='line')

plt.title('Immigration from Haiti')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')

# annotating the 2010 Earthquake. 
plt.text(2000, 6000, '2010 Earthquake') # see note below

plt.show() 


# #### Comparing the number of immigrants from India and China from 1980 to 2013.

# In[29]:


df_CI = df_can.loc[['India', 'China'], years]
df_CI.head()


# In[30]:


df_CI = df_CI.transpose()
df_CI.head()


# In[31]:


df_CI.plot(kind='line')

plt.title('Immigration from India & China')
plt.ylabel('Number of immigrants')
plt.xlabel('Years')

plt.show()


# China and India have very similar immigration trends through the years. 

# #### Comparing the trend of top 5 countries that contributed the most to immigration to Canada.

# In[32]:


#Sorting the 'Total' column to get the top 5 countries using pandas sort_values() method.
##inplace = True paramemter saves the changes to the original df_can dataframe
df_can.sort_values(by='Total', ascending=False, axis=0, inplace=True)

# passing the top 5 entries
df_top5 = df_can.head(5)

# transposing the dataframe
df_top5 = df_top5[years].transpose() 

#Plotting the dataframe. 
df_top5.index = df_top5.index.map(int) # Changing index values of df_top5 to type integer for plotting
df_top5.plot(kind='line', figsize=(14, 8))

plt.title('Immigration Trend of Top 5 Countries')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')

plt.show()

