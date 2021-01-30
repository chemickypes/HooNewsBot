import repo
from rx.subject import Subject
from models import HooNewsMessage
import hoonewsstrings

message_subject = Subject()


def register_user(user, chat_id):
    list1 = repo.start_user(user, chat_id)
    if len(list1) > 0:
        message_subject.on_next(
            HooNewsMessage(chat_id, 'UPDATE_COUNTRY',
                           (hoonewsstrings.get_string(user.language_code, 'UPDATE_COUNTRY'), 'UPDATE_COUNTRY', list1)))


def update_user_county(chat_id, country):
    response = repo.update_user(chat_id, {'country': country.lower()})
    if response:
        message_subject.on_next(HooNewsMessage(chat_id, 'UPDATE', 'OK'))


def get_categories(chat_id, lang):
    categories_dict = hoonewsstrings.get_string(lang, 'CATEGORIES')
    message_subject.on_next(HooNewsMessage(chat_id, 'CATEGORIES_CHOOSE',
                                           (hoonewsstrings.get_string(lang, 'CATEGORIES_CHOOSE'),
                                            'CATEGORIES_CHOOSE', [(categories_dict[cat_id], cat_id) for cat_id in
                                                                  repo.get_categories(chat_id)])))


def get_article(chat_id, article_id):
    art = repo.get_article(chat_id, article_id)
    message_subject.on_next(HooNewsMessage(chat_id, 'ITEM', (art, str(int(article_id) + 1))))


def make_search(chat_id, category):
    need_new_feeds, lang, country = repo.needs_new_feed(chat_id)
    message_subject.on_next((HooNewsMessage(chat_id, 'LOADING', hoonewsstrings.get_string(lang, 'GENERIC_LOADING'))))
    if need_new_feeds:
        message_subject.on_next(
            HooNewsMessage(chat_id, 'LOADING', hoonewsstrings.get_string(lang, 'NEW_FEEDS_LOADING')))
        repo.write_generic_feeds(lang, country)

    message_subject.on_next(HooNewsMessage(chat_id, 'LOADING', hoonewsstrings.get_string(lang, 'NEWS_LOADING')))
    repo.get_articles(chat_id, category, lang, country)
    art = repo.get_article(chat_id, "0")
    message_subject.on_next(HooNewsMessage(chat_id, 'ITEM', (art, '1')))
