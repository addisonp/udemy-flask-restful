from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.item import Item, Items
from security import authenticate, identity

from resources.user import UserRegister
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# specify config property for SQLAlchemy
# turn off the Flask-Sqlahcmey tracking off, but Sqlalchemy tracker is still on
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'joel'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # JWT creates a new end point /auth
# we send /auth a username/password and that is sent to the authenticate function
# if the u/p is valid the authenticate returns the user and that becomes the identity
# the auth endpoint returns a JWT token

# we can send the JWT token to the next request that we make
# when we send a JWT token, is that the JWT calls the identity function and uses the JWT token
#   to get the userid and the correct user for the userid that the JWT token represents
#   if it can do that, then the user was authenticated, the JWT token is valid
#   this is done with flask_jwt.jwt_required

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    # import our flask app into the db
    db.init_app(app)
    app.run(port=5000, debug=True)
