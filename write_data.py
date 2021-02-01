import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

rss_url_struct = "https://news.google.com/news/rss/headlines/section/topic/{}?{}"
general_rss_structure = "https://news.google.com/news/rss/?{}"

rss_url_struct_1 = "https://news.google.com/news/rss/headlines/section/topic/{}?"
general_rss_structure_1 = "https://news.google.com/news/rss/?"

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


def write_generic_feeds_without_country():
    for i, cat in categories.items():
        db.collection('feeds').document().set({
            'link': rss_url_struct_1.format(categories[i]) if i != '8' else general_rss_structure_1,
            'category': cat.lower(),
            'lang_param': 'hl={}',
            'country_param': 'gl={}'
        }, merge=True)


def delete_mine_live_search():
    pass


def delete_all_feeds():
    for doc in db.collection('feeds').stream():
        doc.reference.delete()
    for doc in db.collection('feeds').document('generic').collection('feeds').stream():
        doc.reference.delete()
    db.collection('feeds').document('generic').delete()


if __name__ == '__main__':
    db.collection('feeds').document('categories').set({
        'categories': [cat.lower() for i, cat in categories.items()]})
