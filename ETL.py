#!/usr/bin/env python
# coding: utf-8

# In[31]:


import pandas as pd
import numpy as np

wmp_file = "wiki_movie_plots_deduped.csv"

wmp_data = pd.read_csv(wmp_file, encoding='utf8')
wmp_data.describe()
wmp_data.columns


# In[32]:



wmp_data.drop_duplicates(subset = 'Title', keep = False, inplace = True)

wmp_data = wmp_data[['Release Year', 'Title', 'Director', 'Cast',
       'Genre', 'Wiki Page']]

wmp_data.set_index('Title',inplace=True)
# wmp_data.describe()
wmp_data.head()


# In[33]:


imdb_file = "IMDB-Movie-Data.csv"

imdb_data = pd.read_csv(imdb_file)
imdb_data.describe()
imdb_data.columns


# In[34]:



imdb_data.drop_duplicates(subset = 'Title', keep = False, inplace = True)

imdb_data = imdb_data[['Title', 'Rating']]

imdb_data.set_index('Title',inplace=True)

# imdb_data.describe()
imdb_data.head()


# In[35]:


tmdb_file = "tmdb_5000_movies.csv"

tmdb_data = pd.read_csv(tmdb_file)
tmdb_data.describe()
tmdb_data.columns
# unique_lang = tmdb_data['original_language'].nunique()
# ul_df = pd.DataFrame({"Total Languages": [unique_lang]})
# ul_df.head()


# In[36]:




tmdb_data.drop_duplicates(subset = 'original_title', keep = False, inplace = True)
tmdb_data.rename(columns={'title': 'Title'}, inplace=True)

tmdb_data = tmdb_data[['budget', 'homepage', 'original_language',
       'runtime', 'tagline', 'Title',]]

tmdb_data.set_index('Title',inplace=True)

# tmdb_data.describe()
tmdb_data.head()


# In[37]:


imdb_tmdb_merged = pd.merge(tmdb_data, imdb_data, on='Title', how='left')

# imdb_tmdb_merged.head()
imdb_tmdb_merged.describe()


# In[38]:


all_three_merged = pd.merge(wmp_data, imdb_tmdb_merged, on='Title')

all_three_merged.head(50)
# all_three_merged.describe()


# In[39]:


# reset index
all_three_merged.reset_index(inplace=True)
# make id column
all_three_merged.insert(0, 'ID', range(1, 1 + len(all_three_merged)))
# reassign index on id
all_three_merged.set_index('ID',inplace=True)


# In[40]:


all_three_merged.describe()


# In[41]:


# export file
all_three_merged.to_excel("all_three_merged.xlsx")


# In[42]:


import pymongo
import json


# In[43]:


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
# Declare the database
db = client.movies_db

# Declare the collection
collection = db.info_db

info = db.info.find()

collection.insert_many(all_three_merged.to_dict('records'))


# In[ ]:




