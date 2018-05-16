from __future__ import division 
import numpy as np
import pandas as pd
import itertools
import collections
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats.stats import pearsonr
import sys

def featureSetExtraction(genre):
    feature = np.zeros(len(genreMap.keys()), dtype=int)
    feature[[genreMap[idx] for idx in genre]] += 1
    return feature

def giveGenreArray(strGenre = []):
    genre = []
    for i in strGenre:
        if (i == '[') or (i == ']') or (i == ' ') or (i == '\r') or (i=='\n'):
            continue
        else:
            genre.append(int(i))
    return genre


def recommendMoviesCosineMeasure(userId, validation, userSeenMovies, userFavMovies, animeData):  
    seenMovies = animeData.loc[animeData['Anime_ID'].isin(userSeenMovies[userId])]
    search_result = []
    for iter in xrange(0,1):
	if len(userFavMovies[userId]) < (iter+1):
	    break
    	Y = animeData.loc[(animeData['Anime_ID'] == userFavMovies[userId][iter][1]) == True]
    	if validation == 1:
	    notSeenMovies = animeData.drop(Y.index.tolist(),axis = 0)
    	else:
            notSeenMovies = animeData.drop(seenMovies.index.tolist(), axis = 0)
    	#Get me the Genre Array
    	Y = Y['Genre'].tolist()[0]
    	Y = giveGenreArray(Y)
    	Y = np.array(Y).reshape((1, -1))
    	notSeenMovies['result'] = 0
    	for i,rowData in notSeenMovies.iterrows():
            x = rowData['Genre']
            x = giveGenreArray(x)
            x = np.array(x).reshape((1,-1))
            notSeenMovies.set_value(i,'Genre',x)
        notSeenMovies['result'] = notSeenMovies['Genre'].apply(lambda x: cosine_similarity(Y, x))
        search_result = notSeenMovies.sort('result', ascending=False)['Anime_ID'].head(25)
    return search_result

def recommendMoviesPearsonCoeff(userId, validation, userSeenMovies, userFavMovies, animeData):
    seenMovies = animeData.loc[animeData['Anime_ID'].isin(userSeenMovies[userId])]
    search_result = []
    for iter in xrange(0,1):
	if len(userFavMovies[userId]) < (iter+1):
	    break
        Y = animeData.loc[(animeData['Anime_ID'] == userFavMovies[userId][iter][1]) == True]
	if validation == 1:
	    notSeenMovies = animeData.drop(Y.index.tolist(),axis = 0)
        else:
            notSeenMovies = animeData.drop(seenMovies.index.tolist(), axis = 0)
    	#Get me the Genre Array
    	Y = Y['Genre'].tolist()[0]
	Y = giveGenreArray(Y)
    	#Y = np.array(Y).reshape((1, -1))
    	notSeenMovies['result'] = 0
    	for i,rowData in notSeenMovies.iterrows():
            x = rowData['Genre']
            x = giveGenreArray(x)
            #x = np.array(x).reshape((1,-1))
            notSeenMovies.set_value(i,'Genre',x)
    	notSeenMovies['result'] = notSeenMovies['Genre'].apply(lambda x: pearsonr(Y, x)[0])
    	search_result = notSeenMovies.sort('result', ascending=False)['Anime_ID'].head(25)
    return search_result


if __name__ == "__main__":
#Create a dictionary of user and seen movies
    animeData = pd.read_csv('anime.csv')
    animeData['Genre'] = animeData['Genre'].fillna('None')
    animeData['Genre'] = animeData['Genre'].apply(lambda x: x.split(', '))
    genreData = itertools.chain(*animeData['Genre'].values.tolist())
    genreCounter = collections.Counter(genreData)
    genres = pd.DataFrame.from_dict(genreCounter, orient='index').reset_index().rename(columns={'index':'Genre', 0:'count'})
    genres.sort('count', ascending=False, inplace=True)
    count = 0
    genreMap={}

    for i in genreCounter.keys():
        genreMap[i] = count
        count += 1

    animeData['Genre'] = animeData['Genre'].apply(lambda x: featureSetExtraction(x))
    userData = pd.read_csv('newRating.csv')
    userData = pd.merge(userData,animeData, on='Anime_ID')
    userData.sort('User_ID',ascending = True, inplace = True)
    userData.drop(['Type','Episodes','Rating_y','Members'],inplace=True,axis = 1)

