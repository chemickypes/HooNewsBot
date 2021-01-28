import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

cred = credentials.Certificate("hoonewsbot-firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

cache_live_search = {}


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
