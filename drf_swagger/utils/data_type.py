import six


DATA_TYPE = {
    # Default Value
    'default': ('string', 'string'),

    'string': ('string', 'string'),

    'int': ('integer', 'int32'),
    'int32': ('integer', 'int32'),
    'integer': ('integer', 'int32'),

    'long': ('integer', 'int64'),
    'int64': ('integer', 'int64'),

    'float': ('number', 'float'),
    'number': ('number', 'float'),

    'double': ('number', 'double'),

    'byte': ('string', 'byte'),

    'binary': ('string', 'binary'),

    'boolean': ('boolean', 'boolean'),

    'date': ('string', 'date'),

    'dateTime': ('string', 'date-time'),
    'date-time': ('string', 'date-time'),
    'date_time': ('string', 'date-time'),
    'datetime': ('string', 'date-time'),

    'password': ('string', 'password'),

    'choice': ('choice', 'choice'),
    'hidden': ('hidden', 'hidden'),
    'array': ('array', 'array'),
}


def get_type_format(name):
    return DATA_TYPE.get(name, DATA_TYPE['default'])


def str_to_type(orig_str, data_type):
    if not isinstance(orig_str, six.string_types):
        return orig_str

    try:
        if data_type == 'integer':
            return int(orig_str)
        elif data_type == 'number':
            return float(orig_str)
        elif data_type == 'boolean':
            return not (orig_str.lower() in ["false", "f", "no", "0"])
        else:
            return orig_str
    except ValueError:
        return None
