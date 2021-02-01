import repo
from rx.subject import Subject
from models import HooNewsMessage
import hoonewsstrings

message_subject = Subject()

user_cache = {}


def register_user(user, chat_id):
    default_language = repo.start_user(user, chat_id)
    message_subject.on_next(HooNewsMessage(chat_id, 'INFO',
                                           hoonewsstrings.get_string(default_language.alpha_2,
                                                                     'DEFAULT_LANGUAGE_INFO').format(
                                               default_language.name
                                           )))


def update_user_county_at_start(chat_id, country):
    response = repo.update_user(chat_id, {'country': country.lower()})
    user = repo.get_user(chat_id)
    if response:
        message_subject.on_next(HooNewsMessage(chat_id, 'UPDATE',
                                               hoonewsstrings.get_string(user['language'], 'START_MESSAGE')))


def update_user_language(chat_id, language):
    response = repo.update_user(chat_id, {'language': language})
    if response:
        message_subject.on_next(HooNewsMessage(chat_id, 'INFO',
                                               hoonewsstrings.get_string(language, 'SETTINGS_UPDATED')))


def show_list_of_languages(message):
    list_of_langs = repo.get_popular_languages()
    message_subject.on_next(HooNewsMessage(message.chat.id, 'SET_LANGUAGE',
                                           (hoonewsstrings.get_string(message.from_user.language_code,
                                                                      'CHOOSE_LANG_STRING'), list_of_langs)))


def get_categories(chat_id, lang):
    categories_dict = hoonewsstrings.get_string(lang, 'CATEGORIES')
    message_subject.on_next(HooNewsMessage(chat_id, 'CATEGORIES_CHOOSE',
                                           (hoonewsstrings.get_string(lang, 'CATEGORIES_CHOOSE'),
                                            'CATEGORIES_CHOOSE', [(categories_dict[cat_id], cat_id) for cat_id in
                                                                  repo.get_categories(chat_id)])))


def get_article(chat_id, article_id):
    art = repo.get_article(chat_id, article_id)
    if art:
        message_subject.on_next(HooNewsMessage(chat_id, 'ITEM', (
            art, str(int(article_id) + 1, ), hoonewsstrings.get_string(user_cache[chat_id][0], 'NEXT'))))
    else:
        message_subject.on_next(
            HooNewsMessage(chat_id, 'ITEM_END', hoonewsstrings.get_string(user_cache[chat_id][0], 'READ_ALL')))


def make_search(language_code, chat_id, category):
    need_new_feeds, lang, country = repo.needs_new_feed(chat_id)
    if lang and country:
        user_cache[chat_id] = [lang, country]
        message_subject.on_next(
            (HooNewsMessage(chat_id, 'LOADING', hoonewsstrings.get_string(lang, 'GENERIC_LOADING'))))
        if need_new_feeds:
            message_subject.on_next(
                HooNewsMessage(chat_id, 'LOADING', hoonewsstrings.get_string(lang, 'NEW_FEEDS_LOADING')))
            repo.write_generic_feeds(lang, country)

        message_subject.on_next(HooNewsMessage(chat_id, 'LOADING', hoonewsstrings.get_string(lang, 'NEWS_LOADING')))
        repo.get_articles(chat_id, category, lang, country)
        art = repo.get_article(chat_id, "0")
        message_subject.on_next(
            HooNewsMessage(chat_id, 'ITEM', (art, '1', hoonewsstrings.get_string(user_cache[chat_id][0], 'NEXT'))))
    else:
        country_list = repo.get_country_list(language_code)
        message_subject.on_next(
            HooNewsMessage(chat_id, 'ERROR', hoonewsstrings.get_string(language_code, 'ERROR_COUNTRY')))
        message_subject.on_next(
            HooNewsMessage(chat_id, 'UPDATE_COUNTRY',
                           (
                               hoonewsstrings.get_string(language_code, 'UPDATE_COUNTRY'), 'UPDATE_COUNTRY',
                               country_list)))


def start(message):
    message_subject.on_next(
        HooNewsMessage(message.chat.id, 'INFO', hoonewsstrings.get_string(
            message.from_user.language_code, 'WELCOME_MESSAGE'
        ))
    )
    register_user(message.from_user, message.chat.id)


def help(chat_id, language):
    message_subject.on_next(
        HooNewsMessage(chat_id, 'INFO', hoonewsstrings.get_string(
            language, 'HELP_MESSAGE'
        ))
    )


if __name__ == '__main__':
    message_subject.subscribe(lambda mm: print(mm))
    make_search('it', '33', 'technology')


def donate_message(chat_id, language_code):
    message_subject.on_next(
        HooNewsMessage(chat_id, 'INFO', hoonewsstrings.get_string(
            language_code, 'DONATE_MESSAGE'
        ))
    )
