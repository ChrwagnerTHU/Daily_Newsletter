import requests
from bs4 import BeautifulSoup

def main():
    url = requests.get("https://de.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find(class_="firstHeading").text

    return {"Link": "https://de.wikipedia.org/wiki/%s" % title, "Header": title}

if __name__ == '__main__':
    main()