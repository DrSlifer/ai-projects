# -*- coding: utf-8 -*-
"""
Created on Sun May 2 23:09:22 2021

@author: DrSlifer
This script uses content based similarity (cosine similarity) to recommend k shows to the user, given a sample show name and k
that is inputted into find_rec(movie_name, k).

"""

import csv
import numpy as np


#movie dictionary, where the key is the movie name, and its list value consists of a description and user rating score
movies = {}

#item vector dictionary, used to store the item vector for each movie
item_vects = {}


def read_csv_file(filename): 
    with open(filename) as file:
        csv_file = csv.reader(file)
        for line in csv_file:
            if line[2] != "" and line[5] != "NA" and line[5] != "user rating score": #read only valid rows into the movie dictionary
                movies[line[0]]=[line[2], float(line[5])]
                
                
def encode():
    dimension = 15
    encoding_dict={}  
    
    for movie in movies:
        movie_encoding = 0 #the encoding value for each movie's description
        
        #reuse existing item_vectors if they're already made, and description and rating are the same
        reused = False
        for mov in movies:
            if movies[movie][0] == movies[mov][0] and movies[movie][1] == movies[mov][1] and item_vects.get(mov) is not None:
                item_vects[movie]=item_vects[mov]
                reused = True
                break #(not best practice)
        
        if reused == False:
            sentences = movies[movie][0].split(". ") #seperate each sentence
            for sentence in sentences:
                if encoding_dict.get(sentence) is None: #reuse existing encoding (maybe unneccesary?)
                    encoding_dict[sentence] = np.random.randn(dimension)
                movie_encoding += encoding_dict[sentence]
            item_vects[movie] = np.hstack((movie_encoding, movies[movie][1])) #(movie_encoding, user rating score)
            #item_vects[movie] now represents a full movie encoding.
        
        
def cosine_compare(movie_name):
    comparisons = {} #dictionary of how the movie chosen by the user compares to every other movie (via similarity scores/values)
    A = item_vects[movie_name] #movie item vector chosen by user
    A_norm = 0
    
    for val in A:
        A_norm += val**2
    A_norm**=(1/2)
    
    for item in item_vects:        
        if item != movie_name:
            B = item_vects[item] #movie item vector to compare A to
            B_norm = 0
            
            for val in B:
                B_norm += val**2
            B_norm**=(1/2)
            
            comparisons[item] = ((A.transpose())*B)/(A_norm*B_norm) #cosine similarity equation
            
            #print(comparisons[item])
            
            total=0
            for val in comparisons[item]: #total will represent the overall similarity score (across the dimensions) of the movie from -1 to 1
                total+=float(val)
            comparisons[item] = total
    
    return comparisons

    
def find_rec(movie_name, k):
    read_csv_file('netflix_ratings.csv')
    encode()
    comparisons = cosine_compare(movie_name)

    for x in range(k):
        highest = ("",0) #(movie name, similarity score)
        for movie in comparisons:
            if comparisons[movie] > highest[1]: #grab the movie with the highest similarity score
                highest = (movie, comparisons[movie])
        comparisons.pop(highest[0]) #remove the movie (and then find the next highest scoring movie)
        print(highest,"\n")

    
find_rec("Death Note", 10)
    
        


