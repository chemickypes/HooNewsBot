import telebot
import secrets
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import hoonewsbot
from flask import Flask, request
import os

DEBUG = False

bot = telebot.TeleBot(secrets.get_token(DEBUG))
server = Flask(__name__)


def gen_markup(chat_id, callback_tag, answer_list):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for cat in answer_list:
        markup.add(InlineKeyboardButton(cat[0], callback_data=f"{callback_tag}:{cat[1]}:{chat_id}"))
    return markup


@bot.message_handler(commands=['help'])
def send_help(message):
    if DEBUG: print(message)
    hoonewsbot.help(message.chat.id, message.from_user.language_code)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if DEBUG: print(message)
    hoonewsbot.start(message)


@bot.message_handler(commands=['donate'])
def send_donate_info(message):
    if DEBUG: print(message)
    hoonewsbot.donate_message(message.chat.id, message.from_user.language_code)


@bot.message_handler(commands=['setlanguage'])
def set_language(message):
    if DEBUG: print(message)
    hoonewsbot.show_list_of_languages(message)


@bot.message_handler(commands=['setcountry'])
def set_language(message):
    if DEBUG: print(message)
    hoonewsbot.show_list_of_countries(message)


@bot.message_handler(commands=['settings'])
def settings(message):
    if DEBUG: print(message)
    hoonewsbot.show_settings(message.chat.id, message.from_user.language_code)


@bot.message_handler(commands=[''])
def category(message):
    if DEBUG: print(message)
    hoonewsbot.get_categories(message.chat.id, message.from_user.language_code)


@bot.message_handler(commands=['read'])
def read(message):
    if DEBUG: print(message)
    hoonewsbot.make_search(message.chat.id, 'general')


@bot.message_handler(commands=['addfeed'])
def add_feed(message):
    if DEBUG: print(message)
    hoonewsbot.start_add_feed(message)


@bot.message_handler(func=lambda message: True)
def handle_generic_message(message):
    if DEBUG: print(message)
    hoonewsbot.handle_generic_message(message)


@bot.callback_query_handler(func=lambda call: 'UPDATE_COUNTRY' in call.data)
def callback_query_update_country(call):
    if DEBUG: print(call)
    data = call.data.split(':')
    hoonewsbot.update_user_county_at_start(data[2], data[1])


@bot.callback_query_handler(func=lambda call: 'SET_LANGUAGE' in call.data)
def callback_query_set_language(call):
    if DEBUG: print(call)
    data = call.data.split(':')
    hoonewsbot.update_user_language(data[2], data[1])


@bot.callback_query_handler(func=lambda call: 'CATEGORIES_CHOOSE' in call.data)
def callback_query_categories(call):
    if DEBUG: print(call)
    data = call.data.split(':')
    hoonewsbot.handle_category_choose(data[2], data[1])


@bot.callback_query_handler(func=lambda call: 'ITEM' in call.data)
def callback_query_item(call):
    if DEBUG: print(call)
    data = call.data.split(':')
    hoonewsbot.get_article(data[2], data[1])


@server.route('/' + secrets.BOT_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=secrets.HEROKU_URL + secrets.BOT_TOKEN)
    return "!", 200


def start_polling():
    bot.polling()


def handle_message(hnm):
    print(hnm)
    if hnm.message_type == 'UPDATE_COUNTRY':
        bot.send_message(hnm.chat_id,
                         hnm.content[0], reply_markup=
                         gen_markup(hnm.chat_id, hnm.content[1], [(ii['name'], ii['code']) for ii in hnm.content[2]]))
    elif hnm.message_type == 'CATEGORIES_CHOOSE':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        for i in range(0, len(hnm.content[2]), 2):
            if i + 1 == len(hnm.content[2]):
                cat = hnm.content[2][i]
                markup.add(InlineKeyboardButton(cat[0], callback_data=f"CATEGORIES_CHOOSE:{cat[1]}:{hnm.chat_id}"))
            else:
                cat = hnm.content[2][i]
                cat1 = hnm.content[2][i + 1]
                markup.add(InlineKeyboardButton(cat[0], callback_data=f"CATEGORIES_CHOOSE:{cat[1]}:{hnm.chat_id}"),
                           InlineKeyboardButton(cat1[0], callback_data=f"CATEGORIES_CHOOSE:{cat1[1]}:{hnm.chat_id}"))
        bot.send_message(hnm.chat_id,
                         hnm.content[0], reply_markup=markup)
    elif hnm.message_type in ['LOADING', 'ITEM_END', 'INFO', 'UPDATE', 'ERROR']:
        bot.send_message(hnm.chat_id, hnm.content)
    elif hnm.message_type == 'ITEM':
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton(hnm.content[2], callback_data=f'ITEM:{hnm.content[1]}:{hnm.chat_id}'))
        bot.send_message(hnm.chat_id,
                         f"{hnm.content[0]['title']}\n{hnm.content[0]['link']}", reply_markup=markup)
    elif hnm.message_type == 'SET_LANGUAGE':
        markup = InlineKeyboardMarkup()
        for lang in hnm.content[1]:
            markup.add(InlineKeyboardButton(lang[0].name, callback_data=f'SET_LANGUAGE:{lang[1]}:{hnm.chat_id}'))
        bot.send_message(hnm.chat_id, hnm.content[0], reply_markup=markup)


hoonewsbot.message_subject.subscribe(handle_message)

if __name__ == '__main__':
    if DEBUG:
        start_polling()
    else:
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
