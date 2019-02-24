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


