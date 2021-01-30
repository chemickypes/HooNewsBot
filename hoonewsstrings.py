texts = {'it': {
    'UPDATE_COUNTRY': 'Dove vivi?',
    'CATEGORIES_CHOOSE': 'Cosa vuoi leggere?',
    'GENERIC_LOADING': 'Attendere...',
    'NEW_FEEDS_LOADING': 'Caricamento nuovi feed...',
    'NEWS_LOADING': 'Caricamento nuove notizie...',
    'NEXT': 'Prossima notizia',
    'READ_ALL': 'Sei arrivato alla fine!',
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
