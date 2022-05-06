from bs4 import BeautifulSoup
import requests
import time
import re
def accessSite():
    for i in range (1,88):

        url=f'https://podcastle.org/category/podcasts/page/{i}/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        pages=  soup.find_all( 'h3', class_='entry_title excerpt' )
        count=0

        for el in pages:

            a=pages[count].find('a')
            count += 1

            article(a['href'])



def article(link):
    url = link
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    submission = soup.find('div', class_='entry_content')
    if(submission.find( 'div', class_='show_notes')):
        submission.find('div', class_='show_notes').decompose()
    #submission.find( 'hr', class_='full' ).decompose()

    title=  soup.find( 'h2', class_='post_title' ).text
    #title  = re.subn(':', '?',title)
    title = title.replace(":" , "")
    title = title.replace("?", "")

    #print(submission.text)
    #print(title.text)
    with open(
                f'C:\\Users\\Quake\\Desktop\\StoryGenerator\\resources\\books\\fantasy\\txt\\9k\\{title}.txt',
                'w', encoding="utf-8") as text_file1:
            print(f"{submission.text}", file=text_file1)
    print("Finish ",title)


def test():
    submission=0
    for el in submission:
        print(submission[0].get_text())
        print(el[0].get_text())





