import feedparser
import requests
from rx import of, operators as op

# https://news.google.com/news/rss/headlines/section/topic/CATEGORYNAME?ned=in&hl=en
rss_url_struct = "https://news.google.com/news/rss/headlines/section/topic/{}?{}"
general_rss_structure = "https://news.google.com/news/rss/?{}"

categories = ["WORLD", "NATION", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SPORTS", "SCIENCE", "HEALTH", "GENERAL"]


def resolve_link(link):
    return requests.get(link).url


def __find_lang(lang):
    return f'ned={lang}&hl={lang}'


def get_categories(lang):
    return list(map(lambda cat: cat.lower().capitalize(), categories))


def list_of_news(type_of_news, lang):
    url = rss_url_struct.format(type_of_news,
                                __find_lang(lang)) if type_of_news != "GENERAL" else general_rss_structure.format(
        __find_lang(lang))
    print(url)
    news_feed = feedparser.parse(url)
    source = of(*news_feed['entries'][:15]).pipe(
        op.map(lambda entry: f'{entry["title"]}\n{resolve_link(entry["link"])}')
    )
    return source
