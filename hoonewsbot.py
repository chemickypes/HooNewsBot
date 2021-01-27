import feedparser
import requests
from rx import of, operators as op

categories = {'TECH': (
    'Technology', 1, 'https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY?ned=IT&hl=IT'),
    'GENERAL': ('General', 0, 'https://news.google.com/news/rss/?gl=IN&ned=IT&hl=IT')}


def resolve_link(link):
    return requests.get(link).url


def list_of_news(type_of_news):
    news_feed = feedparser.parse(categories[type_of_news][2])
    source = of(*news_feed['entries'][:15]).pipe(
        op.map(lambda entry: f'{entry["title"]}\n{resolve_link(entry["link"])}')
    )
    return source
