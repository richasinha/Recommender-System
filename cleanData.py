import csv
import pandas as pd
import numpy as np
from collections import defaultdict
from csv import reader
import random

file1 = "./animeFiltered.csv"
file2 = "./rating.csv"

missRatings = []
Anime = {}
meanMembers = 0
with open(file1,'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
	AnimeID = int(line['Anime_ID'])
	rating = float(line['Rating'])
	members = int(line['Members'])
	Anime[AnimeID] = (rating,members)
	meanMembers += members

meanMembers = meanMembers/len(Anime)
modifiedFile = []
with open(file2,'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        if (float(line['Rating']) == -1):
    	    ID = int(line['Anime_ID'])
	    if ID in Anime.keys():
                if Anime[ID][0] >= 8.5 and Anime[ID][1] > meanMembers:
	 	    rating = random.randint(8,9)
		elif Anime[ID][0] < 8.5 and Anime[ID][0] > 5:
		    rating = random.randint(5,8)
		else:
	       	    rating = random.randint(2,5)
		line['Rating'] = rating
	new_row = [line['User_ID'], line['Anime_ID'], line['Rating']]
	modifiedFile.append(new_row)

file3 = open('newRating.csv','wb')
writer = csv.writer(file3)
writer.writerows(modifiedFile)
file3.close()
	
		
		
		
	
	    
