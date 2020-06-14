from datetime import datetime
class City:
    name: str
    latitude: float
    longitude: float

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude


class Flight:
    origin: City
    destination: City
    departure_time: str
    arrival_time: str
    flight_number: str
    listofdays: list

    def __init__(self, s, d, dt, at, fn, l):
        self.origin = s
        self.destination = d
        self.departure_time = dt
        self.arrival_time = at
        self.flight_number = fn
        self.listofdays = l


class Distance:
    source: City
    destination: City
    actual: float #actual score of node
    heuristic: float #heuristic score of node
    total: float #sum of the above scores

    def __init__(self, s, d, a, h, t):
        self.source = s
        self.destination = d
        self.actual = a
        self.heuristic = h
        self.total = t



class Tree:
    city: Distance
    childernList: list

    def __init__(self, city,childs):
        self.city = city
        self.childernList = childs


