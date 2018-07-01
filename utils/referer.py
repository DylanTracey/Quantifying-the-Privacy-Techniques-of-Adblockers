from flask import abort


def check_referer(request, urls):
    if not request.url_root in urls:
        abort(404)
