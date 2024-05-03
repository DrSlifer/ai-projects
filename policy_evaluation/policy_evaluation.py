# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 20:24:04 2021

@author: DrSlifer
This script performs policy evalution on 3 different policies in a given non-deterministic environment.
 
"""

#Nested dictionary of policies with each policy's respective mappings
policies = {"policy1": {"1|A":1,"1|B":1,"1|C":1,"2|A":0,"2|B":0,"2|C":0},"policy2": {"1|A":0,"1|B":0,"1|C":0,"2|A":1,"2|B":1,"2|C":1}, "policy3": {"1|A":0.4,"1|B":1,"1|C":0,"2|A":0.6,"2|B":0,"2|C":1}} #nested dictionary

#List of possible actions
#action = [1,2]

#Reward model, which will always be -10, so a dictionary is unneccesary
reward = -10;

#State transition model, a dictionary listing probabilities of reaching different states
stateTrans = {"B|A,1": 0.9, "C|A,1": 0.1, "C|A,2": 0.9, "B|A,2": 0.1, "D|B,1": 0.9, "A|B,1": 0.1, "A|B,2": 0.9, "D|B,2": 0.1, "A|C,1":0.9, "D|C,1":0.1, "D|C,2":0.9, "A|C,2":0.1}

#State values, a dictionary where every state is 0 except for terminal states, which is instead 100
stateVal = {"VπA":0,"VπB":0,"VπC":0,"VπD":100} 

#Discounting factor
discount = 1


val=0 #temporary val to be used for updating stateVals (however its not strictly necessary)
for policy in policies:
    #Evaluate each policy 100 times by using the Bellman equation
    for x in range(100):
        val = (policies[policy]["1|A"] * stateTrans["B|A,1"] * (reward+discount*stateVal["VπB"])) + (policies[policy]["1|A"] * stateTrans["C|A,1"] * (reward+discount*stateVal["VπC"])) + (policies[policy]["2|A"] * stateTrans["C|A,2"] * (reward+discount*stateVal["VπC"])) + (policies[policy]["2|A"] * stateTrans["B|A,2"] * (reward+discount*stateVal["VπB"]))
        stateVal["VπA"] = val #update the respective stateVal 
        
        val = (policies[policy]["1|B"] * stateTrans["D|B,1"] * (reward+discount*stateVal["VπD"])) + (policies[policy]["1|B"] * stateTrans["A|B,1"] * (reward+discount*stateVal["VπA"])) + (policies[policy]["2|B"] * stateTrans["A|B,2"] * (reward+discount*stateVal["VπA"])) + (policies[policy]["2|B"] * stateTrans["D|B,2"] * (reward+discount*stateVal["VπD"]))
        stateVal["VπB"] = val
        
        val = (policies[policy]["1|C"] * stateTrans["A|C,1"] * (reward+discount*stateVal["VπA"])) + (policies[policy]["1|C"] * stateTrans["D|C,1"] * (reward+discount*stateVal["VπD"])) + (policies[policy]["2|C"] * stateTrans["D|C,2"] * (reward+discount*stateVal["VπD"])) + (policies[policy]["2|C"] * stateTrans["A|C,2"] * (reward+discount*stateVal["VπA"]))
        stateVal["VπC"] = val
    print("Using",policy,": ",stateVal)
    






     
        
        
        
        
        