from base_models import db, BaseUUID, BaseHistory
from utils.cookies import generate_uuid


class SplitTrackableUUIDBase(BaseUUID):
    __abstract__ = True

    @classmethod
    def get_or_create(cls, uuid, split_uuid_length):
        if uuid is None:
            uuid = generate_uuid(split_uuid_length)
        split_user = cls.query.filter_by(uuid=uuid).first()
        if split_user is None:
            split_user = cls(uuid)
            db.session.add(split_user)
            db.session.commit()
        return split_user

    def __init__(self, uuid):
        self.uuid = uuid


class SplitTrackableUUID1(SplitTrackableUUIDBase):
    __tablename__ = 'splitTrackableUUID1'
    visited = db.relationship('SplitHistoryBase1', backref='splitTrackableUUID1', lazy=True)

    def __repr__(self):
        return '<SplitTrackableUUID1 id=%r, uuid=%r>' % (self.id, self.uuid)


class SplitTrackableUUID2(SplitTrackableUUIDBase):
    __tablename__ = 'splitTrackableUUID2'
    visited = db.relationship('SplitHistoryBase2', backref='splitTrackableUUID2', lazy=True)

    def __repr__(self):
        return '<SplitTrackableUUID2 id=%r, uuid=%r>' % (self.id, self.uuid)


class SplitTrackableUUID3(SplitTrackableUUIDBase):
    __tablename__ = 'splitTrackableUUID3'
    visited = db.relationship('SplitHistoryBase3', backref='splitTrackableUUID3', lazy=True)

    def __repr__(self):
        return '<SplitTrackableUUID3 id=%r, uuid=%r>' % (self.id, self.uuid)


class SplitTrackableUUID4(SplitTrackableUUIDBase):
    __tablename__ = 'splitTrackableUUID4'
    visited = db.relationship('SplitHistoryBase4', backref='splitTrackableUUID4', lazy=True)

    def __repr__(self):
        return '<SplitTrackableUUID4 id=%r, uuid=%r>' % (self.id, self.uuid)


class SplitHistoryBase1(BaseHistory):
    visitor_id = db.Column(db.Integer, db.ForeignKey('splitTrackableUUID1.id'), nullable=False)
    visitor = db.relationship(SplitTrackableUUID1)

    def __repr__(self):
        return '<SplitHistoryBase1 id=%r, site=%r, visitor=%r>' % (self.id, self.site, self.visitor)


class SplitHistoryBase2(BaseHistory):
    visitor_id = db.Column(db.Integer, db.ForeignKey('splitTrackableUUID2.id'), nullable=False)
    visitor = db.relationship(SplitTrackableUUID2)

    def __repr__(self):
        return '<SplitHistoryBase2 id=%r, site=%r, visitor=%r>' % (self.id, self.site, self.visitor)


class SplitHistoryBase3(BaseHistory):
    visitor_id = db.Column(db.Integer, db.ForeignKey('splitTrackableUUID3.id'), nullable=False)
    visitor = db.relationship(SplitTrackableUUID3)

    def __repr__(self):
        return '<SplitHistoryBase3 id=%r, site=%r, visitor=%r>' % (self.id, self.site, self.visitor)


class SplitHistoryBase4(BaseHistory):
    visitor_id = db.Column(db.Integer, db.ForeignKey('splitTrackableUUID4.id'), nullable=False)
    visitor = db.relationship(SplitTrackableUUID4)

    def __repr__(self):
        return '<SplitHistoryBase4 id=%r, site=%r, visitor=%r>' % (self.id, self.site, self.visitor)


class JoinedTrackableUUID(BaseUUID):
    __tablename__ = 'joinedTrackableUUID'
    visited = db.relationship('JoinedHistory', backref='joinedTrackableUUID', lazy=True, cascade='all,delete')

    @classmethod
    def get_or_create(cls, uuid):
        split_user = cls.query.filter_by(uuid=uuid).first()
        if split_user is None:
            split_user = cls(uuid)
            db.session.add(split_user)
            db.session.commit()
        return split_user

    def __init__(self, uuid):
        self.uuid = uuid

    def __repr__(self):
        return '<JoinedTrackableUUID id=%r, uuid=%r>' % (self.id, self.uuid)


class JoinedHistory(BaseHistory):
    visitor_id = db.Column(db.Integer, db.ForeignKey('joinedTrackableUUID.id'), nullable=False)
    visitor = db.relationship(JoinedTrackableUUID)

    def __repr__(self):
        return '<JoinedHistory id=%r, site=%r, visitor=%r>' % (self.id, self.site, self.visitor)
