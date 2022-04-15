from bs4 import BeautifulSoup
import requests

def accessSite():
    url="https://blog.reedsy.com/short-stories/fantasy/page/1/"
    page = requests.get(url)


    soup = BeautifulSoup(page.content, "html.parser")
    price=soup.find_all("p")
    submission=soup.find_all( 'div', class_='submission' )
    print(price)
    print("lols")
    for el in submission:
        print(submission[0].get_text())
        print(el[0].get_text())





