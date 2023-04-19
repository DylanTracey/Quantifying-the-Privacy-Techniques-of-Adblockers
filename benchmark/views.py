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
    """
    Updates the results of the benchmark for the given mode.
    :param user: The user for the benchmark.
    :param mode: The mode to update the results of.
    :param result: The result string.
    """
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
    """
    The main loop of the benchmark routing. Starts by incrementing the fp_index (which specifies the first party site to
    iframe in), and then for the outer loop, increments the mode (to test each individual mode of tracking).

    :param config_id: the unique identifier for the user (so the benchmark settings are customized per user).
    :param mode: The current mode (outer loop) being tested.
    :param fp_index: The current first party site (inner loop) being iframed in.
    :return: The HTTP response (template)
    """
    user = implicit_user_login(User, config_id)
    user.mode = mode

    # Once the benchmark is finished (all mode possibilities exhausted), set the mode back to the starting one.
    if mode == '7':
        user.mode = '1'
    db.session.commit()

    # Gets the next first party site index
    next_site_index = int(fp_index) + 1

    # If the next site index is 5, we have tested all the required first party sites to conclude whether tracking
    # between them has occurred, so now we update the results and exit this inner loop.
    if next_site_index == 5:
        return redirect(url_for('benchmark.benchmark_update_result', config_id=config_id, mode=mode), 302)

    middle_url = MIDDLE_URL[int(fp_index) % 3]

    # Generates the next benchmark url string to redirect to
    next_site = URLS[FP_URLS[int(next_site_index) % 3]] + 'benchmark/' + config_id + '/' + mode + '/' + str(
        next_site_index)
    # Generates the next first party site url string to iframe
    first_party_site = URLS[FP_URLS[int(fp_index) % 3]] + middle_url + config_id

    # Responds with the benchmark template
    response = make_response(
        render_template(BENCHMARK_ROUTE_TEMPLATE, urls=URLS, user=user, next_site=next_site,
                        first_party_site=first_party_site, mode=mode, progress=str((int(fp_index)*20)+20)))
    return response


@benchmark.route('/benchmark/results/<config_id>/<mode>')
def benchmark_update_result(config_id, mode):
    """
    Updates the results for the current configuration by examining the redis cache and goes to test the next mode

    :param config_id: the unique identifier for the user (so the benchmark settings are customized per user).
    :param mode: The currently tested mode.
    :return: redirect response to start testing the next mode.
    """
    user = implicit_user_login(User, config_id)

    # Retrieves the result that the third party tracker has for the recently visited site that the user went to
    result_bytes = redis_get_benchmark_recent_site(config_id, mode)

    # If the result doesn't exist, the third party tracker was unable to history log the users recently visited site
    if result_bytes is None:
        update_result(user, mode, 'FAILURE!')
    else:
        result = result_bytes.decode("utf-8")
        correct_url = URLS['FP_URL_1'] + 'fp-1/'

        # Checks that the recently visited site is the correct one.
        if result == correct_url:
            update_result(user, mode, 'SUCCESS!')
        else:
            update_result(user, mode, 'FAILURE!')

    # Redirects to the next mode to test (outer loop increment)
    return redirect(URLS[FP_URLS[0]] + 'benchmark/' + config_id + '/' + str(int(mode) + 1) + '/0')
