import requests
from bs4 import BeautifulSoup
import re


def movieURLSfromActor():
     
    homeurl = 'https://www.imdb.com/name/nm0000102/'

    page = requests.get(homeurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    list = soup.find_all('a')

    for item in list:
        URL = item.get('href')
        try:
            if "flmg_act" in URL:
                x = URL[:17]
                x = "https://www.imdb.com" + x
                print (x)
        except:
            print(URL)



movieURLSfromActor()