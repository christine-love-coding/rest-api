from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import StoreList, Store




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# tell SQLALCHEMY where to find the data.db file, which is the root folder of our project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Both sqlalchemy and rest_api_course-sqlalchemy has a tracker to track the changes we made but not commited to db
# this turns off the rest_api_course-sqlalchemy tracker, since the sqlalchemy is still on

app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()
    # sqlalchemy go through import and creates tables that it sees.
    # eg. we import Store, so sqlalchemy goes to resources.store, find Store(Resource) and import StoreModel


jwt = JWT(app, authenticate, identity)
'''
JWT create a new endpoint, /auth
when we call /auth, we send it a username and a password
JWT extension gets that username and password and sends it over to authenticate function we defined in security file.
If user and password matches our record, the auth endpoint returns a JW token.
We can send the JW token to the next request we make

When we send a JW token, JWT calls the identity function and uses the JWT token to get the user ID.
If this is successful, then the user was authenticated.
'''


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
'''
        1st parameter: this tells the api the Student resource is now available to our API
        2nd parameter: specify the endpoint to access the resource. The name parameter goes to the method parameter 
                        which is name in get()
'''
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
# when we execute a post request to /register, this will call the UserRegister
# to call the post method




if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug = True)