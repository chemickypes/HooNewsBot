import write_data
import feedparser
from datetime import datetime
from time import mktime
from rx.subject import Subject
from models import HooNewsMessage
import requests

db = write_data.db

cache_live_search = {}

message_subject = Subject()


def __resolve_link(link):
    return requests.get(link).url


def start_user(user, chat_id):
    db.collection('users').document(chat_id).set(user)


def get_user(chat_id):
    return db.collection('users').document(chat_id).get().to_dict()


def next_article(chat_id, article_id):
    if cache_live_search.get(chat_id) is None:
        cache_live_search[chat_id] = db.collection('users').document(chat_id).get().to_dict()['live_search']

    return cache_live_search[chat_id][article_id] if article_id or chat_id in cache_live_search[chat_id] else None


def save_search(chat_id, search, search_category):
    cache_live_search[chat_id] = search
    user_doc = db.collection('users').document(chat_id)

    user_doc.add({'live_search': search})

    return search[list(search)[0]]


'''search = db.collection('searches') \
            .where('category', '==', category) \
            .where('lang', '==', lang) \
            .where('country', '==', nation).stream()'''


def make_search(chat_id, lang, category, nation):
    countries = db.collection('feeds').document('countries').get().to_dict()
    if lang not in countries['lang'] or nation not in countries['countries']:
        # populate feeds because there is not the country or the lang or both
        message_subject.on_next(HooNewsMessage('ALERT', (chat_id, 'FEEDS_LOADING')))
        write_data.write_generic_feeds(lang, nation)
        if lang not in countries['lang']: countries['lang'].append(lang)
        if nation not in countries['countries']: countries['countries'].append(nation)
        db.collection('feeds').document('countries').set(countries, merge=True)

    message_subject.on_next(HooNewsMessage('LOADING', (chat_id, 'NEWS_LOADING')))
    feeds = db.collection('feeds').where('category', '==', category) \
        .where('language', '==', lang) \
        .where('country', '==', nation).stream()

    list_of_articles = []

    for feed in feeds:
        ll = feedparser.parse(feed.to_dict()['link'])
        list_of_articles.extend(
            [{'id': entry['id'], 'title': entry['title'], 'link': entry['link'],
              'timestamp_parsed': entry['published_parsed']} for entry in ll['entries']]
        )

    list_of_articles.sort(key=lambda el: datetime.fromtimestamp(mktime(el['timestamp_parsed'])), reverse=True)
    print(len(list_of_articles))

    for index, element in enumerate(list_of_articles[:30]):
        db.collection('live_search').document(str(chat_id)).collection('articles').document(str(index)).set(element,
                                                                                                            merge=True)

    get_article(chat_id, '0')


def get_article(chat_id, article_id):
    art = db.collection('live_search').document(str(chat_id)).collection('articles').document(
        article_id).get().to_dict()
    if art is None:
        db.collection('live_search').document(str(chat_id)).delete()
        message_subject.on_next(HooNewsMessage('VALUE', (chat_id, None)))
    else:
        if 'news.google' in art['link']:
            art['link'] = __resolve_link(art['link'])
        message_subject.on_next(HooNewsMessage('VALUE', (chat_id, art, str(int(article_id) + 1))))


if __name__ == '__main__':
    message_subject.subscribe(lambda item: print(item))
    make_search(6483, 'it', 'technology', 'it')
    get_article(6483, '1')
    get_article(6483, '2')
    get_article(6483, '3')
    get_article(6483, '473946383745846')
