import pymongo
import datetime
import re
import random
import numpy


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["KevinBacon"]
col = mydb["MoviesCOPY"]


solution = ""

#Given an actor as input, returns the title of all the films they appeared in
def moviesGivenActor(actor):
    outputList = []
    content = "cast." + actor
    all = re.compile(".*")
    query = col.find({content: all},{"title":1, "_id":0})
    for item in query:
        title = item["title"]
        outputList.append(title)
    return outputList

#Given a film, returns a list of the cast of the film
def castGivenMovie(movie):
    outputList = []
    finalList = []
    query = col.find({"title":movie},{"cast":1, "_id":0})
    for item in query:
        cast = item["cast"]
        outputList.append(cast)
    for item in outputList[0]:
        stringy = str(item)
        finalList.append(stringy)
   
    return finalList



#Runs game, given an actor and an initially blank solution
#Recurvise

def Engine(actor, solution):


    movies = moviesGivenActor(actor)



    for movie in movies:
        print()
        print()
        print(actor)
        print(movie)
        print()
        print()

        cast = castGivenMovie(movie)

        if actor in cast:
            cast.remove(actor)

        for subactor in cast:

                
                
            if subactor == "Kevin Bacon":
                solution += (actor + " was in " + movie + " with " + subactor)
                print(solution)
                return solution

    cast = 0

    while cast <= 2:
        randMovie = random.choice(movies)
        randCast = castGivenMovie(randMovie)
        cast = len(randCast)
    if actor != randCast[0]:
        solution += (actor + " was in " + randMovie + " with " + randCast[0] + ",  ")
    Engine(randCast[0], solution)

Engine("Willem Dafoe", "")


