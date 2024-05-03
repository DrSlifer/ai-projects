# -*- coding: utf-8 -*-
'''
Created on Tue Mar 27 12:41:34 2021

@author: DrSlifer
This script is a Naïve Bayesian binary classifier for email phishing detection, based on the Multi-variate Bernoulli Event Model.
A training set and testing set use 600 non-spam emails and 600 spam emails, provided from Enron and scamdex.com respectively.
This script must be placed in the same directory as the Ham and Spam folders in order to import the email text files properly.

'''

import random

TP=0 # data labeled as spam, classfied as spam
TN=0 # data labeled as non-spam, classfied as non-spam
FP=0 # data labeled as non-spam, classfied as spam
FN=0 # data labeled as spam, classfied as non-spam
accuracy = 0 
precision = 0
recall = 0
f1Score = 0

trainingSize = 1000

trainingSet = {} #trainingSet that will be a list: [file,bool]
#file is the imported email text file
#bool is the spam/non-spam value

testingSet = {} #testingSet that will also be a list: [file, bool1, bool2]
#file is the imported email text file
#bool1 is the actual non-spam/spam value
#bool2 is the expected non-spam/spam value
#The expected bool will be compared against the actual to calculate TP, TN, FP, and FN.

ham1={} #temporary dictionary used for avoiding duplicates in non-spam email importing
ham2={} #temporary dictionary used for avoiding duplicates in non-spam email importing
spam={} #temporary dictionary used for avoiding duplicates in spam email importing



#Function to fully reset trainingSet and testingSet
def shuffle():
    ham1.clear()
    ham2.clear()
    spam.clear()
    trainingSet.clear()
    testingSet.clear()
    importEmails()


#Function to import emails into trainingSet and testingSet
def importEmails():
    rand=0
    counter=1 #counter used to enumerate the emails in the training and testing sets
    for x in range(250):
        #Choose a random non-spam email
        rand = random.randrange(1,301)
        while(ham1.get(rand)):
            rand = random.randrange(1,301) #not very efficient but it works for now
        file = open(r"Ham\\300 good emails\\"+str(rand)+".txt")
        trainingSet[counter]=[file,False] 
        counter+=1
        ham1[rand]=rand
        
        rand = random.randrange(1,301)
        while(ham2.get(rand)):
            rand = random.randrange(1,301)
        file = open(r"Ham\\301-600 good ones\\"+str(rand)+".txt")
        trainingSet[counter]=[file,False]
        counter+=1
        ham2[rand]=rand
         
    for x in range(500):
        #Choose a random spam email
        rand = random.randrange(1,601)
        while(spam.get(rand)):
            rand = random.randrange(1,601)
        file = open(r"Spam\\"+str(rand)+".txt")
        trainingSet[counter]=[file,True]
        counter+=1
        spam[rand]=rand
        #print(counter)
    
    counter=1
    
    for x in range(1,301):
        #Add the rest of the non-spam emails to testingSet
        if not ham1.get(x):
            file = open(r"Ham\\300 good emails\\"+str(x)+".txt")
            testingSet[counter]=[file,False,False] #currently, bool1 doesn't mean anything. It will be set later
            counter+=1
        if not ham2.get(x):
            file = open(r"Ham\\301-600 good ones\\"+str(x)+".txt")
            testingSet[counter]=[file,False,False]
            counter+=1
            
    for x in range(1,601):
        #Add the rest of the spam emails to testingSet
        if not spam.get(x):
            file = open(r"Spam\\"+str(x)+".txt")
            testingSet[counter]=[file,True,True]
            counter+=1
    
    '''
    print (len(trainingSet))#temporarily used to print # of spam and non-spam emails
    spammy=0
    nonspam=0
    for email in trainingSet.keys():
        if trainingSet[email][2] == 0:
            nonspam+=1
        elif trainingSet[email][1] == 1:
            spammy+=1
    print (spammy)
    print (nonspam)
    '''
    

# Naive Bayesian Classifier function
def naiveBayes():
    for email in testingSet.keys():
        words=[]
        for word in testingSet[email][0]: #put every word of a testingSet email into a list
            words.append(word)
        
        P0=1 #probability of email being non-spam
        P1=1 #probability of email being spam
            
        for word in words:
            #Compute non-spam probability of each word based on the trainingSet's emails
            numerator = 0
            denominator = 0
            for e in trainingSet.keys():
                if trainingSet[e][1] == False:
                    denominator+=1 #if the training email is non-spam, increment denominator
                    if word in trainingSet[e][0]:
                        numerator+=1 #if the training email contains the word and is non-spam, increment numerator

            #Laplace Smoothing
            numerator+=1
            denominator+=2    

            P0*=numerator/denominator #multiply the probability. (This is the chain rule multiplication step)
            
            
            #Compute spam probability of each word based on the trainingSet's emails. Same steps as before, except for spam words.
            numerator = 0
            denominator = 0
            for e in trainingSet.keys():
                if trainingSet[e][1] == True:
                    denominator+=1 
                    if word in trainingSet[e][0]:
                        numerator+=1 
                
            numerator+=1
            denominator+=2
            
            P1*=numerator/denominator
            
        
        #if probability of email being non-spam is greater than probability of being spam, mark email as non-spam, and vice-versa.
        if P0>P1:
            testingSet[email][1] = False
        else:
            testingSet[email][1] = True
             

#Function to calculate accuracy, precision, recall, and F1 Score
def evaluate():
    global TP,TN,FP,FN,accuracy,precision,recall,f1Score
    for email in testingSet.keys():
        if testingSet[email][1]==True and testingSet[email][2]==True:
            TP+=1
        elif testingSet[email][1]==False and testingSet[email][2]==False:
            TN+=1
        elif testingSet[email][1]==False and testingSet[email][2]==True:
            FP+=1
        elif testingSet[email][1]==True and testingSet[email][2]==False:
            FN+=1
    accuracy = (TP+TN)/(TP+TN+FP+FN)
    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    f1Score = (2*precision*recall)/(precision+recall)
    
    #print(TP)
    #print(TN)
    #print(FP)
    #print(FN)
    print("Accuracy = ",accuracy,"\nPrecision = ",precision,"\nRecall = ",recall,"\nF1 Score = ",f1Score)
        
   
importEmails()
naiveBayes()
evaluate()





