#!/usr/bin/env python
# coding: utf-8

# # Initial Libraries

# In[1]:


import pandas as pd 
import numpy as np 
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.patches import Patch


# # Data Import and Cleaning

# In[2]:


# Import the basic data

data_base = pd.read_csv('Mobile Device Data for Assignment 2.csv')  
data_base.head()


# In[3]:


data_base["Aspect Ratio"] =  data_base["Length (mm)"] / data_base["Width (mm)"]
data_base["Display Aspect Ratio"] =  data_base["Display Length(px)"] / data_base["Display Width(px)"]
data_base["Storage/RAM Ratio"] =  data_base["Storage (Mb)"] / data_base["RAM Capacity (Mb)"]
data_base["Density"] =  data_base["Mass (grams)"] / data_base["Volume (cubic cm)"]


# In[4]:


data_year = data_base.groupby(['Release Year']).mean()
data_year.head()


# In[5]:


plt.scatter(data_base['Release Year'], data_base['Mass (grams)'], alpha=0.25, s=15)
plt.plot(data_year['Mass (grams)'])

plt.ylabel('Mass (grams)')
plt.xlabel('Release Year')
plt.title("Mass by Release Year")

plt.ylim([0,0.2])
#plt.show()


# In[6]:


plt.scatter(data_base['Release Year'], data_base['Display Diagonal (in)'], alpha=0.25, s=15)
plt.plot(data_year['Display Diagonal (in)'])

plt.ylabel('Display Diagonal (in)')
plt.xlabel('Release Year')
plt.title("Display Diagonal by Release Year")

plt.ylim([0, 1])
#plt.show()


# In[7]:


plt.scatter(data_base['Release Year'], data_base['Aspect Ratio'], alpha=0.25, s=15)
plt.plot(data_year['Aspect Ratio'])

plt.ylabel('Aspect Ratio')
plt.xlabel('Release Year')
plt.title("Aspect Ratio by Release Year")

plt.ylim([0, 4])
#plt.show()


# In[8]:


plt.scatter(data_base['Width (mm)'], data_base['Length (mm)'], alpha=0.25, s=15)

plt.ylabel('Height')
plt.xlabel('Width')
plt.title("Height vs Width")

plt.xlim([0, 1])
plt.ylim([0, 1])
#plt.show()


# In[9]:


wid = 4
hei = 3
fig, axs = plt.subplots(hei, wid)
for x in range(wid):
    for y in range(hei):
        year = max(data_base['Release Year']) - wid*hei + (wid*y + x)
        data_year = data_base[data_base['Release Year'] == year]
        axs[y, x].scatter(data_year['Width (mm)'], data_year['Length (mm)'], alpha=0.25, s=15)
        axs[y, x].set_title(str(year))
        axs[y, x].set_xlim([0, 1])
        axs[y, x].set_ylim([0, 1])
        
fig.tight_layout(h_pad=0.5,rect=[0, 0.03, 1, 0.95])
fig.suptitle("Dimensions by Year")
fig.text(0.5, 0.02, 'Width', ha='center')
fig.text(0, 0.5, 'Height', va='center', rotation='vertical')

plt.rcParams['figure.figsize'] = [5, 2.5]

#plt.show()


# Define the observed data types

# In[10]:


data_type = data_base
data_type["Type"] = "Null"

# Palmtops and Laptops are wider than they are tall. They are distinguished from each other by their size
palm_width_thresh = 0.45
#data_type.loc[ np.logical_and(data_type['Aspect Ratio'] < 1, data_type['Width (mm)'] < palm_width_thresh), ['Type']] = 'Palmtop'
#data_type.loc[ np.logical_and(data_type['Aspect Ratio'] < 1, data_type['Width (mm)'] > palm_width_thresh), ['Type']] = 'Laptop'
#data_type.loc[ np.logical_and(data_type['Release Year'] > 2009,data_type["Type"] == "Laptop"), ['Type'] ] = 'Tablet'
data_type.loc[ np.logical_and(data_type['Aspect Ratio'] < 1, data_type['Width (mm)'] <= 0.4), ['Type']] = 'Satnav'
data_type.loc[ np.logical_and(data_type['Aspect Ratio'] < 1, data_type['Width (mm)'] > 0.4), ['Type']] = 'Palmtop'
data_type.loc[ np.logical_and(data_type['Release Year'] >= 2001,data_type["Type"] == "Palmtop"), ['Type'] ] = 'Tablet'

print(data_type[data_type["Type"] == "Palmtop"])

# Phones tend to be taller than they are wide. Dumb phones tend to have a display with a very different aspect ratio to the phone in general
display_ratio_thresh = 0.3
data_type.loc[ data_type['Aspect Ratio'] > 1, ['Type'] ] = 'Phone'
data_type.loc[ np.logical_and(data_type['Aspect Ratio'] <= data_type['Display Aspect Ratio'] + display_ratio_thresh,data_type["Type"] == "Phone"), ['Type'] ] = 'Smartphone'
data_type.loc[ np.logical_and(data_type['Aspect Ratio'] > data_type['Display Aspect Ratio'] + display_ratio_thresh,data_type["Type"] == "Phone"), ['Type'] ] = 'Dumbphone'

