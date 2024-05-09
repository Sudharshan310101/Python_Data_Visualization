#!/usr/bin/env python
# coding: utf-8

# <h1 align=center><font size = 5>Visualizing Immigration Trends to Canada with Area Plots, Histograms, and Bar Charts</font></h1>

#                                          Data Visualization Project - II

# ## Table of Contents
# 
# <div class="alert alert-block alert-info" style="margin-top: 20px">
#     <ol>
#         <li><a href="#ref1">About the Data</a></li>
#         <li><a href="#ref2">Downloading and Prepping Data</a></li>
#         <li><a href="#ref3">Area Plots</a></li>
#         <li><a href="#ref4">Histograms</a></li>
#         <li><a href="#ref5">Bar Charts</a></li>
#     </ol>
# </div>

# <a id="ref1"></a> 
# # About the Data
# 
# Dataset: Immigration to Canada from 1980 to 2013 - [International migration flows to and from selected countries - The 2015 revision](http://www.un.org/en/development/desa/population/migration/data/empirical2/migrationflows.shtml) from United Nation's website.
# 
# 
# The dataset comprises yearly records of international migrant movements as documented by the countries where these migrants settle. It includes information on both arrivals and departures, categorized by factors such as birthplace, citizenship, or previous/next residency, applicable to both foreign nationals and citizens of the destination countries.

# <a id="ref2"></a> 
# # Downloading and Prepping Data

# In[1]:


import numpy as np
import pandas as pd 


# In[2]:


df_can = pd.read_excel('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Canada.xlsx',
                       sheet_name='Canada by Citizenship',
                       skiprows=range(20),
                       skipfooter=2
                      )


# In[3]:


df_can.head()


# In[4]:


print(df_can.shape)


# #### Cleaning up the dataset to remove columns that are not informative  for visualization 

# In[5]:


df_can.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True)

df_can.head()


# #### Renaming some columns so that they make sense.

# In[6]:


df_can.rename(columns={'OdName':'Country', 'AreaName':'Continent','RegName':'Region'}, inplace=True)

df_can.head()


# #### For consistency, ensuring that all column labels of type string.

# In[7]:


all(isinstance(column, str) for column in df_can.columns)


# The above line of code returned *False* when it was tested if all the column labels are of type **string**. They will be converted to type string.

# In[8]:


df_can.columns = list(map(str, df_can.columns))

all(isinstance(column, str) for column in df_can.columns)


# #### Setting the country name as index - useful for quickly looking up countries using .loc method.

# In[9]:


df_can.set_index('Country', inplace=True)

df_can.head()


# #### Adding a 'total' column

# In[10]:


df_can['Total'] = df_can.sum(axis=1)

df_can.head()


# Now the dataframe has an extra column that presents the total number of immigrants from each country in the dataset from 1980 - 2013. 

# In[11]:


print ('data dimensions:', df_can.shape)


# In[12]:


get_ipython().run_cell_magic('capture', '', '#Creating a list of years from 1980 - 2013 for plotting purposes\nyears = list(map(str, range(1980, 2014)))\n\nyears')


# <a id="ref3"></a> 
# # Area Plots

# #### Creating an area plot of the top 5 countries that contribued the most immigrants to Canada from 1980 to 2013 (using script layer)

# In[14]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.style.use('ggplot')

print ('Matplotlib version: ', mpl.__version__) 


# In[15]:


df_can.sort_values(['Total'], ascending=False, axis=0, inplace=True)

df_top5 = df_can.head()

# transpose the dataframe
df_top5 = df_top5[years].transpose() 

df_top5.head()


# Note: Area plots are stacked by default. And to produce a stacked area plot, each column must be either all positive or all negative values (any NaN values will defaulted to 0). To produce an unstacked plot, pass `stacked=False`. 

# In[16]:


df_top5.plot(kind='area', 
             alpha=0.25, # 0-1, default value a= 0.5
             stacked=False,
             figsize=(20, 10),
            )

plt.title('Immigration Trend of Top 5 Countries')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')

plt.show()


# #### Creating a stacked area plot of the top 5 countries that contribued the most immigrants to Canada from 1980 to 2013 (using the artist layer)

# In[17]:


ax = df_top5.plot(kind='area', alpha=0.35, figsize=(20, 10))

ax.set_title('Immigration Trend of Top 5 Countries')
ax.set_ylabel('Number of Immigrants')
ax.set_xlabel('Years')


# #### Creating a stacked area plot of the 5 countries that contributed the **least** to immigration to Canada from 1980 to 2013 (using script layer)

# In[18]:


df_can.sort_values(['Total'], ascending=True, axis=0, inplace=True)

# getting the bottom 5 entries
df_bottom5 = df_can.head()

# transposing the dataframe
df_bottom5 = df_bottom5[years].transpose() 

df_bottom5.index = df_bottom5.index.map(int) # changing the index values of df_bottom5 to type integer for plotting
df_bottom5.plot(kind='area',
             alpha = 0.45,
             stacked=True,
             figsize=(20, 10), # passing a tuple (x, y) size
             )

plt.title('Immigration Trend of Bottom 5 Countries')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')

plt.show()


# #### Creating an  area plot of the 5 countries that contributed the least to immigration to Canada **from** 1980 to 2013 (using artist layer)

# In[19]:


ax2 = df_bottom5.plot(kind='area', alpha=0.55, stacked=False, figsize=(20, 10))

ax2.set_title('Immigration Trend of Bottom 5 Countries')
ax2.set_ylabel('Number of Immigrants')
ax2.set_xlabel('Years')


# <a id="ref4"></a> 
# # Histograms

# #### Creating a histogram of the frequency distribution of the number of new immigrants from the various countries to Canada in 2013

# In[20]:


