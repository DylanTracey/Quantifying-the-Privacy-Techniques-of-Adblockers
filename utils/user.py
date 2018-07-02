from base_models import db


def implicit_user_login(user_model, uuid, uuid_length=32):
    """
    Gets a user model object based on the unique identifier string and the user model desired.
    """
    user = user_model.query.filter_by(uuid=uuid).first()
    if user is None:
        user = user_model(uuid_length)
        db.session.add(user)
        db.session.commit()
    return user
