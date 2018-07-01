from urllib.parse import unquote

from flask import Blueprint, make_response, redirect
from flask import request, render_template

from config.models import User
from first_party.models import FirstPartyHistory, FirstPartyUUID, FirstPartyClickHistory
from settings import URLS
from utils.cookies import append_cookie
from utils.history import log_site_visit, generate_recent_history
from utils.redis_cache import redis_set_benchmark_recent_site
from utils.referer import check_referer
from utils.user import implicit_user_login

fp = Blueprint('fp', __name__)

FIRST_PARTY_ONLY_TEMPLATE = 'first_party/first_party_only.html'
FIRST_PARTY_AND_THIRD_PARTY_TEMPLATE = 'first_party/first_party_and_third_party.html'
FIRST_PARTY_AND_THIRD_PARTY_SPLIT_TEMPLATE = 'first_party/first_party_and_third_party_split.html'
FIRST_PARTY_AND_THIRD_PARTY_SPLIT_CHAIN_TEMPLATE = 'first_party/first_party_and_third_party_split_chain.html'
FIRST_PARTY_AND_THIRD_PARTY_SUPER_COOKIE_TEMPLATE = 'first_party/first_party_and_third_party_super_cookie.html'
FIRST_PARTY_MALICIOUS_TEMPLATE = 'first_party/first_party_malicious.html'
FIRST_PARTY_AND_THIRD_PARTY_SPLIT_CHAIN_SUPER_COOKIE_TEMPLATE = 'first_party/first_party_and_third_party_split_chain_super_cookie.html'


def redirect_config():
    return redirect(URLS['CONFIG_URL'], 302)


def config_switch(url, config_id):
    check_referer(request, url + config_id)
    config_user = User.query.filter_by(uuid=config_id).first_or_404()

    fp_uuid = request.cookies.get('id')
    fp_user = implicit_user_login(FirstPartyUUID, fp_uuid, config_user.first_party_cookie_size)
    log_site_visit(FirstPartyHistory, request.url, fp_user, request.remote_addr)
    recent_history = generate_recent_history(FirstPartyHistory, fp_user, 10)
    redis_set_benchmark_recent_site(config_id, '1', request.url)

    if config_user.mode == '1':
        response = make_response(
            render_template(FIRST_PARTY_ONLY_TEMPLATE, urls=URLS, fp_cookie_id=fp_uuid, config_id=config_id,
                            history_log=recent_history))
    elif config_user.mode == '2':
        response = make_response(
            render_template(FIRST_PARTY_AND_THIRD_PARTY_TEMPLATE, urls=URLS, fp_cookie_id=fp_uuid, config_id=config_id))
    elif config_user.mode == '3':
        response = make_response(
            render_template(FIRST_PARTY_AND_THIRD_PARTY_SPLIT_TEMPLATE, urls=URLS, fp_cookie_id=fp_uuid,
                            config_id=config_id))
    elif config_user.mode == '4':
        response = make_response(
            render_template(FIRST_PARTY_AND_THIRD_PARTY_SPLIT_CHAIN_TEMPLATE, urls=URLS, fp_cookie_id=fp_uuid,
                            config_id=config_id))
    elif config_user.mode == '5':
        response = make_response(
            render_template(FIRST_PARTY_AND_THIRD_PARTY_SUPER_COOKIE_TEMPLATE, urls=URLS, fp_cookie_id=fp_uuid,
                            config_id=config_id))
    elif config_user.mode == '6':
        response = make_response(
            render_template(FIRST_PARTY_AND_THIRD_PARTY_SPLIT_CHAIN_SUPER_COOKIE_TEMPLATE, urls=URLS,
                            fp_cookie_id=fp_uuid,
                            config_id=config_id))

    else:
        response = redirect_config()
    if fp_uuid is None:
        response = append_cookie(response, fp_user.uuid)
    return response


@fp.route('/fp-1', defaults={'config_id': None})
@fp.route('/fp-1/<config_id>')
def fp_1(config_id):
    if config_id is None:
        return redirect_config()
    else:
        check_referer(request, URLS['FP_URL_1'] + config_id)
        return config_switch(URLS['FP_URL_1'], config_id)


@fp.route('/fp-2', defaults={'config_id': None})
@fp.route('/fp-2/<config_id>')
def fp_2(config_id):
    if config_id is None:
        return redirect_config()
    else:
        check_referer(request, URLS['FP_URL_2'] + config_id)
        return config_switch(URLS['FP_URL_2'], config_id)


