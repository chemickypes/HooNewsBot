texts = {'it': {
    'UPDATE_COUNTRY': 'Dove vivi?',
    'CATEGORIES_CHOOSE': 'Cosa vuoi leggere?'
},
    'en': {
        'UPDATE_COUNTRY': 'Where do you live?',
        'CATEGORIES_CHOOSE': 'What do you want to read?'
    }}


def get_string(lang_code, string_id):
    str_dict = texts[lang_code] if lang_code in texts else texts['en']
    return str_dict[string_id]
