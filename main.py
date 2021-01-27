import telebot
import secrets
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import hoonewsbot
from flask import Flask, request
import os


bot = telebot.TeleBot(secrets.BOT_TOKEN)
server = Flask(__name__)




@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    print(message)
    bot.reply_to(message, """\
Hi welcome to HooBotNews.
type /read to choose the category
type /donate to help me
type /info to get info about the bot
type /help to read this message once again
""")


@bot.message_handler(commands=['donate'])
def send_welcome(message):
    print(message)
    bot.reply_to(message, """\
Hi welcome to HooBotNews.
If you want to help me, buy me a coffee here

https://paypal.me/AngeloMoroni?locale.x=en_US
""")


@bot.message_handler(commands=['info'])
def send_welcome(message):
    print(message)
    bot.reply_to(message, """\
Hi welcome to HooBotNews.
This bot let you read news without leaving cookies around the web.
I suggest you to use a free-cookie browser if Telegram can't open a link by itself.
Eg. Firefox Focus.

You can help me buying me a coffee (type /donate for more info) and I will improve bot features.
Enjoy your reading.
""")


def gen_markup(chat_id, lang):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for cat in hoonewsbot.get_categories(lang):
        markup.add(InlineKeyboardButton(cat[0], callback_data=f"{cat[1]}:{chat_id}"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call)
    data = call.data.split(':')
    bot.send_message(data[1], "Attendere...")
    hoonewsbot.list_of_news(data[0], call.from_user.language_code).subscribe(
        lambda value: bot.send_message(data[1], value)
    )


@bot.message_handler(commands=['read'])
def read(message):
    print(message)
    bot.reply_to(message, 'Choose Category',
                 reply_markup=gen_markup(message.chat.id, message.from_user.language_code))


@server.route('/' + secrets.BOT_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=secrets.HEROKU_URL + secrets.BOT_TOKEN)
    return "!", 200


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

