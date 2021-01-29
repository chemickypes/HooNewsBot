import feedparser
import json
import firebase_admin
from firebase_admin import credentials

ultimo_uomo_url = "https://www.ultimouomo.com/rss"
g_news = 'https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY?ned=it&hl=it'
wired_news = 'https://www.wired.it/feed/'

rss_url_struct = "https://news.google.com/news/rss/headlines/section/topic/{}?{}"
general_rss_structure = "https://news.google.com/news/rss/?{}"

categories = {'0': 'WORLD', '1': 'NATION', '2': 'BUSINESS', '3': 'TECHNOLOGY', '4': 'ENTERTAINMENT', '5': 'SPORTS',
              '6': 'SCIENCE', '7': 'HEALTH', '8': 'GENERAL'}



cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

if __name__ == '__main__':
    news_feed_ul = feedparser.parse(ultimo_uomo_url)
    news_feed_gn = feedparser.parse(wired_news)

    for entry in [*news_feed_ul['entries'], *news_feed_gn['entries']]:
        print(entry['id'], json.dumps(entry))
