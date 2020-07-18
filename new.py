import requests
from bs4 import BeautifulSoup
url="https://www.google.com/search?q=weather"
r=requests.get(url)
if r.status_code==200:
	soup=BeautifulSoup(r.content,"html.parser")
	x=soup.find_all(id="wob_tm")
	print(x)
	x=x.prettify()
	actionStrinx="\n"+x.getText()