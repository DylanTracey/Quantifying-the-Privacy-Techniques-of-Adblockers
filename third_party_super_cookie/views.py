from urllib.parse import unquote

from flask import Blueprint
from flask import request, render_template, make_response

from config.models import User
from settings import URLS
from third_party.views import THIRD_PARTY_SINGLE_TEMPLATE
from third_party_split.models import JoinedTrackableUUID, JoinedHistory
from utils.history import log_site_visit, generate_recent_history
from utils.redis_cache import redis_set_benchmark_recent_site
from utils.referer import check_referer
from utils.user import implicit_user_login

tp_sc = Blueprint('tp_sc', __name__)

THIRD_PARTY_SUPER_COOKIE_TEMPLATE = 'third_party_super_cookie/third_party_super_cookie.html'
THIRD_PARTY_SPLIT_CHAIN_SUPER_COOKIE_TEMPLATE = 'third_party_super_cookie/third_party_split_chain_super_cookie.html'
THIRD_PARTY_SPLIT_CHAIN_SUPER_COOKIE_DATA_TEMPLATE = 'third_party_super_cookie/third_party_split_chain_super_cookie_data.html'
THIRD_PARTY_CHAIN_MASTER_TEMPLATE = 'third_party_split/third_party_chain_master.html'


@tp_sc.route('/tp-super-cookie-data/<config_id>/<uuid>/safe-referer')
def tp_super_cookie_data(config_id, uuid):
    """
    Iframed website that is redirected into from the function below. This gets the UUID from the URL parameter and
    creates a history log for this UUID.

    :param uuid: Generated client side, this supercookie identifies the user.
    :return: HTTP response which displays the history log for this perceived user
    """
    check_referer(request, URLS['TP_SUPER_COOKIE_URL'])
    trackable_user = JoinedTrackableUUID.get_or_create(uuid)

    site = unquote(request.args.get('id', None))

    log_site_visit(JoinedHistory, site, trackable_user, request.access_route[0])
    redis_set_benchmark_recent_site(config_id, '5', site)

    recent_history = generate_recent_history(JoinedHistory, trackable_user, 10)
    response = make_response(
        render_template(THIRD_PARTY_SINGLE_TEMPLATE, history_log=recent_history, current_url=request.url_root,
                        cookie_id=uuid))
    return response


@tp_sc.route('/tp-super-cookie/<config_id>')
def tp_super_cookie(config_id):
    """
    Iframed website by the first party which in its client side template, generates a super cookie (by localStorage).
    It then redirects to the view function above which records the user with this client side UUID.

    :return: HTTP response which generates a localStorage super cookie if not already set via javascipt (see the
    template) and then redirects to a new URL to transfer this client side cookie to server side.
    """
    check_referer(request, URLS['TP_SUPER_COOKIE_URL'])
    config_cookie_length = implicit_user_login(User, config_id).local_storage_super_cookie_size

    # The site to redirect to.
    next_site = URLS['TP_SUPER_COOKIE_URL'] + 'tp-super-cookie-data/' + config_id

    response = make_response(
        render_template(THIRD_PARTY_SUPER_COOKIE_TEMPLATE, current_url=request.url_root, next_site=next_site,
                        safe_referer=request.referrer, config_cookie_length=config_cookie_length))
    return response

# The functions below combines the chained views in third_party_split package, and the two view functions above to
# user super cookie tracking for segmented chunks as in mode 4.


@tp_sc.route('/tp-split-super-chain-1-data/<config_id>/<uuid>/safe-referer')
def tp_split_super_chain_1_data(config_id, uuid):
    check_referer(request, URLS['TP_SPLIT_SUPER_URL_1'])

    site = unquote(request.args.get('id', None))

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_CHAIN_SUPER_COOKIE_DATA_TEMPLATE, current_url=request.url_root, urls=URLS,
                        cookie_id=uuid,
                        safe_referer=site, index=1, combined_id=uuid, config_id=config_id))
    return response


@tp_sc.route('/tp-split-super-chain-1/<config_id>')
def tp_split_super_chain_1(config_id):
    check_referer(request, URLS['TP_SPLIT_SUPER_URL_1'])
    config_cookie_length = implicit_user_login(User, config_id).local_storage_split_super_cookie_size

    next_site = URLS['TP_SPLIT_SUPER_URL_1'] + 'tp-split-super-chain-1-data/' + config_id

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_CHAIN_SUPER_COOKIE_TEMPLATE, current_url=request.url_root,
                        next_site=next_site,
                        safe_referer=request.referrer, config_cookie_length=config_cookie_length, combined_id=""))
    return response


