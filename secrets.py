BOT_TOKEN = '1639276073:AAH1adwjgnPiREAYCX7iW10V5cNvRpCnr84'
DEBUG_BOT_TOKEN = '1648537217:AAHLsKxDtC2qZ_GVgBUmJjVH35JjIRZcqtE'
HEROKU_URL = 'https://hoonewsbot.herokuapp.com/'


def get_token(debug):
    return DEBUG_BOT_TOKEN if debug else BOT_TOKEN
