import pymongo
import datetime
import re
import random


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
def Engine(actor):

    movies = moviesGivenActor(actor)

    

    for movie in movies:
        print()
        print()
        print(actor)
        print(movie)
        print()
        print()
        cast = castGivenMovie(movie)
        for subactor in cast:
            print(subactor)
            if subactor == "Kevin Bacon":
                solutiony += (subactor + " was in " + movie + " with Kevin Bacon")
                print(solutiony)
                return solutiony

    random.shuffle(cast)
    Engine(cast[0], solutiony)

Engine("Willem Dafoe", "")
        
