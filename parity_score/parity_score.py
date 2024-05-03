# -*- coding: utf-8 -*-
"""
@author: DrSlifer
This script computes the parity score of Diablo III reviews based on dictionaries
of positive and negative words.

"""

print("running...")

#open the review file and the dictionary files
review = open("Diablo-III-PC reviews.txt")
poswords = open("positive-words.txt")
negwords = open("negative-words.txt")

#create dictionaries based on the positive words and negative words
posdict = {}
negdict = {}
for line in poswords.readlines():   
    occurenceDict = {}
    posdict[line.strip()] = [0, occurenceDict]#key points to a list with a 0 flag to prevent recounts, and a occurence dictionary to track occurences and ratings
    
for line in negwords.readlines():
    occurenceDict = {}
    negdict[line.strip()] = [0, occurenceDict]

#rating used for occurenceDict keys
rating = 0.0

#read in each line of review file
for myline in review.readlines():
    if myline.startswith("rating"):
        rating = float(myline[8:11])#set rating for each review
    for word in myline.split():
        if posdict.get(word,-1)!=-1 and posdict[word][0]==0: #if the word is in the positive word dictionary and the flag is false
            if posdict[word][1].get(rating,-1)!=-1: #if the word has already occured before
                posdict[word][1][rating] += 1
            else:
                posdict[word][1][rating] = 1
            posdict[word][0]==1 #set flag to true to prevent recounting
        elif negdict.get(word,-1)!=-1 and negdict[word][0]==0:
            if negdict[word][1].get(rating,-1)!=-1:
                negdict[word][1][rating] += 1
            else:
                negdict[word][1][rating] = 1
            negdict[word][0]==1
    for word in posdict.keys():#reset the flag of every word before moving on (however, its potentially inefficient)
        posdict[word][0] = 0
    for word in negdict.keys():
        negdict[word][0] = 0

#lists to be used for sorting the positive and negative word dictionaries
poslist = []
neglist = []

#compute parity score
for key in posdict.keys():
    score = 0
    amount = 0
    for rating in posdict[key][1].keys():
        score += int(rating) * posdict[key][1][rating] #rating * number of occurences
        amount += posdict[key][1][rating] #number of occurences
    if amount != 0:
        score/=amount
    if score!=0:
        poslist.append((score,key))
for key in negdict.keys():
    score = 0
    amount = 0
    for rating in negdict[key][1].keys():
        score += int(rating) * negdict[key][1][rating] 
        amount += negdict[key][1][rating] 
    if amount != 0:
        score/=amount
    if score!=0:
        neglist.append((score,key))
    #could've used a method or class to reduce code repetition...

#sort the positive and negative word lists
poslist.sort(reverse=True)
neglist.sort()

print("Highest positive words:\n", poslist[0:10],"\n")
print("Lowest negative words:\n", neglist[0:10])

        
    