df_can['2013'].head()


# In[21]:


# np.histogram returns 2 values
count, bin_edges = np.histogram(df_can['2013'])

print(count) # frequency count
print(bin_edges) # bin ranges, default = 10 bins


# By default, the `histrogram` method breaks up the dataset into 10 bins. The figure below summarizes the bin ranges and the frequency distribution of immigration in 2013:
# * 178 countries contributed between 0 to 3412.9 immigrants 
# * 11 countries contributed between 3412.9 to 6825.8 immigrants
# * 1 country contributed between 6285.8 to 10238.7 immigrants, and so on..

# In[22]:


df_can['2013'].plot(kind='hist', figsize=(8, 5))

plt.title('Histogram of Immigration from 195 Countries in 2013')
plt.ylabel('Number of Countries') 
plt.xlabel('Number of Immigrants') 

plt.show()


# In the above plot, the x-axis represents the population range of immigrants in intervals of 3412.9. The y-axis represents the number of countries that contributed to the aforementioned population. 
# 
# The x-axis labels will be adjusted to match with the bin size. 

# In[23]:


# 'bin_edges' is a list of bin intervals
count, bin_edges = np.histogram(df_can['2013'])

df_can['2013'].plot(kind='hist', figsize=(8, 5), xticks=bin_edges)

plt.title('Histogram of Immigration from 195 countries in 2013') 
plt.ylabel('Number of Countries') 
plt.xlabel('Number of Immigrants')

plt.show()


# #### Creating a histogram of the immigration distribution for Denmark, Norway, and Sweden for years 1980 - 2013

# In[24]:


df_can.loc[['Denmark', 'Norway', 'Sweden'], years]


# In[25]:


# transposing dataframe
df_t = df_can.loc[['Denmark', 'Norway', 'Sweden'], years].transpose()
df_t.head()


# In[29]:


count, bin_edges = np.histogram(df_t, 15)
xmin = bin_edges[0] - 10   #  first bin value is 31.0, adding buffer of 10 for aesthetic purposes 
xmax = bin_edges[-1] + 10  #  last bin value is 308.0, adding buffer of 10 for aesthetic purposes

# stacked Histogram
df_t.plot(kind='hist',
          figsize=(10, 6), 
          bins=15,
          xticks=bin_edges,
          color=['coral', 'darkslateblue', 'mediumseagreen'],
          stacked=True,
          xlim=(xmin, xmax)
         )

plt.title('Histogram of Immigration from Denmark, Norway, and Sweden from 1980 - 2013')
plt.ylabel('Number of Years')
plt.xlabel('Number of Immigrants') 

plt.show()


# #### Creating a histogram of immigration distribution for Greece, Albania, and Bulgaria for years 1980 - 2013

# In[28]:


df_cof = df_can.loc[['Greece', 'Albania', 'Bulgaria'], years]

# transpose dataframe
df_cof = df_cof.transpose() 

#x-tick values
count, bin_edges = np.histogram(df_cof, 15)

# Un-stacked Histogram
df_cof.plot(kind ='hist',
            figsize=(10, 6),
            bins=15,
            alpha=0.35,
            xticks=bin_edges,
            color=['coral', 'darkslateblue', 'mediumseagreen']
            )
plt.title('Histogram of Immigration from Greece, Albania, and Bulgaria from 1980 - 2013')
plt.ylabel('Number of Years')
plt.xlabel('Number of Immigrants')

plt.show()


# <a id="ref5"></a> 
# # Bar Charts

# #### Comparing the number of Icelandic immigrants to Canada from year 1980 to 2013. 

# In[29]:


df_iceland = df_can.loc['Iceland', years]
df_iceland.head()


# In[32]:


df_iceland.plot(kind='bar', figsize=(10, 6), rot=90) 

plt.xlabel('Year')
plt.ylabel('Number of Immigrants')
plt.title('Icelandic Immigrants to Canada from 1980 to 2013')

# Annotate arrow
plt.annotate('',                      # s: str. will leave it blank for no text
             xy=(32, 70),             # place head of the arrow at point (year 2012 , pop 70)
             xytext=(28, 20),         # place base of the arrow at point (year 2008 , pop 20)
             xycoords='data',         # will use the coordinate system of the object being annotated 
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='blue', lw=2)
            )

# Annotate Text
plt.annotate('2008 - 2011 Financial Crisis', # text to display
             xy=(28, 30),                    # start the text at at point (year 2008 , pop 30)
             rotation=72.5,                  # based on trial and error to match the arrow
             va='bottom',                    # want the text to be vertically 'bottom' aligned
             ha='left',                      # want the text to be horizontally 'left' algned.
            )

plt.show()


# The bar plot above shows the total number of immigrants broken down by each year. The impact of the financial crisis can be viewed on the graph; the number of immigrants to Canada started increasing rapidly after 2008. 

# #### Creating a horizontal bar plot showing the total number of immigrants to Canada from the top 15 countries, for the period 1980 - 2013. 

# In[33]:


# sorting dataframe on 'Total' column (descending)
df_can.sort_values(by='Total', ascending=True, inplace=True)

#top 15 countries
df_top15 = df_can['Total'].tail(15)
df_top15


# In[36]:


# generating plot
df_top15.plot(kind='barh', figsize=(12, 12), color='steelblue')
plt.xlabel('Number of Immigrants')
plt.title('Top 15 Conuntries Contributing to the Immigration to Canada between 1980 - 2013')

# annotates value labels to each country
for index, value in enumerate(df_top15): 
    label = format(int(value), ',') # formatting int with commas
    
    # places text at the end of bar (subtracting 47000 from x, and 0.1 from y to make it fit within the bar)
    plt.annotate(label, xy=(value - 47000, index - 0.10), color='white')



