from bs4 import BeautifulSoup
import random
import requests

def lercio_soup():
    p = requests.get('http://www.lercio.it')
    if p.status_code != 200:
        raise RuntimeError('could not download lercio\'s frontpage')
    return BeautifulSoup(p.content, 'lxml').html.body

def lercio_main():
    """
    get the main article of today's lercio
    """
    # assuming the main article is the first link with a title on the page
    article = lercio_soup().find('a', title=True)
    return '[{title}]({link})'.format(title=article['title'], link=article['href'])

def lercio_latest():
    """
    get the latest news from lercio
    """
    is_ultimora = lambda tag: tag.name == 'span' and tag.get_text(strip=True) == 'ULTIMORA'
    latest_articles = lercio_soup().find(is_ultimora).parent.find_all('a')
    article = random.choice(latest_articles)
    return '[{title}]({link})'.format(title=article.get_text(), link=article['href'])

text_generators = {
    'lercio': lercio_main,
    'latest': lercio_latest,
}

def random_text():
    text_generator = random.choice(list(text_generators.values()))
    return text_generator()

image_generators = {
}

def random_image():
    img_generator = random.choice(list(image_generators.values()))
    return img_generator()
