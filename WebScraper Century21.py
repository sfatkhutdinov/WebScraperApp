#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[19]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# # Extracting 'div'

# In[58]:


request = requests.get('http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/', 
                 headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
content = request.content

soup = BeautifulSoup(content, 'html.parser')

properties = soup.find_all('div', {'class':'propertyRow'})

first_price = properties[0].find('h4', {'class':'propPrice'}).text.replace('\n', '').replace(' ', '')

page_nr = soup.find_all('a', {'class':'Page'})[-1].text


# # Iteration

# In[59]:


property_list = []

base_url = 'http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s='

for page in range(0, int(page_nr) * 10, 10):
    request = requests.get(base_url + str(page) + '.html', headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    content = request.content
    soup = BeautifulSoup(content, 'html.parser')
    properties = soup.find_all('div', {'class':'propertyRow'})


    for property in properties:
        # empty dictionary
        dictionary = {}
        
        # extract addresses
        address = property.find_all('span', {'class':'propAddressCollapse'})[0].text
        dictionary['Address'] = address
        city_state_zip = property.find_all('span', {'class':'propAddressCollapse'})[1].text
        dictionary['City, State, Zip'] = city_state_zip
        
        # extract prices
        price = property.find('h4', {'class':'propPrice'}).text.replace('\n', '').replace(' ', '')
        dictionary['Price'] = price

       


        # extract number of bedrooms
        bedrooms = property.find('span', {'class':'infoBed'})
        try: 
            bedrooms = bedrooms.find('b').text
            dictionary['Bedrooms'] = bedrooms
        except:
            dictionary['Bedrooms'] = None

        # extract square footage
        sqfeet = property.find('span', {'class':'infoSqFt'})
        try:
            sqfeet = sqfeet.find('b').text
            dictionary['Area'] = sqfeet
        except:
            dictionary['Area'] = None


        # extract number of full baths
        full_baths = property.find('span', {'class':'infoValueFullBath'})
        try:
            full_baths = full_baths.find('b').text
            dictionary['Full Baths'] = full_baths
        except:
            dictionary['Full Baths'] = None

        # extract number of half baths
        half_baths = property.find('span', {'class':'infoValueHalfBath'})
        try:
            half_baths = half_baths.find('b').text
            dictionary['Half Baths'] = half_baths
        except:
            dictionary['Half Baths'] = None

        for column_group in property.find_all('div', {'class':'columnGroup'}):
            for feature_group, feature_name in zip(column_group.find_all('span', {'class':'featureGroup'}), 
                                                   column_group.find_all('span', {'class':'featureName'})):
                if 'Lot Size' in feature_group.text:
                    dictionary['Lot Size'] = feature_name.text
                else:
                    dictionary['Lot Size'] = None
        property_list.append(dictionary)


# # Creating a DataFrame

# In[60]:


df = pd.DataFrame(property_list)
df


# In[61]:


df.to_csv('output.csv')


# In[ ]:





# In[ ]:




