from datetime import datetime
import geopy.distance
import null as null
from data import cities, listofflights
from classes import *
from collections import deque


def travel(start, goal, listofdays):
    path = []
    # the list of flights after filteration of the listofflights
    # filteration-> means just take the flights that satisfy the given list of days
    flights = []
    for x in listofflights:
        if(Contain(x.listofdays,listofdays)==True):
            flights.append(x)
    path = search(flights,start, goal)
    steps = []
    steps = find_flights(path)
    counter = 1
    for x in steps: #loop to print the solution
        print('Step ',counter,': use flight',x.flight_number,'From',x.origin.name,'To',
              x.destination.name,'Departure Time',x.departure_time,'Arrival Time',x.arrival_time)
        counter = counter+1



def find_flights(paths):
    available_flights = []
    for path in paths:
        for flight in listofflights:
            if (flight.origin.name==path.source.name and flight.destination.name==path.destination.name):
                available_flights.append(flight)
                break

    if(len(available_flights)==0):
        print("There is no available flights now")
        return

    return available_flights


def Contain(available_days,requested_days):
    for day in requested_days:
        if(available_days.__contains__(day)):
            return True

    return False

goal_city: City
start_city: City

def search(flights,start, goal):
    List = []
    for i in range(len(cities)):
        if (cities[i].name == goal):
            goal_city = City(cities[i].name, cities[i].latitude, cities[i].longitude)
        elif (cities[i].name == start):
            start_city = City(cities[i].name, cities[i].latitude, cities[i].longitude)
    # distance between start and goal cities
    z=calculate_distance(start_city.latitude, start_city.longitude,goal_city.latitude, goal_city.longitude)
    r = Distance(start_city, goal_city, 0, z, z)
    root = Tree(r,[])
    openTree:Tree #it is the tree that shows each city and its destination cities
    pathTree:list #it has all the paths that will be visited to find the final path
    for i in range(len(flights)):

        if (flights[i].origin.name == start):
            if(List.__contains__(flights[i].destination.name)):
                continue

            else:
                List.append(flights[i].destination.name)
                # distance between the start point to the current point
                actual = calculate_distance(flights[i].origin.latitude, flights[i].origin.longitude,
                                            flights[i].destination.latitude, flights[i].destination.longitude)
                # distance between the current point to the goal point
                heuristic = calculate_distance(flights[i].destination.latitude, flights[i].destination.longitude,
                                               goal_city.latitude, goal_city.longitude)
                # sum of both distances{ f(n)=g(n)+h(n) }
                total = actual + heuristic
                c = Distance(flights[i].origin, flights[i].destination, actual, heuristic, total)
                child = Tree(c, [])
                root.childernList.append(child)


    openTree = Tree(root.city,root.childernList)
    pathTree = []
    flightss = preorderTraversal(openTree)
    f = flightss.pop(0)
    current = f
    #list to ensure to not taking a visited path
    visited=[f]

    while (len(flightss)!=0):
        min=999999999999999.0 #just intitial value
        index:int
        for i in range(len(flightss)):
            if(flightss[i].source != current.source and flightss[i].destination != current.destination and flightss[i].total != current.total
            and flightss[i].heuristic!=current.heuristic and flightss[i].actual!=current.actual and flightss[i] not in visited):
                if (flightss[i].total < min):
                    min = flightss[i].total
                    index = i


        visited.append(flightss[index])
        current = flightss[index]
        pathTree.append(flightss[index])
        if flightss[index].destination.name == goal_city.name:
            print("PATH FOUND")
            finalpath=[flightss[index]]
            while(True): #this loop will retrieve the final path
                for i in range(0, len(pathTree)):
                    if (pathTree[i].destination.name == finalpath[0].source.name):
                        finalpath.insert(0, pathTree[i])
                if (finalpath[0].source.name == start_city.name):
                    break


            return finalpath

        add_child_to_child(flights,openTree, flightss[index],goal_city)
        flightss = preorderTraversal(openTree)
        flightss.pop(0)


def add_child_to_child(flights,root:Tree, source: Distance, goal_city:Distance):
    if ( root.city.destination.name == source.destination.name):
        L = []
        for i in range(len(flights)):

            if (flights[i].origin.name == source.destination.name):
                if (L.__contains__(flights[i].destination.name)):
                    continue

                elif(flights[i].destination.name == source.source.name):
                    continue

                else:
                    L.append(flights[i].destination.name)

                    # distance between the start point to the current point
                    a1 = calculate_distance(flights[i].origin.latitude, flights[i].origin.longitude,
                                                flights[i].destination.latitude, flights[i].destination.longitude)
                    a2=root.city.actual
                    actual=a1+a2
                    # distance between the current point to the goal point
                    heuristic = calculate_distance(flights[i].destination.latitude, flights[i].destination.longitude,
                                                   goal_city.latitude, goal_city.longitude)
                    # sum of both distances( f(n)=g(n)+h(n)
                    total = actual + heuristic
                    c = Distance(flights[i].origin, flights[i].destination, actual, heuristic, total)
                    child = Tree(c, [])
                    root.childernList.append(child)
        return root
    for i in range(0, (len(root.childernList))):
        add_child_to_child(flights,root.childernList[i], source,goal_city)


def preorderTraversal(root:Tree):
    Stack = deque([])
    # 'Preorder'-> contains all the
    # visited nodes.
    Preorder = []
    Preorder.append(root.city)
    Stack.append(root)
    while len(Stack) > 0:
        # 'Flag' checks whether all the child nodes have been visited.
        flag = 0
        # CASE 1- If Top of the stack is a leaf node then remove it from the stack:
        if len((Stack[len(Stack) - 1]).childernList) == 0:
            X = Stack.pop()
            # CASE 2- If Top of the stack is Parent with children:
        else:
            Par = Stack[len(Stack) - 1]

            for i in range(0, len(Par.childernList)):
                if Par.childernList[i].city not in Preorder:
                   flag = 1
                   Stack.append(Par.childernList[i])
                   Preorder.append(Par.childernList[i].city)
                   break;

            if flag == 0:
                Stack.pop()
    return Preorder

def calculate_distance(latitude1, longitude1, latitude2, longitude2):
    d = geopy.distance.distance((latitude1, longitude1), (latitude2, longitude2)).km
    return d


print("enter start city")
start = input()
print("enter goal city")
goal = input()
print('enter list of days separated by space')
l = input()
days = l.split()
travel(start,goal,days)

