from base_models import db


def log_site_visit(history_model, site, visitor, ip):
    visited_site = history_model(site=site or '/', visitor=visitor, ip=ip)
    db.session.add(visited_site)
    db.session.commit()


def generate_recent_history(history_model, visitor, amount):
    return history_model.query.filter_by(visitor=visitor).order_by(history_model.id.desc())[:amount]
