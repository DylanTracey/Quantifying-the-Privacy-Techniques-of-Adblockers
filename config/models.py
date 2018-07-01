from base_models import db, BaseUUID


class User(BaseUUID):
    mode = db.Column(db.String(1), default='1', nullable=False)
    first_party_cookie_size = db.Column(db.Integer, default=16, nullable=False)
    cookie_size = db.Column(db.Integer, default=16, nullable=False)
    split_cookie_size = db.Column(db.Integer, default=3, nullable=False)
    local_storage_super_cookie_size = db.Column(db.Integer, default=16, nullable=False)
    local_storage_split_super_cookie_size = db.Column(db.Integer, default=4, nullable=False)

    first_party_test_result = db.Column(db.String(16), default='Untested', nullable=False)
    third_party_test_result = db.Column(db.String(16), default='Untested', nullable=False)
    third_party_split_result = db.Column(db.String(16), default='Untested', nullable=False)
    third_party_split_chain_result = db.Column(db.String(16), default='Untested', nullable=False)
    third_party_super_cookie_result = db.Column(db.String(16), default='Untested', nullable=False)
    third_party_split_super_cookie_result = db.Column(db.String(16), default='Untested', nullable=False)


    def __init__(self, uuid_length):
        if self.isFull(int(10 ** (uuid_length / 2))):
            self.delete_oldest()
        self.uuid = self.generate_unused_uuid(uuid_length)

    def __repr__(self):
        return '<User: id=%r, uuid=%r>' % (self.id, self.uuid)
