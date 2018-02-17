from db import db


class UserModel(db.Model):
    # initialize the connection to SQLAlchemy
    __tablename__ = 'users'
    # define the columns that SQLAlchemy will understand
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))



    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # tested with POSTMAN where the Header contains a key: Authorization
    # and a value: JWT <token>
    # <token> is retrieved from /auth where we pass the u/p