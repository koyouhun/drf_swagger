import six


def get_prefix(path):
    """
    Extract prefixes from paths.
    For example,
    paths: [/api/hello/world/{id}, /api/hello/{id}/world/{id}...]
    prefix: [/api/hello/world/, /api/hello/...]
    """
    if isinstance(path, six.string_types):
        return _get_prefix([path])[0]
    else:
        return _get_prefix(path)


def _get_prefix(paths):
    prefix = list()
    for path in paths:
        split_paths = path.strip('/').split('/')
        raw_prefixes = list()
        for split_path in split_paths:
            if split_path.startswith('{'):
                break
            raw_prefixes.append(split_path)
        prefix.append('/' + '/'.join(raw_prefixes))
    return prefix


def get_common_path(paths):
    """
    Find common path.
    For example, [/api/test, /api/hello] => /api

    :param paths: list of path
    :return: string of common path
    """
    if len(paths) == 0:
        return '/'
    mini_paths = [path.strip('/').split('/') for path in paths]
    common_mini_paths = min(mini_paths)
    common_path = []
    for common_mini_path in common_mini_paths:
        check_path = '/'.join(common_path) + common_mini_path
        exist_flag = True
        for path in paths:
            if not path.strip('/').startswith(check_path):
                exist_flag = False
                break
        if exist_flag:
            common_path.append(common_mini_path)
        else:
            break
    return '/' + '/'.join(common_path)