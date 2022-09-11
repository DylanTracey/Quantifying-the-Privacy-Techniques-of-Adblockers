import os
import redis


# CONSTANTS

DEBUG = os.environ['APPLICATION_CONFIGURATION'] == 'app_config.DevConfig'

# Uses the correct Redis cache depending on whether it is used on a debugging local environment, or the live website
r = redis.from_url(os.environ.get("REDIS_URL")) if DEBUG is False else redis.Redis('localhost')

# Sets up the correct URLs to use based on a debugging local environment, or the live website
URLS = {
    'FP_URL_1': 'http://adblocktester1.tk/' if DEBUG is False else 'http://local.adblocktester1:5000/',
    'FP_URL_2': 'http://adblocktester2.tk/' if DEBUG is False else 'http://local.adblocktester2:5000/',
    'FP_URL_3': 'http://adblocktester3.tk/' if DEBUG is False else 'http://local.adblocktester3:5000/',

    'FP_URL_MALICIOUS_1': 'http://adblocktestermalicious1.tk/' if DEBUG is False
    else 'http://local.adblocktestermalicious1:5000/',
    'FP_URL_MALICIOUS_2': 'http://adblocktestermalicious2.tk/' if DEBUG is False
    else 'http://local.adblocktestermalicious2:5000/',
    'FP_URL_MALICIOUS_3': 'http://adblocktestermalicious3.tk/' if DEBUG is False
    else 'http://local.adblocktestermalicious3:5000/',

    'TP_URL': 'http://third-party-tracker-single-cookie.tk/' if DEBUG is False
    else 'http://local.third-party-tracker-single-cookie:5000/',

    'TP_SPLIT_URL_1': 'http://third-party-tracker-split-1.tk/' if DEBUG is False
    else 'http://local.third-party-tracker-split-1:5000/',
    'TP_SPLIT_URL_2': 'http://third-party-tracker-split-2.tk/' if DEBUG is False
    else 'http://local.third-party-tracker-split-2:5000/',
    'TP_SPLIT_URL_3': 'http://third-party-tracker-split-3.tk/' if DEBUG is False
    else 'http://local.third-party-tracker-split-3:5000/',
    'TP_SPLIT_URL_4': 'http://third-party-tracker-split-4.tk/' if DEBUG is False
    else 'http://local.third-party-tracker-split-4:5000/',

    'TP_MASTER_URL': 'http://third-party-tracker-master-join.tk/' if DEBUG is False
    else 'http://local.third-party-tracker-master-join:5000/',

    'TP_SUPER_COOKIE_URL': 'http://third-party-tracker-super-cookie.tk/' if DEBUG is False
    else 'http://local.third-party-tracker-super-cookie:5000/',

    'TP_SPLIT_SUPER_URL_1': 'http://third-party-tracker-split-super-1.tk/' if DEBUG is False
    else 'http://local.third-party-tracker-split-super-1:5000/',
    'TP_SPLIT_SUPER_URL_2': 'http://third-party-tracker-split-super-2.tk/' if DEBUG is False
    else 'http://local.third-party-tracker-split-super-2:5000/',
    'TP_SPLIT_SUPER_URL_3': 'http://third-party-tracker-split-super-3.tk/' if DEBUG is False
    else 'http://local.third-party-tracker-split-super-3:5000/',
    'TP_SPLIT_SUPER_URL_4': 'http://third-party-tracker-split-super-4.tk/' if DEBUG is False
    else 'http://local.third-party-tracker-split-super-4:5000/',

    'CONFIG_URL': 'http://www.adblocktesterconfig.tk/' if DEBUG is False else 'http://local.adblocktesterconfig:5000/'
}

FP_URLS = 'FP_URL_1', 'FP_URL_2', 'FP_URL_3'


TRACKING_MODES = {
    '1': 'first party only',
    '2': 'third party single cookie',
    '3': 'third party split cookies',
    '4': 'third party chained cookies',
    '5': 'third party local storage super cookie',
    '6': 'third party local storage super split cookies',
}
