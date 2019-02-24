import requests
from bs4 import BeautifulSoup
import re


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

def CleanData(string):
    stringy = str(string)
    stringy = stringy.strip(' []\'')
    return stringy

def movieParser(URL):

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
                        dict[actor] = role


    return dict



def Engine():

    # All Movies Kevin Bacon was in
    initialMovieList = movieURLSfromActor('https://www.imdb.com/name/nm0000102/')

    initialActorList = []
    
    iterator = 0

    while iterator < 2:
        for URL in initialMovieList:
            actorReturnedList = actorsURLSfromMovie(URL)
            for item in actorReturnedList:
                initialActorList.append(item)
                print(item)


        for URL in initialActorList:
            moviesReturnedList = movieURLSfromActor(URL)
            for item in moviesReturnedList:
                initialMovieList.append(item)
                print(item)


        iterator+=1

    movieSet = set(initialMovieList)
    for item in initialMovieList:
        print(item)

Engine()
    