#For recommending keep only those data where the rating > 7
    dropData = userData.loc[(userData['Rating_x'] < 8) == True]
    recommendData = userData.drop(dropData.index.tolist(),axis = 0)
    userSeenMovies = {}

    for i,rowData in userData.iterrows():
        if rowData['User_ID'] not in userSeenMovies:
            userSeenMovies[rowData['User_ID']] = []
        userSeenMovies[rowData['User_ID']].append(rowData['Anime_ID'])

#Similarly create a dictionary of user and favored movies
    userFavMovies = {}
    for i,rowData in recommendData.iterrows():
        if rowData['User_ID'] not in userFavMovies:
            userFavMovies[rowData['User_ID']] = []
	Rating = rowData['Rating_x']
	AnimeID = rowData['Anime_ID']
	value = (Rating, AnimeID)
        userFavMovies[rowData['User_ID']].append(value)

    for user in userFavMovies:
	userFavMovies[user] = sorted(userFavMovies[user], key = lambda x : x[0], reverse = True)



#Y = animeData.loc[(animeData['Anime_ID'] == userFavMovies[100][0]) == True]
#Y = Y['Genre'].tolist()[0]
#Y = giveGenreArray(Y)


# In[25]:
    if len(sys.argv) < 4:
	UID = 99 #Change User ID
    	validation = 1 #Change if to validate or not
    	cosine = 1 
    else:
	UID = int(sys.argv[1])
	validation = int(sys.argv[2])
	cosine = int(sys.argv[3])

    if cosine == 1:
       	for UserID in xrange(1000,11000,1000):
            moviesToWatch = recommendMoviesCosineMeasure(UserID, validation, userSeenMovies, userFavMovies, animeData)
	    fileStr = "cosine"
            print "Cosine"
	    accuracy = 0
	    for i in moviesToWatch:
	        if i in userSeenMovies[UserID]:
		    accuracy += 1

	    print "=================================================================================="
	    print "User is " + str(UserID)
	    val = accuracy/len(userSeenMovies[UserID])
	    print "Accuracy is " + str(accuracy) + " val is " + str(val) 
	    print "Total movies watched by user " + str(UserID) + " is " + str(len(userSeenMovies[UserID]))
	    print "=================================================================================="
    else:
	for UserID in xrange(1000,11000,1000):
            moviesToWatch = recommendMoviesPearsonCoeff(UserID, validation, userSeenMovies, userFavMovies, animeData)
	    fileStr = "pearson"
            print "PearsonR"
	    accuracy = 0
	    for i in moviesToWatch:
	        if i in userSeenMovies[UserID]:
		    accuracy += 1
	    
	    print "=================================================================================="
	    print "User is " + str(UserID)
	    val = accuracy/len(userSeenMovies[UserID])
	    print "Accuracy is " + str(accuracy) + " val is " + str(val)
	    print "Total movies watched by user " + str(UserID) + " is " + str(len(userSeenMovies[UserID]))
	    print "=================================================================================="


    #moviesRecommended = userData.loc[userData['Anime_ID'].isin(moviesToWatch) == True, ('Name')]
    #moviesRecommended.to_csv('animeMovies' + fileStr + 'Recommended_forUser_' + str(UserID) + '.csv', sep = ',')
#moviesSeen = UserMap.loc[UserMap['Anime_ID'].isin(UserSeenMovies[1]) == True,('Name')]

#Validation of DataSet
