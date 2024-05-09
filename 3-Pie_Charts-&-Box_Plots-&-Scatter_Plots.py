#!/usr/bin/env python
# coding: utf-8

# <h1 align=center><font size = 5>Visualizing Immigration Trends to Canada with Pie Charts, Box Plots, Scatter Plots, and Bubble Plots</font></h1>

#                                        Data Visualization Project - III

# ## Table of Contents
# 
# <div class="alert alert-block alert-info" style="margin-top: 20px">
#     <ol>
#         <li><a href="#ref1">About the Data</a></li>
#         <li><a href="#ref2">Downloading and Prepping Data</a></li>
#         <li><a href="#ref3">Pie Charts</a></li>
#         <li><a href="#ref4">Box Plots</a></li>
#         <li><a href="#ref5">Scatter Plots</a></li>
#         <li><a href="#ref6">Bubble Plots</a></li>
#     </ol>
# </div>

# <a id="ref1"></a> 
# # About the Data
# 
# Dataset: Immigration to Canada from 1980 to 2013 - [International migration flows to and from selected countries - The 2015 revision](http://www.un.org/en/development/desa/population/migration/data/empirical2/migrationflows.shtml) from United Nation's website.
# 
# 
# The dataset includes yearly information on the migration patterns recorded by destination countries, covering both incoming and outgoing movements based on factors like birthplace, citizenship, or prior/next residence for both foreign individuals and citizens of the destination nations.

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


# In[5]:


# Removing unnecessary columns 
df_can.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True)

# renaming the columns so that they make sense
df_can.rename(columns={'OdName':'Country', 'AreaName':'Continent','RegName':'Region'}, inplace=True)

# for sake of consistency, making all column labels of type string
df_can.columns = list(map(str, df_can.columns))

# setting the country name as index - useful for quickly looking up countries using .loc method
df_can.set_index('Country', inplace=True)

# adding total column
df_can['Total'] = df_can.sum(axis=1)

# years that will be used
years = list(map(str, range(1980, 2014)))
print('data dimensions:', df_can.shape)


# <a id="ref3"></a> 
# # Pie Charts 

# #### Creating a pie chart to explore the proportion (percentage) of new immigrants grouped by continents for the entire time period from 1980 to 2013.

# In[6]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.style.use('ggplot') # optional: for ggplot-like style

# check for latest version of Matplotlib
print('Matplotlib version: ', mpl.__version__) # >= 2.0.0


# In[7]:


# grouping countries by continents and applying sum() function 
df_continents = df_can.groupby('Continent', axis=0).sum()

print(type(df_can.groupby('Continent', axis=0)))

df_continents.head()


# Plotting the data
# - `autopct` -  is a string or function used to label the wedges with their numeric value. The label will be placed inside the wedge. If it is a format string, the label will be `fmt%pct`.
# - `startangle` - rotates the start of the pie chart by angle degrees counterclockwise from the x-axis.
# - `shadow` - Draws a shadow beneath the pie (to give a 3D feel).

# In[8]:


# autopct creates %, start angle represents starting point
df_continents['Total'].plot(kind='pie',
                            figsize=(5, 6),
                            autopct='%1.1f%%', 
                            startangle=90,    
                            shadow=True,            
                            )

plt.title('Immigration to Canada by Continent [1980 - 2013]')
plt.axis('equal') # Sets the pie chart to look like a circle.

plt.show()


# The following modifications will be used to improve the visuals:
# 
# * Remove the text labels on the pie chart by passing in `legend` and add it as a seperate legend using `plt.legend()`.
# * Push out the percentages to sit just outside the pie chart by passing in `pctdistance` parameter.
# * Pass in a custom set of colors for continents by passing in `colors` parameter.
# * **Explode** the pie chart to emphasize the lowest three continents (Africa, North America, and Latin America and Carribbean) by pasing in `explode` parameter.
# 

# In[9]:


colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen', 'pink']
explode_list = [0.1, 0, 0, 0, 0.1, 0.1] # ratio for each continent with which to offset each wedge.

df_continents['Total'].plot(kind='pie',
                            figsize=(15, 6),
                            autopct='%1.1f%%', 
                            startangle=90,    
                            shadow=True,       
                            labels=None,         # turn off labels on pie chart
                            pctdistance=1.12,    # the ratio between the center of each pie slice and the start of the text generated by autopct 
                            colors=colors_list,  # add custom colors
                            explode=explode_list # 'explode' lowest 3 continents
                            )

# scale the title up by 12% to match pctdistance
plt.title('Immigration to Canada by Continent [1980 - 2013]', y=1.12) 

plt.axis('equal') 

# add legend
plt.legend(labels=df_continents.index, loc='upper left') 

plt.show()


# <a id="ref4"></a> 
# # Box Plots

# #### Plotting the box plot for the Japanese immigrants between 1980 - 2013.

# Getting the dataset for Japan

# In[11]:


df_japan = df_can.loc[['Japan'], years].transpose()
df_japan.head()


# In[12]:


df_japan.plot(kind='box', figsize=(8, 6))

plt.title('Box plot of Japanese Immigrants from 1980 - 2013')
plt.ylabel('Number of Immigrants')

plt.show()


# In[13]:


df_japan.describe()


# #### Comparing the distribution of the number of new immigrants from India and China for the period 1980 - 2013.

# Getting the dataset for China and India

# In[14]:


df_CI = df_can.loc[['China', 'India'], years].transpose()
df_CI.head()


# In[15]:


df_CI.describe()


# In[16]:


df_CI.plot(kind='box', figsize=(8, 6))

plt.title('Box plot of Chinese and Indian Immigrants from 1980 - 2013')
plt.ylabel('Number of Immigrants')

plt.show()


# While both countries have around the same median immigrant population (~20,000),  China's immigrant population range is more spread out than India's. The maximum population from India for any year (36,210) is around 15% lower than the maximum population from China (42,584).

# Changing the box plot to be horizontal instead.

# In[17]:


df_CI.plot(kind='box', figsize=(10, 7), color='blue', vert=False)

plt.title('Box plots of Immigrants from China and India (1980 - 2013)')
plt.xlabel('Number of Immigrants')

plt.show()


# **Subplots**

# In[18]:


fig = plt.figure() # create figure

ax0 = fig.add_subplot(1, 2, 1) # add subplot 1 (1 row, 2 columns, first plot)
ax1 = fig.add_subplot(1, 2, 2) # add subplot 2 (1 row, 2 columns, second plot). 

# Subplot 1: Box plot
df_CI.plot(kind='box', color='blue', vert=False, figsize=(20, 6), ax=ax0) # add to subplot 1
ax0.set_title('Box Plots of Immigrants from China and India (1980 - 2013)')
ax0.set_xlabel('Number of Immigrants')
ax0.set_ylabel('Countries')

# Subplot 2: Line plot
df_CI.plot(kind='line', figsize=(20, 6), ax=ax1) # add to subplot 2
ax1.set_title ('Line Plots of Immigrants from China and India (1980 - 2013)')
ax1.set_ylabel('Number of Immigrants')
ax1.set_xlabel('Years')

plt.show()


# #### Creating a box plot to visualize the distribution of the top 15 countries (based on total immigration) grouped by the *decades* `1980s`, `1990s`, and `2000s`.

# Getting the top 15 countries based on Total immigrant population.

# In[19]:


df_top15 = df_can.sort_values(['Total'], ascending=False, axis=0).head(15)
df_top15


# Creating a new dataframe which contains the aggregate for each decade:

# In[20]:


# create a list of all years in decades 80's, 90's, and 00's
years_80s = list(map(str, range(1980, 1990))) 
years_90s = list(map(str, range(1990, 2000))) 
years_00s = list(map(str, range(2000, 2010))) 

# slice the original dataframe df_can to create a series for each decade
df_80s = df_top15.loc[:, years_80s].sum(axis=1) 
df_90s = df_top15.loc[:, years_90s].sum(axis=1) 
df_00s = df_top15.loc[:, years_00s].sum(axis=1)


# merge the three series into a new data frame
new_df = pd.DataFrame({'1980s': df_80s, '1990s': df_90s, '2000s':df_00s}) 



new_df.head()


# In[21]:


new_df.describe()


# Plotting the box plots.

# In[22]:


new_df.plot(kind='box', figsize=(10,6))
plt.title('Immigration from top 15 countries for decades 80s, 90s and 2000s')
plt.show()


# Note: the box plot differs from the summary table created. The box plot scans the data and identifies the outliers. In order to be an outlier, the data value must be:<br>
# * larger than Q3 by at least 1.5 times the interquartile range (IQR), or,
# * smaller than Q1 by at least 1.5 times the IQR.
# 
# Viewing the 2000s as an example: <br>
# * Q1 (25%) = 36,101.5 <br>
# * Q3 (75%) = 105,505.5 <br>
# * IQR = Q3 - Q1 = 69,404 <br>
# 
# Using the definition of outlier, any value that is greater than Q3 by 1.5 times IQR will be flagged as outlier.
# 
# Outlier > 105,505.5 + (1.5 * 69,404) <br>
# Outlier > 209,611.5

# In[23]:


# Checking how many entries fall above the outlier threshold 
new_df[new_df['2000s']> 209611.5]


# China and India are both considered as outliers since their population for the decade exceeds 209,611.5. 

# <a id="ref5"></a> 
# # Scatter Plots
# 
# #### Using a scatter plot, to visualize the trend of total immigrantion to Canada (all countries combined) for the years 1980 - 2013.

# Getting the dataset.

# In[24]:


# using the sum() method to get the total population per year
df_tot = pd.DataFrame(df_can[years].sum(axis=0))

# changeing the years to type int (useful for regression later on)
df_tot.index = map(int, df_tot.index)

# resetting the index to put in back in as a column in the df_tot dataframe
df_tot.reset_index(inplace = True)

# renaming columns
df_tot.columns = ['year', 'total']

df_tot.head()


# Plotting the data.

# In[25]:


df_tot.plot(kind='scatter', x='year', y='total', figsize=(10, 6), color='darkblue')

plt.title('Total Immigration to Canada from 1980 - 2013')
plt.xlabel('Year')
plt.ylabel('Number of Immigrants')

plt.show()


# Plotting a linear line of best fit, and using it to  predict the number of immigrants in 2015.

# In[26]:


x = df_tot['year']      
y = df_tot['total']     
fit = np.polyfit(x, y, deg=1)

fit


# Plotting the regression line on the `scatter plot`.

# In[27]:


df_tot.plot(kind='scatter', x='year', y='total', figsize=(10, 6), color='darkblue')

plt.title('Total Immigration to Canada from 1980 - 2013')
plt.xlabel('Year')
plt.ylabel('Number of Immigrants')

# plot line of best fit
plt.plot(x, fit[0] * x + fit[1], color='red') # recall that x is the Years
plt.annotate('y={0:.0f} x + {1:.0f}'.format(fit[0], fit[1]), xy=(2000, 150000))

plt.show()

# print out the line of best fit
'No. Immigrants = {0:.0f} * Year + {1:.0f}'.format(fit[0], fit[1]) 


# #### Creating a scatter plot of the total immigration from Denmark, Norway, and Sweden to Canada from 1980 to 2013.

# In[28]:


# create dataframe
df_countries = df_can.loc[['Denmark', 'Norway', 'Sweden'], years].transpose()

# create df_total by summing across three countries for each year
df_total = pd.DataFrame(df_countries.sum(axis=1))

# reset index in place
df_total.reset_index(inplace=True)

# rename columns
df_total.columns = ['year', 'total']

# change column year from string to int to create scatter plot
df_total['year'] = df_total['year'].astype(int)

# show resulting dataframe
df_total.head()


# Generating the scatter plot by plotting the total versus year in **df_total**.

# In[29]:


# generate scatter plot
df_total.plot(kind='scatter', x='year', y='total', figsize=(10, 6), color='darkblue')

# add title and label to axes
plt.title('Immigration from Denmark, Norway, and Sweden to Canada from 1980 - 2013')
plt.xlabel('Year')
plt.ylabel('Number of Immigrants')

# show plot
plt.show()


# <a id="ref6"></a> 
# # Bubble Plots
# 
# #### Creating a bubble plot of immigration from Brazil and Argentina for the years 1980 - 2013

# The weights for the bubbles will be set as the *normalized* value of the population for each year.

# Getting the Data for Brazil & Argentina.

# In[30]:


df_can_t = df_can[years].transpose() # transposed dataframe

# casting the Years (the index) to type int
df_can_t.index = map(int, df_can_t.index)

# labeleling the index.
df_can_t.index.name = 'Year'

# resetting the index to bring the Year in as a column
df_can_t.reset_index(inplace=True)

df_can_t.head()


# Creating the normalized weights. 

# In[31]:


# normalizing Brazil data
norm_brazil = (df_can_t['Brazil'] - df_can_t['Brazil'].min()) / (df_can_t['Brazil'].max() - df_can_t['Brazil'].min())

# normalizing Argentina data
norm_argentina = (df_can_t['Argentina'] - df_can_t['Argentina'].min()) / (df_can_t['Argentina'].max() - df_can_t['Argentina'].min())


# Plotting the Data

# In[32]:


# Brazil
ax0 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='Brazil',
                    figsize=(14, 8),
                    alpha=0.5,                  # transparency
                    color='green',
                    s=norm_brazil * 2000 + 10,  # pass in weights 
                    xlim=(1975, 2015)
                   )

# Argentina
ax1 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='Argentina',
                    alpha=0.5,
                    color="blue",
                    s=norm_argentina * 2000 + 10,
                    ax = ax0
                   )

ax0.set_ylabel('Number of Immigrants')
ax0.set_title('Immigration from Brazil and Argentina from 1980 - 2013')
ax0.legend(['Brazil', 'Argentina'], loc='upper left', fontsize='x-large')


# The size of the bubble corresponds to the magnitude of immigrating population for that year, compared to the 1980 - 2013 data. The larger the bubble, the more immigrants in that year.
# 
# There is a corresponding increase in immigration from Argentina during the 1998 - 2002 great depression. A similar spike occurs around 1985 to 1993. In fact, Argentina had suffered a great depression from 1974 - 1990, just before the onset of 1998 - 2002 great depression. 
# 
# On a similar note, Brazil suffered the *Samba Effect* where the Brazilian real (currency) dropped nearly 35% in 1999. There was a fear of a South American financial crisis as many South American countries were heavily dependent on industrial exports from Brazil. The Brazilian government subsequently adopted an austerity program, and the economy slowly recovered over the years, culminating in a surge in 2010. The immigration data reflect these events.

# #### Creating bubble plots of immigration from China and India to visualize any differences with time from 1980 to 2013. 

# Normalizing the data pertaining to China and India.

# In[33]:


# normalizing China data
norm_china = (df_can_t['China'] - df_can_t['China'].min()) / (df_can_t['China'].max() - df_can_t['China'].min())

# normalizing India data
norm_india = (df_can_t['India'] - df_can_t['India'].min()) / (df_can_t['India'].max() - df_can_t['India'].min())


# Generating the bubble plots.

# In[34]:


# China
ax0 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='China',
                    figsize=(14, 8),
                    alpha=0.5,                  # transparency
                    color='green',
                    s=norm_china * 2000 + 10,  # pass in weights 
                    xlim=(1975, 2015)
                   )

# India
ax1 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='India',
                    alpha=0.5,
                    color="blue",
                    s=norm_india * 2000 + 10,
                    ax = ax0
                   )

ax0.set_ylabel('Number of Immigrants')
ax0.set_title('Immigration from China and India from 1980 - 2013')
ax0.legend(['China', 'India'], loc='upper left', fontsize='x-large')

