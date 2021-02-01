import write_data
import feedparser
from datetime import datetime
from time import mktime
import requests
from country_list import countries_for_language
import pycountry

db = write_data.db

cache_user = {}


def __resolve_link(link):
    return requests.get(link).url


def get_country_list(lang_code):
    ll = db.collection('languages').document('languages').get().to_dict()[lang_code] if lang_code != 'en' else \
        db.collection('languages').document('popular').get().to_dict()['en']
    countries_for_lang = dict(countries_for_language(lang_code))
    return [{'code': l1, 'name': countries_for_lang[l1]} for l1 in ll]


def start_user(user, chat_id):
    uuser = {'name': user.first_name, 'language': user.language_code if user.language_code else 'en',
             'username': user.username}
    db.collection('users').document(str(chat_id)).set(uuser, merge=True)
    try:
        return pycountry.languages.get(alpha_2=user.language_code if user.language_code else 'en')
    except LookupError:
        return []


def update_user(chat_id, content):
    db.collection('users').document(str(chat_id)).set(content, merge=True)
    get_user(chat_id, True)
    return 'OK'


def get_user(chat_id, refresh=False):
    cc_id = chat_id if type(chat_id) is str else str(chat_id)

    if refresh or cache_user.get(cc_id) is None:
        cache_user[cc_id] = db.collection('users').document(cc_id).get().to_dict()

    return cache_user[cc_id]


def get_categories(chat_id):
    return db.collection('feeds').document('categories').get().to_dict()['categories']


def needs_new_feed(chat_id):
    user = get_user(chat_id)
    countries = db.collection('feeds').document('countries').get().to_dict()

    if user:
        return (
            user['language'] not in countries['lang'] or user['country'] not in countries['countries'],
            user['language'],
            user['country'])
    else:
        return None, None, None


def write_generic_feeds(lang, country):
    countries = db.collection('feeds').document('countries').get().to_dict()
    write_data.write_generic_feeds(lang, country)
    if lang not in countries['lang']: countries['lang'].append(lang)
    if country not in countries['countries']: countries['countries'].append(country)
    db.collection('feeds').document('countries').set(countries, merge=True)
    return True


def __get_generic_feed(category, lang):
    feeds = db.collection('feeds').document('generic').collection().where('category', '==', category)
    return [f"{feed.to_dict['link']}hl={lang}" for feed in feeds]


def __get_feeds(category, lang, country):
    feeds = db.collection('feeds').where('category', '==', category) \
        .where('language', '==', lang) \
        .where('country', '==', country).stream()
    return [feed.to_dict['link'] for feed in feeds]


def get_articles(chat_id, category, lang, country):
    feeds = __get_feeds(category, lang, country) if country else __get_generic_feed(category, lang)

    list_of_articles = []

    for feed in feeds:
        ll = feedparser.parse(feed)
        list_of_articles.extend(
            [{'id': entry['id'], 'title': entry['title'], 'link': entry['link'],
              'timestamp_parsed': entry['published_parsed']} for entry in ll['entries']]
        )

    list_of_articles.sort(key=lambda el: datetime.fromtimestamp(mktime(el['timestamp_parsed'])), reverse=True)
    print(len(list_of_articles))

    for index, element in enumerate(list_of_articles[:30]):
        db.collection('live_search').document(str(chat_id)).collection('articles').document(str(index)).set(element,
                                                                                                            merge=True)
    return True


def get_article(chat_id, article_id):
    art_doc = db.collection('live_search').document(str(chat_id)).collection('articles').document(
        article_id).get()

    art = art_doc.to_dict()
    if art is None:
        db.collection('live_search').document(str(chat_id)).delete()
    #  message_subject.on_next(HooNewsMessage('VALUE', (chat_id, None)))
    else:
        art_doc.reference.delete()
        try:
            if 'news.google' in art['link']:
                art['link'] = __resolve_link(art['link'])
        except:
            pass
        #  message_subject.on_next(HooNewsMessage('VALUE', (chat_id, art, str(int(article_id) + 1))))
    return art


if __name__ == '__main__':
    print(pycountry.languages.get(alpha_2='en'))


def get_popular_languages(language_code):
    list_of_langs = db.collection('languages').document('popular').get().to_dict()['languages']
    if language_code not in list_of_langs:
        list_of_langs.append(language_code)

    return [(pycountry.languages.get(alpha_2=lang), lang) for lang in list_of_langs]