@fp.route('/fp-3', defaults={'config_id': None})
@fp.route('/fp-3/<config_id>')
def fp_3(config_id):
    if config_id is None:
        return redirect_config()
    else:
        check_referer(request, URLS['FP_URL_3'] + config_id)
        return config_switch(URLS['FP_URL_3'], config_id)


def generate_record_url(fp_malicious_base_url):
    if fp_malicious_base_url == URLS['FP_URL_MALICIOUS_1']:
        return fp_malicious_base_url + 'fp-malicious-1-record/'
    elif fp_malicious_base_url == URLS['FP_URL_MALICIOUS_2']:
        return fp_malicious_base_url + 'fp-malicious-2-record/'
    elif fp_malicious_base_url == URLS['FP_URL_MALICIOUS_3']:
        return fp_malicious_base_url + 'fp-malicious-3-record/'
    else:
        return None


def fp_malicious(url, config_id):
    config_user = User.query.filter_by(uuid=config_id).first_or_404()
    fp_uuid = request.cookies.get('id')
    fp_user = implicit_user_login(FirstPartyUUID, fp_uuid, config_user.first_party_cookie_size)

    url_fp1 = URLS['FP_URL_1'] + 'fp-1/' + config_id
    url_fp2 = URLS['FP_URL_2'] + 'fp-2/' + config_id
    url_fp3 = URLS['FP_URL_3'] + 'fp-3/' + config_id

    url_malicious = generate_record_url(url)

    recent_history = generate_recent_history(FirstPartyClickHistory, fp_user, 10)

    response = make_response(
        render_template(FIRST_PARTY_MALICIOUS_TEMPLATE, urls=URLS, fp_cookie_id=fp_uuid, config_id=config_id,
                        url_fp1=url_fp1, url_fp2=url_fp2, url_fp3=url_fp3, url_malicious=url_malicious,
                        history_log=recent_history))

    if fp_uuid is None:
        response = append_cookie(response, fp_user.uuid)
    return response


@fp.route('/fp-malicious-1', defaults={'config_id': None})
@fp.route('/fp-malicious-1/<config_id>')
def fp_malicious_1(config_id):
    if config_id is None:
        return redirect_config()
    else:
        check_referer(request, URLS['FP_URL_MALICIOUS_1'] + config_id)
        return fp_malicious(URLS['FP_URL_MALICIOUS_1'], config_id)


@fp.route('/fp-malicious-2', defaults={'config_id': None})
@fp.route('/fp-malicious-2/<config_id>')
def fp_malicious_2(config_id):
    if config_id is None:
        return redirect_config()
    else:
        check_referer(request, URLS['FP_URL_MALICIOUS_2'] + config_id)
        return fp_malicious(URLS['FP_URL_MALICIOUS_2'], config_id)


@fp.route('/fp-malicious-3', defaults={'config_id': None})
@fp.route('/fp-malicious-3/<config_id>')
def fp_malicious_3(config_id):
    if config_id is None:
        return redirect_config()
    else:
        check_referer(request, URLS['FP_URL_MALICIOUS_3'] + config_id)
        return fp_malicious(URLS['FP_URL_MALICIOUS_3'], config_id)


def fp_malicious_record(config_id):
    config_user = User.query.filter_by(uuid=config_id).first_or_404()
    fp_uuid = request.cookies.get('id')
    fp_user = implicit_user_login(FirstPartyUUID, fp_uuid, config_user.first_party_cookie_size)

    site = unquote(request.args.get('id', None))

    log_site_visit(FirstPartyClickHistory, site, fp_user, request.remote_addr)

    return redirect(site)


@fp.route('/fp-malicious-1-record/<config_id>/u')
def fp_malicious_1_record(config_id):
    check_referer(request, URLS['FP_URL_MALICIOUS_1'] + config_id)
    return fp_malicious_record(config_id)


@fp.route('/fp-malicious-2-record/<config_id>/u')
def fp_malicious_2_record(config_id):
    check_referer(request, URLS['FP_URL_MALICIOUS_2'] + config_id)
    return fp_malicious_record(config_id)


@fp.route('/fp-malicious-3-record/<config_id>/u')
def fp_malicious_3_record(config_id):
    check_referer(request, URLS['FP_URL_MALICIOUS_3'] + config_id)
    return fp_malicious_record(config_id)
