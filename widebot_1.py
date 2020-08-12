
import time
import urllib
import re
import bs4
import requests

start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"


def getFirst(url):
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    #Find content div
    content_div = soup.find(
        id="mw-content-text").find(class_="mw-parser-output")

    article_link = None
    found=False
    for element in content_div.find_all("p", recursive=False):
        #Remove translations/Prononciation
        txt= element.text.replace("(listen)","")[:150]
        f= txt[txt.find("(")+1:txt.find(")")]
        if txt[:-1]==f:
          #No links between ()
          f=""
        else:
          #Remove punctuation
          f= f.replace(":","").replace(",","").replace(".","").replace("'","")
        for idx,i in enumerate(element.find_all("a", recursive=False)):
          article_link = i.get('href')
          #print(article_link)
          if not article_link:
            continue
          if ("Help:" in article_link or "#" in article_link):
            continue
          if i.text in f:
            continue
          found=True
          break
      
        if found:
          break
    first_link = urllib.parse.urljoin(
        'https://en.wikipedia.org/', article_link)

    return first_link

l=[start_url]
#https://en.wikipedia.org/wiki/Wikipedia:Dead-end_pages There is no dead-end pages on wikipedia currently
print(start_url)
while(target_url not in l):
  x= getFirst(l[-1])
  print(x)
  if x in l and x != start_url:
    print("Loop Found")
    break
  l.append(x)
  time.sleep(0.5)
if target_url in l:
  print("Found")

