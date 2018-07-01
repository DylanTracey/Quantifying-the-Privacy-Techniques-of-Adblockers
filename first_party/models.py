from base_models import db, BaseUUID, BaseHistory


class FirstPartyUUID(BaseUUID):
    __tablename__ = 'firstpartyUUID'
    visited = db.relationship('FirstPartyHistory', backref='firstpartyUUID', lazy=True, cascade='all,delete')

    def __init__(self, uuid_length):
        if self.isFull(int(10 ** uuid_length)):
            self.delete_oldest()
        self.uuid = self.generate_unused_uuid(uuid_length)

    def __repr__(self):
        return '<FirstPartyUUID id=%r, uuid=%r>' % (self.id, self.uuid)


class FirstPartyHistory(BaseHistory):
    visitor_id = db.Column(db.Integer, db.ForeignKey('firstpartyUUID.id'), nullable=False)
    visitor = db.relationship(FirstPartyUUID)

    def __repr__(self):
        return '<FirstPartyHistory id=%r, site=%r, visitor=%r>' % (self.id, self.site, self.visitor)


class FirstPartyClickHistory(BaseHistory):
    visitor_id = db.Column(db.Integer, db.ForeignKey('firstpartyUUID.id'), nullable=False)
    visitor = db.relationship(FirstPartyUUID)

    def __repr__(self):
        return '<FirstPartyClickHistory id=%r, site=%r, visitor=%r>' % (self.id, self.site, self.visitor)
