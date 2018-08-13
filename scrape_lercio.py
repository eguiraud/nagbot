import requests
from bs4 import BeautifulSoup

def article_tag(tag):
    """
    Filter tags that contain lercio articles.
    All link tags with a title are considered articles.
    """
    return tag.name == 'a' and tag.has_attr('title')

def get_main_article():
    p = requests.get('http://www.lercio.it')
    if p.status_code != 200:
        raise RuntimeError('could not download lercio\'s frontpage')
    soup = BeautifulSoup(p.content, 'lxml')
    return soup.html.body.find(article_tag)

def get_main_title():
    main_article = get_main_article()
    if not main_article:
        raise RuntimeError('could not find lercio\'s main article')
    return main_article['title']

if __name__ == '__main__':
    print(get_main_title())
