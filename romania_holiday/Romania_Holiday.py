# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 13:23:41 2021

@author: [redacted] and DrSlifer

This script computes the route from a starting city to a goal city by random walking.
Each city connection has a cost, so the route's total cost must be under the specified budget.
No revisiting of cities that have been previously visited.

The Romania problem
"""
import random

Romania_Map = {'Oradea':[[('Zerind',71),('Sibiu',151)],0],
               'Zerind':[[('Arad',75),('Oradea',71)],0],
               'Arad':[[('Zerind',75),('Sibiu',140),('Timisoara',118)],0],
               'Timisoara':[[('Arad',118),('Lugoj',111)],0],
               'Lugoj':[[('Timisoara',111),('Mehadia',75)],0],
               'Mehadia':[[('Lugoj',70),('Drobeta',75)],0],
               'Drobeta':[[('Mehadia',75),('Craiova',120)],0],
               'Craiova':[[('Drobeta',120),('Rimnicu Vilcea',146),('Pitesti',138)],0],
               'Rimnicu Vilcea':[[('Craiova',146),('Sibiu',80),('Pitesti',97)],0],
               'Sibiu':[[('Oradea',151),('Arad',140),('Fagaras',99),('Rimnicu Vilcea',80)],0],
               'Fagaras':[[('Sibiu',99),('Bucharest',211)],0],
               'Pitesti':[[('Rimnicu Vilcea',97),('Craiova',138),('Bucharest',101)],0],
               'Bucharest':[[('Fagaras',211),('Pitesti',101),('Giurgiu',90),('Urziceni',85)],0],
               'Giurgiu':[[('Bucharest',90)],0],
               'Urziceni':[[('Bucharest',85),('Vaslui',142),('Hirsova',98)],0],
               'Neamt':[[('Iasi',87)],0],
               'Iasi':[[('Neamt',87),('Vaslui',92)],0],
               'Vaslui':[[('Iasi',92),('Urziceni',142)],0],
               'Hirsova':[[('Urziceni',98),('Eforie',86)],0],
               'Eforie':[[('Hirsova',86)],0]           
              } #City dictionary. Each key points to a list, first element is a list of tuples and second element is a flag
                #The flag signifies if the city been visited yet. 0 is no, 1 is yes
                        

class PathFindingAgent(object):
    def __init__(self, Map):
        self.map = Map
        self.route = []
        self.total_cost = 0
    def solve(self, start, end, budget):
        flag = True
        self.route.append(start)
        self.current_city = start
        while flag:
            self.map[self.current_city][1]=1 #mark the current city as visited
            #print(self.map[self.current_city])
            if self.total_cost>budget:
                flag = False
                self.total_cost = 0
                self.route.clear()
                return 0
            elif self.current_city == end:
                flag = False
                return 1
            else:
                #Make a list of next cities: Observing
                cities = [city for city, cost in self.map[self.current_city][0]]
                #Make a list of next costs: Observing
                costs = [cost for city, cost in self.map[self.current_city][0]]
                #See if the destination is in the next cities' list
                try:
                    i = cities.index(end)
                    self.current_city = end
                    self.route.append(self.current_city)
                    self.total_cost += costs[i]
                #if not then random walk    
                except ValueError:
                    #print ("current city:", self.route[-1])
                    deadEnd = 1
                    for i in self.map[self.current_city][0]:
                        if self.map[i[0]][1] == 0:
                            deadEnd = 0
                    if deadEnd == 1:
                        self.total_cost=0
                        self.route.clear()
                        #print("dead end")
                        return 0
                        
                    
                    next_city, cost = random.sample(self.map[self.current_city][0],1)[0]
                    #print ("next city: ", next_city, cost)
                    while (self.map[next_city][1]==1):
                        next_city, cost = random.sample(self.map[self.current_city][0],1)[0]
                        #print("change next city:", next_city, cost)
                    
                    #Add the current cost to the total
                    self.total_cost += cost
                    #Set next city to the current city
                    self.current_city = next_city
                    #Add the current city to the route
                    self.route.append(self.current_city)
                #do 9999 tries for budget
                
if __name__ == '__main__':
    agent = PathFindingAgent(Romania_Map)
    success = 0
    attempts = 0
    while success == 0 and attempts < 20: #try reaching the goal in 20 attempts
        success = agent.solve('Arad','Bucharest',440) #budget of 440 in 20 attempts will show that often the budget needs to be increased
        for city in Romania_Map.keys():
                Romania_Map[city][1]=0 #reset the visited flags on each city
        attempts+=1
    if success == 0 :
        print("Please increase the budget")
    else:
        print (agent.route, agent.total_cost) 
             