import requests
from bs4 import BeautifulSoup
def getNews():
    try:
        response=requests.get("https://timesofindia.indiatimes.com/")
        if response.status_code==200:
            soup=BeautifulSoup(response.text,"html.parser")
            news=soup.find("ul",{"class":"list8"}).text.split("\n\n\n")
            newsString=""
            for n in news:
                newsString+=n+";\n"
            return newsString
        return "Could not fetch news"
    except:
        return "Could not fetch news"
