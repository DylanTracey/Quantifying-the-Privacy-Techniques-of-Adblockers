from flask import Blueprint
from flask import request, render_template, make_response

from config.models import User
from settings import URLS
from third_party.models import TrackableUUID, History
from utils.cookies import append_cookie
from utils.history import log_site_visit, generate_recent_history
from utils.redis_cache import redis_set_benchmark_recent_site
from utils.referer import check_referer
from utils.user import implicit_user_login

tp = Blueprint('tp', __name__)

THIRD_PARTY_SINGLE_TEMPLATE = 'third_party/third_party_single.html'


@tp.route('/tp-single-cookie/<config_id>')
def tp_single_cookie(config_id):
    check_referer(request, URLS['TP_URL'])
    config_cookie_length = implicit_user_login(User, config_id).cookie_size
    uuid = request.cookies.get('id')
    trackable_user = implicit_user_login(TrackableUUID, uuid, config_cookie_length)

    log_site_visit(History, request.referrer, trackable_user, request.remote_addr)
    recent_history = generate_recent_history(History, trackable_user, 10)
    if uuid is not None:
        redis_set_benchmark_recent_site(config_id, '2', request.referrer)

    response = make_response(
        render_template(THIRD_PARTY_SINGLE_TEMPLATE, history_log=recent_history, current_url=request.url_root,
                        cookie_id=uuid))
    if uuid is None:
        response = append_cookie(response, trackable_user.uuid)
    return response
