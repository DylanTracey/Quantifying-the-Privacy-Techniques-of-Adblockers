import random
import datetime

AVAILABLE_CHARACTERS = '0123456789'


def generate_uuid(digit_length):
    list = [random.choice(AVAILABLE_CHARACTERS) for n in range(digit_length)]
    uuid = ''.join(list)
    return uuid


def append_cookie(response, uuid):
    expire_date = datetime.datetime.now() + datetime.timedelta(days=100)
    response.set_cookie('id', uuid, expires=expire_date)
    return response


def append_cookies(response, basename, uuid):
    for i in range(len(uuid)):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=100)
        name = '{basename}{index}'.format(basename=basename, index=str(i))
        value = uuid[i]
        response.set_cookie(name, value, expires=expire_date)
    return response


def get_cookie(request):
    cookie = request.cookies.get('id')
    return cookie


def get_uuid_from_cookies(request, basename, length):
    uuid = ''
    for i in range(length):
        cookie = request.cookies.get(basename + str(i))
        if cookie is None:
            return None
        uuid += request.cookies.get(basename + str(i))
    else:
        return uuid
