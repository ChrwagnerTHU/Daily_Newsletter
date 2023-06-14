import feedparser
import requests
from bs4 import BeautifulSoup

def getRecipe():
    feed = feedparser.parse('https://www.chefkoch.de/recipe-of-the-day/rss')
    title = feed['entries'][0]['title']
    link = feed['entries'][0]['link']

    res = requests.get(link)
    soup = BeautifulSoup(res.text, "lxml")
    imgTag = soup.find_all("img", {"class": "i-amphtml-fill-content i-amphtml-replaced-content"})
    img = imgTag[0].attrs['src']

    return {"Link": link, "Title": title, "Img": img}