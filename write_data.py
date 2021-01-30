
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from country_list import countries_for_language
import language_tags
import json


ultimo_uomo_url = "https://www.ultimouomo.com/rss"
g_news = 'https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY?ned=it&hl=it'
wired_news = 'https://www.wired.it/feed/'

rss_url_struct = "https://news.google.com/news/rss/headlines/section/topic/{}?{}"
general_rss_structure = "https://news.google.com/news/rss/?{}"

categories = {'0': 'WORLD', '1': 'NATION', '2': 'BUSINESS', '3': 'TECHNOLOGY', '4': 'ENTERTAINMENT', '5': 'SPORTS',
              '6': 'SCIENCE', '7': 'HEALTH', '8': 'GENERAL'}

cred = credentials.Certificate("hoonewsbot-firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

cache_live_search = {}


def __find_lang(lang, country):
    return f'gl={country}&ned={country}&hl={lang}'


def write_generic_feeds(lang, country):
    for i, cat in categories.items():
        db.collection('feeds').document().set({
            'link': rss_url_struct.format(categories[i],
                                          __find_lang(lang, country)) if i != '8' else general_rss_structure.format(
                __find_lang(lang, country)),
            'category': cat.lower(),
            'language': lang,
            'country': country
        })


if __name__ == '__main__':
    __ll = {}
    with open('langs.json', 'r') as fi:
        __ll = json.loads(fi.read())
        fi.close()
    db.collection('languages').document('languages').set(__ll)