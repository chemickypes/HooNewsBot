import repo
from rx.subject import Subject
from models import HooNewsMessage
import hoonewsstrings

message_subject = Subject()


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
                                               hoonewsstrings.get_string(user['language'], 'SETTINGS_UPDATED')))


def update_user_language(chat_id, language):
    response = repo.update_user(chat_id, {'language': language})
    if response:
        message_subject.on_next(HooNewsMessage(chat_id, 'INFO',
                                               hoonewsstrings.get_string(language, 'SETTINGS_UPDATED')))


def show_list_of_languages(message):
    list_of_langs = repo.get_popular_languages(message.from_user.language_code)
    message_subject.on_next(HooNewsMessage(message.chat.id, 'SET_LANGUAGE',
                                           (hoonewsstrings.get_string(message.from_user.language_code,
                                                                      'CHOOSE_LANG_STRING'), list_of_langs)))


def show_list_of_countries(message):
    country_list = repo.get_country_list(message.from_user.language_code)
    user = repo.get_user(str(message.chat.id))
    if country_list:
        message_subject.on_next(
            HooNewsMessage(message.chat.id, 'UPDATE_COUNTRY',
                           (hoonewsstrings.get_string(user['language'], 'UPDATE_COUNTRY'), 'UPDATE_COUNTRY',
                            country_list)))


def get_categories(chat_id, lang):
    categories_dict = hoonewsstrings.get_string(lang, 'CATEGORIES')
    message_subject.on_next(HooNewsMessage(chat_id, 'CATEGORIES_CHOOSE',
                                           (hoonewsstrings.get_string(lang, 'CATEGORIES_CHOOSE'),
                                            'CATEGORIES_CHOOSE', [(categories_dict[cat_id], cat_id) for cat_id in
                                                                  repo.get_categories(chat_id)])))


def get_article(chat_id, article_id):
    art = repo.get_article(chat_id, article_id)
    user = repo.get_user(chat_id)
    if art:
        message_subject.on_next(HooNewsMessage(chat_id, 'ITEM', (
            art, str(int(article_id) + 1, ), hoonewsstrings.get_string(user['language'], 'NEXT'))))
    else:
        message_subject.on_next(
            HooNewsMessage(chat_id, 'ITEM_END', hoonewsstrings.get_string(user['language'], 'READ_ALL')))


def make_search(chat_id, category):
    user = repo.get_user(chat_id)

    message_subject.on_next(
        (HooNewsMessage(chat_id, 'LOADING', hoonewsstrings.get_string(user['language'], 'GENERIC_LOADING'))))

    message_subject.on_next(
        HooNewsMessage(chat_id, 'LOADING', hoonewsstrings.get_string(user['language'], 'NEWS_LOADING')))
    repo.get_articles(chat_id, category, user['language'], user.get('country'))
    art = repo.get_article(chat_id, "0")
    message_subject.on_next(
        HooNewsMessage(chat_id, 'ITEM', (art, '1', hoonewsstrings.get_string(user['language'], 'NEXT'))))


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
    make_search('33', 'technology')


def donate_message(chat_id, language_code):
    message_subject.on_next(
        HooNewsMessage(chat_id, 'INFO', hoonewsstrings.get_string(
            language_code, 'DONATE_MESSAGE'
        ))
    )


def show_settings(chat_id, language_code):
    message_subject.on_next(
        HooNewsMessage(chat_id, 'INFO', hoonewsstrings.get_string(
            language_code, 'SETTINGS_MESSAGE'
        ))
    )