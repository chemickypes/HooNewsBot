import telebot
import secrets
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import hoonewsbot
from hoonewsbot import categories
import rx

bot = telebot.TeleBot(secrets.BOT_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi you can read news.
type /read to choose the category
""")


def gen_markup(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = len(categories)
    for key, cat in categories.items():
        markup.add(InlineKeyboardButton(cat[0], callback_data=f"{key}:{chat_id}"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split(':')
    bot.send_message(data[1], "Attendere...")
    hoonewsbot.list_of_news(data[0]).subscribe(
        lambda value: bot.send_message(data[1], value)
    )


@bot.message_handler(commands=['read'])
def read(message):
    bot.reply_to(message, 'Choose Category', reply_markup=gen_markup(message.chat.id))


def start_polling():
    # Use a breakpoint in the code line below to debug your script.
    bot.polling()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_polling()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