@tp_sc.route('/tp-split-super-chain-2-data/<config_id>/<uuid>/safe-referer')
def tp_split_super_chain_2_data(config_id, uuid):
    check_referer(request, URLS['TP_SPLIT_SUPER_URL_2'])

    site = unquote(request.args.get('id', None))

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_CHAIN_SUPER_COOKIE_DATA_TEMPLATE, current_url=request.url_root, urls=URLS,
                        cookie_id=uuid,
                        safe_referer=site, index=2, combined_id=uuid, config_id=config_id))
    return response


@tp_sc.route('/tp-split-super-chain-2', defaults={'cookie_id': 'None'})
@tp_sc.route('/tp-split-super-chain-2/<config_id>/<cookie_id>/safe_referer')
def tp_split_super_chain_2(config_id, cookie_id):
    check_referer(request, URLS['TP_SPLIT_SUPER_URL_2'])
    config_cookie_length = implicit_user_login(User, config_id).local_storage_split_super_cookie_size

    next_site = URLS['TP_SPLIT_SUPER_URL_2'] + 'tp-split-super-chain-2-data/' + config_id

    site = request.args.get('ref', None)

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_CHAIN_SUPER_COOKIE_TEMPLATE, current_url=request.url_root,
                        next_site=next_site,
                        safe_referer=site, config_cookie_length=config_cookie_length, combined_id=cookie_id))
    return response


@tp_sc.route('/tp-split-super-chain-3-data/<config_id>/<uuid>/safe-referer')
def tp_split_super_chain_3_data(config_id, uuid):
    check_referer(request, URLS['TP_SPLIT_SUPER_URL_3'])

    site = unquote(request.args.get('id', None))

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_CHAIN_SUPER_COOKIE_DATA_TEMPLATE, current_url=request.url_root, urls=URLS,
                        cookie_id=uuid,
                        safe_referer=site, index=3, combined_id=uuid, config_id=config_id))
    return response


@tp_sc.route('/tp-split-super-chain-3', defaults={'cookie_id': 'None'})
@tp_sc.route('/tp-split-super-chain-3/<config_id>/<cookie_id>/safe_referer')
def tp_split_super_chain_3(config_id, cookie_id):
    check_referer(request, URLS['TP_SPLIT_SUPER_URL_3'])
    config_cookie_length = implicit_user_login(User, config_id).local_storage_split_super_cookie_size

    next_site = URLS['TP_SPLIT_SUPER_URL_3'] + 'tp-split-super-chain-3-data/' + config_id

    site = request.args.get('ref', None)

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_CHAIN_SUPER_COOKIE_TEMPLATE, current_url=request.url_root,
                        next_site=next_site,
                        safe_referer=site, config_cookie_length=config_cookie_length, combined_id=cookie_id))
    return response


@tp_sc.route('/tp-split-super-chain-master-data/<config_id>/<uuid>/safe-referer')
def tp_split_super_chain_master_data(config_id, uuid):
    check_referer(request, URLS['TP_SPLIT_SUPER_URL_4'])

    site = unquote(request.args.get('id', None))

    joined_user = JoinedTrackableUUID.get_or_create(uuid)
    log_site_visit(JoinedHistory, site, joined_user, request.referrer)
    redis_set_benchmark_recent_site(config_id, '6', site)
    recent_history = generate_recent_history(JoinedHistory, joined_user, 10)

    response = make_response(
        render_template(THIRD_PARTY_CHAIN_MASTER_TEMPLATE, current_url=request.url_root, urls=URLS, cookie_id=uuid,
                        history_log=recent_history, index=4, combined_id=uuid, trackable=True,
                        config_id=config_id))
    return response


@tp_sc.route('/tp-split-super-chain-master', defaults={'cookie_id': 'None'})
@tp_sc.route('/tp-split-super-chain-master/<config_id>/<cookie_id>/safe_referer')
def tp_split_super_chain_master(config_id, cookie_id):
    check_referer(request, URLS['TP_SPLIT_SUPER_URL_4'])
    config_cookie_length = implicit_user_login(User, config_id).local_storage_split_super_cookie_size

    next_site = URLS['TP_SPLIT_SUPER_URL_4'] + 'tp-split-super-chain-master-data/' + config_id

    site = request.args.get('ref', None)

    response = make_response(
        render_template(THIRD_PARTY_SPLIT_CHAIN_SUPER_COOKIE_TEMPLATE, current_url=request.url_root,
                        next_site=next_site,
                        safe_referer=site, config_cookie_length=config_cookie_length, combined_id=cookie_id))
    return response
