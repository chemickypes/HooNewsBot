import repo
from rx.subject import Subject
from models import HooNewsMessage

message_subject = Subject()


def register_user(user, chat_id):
    list1 = repo.start_user(user, chat_id)
    message_subject.on_next(HooNewsMessage(chat_id, 'INKEY', list1))


def update_user_county(chat_id, country):
    response = repo.update_user(chat_id, {'country': country})
    if response:
        message_subject.on_next(HooNewsMessage(chat_id, 'UPDATE', 'OK'))


def get_categories(chat_id, lang):
    message_subject.on_next(HooNewsMessage(chat_id, 'INKEY', repo.get_categories(chat_id)))


def get_article(chat_id, article_id):
    art = repo.get_article(chat_id, article_id)
    message_subject.on_next(HooNewsMessage(chat_id, 'ITEM', (art, str(int(article_id) + 1))))


def make_search(chat_id, category):
    need_new_feeds, lang, country = repo.needs_new_feed(chat_id)
    if need_new_feeds:
        message_subject.on_next(HooNewsMessage(chat_id, 'ALERT', 'FEEDS_LOADING'))
        repo.write_generic_feeds(lang, country)

    message_subject.on_next(HooNewsMessage(chat_id, 'LOADING',  'NEWS_LOADING'))
    repo.get_articles(chat_id, category, lang, country)
    art = repo.get_article(chat_id, "0")
    message_subject.on_next(HooNewsMessage(chat_id, 'ITEM', (art, '1')))
