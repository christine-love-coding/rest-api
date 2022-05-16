import sqlite3
from flask_restful import Resource, reqparse

import sys
sys.path.append("/Users/christinewang/rest_api_course")
from section6.code.models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='username is required')

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='username is required')

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'Message': 'User already exists'}, 400

        user = UserModel(**data)
        user.sav_to_db()
        return {'Message': 'User created successfully'}, 201
