texts = {'it': {
    'UPDATE_COUNTRY': 'Dove vivi?',
    'CATEGORIES_CHOOSE': 'Cosa vuoi leggere?',
    'GENERIC_LOADING': 'Attendere...',
    'NEW_FEEDS_LOADING': 'Caricamento nuovi feed...',
    'NEWS_LOADING': 'Caricamento nuove notizie...',
    'NEXT': 'Prossima notizia',
    'READ_ALL': 'Sei arrivato alla fine!',
    'ERROR_COUNTRY': 'Ops, non so dove vivi, mi serve saperlo per personalizzare la tua ricerca.',
    'WELCOME_MESSAGE': 'Ciao, benvenuto su HooNewsBot!',
    'GENERIC_SET_LANGUAGE': 'Tell me your tongue:',
    'DEFAULT_LANGUAGE_INFO': 'La lingua impostata è {}. Puoi cambiarla scrivendo /setlanguage o /read per iniziare a leggere le notizie',
    'START_MESSAGE': """\
    Perfetto, grazie! Adesso puoi leggere le notizie.
    scrivi /read per cominciare
    o /help per avere aiuto
    """,
    'DONATE_MESSAGE': """\
            Ciao, se vuoi aiutarmi pagami un caffè o una birra!
            Ne sarei contento!

            https://paypal.me/AngeloMoroni?locale.x=en_US
            """,
    'HELP_MESSAGE': """\
            Ciao Benvenuto/a! Questo è HooNewsBot.
            Un Feed di notizie senza preoccuaprsi di Cookie.
            scrivi /read per scegliere la categoria da leggere
            scrivi /donate per sostenere questo progetto
            scrivi /info per ottenere info su questo progetto
            scrivi /help per leggere di nuovo questo messaggio
            """,
    'CATEGORIES': {
        'world': 'Mondo',
        'business': 'Business',
        'technology': 'Tech',
        'entertainment': 'Intrattenimento',
        'sports': 'Sport',
        'science': 'Scienza',
        'health': 'Salute',
        'general': 'Top Notizie'
    }
},
    'en': {
        'UPDATE_COUNTRY': 'Where do you live?',
        'CATEGORIES_CHOOSE': 'What do you want to read?',
        'GENERIC_LOADING': 'Waiting...',
        'NEW_FEEDS_LOADING': 'New feeds loading...',
        'NEWS_LOADING': 'News loading...',
        'NEXT': 'Next',
        'READ_ALL': 'You read all!',
        'ERROR_COUNTRY': 'Ops, I don\'y know where do you live. I need to know to fit the feed',
        'WELCOME_MESSAGE': 'Hi,wellcome to HooNewsBot!',
        'GENERIC_SET_LANGUAGE': 'Tell me your tongue:',
        'DEFAULT_LANGUAGE_INFO': 'Default language is {}. You can change typing /setlanguage \n Type /read to start reading',
        'START_MESSAGE': """
        Oh, Thank you! Now you can start reading news.
        type /read to choose the category
        or /help to get help
        """,
        'DONATE_MESSAGE': """\
            If you want to help me, buy me a coffee here
            
            https://paypal.me/AngeloMoroni?locale.x=en_US
            """,
        'HELP_MESSAGE': """\
            Hi welcome to HooBotNews.
            You can read news without worrying about leaving cookies.
            type /read to choose the category
            type /donate to help me
            type /info to get info about the bot
            type /help to read this message once again
            """,
        'CATEGORIES': {
            'world': 'World',
            'business': 'Business',
            'technology': 'Tech',
            'entertainment': 'Entertainment',
            'sports': 'Sports',
            'science': 'Science',
            'health': 'Health',
            'general': 'Top News'
        }
    }}


def get_string(lang_code, string_id):
    str_dict = texts[lang_code] if lang_code in texts else texts['en']
    return str_dict[string_id]
