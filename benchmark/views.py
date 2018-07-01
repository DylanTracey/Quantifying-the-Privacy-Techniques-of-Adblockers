from flask import Blueprint, redirect
from flask import render_template, make_response, url_for

from base_models import db
from config.models import User
from settings import URLS, FP_URLS
from utils.redis_cache import redis_get_benchmark_recent_site
from utils.user import implicit_user_login

benchmark = Blueprint('benchmark', __name__)

BENCHMARK_ROUTE_TEMPLATE = 'benchmark/benchmark_route.html'

MIDDLE_URL = ['fp-1/', 'fp-2/', 'fp-3/']


def update_result(user, mode, result):
    if mode == '1':
        user.first_party_test_result = result
    if mode == '2':
        user.third_party_test_result = result
    if mode == '3':
        user.third_party_split_result = result
    if mode == '4':
        user.third_party_split_chain_result = result
    if mode == '5':
        user.third_party_super_cookie_result = result
    if mode == '6':
        user.third_party_split_super_cookie_result = result
    db.session.commit()


@benchmark.route('/benchmark/<config_id>/<mode>/<fp_index>')
def benchmark_route(config_id, mode, fp_index):
    user = implicit_user_login(User, config_id)
    user.mode = mode
    if mode == '7':
        user.mode = '1'
    db.session.commit()
    next_site_index = int(fp_index) + 1
    if next_site_index == 5:
        return redirect(url_for('benchmark.benchmark_update_result', config_id=config_id, mode=mode), 302)

    middle_url = MIDDLE_URL[int(fp_index) % 3]

    next_site = URLS[FP_URLS[int(next_site_index) % 3]] + 'benchmark/' + config_id + '/' + mode + '/' + str(
        next_site_index)
    first_party_site = URLS[FP_URLS[int(fp_index) % 3]] + middle_url + config_id

    response = make_response(
        render_template(BENCHMARK_ROUTE_TEMPLATE, urls=URLS, user=user, next_site=next_site,
                        first_party_site=first_party_site, mode=mode, progress=str((int(fp_index)*20)+20)))

    return response


@benchmark.route('/benchmark/results/<config_id>/<mode>')
def benchmark_update_result(config_id, mode):
    user = implicit_user_login(User, config_id)
    result_bytes = redis_get_benchmark_recent_site(config_id, mode)

    if result_bytes is None:
        update_result(user, mode, 'FAILURE!')
    else:
        result = result_bytes.decode("utf-8")
        correct_url = URLS['FP_URL_1'] + 'fp-1/' + config_id

        if result == correct_url:
            update_result(user, mode, 'SUCCESS!')
        else:
            update_result(user, mode, 'FAILURE!')

    return redirect(URLS[FP_URLS[0]] + 'benchmark/' + config_id + '/' + str(int(mode) + 1) + '/0')
