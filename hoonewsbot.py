import feedparser
import requests
from rx import of, operators as op
import pycountry
import repo

# https://news.google.com/news/rss/headlines/section/topic/CATEGORYNAME?ned=in&hl=en
rss_url_struct = "https://news.google.com/news/rss/headlines/section/topic/{}?{}"
general_rss_structure = "https://news.google.com/news/rss/?{}"

categories = {'0': 'WORLD', '1': 'NATION', '2': 'BUSINESS', '3': 'TECHNOLOGY', '4': 'ENTERTAINMENT', '5': 'SPORTS',
              '6': 'SCIENCE', '7': 'HEALTH', '8': 'GENERAL'}


def resolve_link(link):
    return requests.get(link).url


def __find_lang(lang):
    return f'ned={lang}&hl={lang}'


def save_user(user, chat_id):
    repo.start_user(user, chat_id)


def get_categories(lang):
    categories_ = []
    country = pycountry.countries.get(alpha_2=lang)
    for index, cat in categories.items():
        categories_.append(
            (cat.lower().capitalize(), index) if index != '1' else
            (country.name, index)
        )
    return categories_


def list_of_news(type_of_news, lang):
    url = rss_url_struct.format(categories[type_of_news],
                                __find_lang(lang)) if type_of_news != '8' else general_rss_structure.format(
        __find_lang(lang))
    print(url)
    news_feed = feedparser.parse(url)
    source = of(*news_feed['entries'][:15]).pipe(
        op.map(lambda entry: f'{entry["title"]}\n{resolve_link(entry["link"])}')
    )
    return source
