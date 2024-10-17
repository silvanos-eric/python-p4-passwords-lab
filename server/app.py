#!/usr/bin/env python3

from config import api, app, db
from flask import request, session
from flask_restful import Resource
from models import User


class ClearSession(Resource):

    def delete(self):

        session['page_views'] = None
        session['user_id'] = None

        return {}, 204


class Signup(Resource):

    def post(self):
        try:
            data = request.json

            password = data['password']
            password_confirmation = data['password_confirmation']

            if password != password_confirmation:
                raise ValueError('Passowrds do not match')

            user = User(username=data['username'])
            user.password_hash = data['password']

            db.session.add(user)
            db.session.commit()

            return user.to_dict(rules=('-_password_hash', )), 201
        except (KeyError, ValueError) as e:
            errors = []

            if isinstance(e, KeyError):
                errors.append(f'Missing required field: {e}')

            if isinstance(e, ValueError):
                errors.append(str(e))

            return {'errors': errors}, 400
        except:
            return {'errors': ['An unknown error occurred']}, 500


class CheckSession(Resource):
    pass


class Login(Resource):
    pass


class Logout(Resource):
    pass


api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
