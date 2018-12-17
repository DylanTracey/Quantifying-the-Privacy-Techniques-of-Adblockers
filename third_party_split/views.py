import time

from urllib.parse import quote, unquote

from flask import Blueprint
from flask import request, render_template, make_response

from config.models import User
from settings import URLS
from third_party_split.models import SplitTrackableUUID1, SplitTrackableUUID2, \
    SplitTrackableUUID3, SplitTrackableUUID4, SplitHistoryBase1, SplitHistoryBase2, SplitHistoryBase3, \
    SplitHistoryBase4, \
    JoinedTrackableUUID, JoinedHistory
from utils.cookies import append_cookies, get_uuid_from_cookies
from utils.history import log_site_visit, generate_recent_history
from utils.redis_cache import redis_register_split, redis_retrieve_join, redis_set_benchmark_recent_site
from utils.referer import check_referer
from utils.user import implicit_user_login

tps = Blueprint('tps', __name__)

THIRD_PARTY_MASTER_TEMPLATE = 'third_party_split/third_party_master.html'
THIRD_PARTY_SPLIT_TEMPLATE = 'third_party_split/third_party_split.html'
THIRD_PARTY_CHAIN_MASTER_TEMPLATE = 'third_party_split/third_party_chain_master.html'
THIRD_PARTY_SPLIT_CHAIN_TEMPLATE = 'third_party_split/third_party_split_chain.html'


@tps.route('/tp-master/<config_id>/<index>/safe_referer')
def tp_master(config_id, index):
    """
    Iframed master website view which creates a cookie from the four segments and logs the visit for the user
    :param index: which split URL called this master URL
    :return: HTTP response for this master URL website
    """
    check_referer(request, URLS['TP_MASTER_URL'])
    ip = request.remote_addr
    site = unquote(request.args.get('id', None))

    # Doesn't render this history view template until the other segments of the cookie (index 1-3) are loaded.
    if index != '4':
        return render_template(THIRD_PARTY_MASTER_TEMPLATE)

    # Creates a cookie based on the four separate segments concatenated together.
    joined_uuid = redis_retrieve_join(ip, site)
    if joined_uuid is None:
        return render_template(THIRD_PARTY_MASTER_TEMPLATE)

    # Logs the visited site by the joined user (from the separate segments), and generates the history table to display
    # to manual people using the benchmark site
    joined_user = JoinedTrackableUUID.get_or_create(joined_uuid)
    log_site_visit(JoinedHistory, site, joined_user, ip)
    recent_history = generate_recent_history(JoinedHistory, joined_user, 10)
    # Records the recently visited site fot the benchmark
    redis_set_benchmark_recent_site(config_id, '3', site)

    return render_template(THIRD_PARTY_MASTER_TEMPLATE, history_log=recent_history, trackable=True,
                           uuid=joined_uuid)


@tps.route('/tp-split-1/<config_id>')
def tp_split_1(config_id):
    """
    Iframed split third party URL which records the first segment of the cookie (used to identify the user)
    """
    check_referer(request, URLS['TP_SPLIT_URL_1'])

    # Ensures the cookie is of the right length (based on the configuration)
    config_cookie_length = implicit_user_login(User, config_id).split_cookie_size

    # Gets what the third party perceives to be a first segment of the user (based on the cookie segment it sets)
    uuid = get_uuid_from_cookies(request, 'id', config_cookie_length)
    trackable_uuid_1 = SplitTrackableUUID1.get_or_create(uuid, config_cookie_length)

    # Logs the site visited for this segment
    log_site_visit(SplitHistoryBase1, request.referrer, trackable_uuid_1, request.remote_addr)
    redis_register_split('1', request.remote_addr, trackable_uuid_1.uuid, request.referrer)

    # Make a URL safe encoding of the site visited
    safe_referer = quote(request.referrer)

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_TEMPLATE, current_url=request.url_root, urls=URLS, cookie_id=uuid,
                        safe_referer=safe_referer, index=1, config_id=config_id))
    # Sets a cookie for this segment if not done before
    if uuid is None:
        response = append_cookies(response, 'id', trackable_uuid_1.uuid)
    return response


