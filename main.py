from flask import Flask
from flask import request, redirect, url_for
import os
from urllib.parse import quote

from base_models import db
from benchmark.views import benchmark
from config.views import config
from first_party.views import fp
from settings import URLS
from third_party.views import tp
from third_party_split.views import tps
from third_party_super_cookie.views import tp_sc

app = Flask(__name__)
app.jinja_env.filters['quote'] = lambda u: quote(u)
app.config.from_object(os.environ['APPLICATION_CONFIGURATION'])
db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(benchmark)
app.register_blueprint(config)
app.register_blueprint(fp)
app.register_blueprint(tp)
app.register_blueprint(tps)
app.register_blueprint(tp_sc)


@app.route('/')
def entry():
    if request.url_root == URLS['FP_URL_1']:
        return redirect(url_for('fp.fp_1'))
    if request.url_root == URLS['FP_URL_2']:
        return redirect(url_for('fp.fp_2'))
    if request.url_root == URLS['FP_URL_3']:
        return redirect(url_for('fp.fp_3'))
    if request.url_root == URLS['CONFIG_URL']:
        return redirect(url_for('config.config_checkbox'))


if __name__ == '__main__':
    app.run()
