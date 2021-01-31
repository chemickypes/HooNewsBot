texts = {'it': {
    'UPDATE_COUNTRY': 'Dove vivi?',
    'CATEGORIES_CHOOSE': 'Cosa vuoi leggere?',
    'GENERIC_LOADING': 'Attendere...',
    'NEW_FEEDS_LOADING': 'Caricamento nuovi feed...',
    'NEWS_LOADING': 'Caricamento nuove notizie...',
    'NEXT': 'Prossima notizia',
    'READ_ALL': 'Sei arrivato alla fine!',
    'ERROR_COUNTRY': 'Ops, non so dove vivi, mi serve saperlo per personalizzare la tua ricerca.',
    'WELCOME_MESSAGE': 'Ciao, mi servirebbe giusto un\'informazione per iniziare',
    'START_MESSAGE': """\
    Perfetto, grazie! Adesso puoi leggere le notizie.
    scrivi /read per cominciare
    o /help per avere aiuto
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
        'WELCOME_MESSAGE': 'Hi, I need just one info before starting',
        'START_MESSAGE': """
        Oh, Thank you! Now you can start reading news.
        type /read to choose the category
        or /help to get help
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