@tps.route('/tp-split-2/<config_id>')
def tp_split_2(config_id):
    """
    Iframed split third party URL which records the second segment of the cookie (used to identify the user)
    Functions similar to tp_split_1 above.
    """
    check_referer(request, URLS['TP_SPLIT_URL_2'])
    config_cookie_length = implicit_user_login(User, config_id).split_cookie_size

    time.sleep(0.4)

    uuid = get_uuid_from_cookies(request, 'id', config_cookie_length)
    trackable_uuid_2 = SplitTrackableUUID2.get_or_create(uuid, config_cookie_length)

    log_site_visit(SplitHistoryBase2, request.referrer, trackable_uuid_2, request.remote_addr)
    redis_register_split('2', request.remote_addr, trackable_uuid_2.uuid, request.referrer)

    safe_referer = quote(request.referrer)

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_TEMPLATE, current_url=request.url_root, urls=URLS, cookie_id=uuid,
                        safe_referer=safe_referer, index=2, config_id=config_id))
    if uuid is None:
        response = append_cookies(response, 'id', trackable_uuid_2.uuid)
    return response


@tps.route('/tp-split-3/<config_id>')
def tp_split_3(config_id):
    """
    Iframed split third party URL which records the third segment of the cookie (used to identify the user)
    Functions similar to tp_split_1 above.
    """
    check_referer(request, URLS['TP_SPLIT_URL_3'])
    config_cookie_length = implicit_user_login(User, config_id).split_cookie_size

    time.sleep(0.8)

    uuid = get_uuid_from_cookies(request, 'id', config_cookie_length)
    trackable_uuid_3 = SplitTrackableUUID3.get_or_create(uuid, config_cookie_length)

    log_site_visit(SplitHistoryBase3, request.referrer, trackable_uuid_3, request.remote_addr)
    redis_register_split('3', request.remote_addr, trackable_uuid_3.uuid, request.referrer)

    safe_referer = quote(request.referrer)

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_TEMPLATE, current_url=request.url_root, urls=URLS, cookie_id=uuid,
                        safe_referer=safe_referer, index=3, config_id=config_id))
    if uuid is None:
        response = append_cookies(response, 'id', trackable_uuid_3.uuid)
    return response


@tps.route('/tp-split-4/<config_id>')
def tp_split_4(config_id):
    """
    Iframed split fourth party URL which records the third segment of the cookie (used to identify the user)
    Functions similar to tp_split_1 above.
    """
    check_referer(request, URLS['TP_SPLIT_URL_4'])
    config_cookie_length = implicit_user_login(User, config_id).split_cookie_size

    time.sleep(1.2)

    uuid = get_uuid_from_cookies(request, 'id', config_cookie_length)
    trackable_uuid_4 = SplitTrackableUUID4.get_or_create(uuid, config_cookie_length)

    log_site_visit(SplitHistoryBase4, request.referrer, trackable_uuid_4, request.remote_addr)
    redis_register_split('4', request.remote_addr, trackable_uuid_4.uuid, request.referrer)

    safe_referer = quote(request.referrer)

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_TEMPLATE, current_url=request.url_root, urls=URLS, cookie_id=uuid,
                        safe_referer=safe_referer, index=4, config_id=config_id))
    if uuid is None:
        response = append_cookies(response, 'id', trackable_uuid_4.uuid)
    return response


@tps.route('/tp-split-chain-1/<config_id>')
def tp_split_chain_1(config_id):
    """
    Iframed chained third party URL which records the first segment of the cookie (used to identify the user)
    Functions similar to tp_split_1 above.
    """
    check_referer(request, URLS['TP_SPLIT_URL_1'])
    config_cookie_length = implicit_user_login(User, config_id).split_cookie_size

    uuid = get_uuid_from_cookies(request, 'id', config_cookie_length)
    trackable_uuid_1 = SplitTrackableUUID1.get_or_create(uuid, config_cookie_length)

    safe_referer = quote(request.referrer)

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_CHAIN_TEMPLATE, current_url=request.url_root, urls=URLS, cookie_id=uuid,
                        safe_referer=safe_referer, index=1, combined_id=uuid, config_id=config_id))
    if uuid is None:
        response = append_cookies(response, 'id', trackable_uuid_1.uuid)
    return response


