import telebot
import secrets
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import hoonewsbot

bot = telebot.TeleBot(secrets.BOT_TOKEN)


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
This bot let you read news without leave cookies around the web.
I suggest you tu use a free-cookie browser if Telegram can't open a link by itself.
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


def start_polling():
    # Use a breakpoint in the code line below to debug your script.
    bot.polling()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_polling()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
