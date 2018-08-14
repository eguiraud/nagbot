from bs4 import BeautifulSoup
import random
import re
import requests

def absurdityisnothing():
    """
    get a random article from absurdityisnothing.net
    """
    p = requests.get('http://www.absurdityisnothing.net/random')
    if p.status_code != 200:
        raise RuntimeError(f'could not access absurdityisnothing.net')
    absurd_soup = BeautifulSoup(p.content, 'lxml').html.body
    title = absurd_soup.find('h1','entry-title').text
    return '[{title}]({link})'.format(title=title, link=p.url)

def carcassonne_road():
    """
    get an image of a carcassonne road tile
    """
    return 'https://i.stack.imgur.com/YQHH2.png'

def get_page_body(url):
    r = requests.get(url, headers={'User-agent': 'telegram-nagbot-12831023'})
    if r.status_code != 200:
        raise RuntimeError(f'could not download page at url "{url}"')
    return BeautifulSoup(r.content, 'lxml').html.body

def hmmm():
    """
    get a post from r/hmmm
    """
    soup = get_page_body('https://old.reddit.com/r/hmmm')
    post_links = soup.find_all('a', href=re.compile('^/r/hmmm/comments'))
    rnd_post = random.choice(post_links)
    title = rnd_post.text.strip() or 'link'
    link = 'https://www.reddit.com' + rnd_post['href']
    return f'[{title}]({link})'

def itemshop():
    """
    get a post from r/ItemShop
    """
    soup = get_page_body('https://old.reddit.com/r/ItemShop')
    post_links = soup.find_all('a', href=re.compile('^/r/ItemShop/comments'))
    rnd_post = random.choice(post_links)
    title = rnd_post.text.strip() or 'link'
    link = 'https://www.reddit.com' + rnd_post['href']
    return f'[{title}]({link})'

def lercio_latest():
    """
    get the latest news from lercio
    """
    is_ultimora = lambda tag: tag.name == 'span' and tag.get_text(strip=True) == 'ULTIMORA'
    lercio_soup = get_page_body('http://www.lercio.it')
    latest_articles = lercio_soup.find(is_ultimora).parent.find_all('a')
    article = random.choice(latest_articles)
    return '[{title}]({link})'.format(title=article.get_text(), link=article['href'])

def lercio_main():
    """
    get the main article of today's lercio
    """
    # assuming the main article is the first link with a title on the page
    lercio_soup = get_page_body('http://www.lercio.it')
    article = lercio_soup.find('a', title=True)
    return '[{title}]({link})'.format(title=article['title'], link=article['href'])

def tanadelmimic():
    """
    get a random page from tanadelmimic.it
    """
    r = requests.get('http://tanadelmimic.it/wiki/Speciale:PaginaCasuale')
    if r.status_code != 200:
        raise RuntimeError(f'could not access tanadelmimic.it')
    title = r.url.split('/')[-1].replace('_', ' ')
    text = '[{title}]({link})'.format(title=title, link=r.url)
    first_paragraph = BeautifulSoup(r.content, 'lxml').html.body.find('p')
    if first_paragraph:
        text += '\n' + first_paragraph.text.strip()
    return text


links = {
    'absurd': absurdityisnothing,
    'lercio': lercio_main,
    'latest': lercio_latest,
    'mimic': tanadelmimic,
    'itemshop': itemshop,
    'hmmm': hmmm,
}

def random_link():
    text_generator = random.choice(list(links.values()))
    return text_generator()

images = {
    'road': carcassonne_road
}

def random_image():
    img_generator = random.choice(list(images.values()))
    return img_generator()
