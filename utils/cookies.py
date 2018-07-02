import random
import datetime

AVAILABLE_CHARACTERS = '0123456789'


def generate_uuid(digit_length):
    """
    Generates a unique user identifier string based on the number of digits and available characters above. Each
    character has equal chance of being picked per digit.
    """
    list = [random.choice(AVAILABLE_CHARACTERS) for n in range(digit_length)]
    uuid = ''.join(list)
    return uuid


def append_cookie(response, uuid):
    """
    Appends a cookie unique user identifier string onto the HTTP response.
    """
    expire_date = datetime.datetime.now() + datetime.timedelta(days=100)
    response.set_cookie('id', uuid, expires=expire_date)
    return response


def append_cookies(response, basename, uuid):
    """
    Appends cookies split between separate cookie name, value pairs.
    """
    for i in range(len(uuid)):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=100)
        name = '{basename}{index}'.format(basename=basename, index=str(i))
        value = uuid[i]
        response.set_cookie(name, value, expires=expire_date)
    return response


def get_cookie(request):
    """
    Gets a cookies unique user identifier string.
    """
    cookie = request.cookies.get('id')
    return cookie


def get_uuid_from_cookies(request, basename, length):
    """
    Gets cookies split between separate cookie name, value pairs. Combines them into a single unique user identifier
    string.
    """
    uuid = ''
    for i in range(length):
        cookie = request.cookies.get(basename + str(i))
        if cookie is None:
            return None
        uuid += request.cookies.get(basename + str(i))
    else:
        return uuid
