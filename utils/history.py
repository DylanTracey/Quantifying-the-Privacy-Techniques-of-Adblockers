from base_models import db


def log_site_visit(history_model, site, visitor, ip):
    """
    Logs a site visited entry based on the History Model intended.
    """
    visited_site = history_model(site=site or '/', visitor=visitor, ip=ip)
    db.session.add(visited_site)
    db.session.commit()


def generate_recent_history(history_model, visitor, amount):
    """
    Generates a recent history log based on the History Model intended.

    :param history_model: History model used.
    :param visitor: User's history logs to check
    :param amount: How much of the recent entries are needed (10 would specify the 10 most recent entries)
    """
    return history_model.query.filter_by(visitor=visitor).order_by(history_model.id.desc())[:amount]
