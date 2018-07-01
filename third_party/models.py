from base_models import db, BaseUUID, BaseHistory


class TrackableUUID(BaseUUID):
    visited = db.relationship('History', backref='trackableUUID', lazy=True, cascade='all,delete')

    def __init__(self, uuid_length):
        if self.isFull(int(10 ** uuid_length)):
            self.delete_oldest()
        self.uuid = self.generate_unused_uuid(uuid_length)

    def __repr__(self):
        return '<TrackableUUID id=%r, uuid=%r>' % (self.id, self.uuid)


class History(BaseHistory):
    visitor_id = db.Column(db.Integer, db.ForeignKey('trackableUUID.id'), nullable=False)
    visitor = db.relationship(TrackableUUID)

    def __repr__(self):
        return '<History id=%r, site=%r, visitor=%r>' % (self.id, self.site, self.visitor)
