from hmac import compare_digest
from models.user import UserModel

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and compare_digest(user.password, password):
        return user

def identity(payload):
    # when user make a request that need authntication, we use this function
    # we get a payload coming from the request
    # In the payload, we get the identity, which is user id
    # a unique function to Flask JWT. It takes a payload.
    # The payload is the contents of the JWT Token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
