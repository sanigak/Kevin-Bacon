import pymongo
import datetime
import re



myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["KevinBacon"]
col = mydb["MoviesCOPY"]

solution = ""

def moviesGivenActor(actor):
    outputList = []
    content = "cast." + actor
    all = re.compile(".*")
    query = col.find({content: all},{"title":1, "_id":0})
    for item in query:
        title = item["title"]
        outputList.append(title)
    return outputList



def castGivenMovie(movie):
    outputList = []
    query = col.find({"title":movie},{"cast":1, "_id":0})
    for item in query:
        cast = item["cast"]
        outputList.append(cast)
   
    return outputList[0]

def Engine(actor, solution):

    movies = moviesGivenActor(actor)

    for movie in movies:
        print(movie)
        cast = castGivenMovie(movie)
        for subactor in cast:
            print(subactor)
            if subactor == "Kevin Bacon":
                solution += actor + " was in " + movie + " with Kevin Bacon"
                return solution
    Engine(subactor, solution)
