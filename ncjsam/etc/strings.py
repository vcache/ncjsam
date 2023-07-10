def normalize_string(input):
    SAFE = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_'

    def transform_char(x):
        return x if x in SAFE else '_'

    result = ''.join([transform_char(i) for i in input])
    if result and result[0] in '1234567890':
        result = '_' + result
    return result


def name_to_id(name):
    return f'{normalize_string(name).lower()}'


def snake_to_camel(value):
    parts = value.split('_')
    return ''.join(
        parts[:1] + [i.capitalize() for i in parts[1:]]
    )
