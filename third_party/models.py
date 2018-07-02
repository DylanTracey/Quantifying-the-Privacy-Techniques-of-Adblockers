from base_models import db, BaseUUID, BaseHistory


class TrackableUUID(BaseUUID):
    """
    Unique users that the third party site keeps track of via a unique identifier (cookie)
    """
    visited = db.relationship('History', backref='trackableUUID', lazy=True, cascade='all,delete')

    def __init__(self, uuid_length):
        if self.isFull(int(10 ** uuid_length)):
            self.delete_oldest()
        self.uuid = self.generate_unused_uuid(uuid_length)

    def __repr__(self):
        return '<TrackableUUID id=%r, uuid=%r>' % (self.id, self.uuid)


class History(BaseHistory):
    """
    History log table that creates logs of the visited first party sites for each user identifier (model above)
    """
    visitor_id = db.Column(db.Integer, db.ForeignKey('trackableUUID.id'), nullable=False)
    visitor = db.relationship(TrackableUUID)

    def __repr__(self):
        return '<History id=%r, site=%r, visitor=%r>' % (self.id, self.site, self.visitor)
