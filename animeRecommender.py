
# coding: utf-8

# In[2]:

import pandas as pd
import numpy as np
import csv


# In[10]:

animeData = pd.read_csv('./anime.csv',names=['Anime_ID','Name','Genre','Type','Episodes','Rating','Members'],sep=",",skiprows = 1)
missData = animeData.loc[animeData['Rating'].isnull() == True] #(12294, 7)
animeData = animeData.drop(missData.index.tolist(),axis = 0)
animeData.head()

animeData.to_csv("animeFiltered.csv")


# In[23]:



userData = pd.read_csv('./rating.csv',names=['User_ID','Anime_ID','Rating'],skiprows = 1,sep = ',',na_values = [-1])
userData.head()
#userData.shape (7813737, 3)


# In[26]:

missData = userData.loc[userData['Rating'].isnull() == True]
missData.head()
userData = userData.drop(missData.index.tolist(),axis= 0)
#userData.shape (6337241, 3)


# In[14]:

#missData['Rating'] = animeData.loc[animeData['Anime_ID'].isin(missData.Anime_ID.tolist()) == True, ('Rating')]


# In[15]:




# In[ ]:



