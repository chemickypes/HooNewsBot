texts = {'it': {
    'UPDATE_COUNTRY': 'Dove vivi?'
},
    'en': {
        'UPDATE_COUNTRY': 'Where do you live?'
    }}


def get_string(lang_code, string_id):
    str_dict = texts[lang_code] if lang_code in texts else texts['en']
    return str_dict[string_id]
