DATA_TYPE = {
    # Default Value
    'default': ('string', 'string'),

    'string': ('string', 'string'),

    'integer': ('integer', 'int32'),
    'int32': ('integer', 'int32'),

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
    'datetime': ('string', 'date-time'),

    'password': ('string', 'password'),

    'choice': ('choice', 'choice'),
    'hidden': ('hidden', 'hidden'),
    'array': ('array', 'array'),
}