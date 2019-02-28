import pymongo
import datetime
import re



myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["KevinBacon"]
col = mydb["MoviesCOPY"]

solution = ""
stillWorking = True

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
    finalList = []
    query = col.find({"title":movie},{"cast":1, "_id":0})
    for item in query:
        cast = item["cast"]
        outputList.append(cast)
    for item in outputList[0]:
        stringy = str(item)
        finalList.append(stringy)
   
    return finalList

def Engine(actor, solution):

    movies = moviesGivenActor(actor)
    actorTEMP = ""

    levelOfActors = []

    for movie in movies:
        
        cast = castGivenMovie(movie)
        for subactor in cast:
            interator = 0

            if subactor == "Kevin Bacon":
                solution += (subactor + " was in " + movie + " with Kevin Bacon")
                global stillWorking
                stillWorking = False
                print(solution)
                return solution
            else:
                levelOfActors.append(subactor)

    levelOfActors = set(levelOfActors)
    levelOfActors = list(levelOfActors)


    return levelOfActors
        


solutiony = Engine("Donald Trump", solution)

