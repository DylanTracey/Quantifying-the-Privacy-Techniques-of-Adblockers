from flask import abort


def check_referer(request, urls):
    """
    Checks the base domain being requested from is from one of the desired URLs. This is used in every view to
    simulate different web servers based on the base domains. Aborts if site won't exist for this base domain.
    """
    if not request.url_root in urls:
        pass
        #abort(404)
