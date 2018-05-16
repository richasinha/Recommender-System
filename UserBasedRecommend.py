
# coding: utf-8

# In[1]:

import pandas as pd
import csv
import itertools
import collections
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import OrderedDict
from scipy.stats.stats import pearsonr
import sys

# In[2]:

def recommendMoviesCosineMeasure(UserID, validation, UserGenreDict, UserSeenMovies, UserFavMovies):
    search = {}
    x = UserGenreDict[UserID]
    x = np.array(x).reshape((1,-1))
    for i in UserGenreDict:
        if i == UserID:
            continue
        else:
            y = UserGenreDict[i]
            y = np.array(y).reshape((1,-1))
            cosineMeasure = cosine_similarity(x,y)
            search[i] = cosineMeasure
    search = OrderedDict(sorted(search.items(), key = lambda x: x[1], reverse = True))
    recommendMovies = []
    count = 0
    for ID in search:
        count += 1
        for i in UserFavMovies[ID]:
	    if validation == 1:
	        if i not in UserSeenMovies[UserID]:
        	    recommendMovies.append(i)
            else:
		recommendMovies.append(i)
        if count > 3 or len(recommendMovies) > 75:
            break
    return recommendMovies

def recommendMoviesPearsonCoeff(UserID, validation, UserGenreDict, UserSeenMovies, UserFavMovies): 
    search = {}
    x = UserGenreDict[UserID]
    #x = np.array(x).reshape((1,-1))
    for i in UserGenreDict:
        if i == UserID:
            continue
        else:
            y = UserGenreDict[i]
            #y = np.array(y).reshape((1,-1))
            pearsonCoeff = pearsonr(x,y)[0]
            search[i] = pearsonCoeff 
    search = OrderedDict(sorted(search.items(), key = lambda x: x[1], reverse = True))
    recommendMovies = []
    count = 0
    for ID in search:
        count += 1
        for i in UserFavMovies[ID]:
	    if validation == 1:
	        if i not in UserSeenMovies[UserID]:
        	    recommendMovies.append(i)
            else:
		recommendMovies.append(i)
        if count > 3 or len(recommendMovies) > 75:
            break
    return recommendMovies


file1 = "UserMap.csv"
UserMap = pd.read_csv(file1, names = ['User_ID','Anime_ID','Rating','Name','Genre'], skiprows = 1)
UserMap.head()


# In[3]:

UserGenreDict = {}
UserSeenMovies = {}
UserFavMovies = {}
for i,rowData in UserMap.iterrows():
    x = rowData['Genre']
    genre = []
    for i in x:
        if (i == '[') or (i == ']') or (i == ' ') or (i == '\r') or (i=='\n'):
            continue
        else:
            genre.append(int(i))
    if rowData['User_ID'] not in UserGenreDict:
        UserGenreDict[rowData['User_ID']] = genre
    else:
        for i in genre:
            UserGenreDict[rowData['User_ID']][i] += genre[i]
    
    if rowData['User_ID'] not in UserSeenMovies:
        UserSeenMovies[rowData['User_ID']] = []
        UserFavMovies[rowData['User_ID']] = []
    UserSeenMovies[rowData['User_ID']].append(rowData['Anime_ID'])
    if rowData['Rating'] > 7:
        UserFavMovies[rowData['User_ID']].append(rowData['Anime_ID'])


# In[4]:


# In[5]:
if len(sys.argv) < 4:
    UserID = 99 #int(sys.argv[1]) Change UserID for different Users
    validation = 1 #ints(sys.argv[2]) Change Validation values
    cosine = 1 #Change to use cosine or pearson
else:
    UserID = int(sys.argv[1])
    validation = int(sys.argv[2])
    cosine = int(sys.argv[3])

#if cosine == 1:
 #   moviesToWatch = recommendMoviesCosineMeasure(UserID,validation, UserGenreDict, UserSeenMovies, UserFavMovies)
  #  fileStr = "cosine"
#else:
 #   moviesToWatch = recommendMoviesPearsonCoeff(UserID, validation, UserGenreDict, UserSeenMovies, UserFavMovies)
  #  fileStr = "pearson"

if cosine == 1:
    for UserID in xrange(1000,11000,1000):
        moviesToWatch = recommendMoviesCosineMeasure(UserID, validation, UserGenreDict, UserSeenMovies, UserFavMovies)
	fileStr = "cosine"
        print "Cosine"
	accuracy = 0
	for i in moviesToWatch:
	    if i in UserSeenMovies[UserID]:
	        accuracy += 1

	print "=================================================================================="
	print "User is " + str(UserID)
	val = accuracy/len(UserSeenMovies[UserID])
	print "Accuracy is " + str(accuracy) + " val is " + str(val) 
	print "Total movies watched by user " + str(UserID) + " is " + str(len(UserSeenMovies[UserID]))
	print "=================================================================================="
else:
    for UserID in xrange(1000,11000,1000):
        moviesToWatch = recommendMoviesPearsonCoeff(UserID, validation, UserGenreDict, UserSeenMovies, UserFavMovies)
	fileStr = "pearson"
        print "PearsonR"
	accuracy = 0
	for i in moviesToWatch:
	    if i in UserSeenMovies[UserID]:
	        accuracy += 1
	    
	print "=================================================================================="
	print "User is " + str(UserID)
	val = accuracy/len(UserSeenMovies[UserID])
	print "Accuracy is " + str(accuracy) + " val is " + str(val)
	print "Total movies watched by user " + str(UserID) + " is " + str(len(UserSeenMovies[UserID]))
	print "=================================================================================="

# In[10]:

#moviesRecommended = UserMap.loc[UserMap['Anime_ID'].isin(moviesToWatch) == True, ('Name')].head(25)
#moviesRecommended.to_csv('Movies' + fileStr + 'Recommended_forUser_' + str(UserID) + '.csv', sep = ',')
#moviesSeen = UserMap.loc[UserMap['Anime_ID'].isin(UserSeenMovies[1]) == True,('Name')]

#if cosine == 1:
#    print "Cosine"
#else:
#    print "PearsonR"

#print "User is " + str(UserID)
#Validation of DataSet
#accuracy = 0
#for i in moviesToWatch:
#    if i in UserSeenMovies[UserID]:
#        accuracy += 1

#print accuracy
#print len(UserSeenMovies[UserID])



