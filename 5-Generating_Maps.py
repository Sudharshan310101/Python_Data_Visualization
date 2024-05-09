#!/usr/bin/env python
# coding: utf-8

# <h1 align=center><font size = 5>Generating Maps with Python & Folium</font></h1>

#                                        Data Visualization Project - V

# ## Objectives
#   * Superimpose the locations of recorded crimes onto a folium map of San Francisco.
#   * Make each circle marker on the San Francisco map into a location marker to display the category of the crime when hovered over.
#   * Remove the location markers and instead adding text to the circle markers themselves.
#   * Group the crime circle markers into different clusters.
#   * Create a Choropleth map of the world depicting immigration from various countries to Canada.

# ## Table of Contents
# 
# <div class="alert alert-block alert-info" style="margin-top: 20px">
#     <ol>
#         <li><a href="#ref1">About the Data</a></li>
#         <li><a href="#ref2">Downloading and Prepping Data</a></li>
#         <li><a href="#ref3">San Fran Maps with Markers</a></li>
#         <li><a href="#ref4">Choropleth Maps</a></li>
#     </ol>
# </div>

#  

# <a id="ref2"></a> 
# # Downloading and Prepping Data 

# In[26]:


import numpy as np 
import pandas as pd 


# In[27]:


get_ipython().run_cell_magic('capture', '', '!pip install folium\nimport folium')


# In[28]:


# defining the world map
world_map = folium.Map()

world_map


# In[29]:


# defining the world map centered around Canada with a higher zoom level
world_map = folium.Map(location=[56.130, -106.35], zoom_start=8)

world_map


# <a id="ref3"></a> 
# # San Fran Maps with Markers 

# In[30]:


df_incidents = pd.read_csv('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Police_Department_Incidents_-_Previous_Year__2016_.csv')


# In[31]:


df_incidents.head()


# Each row consists of 13 features:
# > 1. **IncidntNum**: Incident Number
# > 2. **Category**: Category of crime or incident
# > 3. **Descript**: Description of the crime or incident
# > 4. **DayOfWeek**: The day of week on which the incident occurred
# > 5. **Date**: The Date on which the incident occurred
# > 6. **Time**: The time of day on which the incident occurred
# > 7. **PdDistrict**: The police department district
# > 8. **Resolution**: The resolution of the crime in terms whether the perpetrator was arrested or not
# > 9. **Address**: The closest address to where the incident took place
# > 10. **X**: The longitude value of the crime location 
# > 11. **Y**: The latitude value of the crime location
# > 12. **Location**: A tuple of the latitude and the longitude values
# > 13. **PdId**: The police department ID

# In[32]:


df_incidents.shape


# In[33]:


# getting the first 100 crimes in the df_incidents dataframe
limit = 100
df_incidents = df_incidents.iloc[0:limit, :]


# In[34]:


df_incidents.shape


# Visualizing where these crimes took place in the city of San Francisco. Default map style will be used and will be initialized to a zoom level of 12. 

# In[35]:


# San Francisco latitude and longitude values
latitude = 37.77
longitude = -122.42


# In[36]:


# creating San Fran map
sanfran_map = folium.Map(location=[latitude, longitude], zoom_start=12)

sanfran_map


# #### Superimposing the locations of the crimes onto the map. 

# In[37]:


# instantiating a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

# looping through the 100 crimes and adding each to the incidents feature group
for lat, lng, in zip(df_incidents.Y, df_incidents.X):
    incidents.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            radius=5, # to define how big the circle markers to be
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# adding incident locations to the map
sanfran_map.add_child(incidents)


# #### Making each circle marker into a location marker and displaying the category of the crime when hovered over.

# In[38]:


# instantiating a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

# looping through the 100 crimes and adding each to the incidents feature group
for lat, lng, in zip(df_incidents.Y, df_incidents.X):
    incidents.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            radius=5, # defining how big the circle markers to be
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# adding pop-up text to each marker on the map
latitudes = list(df_incidents.Y)
longitudes = list(df_incidents.X)
labels = list(df_incidents.Category)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(sanfran_map)    
    
# adding incident locations to the map
sanfran_map.add_child(incidents)


# #### Removing the location markers and instead adding text to the circle markers themselves.

# In[39]:


# creating map 
sanfran_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# looping through the 100 crimes and adding each to the map
for lat, lng, label in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5, # defining how big the circle markers to be
        color='yellow',
        fill=True,
        popup=label,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(sanfran_map)

sanfran_map


# #### Grouping the markers into different clusters. 
# Each cluster is then represented by the number of crimes in each neighborhood. These clusters can be thought of as pockets of San Francisco which can be analyzed separately.

# In[40]:


from folium import plugins

# Starting again with a clean copy of the map of San Francisco
sanfran_map = folium.Map(location = [latitude, longitude], zoom_start = 12)

# instantiating a mark cluster object for the incidents in the dataframe
incidents = plugins.MarkerCluster().add_to(sanfran_map)

# looping through the dataframe and adding each data point to the mark cluster
for lat, lng, label, in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
    folium.Marker(
        location=[lat, lng],
        icon=None,
        popup=label,
    ).add_to(incidents)

sanfran_map


# <a id="ref4"></a> 
# # Choropleth Maps

# #### Creating a `Choropleth` map of the world depicting immigration from various countries to Canada 

# In[41]:


df_can = pd.read_excel('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Canada.xlsx',
                     sheet_name='Canada by Citizenship',
                     skiprows=range(20),
                     skipfooter=2)

print('Data downloaded and read into a dataframe!')


# In[42]:


df_can.head()


# In[43]:


print(df_can.shape)


# In[44]:


# Removing unnecessary columns (eg. REG) 
df_can.drop(['AREA','REG','DEV','Type','Coverage'], axis=1, inplace=True)

# Renaming the columns so that they make sense
df_can.rename(columns={'OdName':'Country', 'AreaName':'Continent','RegName':'Region'}, inplace=True)

# for sake of consistency, making all column labels of type string
df_can.columns = list(map(str, df_can.columns))

# add total column
df_can['Total'] = df_can.sum(axis=1)

# years that will be used in this lesson - useful for plotting later on
years = list(map(str, range(1980, 2014)))
print ('data dimensions:', df_can.shape)


# In[45]:


df_can.head()


# In order to create a `Choropleth` map, a GeoJSON file that defines the interested areas/boundaries of the state, county, or country is needed. In this case, a GeoJSON that defines the boundaries of all world countries is needed.

# In[46]:





# Creating a world map, centered around **[0, 0]** *latitude* and *longitude* values, with an intial zoom level of 2, and using Default style.

# In[50]:


import folium

# Specify the local file path of the GeoJSON file
world_geo = 'C:\\Users\\Sudharshan Ravikumar\\Downloads\\world_countries.json'


# Create a plain world map
world_map = folium.Map(location=[0, 0], zoom_start=2)

# Display the map
world_map


# Parameters to create a `Choropleth` map:
# 
# 1. geo_data, which is the GeoJSON file.
# 2. data, which is the dataframe containing the data.
# 3. columns, which represents the columns in the dataframe that will be used to create the `Choropleth` map.
# 4. key_on, which is the key or variable in the GeoJSON file that contains the name of the variable of interest. 

# In[52]:


import folium

# Load the GeoJSON file for world map
world_geo = 'C:\\Users\\Sudharshan Ravikumar\\Downloads\\world_countries.json'

# Create a plain world map
world_map = folium.Map(location=[0, 0], zoom_start=2)

# Generate choropleth map using the total immigration of each country to Canada from 1980 to 2013
folium.Choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'Total'],
    key_on='feature.properties.name',
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Immigration to Canada'
).add_to(world_map)

# Display the map
world_map


# As per the `Choropleth` map legend, the darker the color of a country and the closer the color to red, the higher the number of immigrants from that country. Accordingly, the highest immigration over the course of 33 years (from 1980 to 2013) was from China, India, and the Philippines, followed by Poland, Pakistan, and interestingly, the US.

# Fixing the legend that is displaying a negative boundary or threshold.

# In[54]:


world_geo = 'C:\\Users\\Sudharshan Ravikumar\\Downloads\\world_countries.json'

# Create a numpy array with linear spacing from the minimum to maximum total immigration
threshold_scale = np.linspace(df_can['Total'].min(),
                              df_can['Total'].max(),
                              6, dtype=int)

# Convert numpy array to a list
threshold_scale = threshold_scale.tolist()

# Ensure the last value of the list is greater than the maximum immigration
threshold_scale[-1] = threshold_scale[-1] + 1

# Create the map
world_map = folium.Map(location=[0, 0], zoom_start=2)

# Create the choropleth map with threshold scale
folium.Choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'Total'],
    key_on='feature.properties.name',
    threshold_scale=threshold_scale,
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Immigration to Canada',
    reset=True
).add_to(world_map)

world_map


# In[ ]:




