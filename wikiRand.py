import requests
from bs4 import BeautifulSoup

def main():
    url = requests.get("https://de.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find(class_="firstHeading").text
    titleURL = title.replace(" ", "_")

    return {"Link": "https://de.wikipedia.org/wiki/%s" % titleURL, "Header": title}

if __name__ == '__main__':
    main()