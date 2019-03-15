import requests
from bs4 import BeautifulSoup
import re
import pymongo



#Given the URL of an actor's IMDB page, returns a list of the URLs of all the films they were in 
def movieURLSfromActor(URL):
     
    homeurl = URL

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')

    outputList = []

    for item in list:
        URL = item.get('href')
        try:
            if "flmg_act" in URL:
                x = URL[:17]
                x = "https://www.imdb.com" + x
                outputList.append(x)
        except:
            print(URL)
    
    
    finalList = set(outputList)
    return finalList  

#Given the URL of an film's IMDB page, returns a list of the URLs of all the (significant) actors who were in it
def actorsURLSfromMovie(URL):

    homeurl = URL + 'fullcredits/'

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')

    outputList = []

    for item in list:
        URL = item.get('href')
        if "/name/" in URL:
            if "fc_cr" not in URL:
                if "fc_dr" not in URL:
                    if ("fc_wr") not in URL:
                        if ("nv_cel") not in URL:
                            x = URL[:16]
                            x = "https://www.imdb.com" + x
                            outputList.append(x)

    finalList = set(outputList)
    return finalList  

#Given the URL of a film's IMDB page, returns a dict as dict[name] = role
def movieCastParser(URL):

    homeurl = URL + 'fullcredits'

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')
    
    iterator = 1

    actor = ""
    role = ""

    dict = {}

    for item in list:
        URL = str(item)
        if "ttfc_fc_cl" in URL:

            stringy = item.contents
            stringy = CleanData(stringy)

            if(len(stringy) < 40):

                if (iterator%2 == 1):
                    actor = stringy[:-2]
                    iterator += 1
                elif (iterator%2 == 0):
                    if "\\n" in stringy:
                        actor = stringy[:-2]
                    else:
                        role = stringy
                        iterator += 1
                        actor = actor.replace(".","")
                        role = role.replace(".","")
                        dict[actor] = role


    return dict

#Helper method for movieCastParser(URL) to remove formatting before appending
#Given a string, returns a cleaned string
def CleanData(string):
    stringy = str(string)
    stringy = stringy.strip(' []\'')
    return stringy

#Takes advantage of the formatting of all actor's IMDB pages
#It seems a disproportionate number of famous people are in the first few thousand
def actorURLgenerator(depth):
    
    iterator = 1

    returnList = []

    while (iterator < depth):

        if (iterator < 10):
            itStr = str(iterator)
            URL = 'https://www.imdb.com/name/nm000000' + itStr + '/'
        elif (iterator < 100):
            itStr = str(iterator)
            URL = 'https://www.imdb.com/name/nm00000' + itStr + '/'
        elif (iterator < 1000):
            itStr = str(iterator)
            URL = 'https://www.imdb.com/name/nm0000' + itStr + '/'
        elif (iterator < 10000):
            itStr = str(iterator)
            URL = 'https://www.imdb.com/name/nm000' + itStr + '/'

        returnList.append(URL)

        iterator += 1

    return returnList

#Given the URL of a film's IMDB page, returns film's title
def movieTitleParser(URL):

     homeurl = URL

     page = requests.get(homeurl)
     soup = BeautifulSoup(page.text, 'html.parser')
     list = soup.find_all('title')


     stringy = list[0].contents
     stringy = CleanData(stringy)
     return stringy

 #Runs everything and populates database, given the number of actor's pages you want to hit.  ~1000 deemed optimal in testing
def Engine(depth):
    
    actorList = actorURLgenerator(depth)
    movieList = []

    for URL in actorList:
        print(URL)
        moviesReturnedList = movieURLSfromActor(URL)
        for item in moviesReturnedList:
            if "TV" not in item:
                movieList.append(item)

    movieList = set(movieList)

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["KevinBacon"]

    mycol = mydb["Movies"]

    lengthyBoi = len(movieList)
    iterator = 1

    for movie in movieList:
        status = str(iterator) + "/" + str(lengthyBoi)
        print(status)
        cast = movieCastParser(movie)
        if(bool(cast)):
            title = movieTitleParser(movie)

            dict = {"title": title,
                    "cast": cast}
            mycol.insert_one(dict)

        iterator +=1

Engine(1000)