# PDAs also tended to have similar characteristics to smartphones, but they can be differentiated since proper smartphones only existed after 2007
data_type.loc[ np.logical_and(data_type['Release Year'] < 2007,data_type["Type"] == "Smartphone"), ['Type'] ] = 'PDA'


# In[11]:


#pd.set_option('display.max_rows', None)
#data_type[np.logical_and(data_type['Type'] == "Laptop and Tablet", data_type['Release Year'] > 2010)]
print(data_type.loc[data_type['Type'] == 'Palmtop'])


# In[12]:


data_colour = data_type
data_colour["Colour"] = "grey"

colours = {
    "Palmtop":"turquoise",
    "Satnav":"blue",
    "Tablet": "navy",
    "Dumbphone":"darkorange",
    "Smartphone":"red",
    "PDA":"green",
}

colour_handles = []

for dev_type in colours:
    colour = colours[dev_type]
    data_colour.loc[ data_colour['Type'] == dev_type, ['Colour'] ] = colour
    
    colour_handles.append(
         Patch(facecolor=colour, edgecolor=colour, label=dev_type)
    )


# In[13]:


plt.rcParams['figure.figsize'] = [7.5, 7.5]
plt.scatter(data_colour['Width (mm)'], data_colour['Length (mm)'], alpha=0.5, s=15, c=data_colour['Colour'])

plt.ylabel('Length')
plt.xlabel('Width')
#plt.title("Length vs Width")

plt.xlim([0, 1])
plt.ylim([0, 1])

plt.legend(handles=colour_handles)
#plt.savefig('length-width-ctype.png')
#plt.show()


# In[14]:


plt.rcParams['figure.figsize'] = [7.5, 5]
plt.scatter(data_colour['Aspect Ratio'], data_colour['Display Aspect Ratio'], alpha=0.5, s=15, c=data_colour['Colour'])

plt.xlabel('Device Aspect Ratio')
plt.ylabel('Display Aspect Ratio')
#plt.title("Device vs Display - Aspect Ratios")

plt.xlim([0, 5])
plt.ylim([0, 4])

plt.legend(handles=colour_handles)
#plt.savefig('dr-r-ctype.png')
#plt.show()


# In[15]:


wid = 4
hei = 5
fig, axs = plt.subplots(hei, wid, figsize=(10,10))
for x in range(wid):
    for y in range(hei):
        year = max(data_colour['Release Year']) - wid*hei + (wid*y + x) + 1
        data_year = data_colour[data_colour['Release Year'] == year]
        axs[y, x].scatter(data_year['Width (mm)'], data_year['Length (mm)'], alpha=0.5, s=15, c=data_year['Colour'])
        axs[y, x].set_title(str(year))
        axs[y, x].set_xlim([0, 1])
        axs[y, x].set_ylim([0, 1])
        
fig.tight_layout(h_pad=0.5,rect=[0, 0.03, 1, 0.95])
#fig.suptitle("Dimensions by Year")
fig.text(0.5, 0.02, 'Width', ha='center')
fig.text(0, 0.5, 'Length', va='center', rotation='vertical')

fig.legend(handles=colour_handles)

#plt.savefig('length-width-ctype-syear.png')
#plt.show()


# In[16]:

wid = 5
hei = 5
fig, axs = plt.subplots(hei, wid, figsize=(10,8.5))
for x in range(wid):
    for y in range(hei):
        year = max(data_colour['Release Year']) - wid*hei + (wid*y + x) + 1
        data_year = data_colour[data_colour['Release Year'] == year]
        axs[y, x].scatter(data_year['Aspect Ratio'], data_year['Display Aspect Ratio'], alpha=0.5, s=15, c=data_year['Colour'])
        axs[y, x].set_title(str(year))
        axs[y, x].set_xlim([0, 5])
        axs[y, x].set_ylim([0, 4])
        
fig.tight_layout(h_pad=0.5,rect=[0, 0.03, 1, 0.95])
#fig.suptitle("Aspect Ratios by Year")
fig.text(0.5, 0.02, 'Device Aspect Ratio', ha='center')
fig.text(0, 0.5, 'Display Aspect Ratio', va='center', rotation='vertical')

fig.legend(handles=colour_handles)

plt.savefig('dr-r-ctype-syear.png')
#plt.show()


# In[17]:


# Keep track of the market share of each type by time
data_time = data_type.groupby(['Release Year','Type']).size().unstack()
data_time=data_time.fillna(0)
data_time = data_time[colours.keys()]
data_time_percent = data_time.divide(data_time.sum(axis=1), axis=0)


# In[18]:


fig, axs = plt.subplots(2, 1, figsize=(10,8.5))
axs[0].stackplot(list(data_time_percent.index.values), data_time_percent.T.values * 100, colors=colours.values())
axs[1].stackplot(list(data_time.index.values), data_time.T.values, colors=colours.values())

#axs[0].set_title('Market Share by Release Year')

axs[0].set_xlim([1989, 2013])
axs[1].set_xlim([1989, 2013])
axs[0].set_xlabel("Release Year")
axs[1].set_xlabel("Release Year")

axs[0].set_ylabel("Market Share (%)")
axs[0].set_ylim([0, 100])

axs[1].set_ylabel("Market Share")
axs[1].set_ylim([0, 475])

axs[0].legend(handles=colour_handles)
axs[1].legend(handles=colour_handles)
plt.savefig('share-year.png', dpi=199)
#plt.show()


# In[ ]:




