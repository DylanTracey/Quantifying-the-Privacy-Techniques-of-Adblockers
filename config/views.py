from flask import Blueprint, redirect
from flask import request, render_template, make_response

from config.forms import TrackerForm
from config.models import User
from config.models import db
from settings import URLS
from utils.cookies import append_cookie
from utils.referer import check_referer
from utils.user import implicit_user_login

config = Blueprint('config', __name__)

CONFIG_TEMPLATE = 'config/config.html'


@config.route('/config', methods=['GET', 'POST'])
def config_checkbox():
    check_referer(request, URLS['CONFIG_URL'])
    uuid = request.cookies.get('id')
    user = implicit_user_login(User, uuid)
    form = TrackerForm(meta={'csrf': False})

    if request.method == 'GET':
        form.tracker.default = user.mode
        form.tracker.data = user.mode
        form.first_party_cookie_size.data = user.first_party_cookie_size
        form.first_party_cookie_size.default = user.first_party_cookie_size
        form.cookie_size.default = user.cookie_size
        form.cookie_size.data = user.cookie_size
        form.split_cookie_size.default = user.split_cookie_size
        form.split_cookie_size.data = user.split_cookie_size
        form.local_storage_super_cookie_size.default = user.local_storage_super_cookie_size
        form.local_storage_super_cookie_size.data = user.local_storage_super_cookie_size
        form.local_storage_split_super_cookie_size.default = user.local_storage_split_super_cookie_size
        form.local_storage_split_super_cookie_size.data = user.local_storage_split_super_cookie_size

    elif form.validate_on_submit():
        user.mode = form.tracker.data
        user.first_party_cookie_size = form.first_party_cookie_size.data
        user.cookie_size = form.cookie_size.data
        user.split_cookie_size = form.split_cookie_size.data
        user.local_storage_super_cookie_size = form.local_storage_super_cookie_size.data
        user.local_storage_split_super_cookie_size = form.local_storage_split_super_cookie_size.data
        db.session.commit()

    response = make_response(
        render_template(CONFIG_TEMPLATE, urls=URLS, form=form, user=user, config_id=user.uuid))
    if uuid is None:
        response = append_cookie(response, user.uuid)
    return response


@config.route('/start-benchmark')
def start_benchmark():
    check_referer(request, URLS['CONFIG_URL'])
    uuid = request.cookies.get('id')
    user = implicit_user_login(User, uuid)
    user.mode = '1'
    user.first_party_test_result = 'Untested'
    user.third_party_test_result = 'Untested'
    user.third_party_split_result = 'Untested'
    user.third_party_split_chain_result = 'Untested'
    user.third_party_super_cookie_result = 'Untested'
    user.third_party_split_super_cookie_result = 'Untested'
    db.session.commit()
    return redirect(URLS['FP_URL_1'] + 'benchmark/' + user.uuid + '/' + user.mode + '/0')
