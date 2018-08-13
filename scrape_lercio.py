import requests
from bs4 import BeautifulSoup

def lercio_soup():
    p = requests.get('http://www.lercio.it')
    if p.status_code != 200:
        raise RuntimeError('could not download lercio\'s frontpage')
    return BeautifulSoup(p.content, 'lxml').html.body

def get_main_article():
    # ...assuming the main article is the first link with a title on the page
    return lercio_soup().find('a', title=True)

def get_main_title():
    main_article = get_main_article()
    if not main_article:
        raise RuntimeError('could not find lercio\'s main article')
    return main_article['title']

if __name__ == '__main__':
    print(get_main_title())