@tps.route('/tp-split-chain-2', defaults={'cookie_id': 'None'})
@tps.route('/tp-split-chain-2/<config_id>/<cookie_id>/safe_referer')
def tp_split_chain_2(config_id, cookie_id):
    """
    Iframed chained third party URL which records the second segment of the cookie (used to identify the user)
    Functions similar to tp_split_1 above.
    """
    check_referer(request, URLS['TP_SPLIT_URL_2'])
    config_cookie_length = implicit_user_login(User, config_id).split_cookie_size

    uuid = get_uuid_from_cookies(request, 'id', config_cookie_length)
    trackable_uuid_2 = SplitTrackableUUID2.get_or_create(uuid, config_cookie_length)

    # Builds up the cookie by appending the first cookie segment to the second to create a combined string
    if cookie_id != 'None' and uuid is not None:
        cookie_id += uuid

    site = request.args.get('ref', None)

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_CHAIN_TEMPLATE, current_url=request.url_root, urls=URLS, cookie_id=uuid,
                        safe_referer=site, index=2, combined_id=cookie_id, config_id=config_id))
    if uuid is None:
        response = append_cookies(response, 'id', trackable_uuid_2.uuid)
    return response


@tps.route('/tp-split-chain-3', defaults={'cookie_id': 'None'})
@tps.route('/tp-split-chain-3/<config_id>/<cookie_id>/safe_referer')
def tp_split_chain_3(config_id, cookie_id):
    """
    Iframed chained third party URL which records the third segment of the cookie (used to identify the user)
    Functions similar to tp_split_1 above.
    """
    check_referer(request, URLS['TP_SPLIT_URL_3'])
    config_cookie_length = implicit_user_login(User, config_id).split_cookie_size

    uuid = get_uuid_from_cookies(request, 'id', config_cookie_length)
    trackable_uuid_3 = SplitTrackableUUID3.get_or_create(uuid, config_cookie_length)

    # Builds up the cookie by appending the fist and second cookie segments to the third to create a combined string
    if cookie_id != 'None' and uuid is not None:
        cookie_id += uuid

    site = request.args.get('ref', None)

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_CHAIN_TEMPLATE, current_url=request.url_root, urls=URLS, cookie_id=uuid,
                        safe_referer=site, index=3, combined_id=cookie_id, config_id=config_id))
    if uuid is None:
        response = append_cookies(response, 'id', trackable_uuid_3.uuid)
    return response


@tps.route('/tp-split-chain-master', defaults={'cookie_id': 'None'})
@tps.route('/tp-split-chain-master/<config_id>/<cookie_id>/safe_referer')
def tp_split_chain_master(config_id, cookie_id):
    """
    Iframed chained third party URL which records the third segment of the cookie (used to identify the user)
    Functions similar to tp_split_1 above.
    """
    check_referer(request, URLS['TP_SPLIT_URL_4'])
    config_cookie_length = implicit_user_login(User, config_id).split_cookie_size

    uuid = get_uuid_from_cookies(request, 'id', config_cookie_length)
    trackable_uuid_4 = SplitTrackableUUID4.get_or_create(uuid, config_cookie_length)

    trackable = False

    site = unquote(request.args.get('ref', None))

    # Builds up the completed cookie by appending the fist, second and third cookie segments to the fourth to create a
    # unique identifier
    if cookie_id != 'None' and uuid is not None:
        cookie_id += uuid
        trackable = True
        redis_set_benchmark_recent_site(config_id, '4', site)

    # Records the site visited by what the third party perceives as the unique user (from the combined string)
    joined_user = JoinedTrackableUUID.get_or_create(cookie_id)
    log_site_visit(JoinedHistory, site, joined_user, request.referrer)
    recent_history = generate_recent_history(JoinedHistory, joined_user, 10)

    response = make_response(
        render_template(THIRD_PARTY_CHAIN_MASTER_TEMPLATE, current_url=request.url_root, urls=URLS, cookie_id=uuid,
                        history_log=recent_history, index=4, combined_id=cookie_id, trackable=trackable,
                        config_id=config_id))
    # Sets a cookie for this combined string which identifies a user if not done before
    if uuid is None:
        response = append_cookies(response, 'id', trackable_uuid_4.uuid)
    return response
