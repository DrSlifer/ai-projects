# -*- coding: utf-8 -*-
"""
Created on Fri Mar  20 20:24:04 2021

@author: DrSlifer
This script performs policy iteration on an arbitrary policy in a given non-deterministic environment.
 
"""

#arbitrary policy, which can optionally be any of the actions (1 or 2)
policy = 1

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

#Used temporarily to see a defined amount of iterations
#counter = 10;


def policyIteration():
    global policy
    #global counter
    
    #antipolicy = 1
    #if policy==1:
       # antipolicy=2
    for x in range(100):
        #evaluate the stateValues of each non-terminal state. Use the arbitrary policy to select a stateTransition model value.
        stateVal["VπA"] = (stateTrans["B|A,"+str(policy)] * (reward+discount*stateVal["VπB"])) + (stateTrans["C|A,"+str(policy)] * (reward+discount*stateVal["VπC"])) + (stateTrans["C|A,"+str(policy)] * (reward+discount*stateVal["VπC"])) + (stateTrans["B|A,"+str(policy)] * (reward+discount*stateVal["VπB"]))
        
        stateVal["VπB"] = (stateTrans["D|B,"+str(policy)] * (reward+discount*stateVal["VπD"])) + (stateTrans["A|B,"+str(policy)] * (reward+discount*stateVal["VπA"])) + (stateTrans["A|B,"+str(policy)] * (reward+discount*stateVal["VπA"])) + (stateTrans["D|B,"+str(policy)] * (reward+discount*stateVal["VπD"]))
        
        stateVal["VπC"] = (stateTrans["A|C,"+str(policy)] * (reward+discount*stateVal["VπA"])) + (stateTrans["D|C,"+str(policy)] * (reward+discount*stateVal["VπD"])) + (stateTrans["D|C,"+str(policy)] * (reward+discount*stateVal["VπD"])) + (stateTrans["A|C,"+str(policy)] * (reward+discount*stateVal["VπA"]))

    #print (stateVal)
    
    #---------------------------------------
    
    policyStable = True #flag for if the policy is optimal
    chooseOne = 0 #compared to chooseTwo to get the argmax
    chooseTwo = 0 #compared to chooseOne to get the argmax
    
    #A loop would be better for going through each state (as shown in class.) However, each stateTransition model value is specific, so I choose to seperate it.
    #Some code can probably be condensed here
    
    #State A: 
    oldAction = policy
        
    chooseOne = (stateTrans["B|A,1"] * (reward+discount*stateVal["VπB"]))+(stateTrans["C|A,1"] * (reward+discount*stateVal["VπC"]))
    #print (chooseOne)
    
    chooseTwo = (stateTrans["C|A,2"] * (reward+discount*stateVal["VπC"]))+(stateTrans["B|A,2"] * (reward+discount*stateVal["VπB"]))
    #print (chooseTwo)
    
    if chooseOne>chooseTwo:
        #the value of using action 1 is better, so assign action 1 to choose1. (chooseOne then acts as argmax, and is assigned to the policy)
        chooseOne = 1
        policy = chooseOne
    else:
        #the value of using action 2 is better, so assign action 2 to choose2. (chooseTwo then acts as argmax, and is assigned to the policy)
        chooseTwo = 2            
        policy = chooseTwo
    
    if oldAction != policy:
        #policy is not stable yet
        policyStable = False
        #print(oldAction, policy)
        
        
    #State B:
    oldAction = policy
        
    chooseOne = (stateTrans["D|B,1"] * (reward+discount*stateVal["VπD"]))+(stateTrans["A|B,1"] * (reward+discount*stateVal["VπA"]))
    #print (chooseOne)
    
    chooseTwo = (stateTrans["A|B,2"] * (reward+discount*stateVal["VπA"]))+(stateTrans["D|B,2"] * (reward+discount*stateVal["VπD"]))
    #print (chooseTwo)
    
    if chooseOne>chooseTwo:
        chooseOne = 1 
        policy = chooseOne
    else:
        chooseTwo = 2            
        policy = chooseTwo
    
    if oldAction != policy:
        policyStable = False
        #print(oldAction, policy)
        
        
    #State C:
    oldAction = policy
        
    chooseOne = (stateTrans["A|C,1"] * (reward+discount*stateVal["VπA"]))+(stateTrans["D|C,1"] * (reward+discount*stateVal["VπD"]))
    #print (chooseOne)
    
    chooseTwo = (stateTrans["D|C,2"] * (reward+discount*stateVal["VπD"]))+(stateTrans["A|C,2"] * (reward+discount*stateVal["VπA"]))
    #print (chooseTwo)
    
    if chooseOne>chooseTwo:
        chooseOne = 1
        policy = chooseOne
    else:
        chooseTwo = 2            
        policy = chooseTwo
    
    if oldAction != policy:
        policyStable = False
        #print(oldAction, policy)
        
        
        
    if policyStable == True:
        #policy is stable, so its done
        print("Arbitrary policy:",stateVal)
    else:
        #print("running again")
        #if counter>0: #used temporarily to see a defined amount of iterations
            #counter-=1;
        #Re-run, starting from the policy evaluation step
        policyIteration()
        
policyIteration()



     
        
        
        
        
        