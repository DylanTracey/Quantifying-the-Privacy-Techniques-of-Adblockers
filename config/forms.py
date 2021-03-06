from flask_wtf import FlaskForm
from wtforms import RadioField, IntegerField
from wtforms.validators import InputRequired, NumberRange

from settings import TRACKING_MODES


class TrackerForm(FlaskForm):
    """
    The form to customize what the user wants the tracking to function like. You can specify the tracking mode (for
    manual testing via the navigation bar), and the related unique identifier cookie sizes (how long the string is) for
    each of the modes.

    For instance if the user sets the tracking mode to 2, and the cookie_size parameter to 32; clicking on the first
    party sites will user tracking mode 2 (third party tracking) and the unique identifier will be a string of 32
    characters.
    """
    tracker = RadioField('Tracker Options',
                         choices=[('1', TRACKING_MODES['1']),
                                  ('2', TRACKING_MODES['2']),
                                  ('3', TRACKING_MODES['3']),
                                  ('4', TRACKING_MODES['4']),
                                  ('5', TRACKING_MODES['5']),
                                  ('6', TRACKING_MODES['6'])],
                         default='1')
    first_party_cookie_size = IntegerField('First Party Cookie Size',
                                           validators=[InputRequired('This field is required'),
                                                       NumberRange(min=3, max=64,
                                                                   message='Must be a number between 3 and 64')],
                                           default=12)
    cookie_size = IntegerField('Third Party Single Cookie Size',
                               validators=[InputRequired('This field is required'),
                                           NumberRange(min=3, max=64, message='Must be a number between 3 and 64')],
                               default=12)
    split_cookie_size = IntegerField('Third Party Split/Chained Cookie Size',
                                     validators=[InputRequired('This field is required'),
                                                 NumberRange(min=1, max=16,
                                                             message='Must be a number between 1 and 16')],
                                     default=3)
    local_storage_super_cookie_size = IntegerField('Third Party Local Storage Super Cookie Size',
                               validators=[InputRequired('This field is required'),
                                           NumberRange(min=3, max=64, message='Must be a number between 3 and 64')],
                               default=12)
    local_storage_split_super_cookie_size = IntegerField('Third Party Local Storage Split/Chained Cookie Size',
                                     validators=[InputRequired('This field is required'),
                                                 NumberRange(min=1, max=16,
                                                             message='Must be a number between 1 and 16')],
                                     default=3)


