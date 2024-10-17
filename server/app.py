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

            username = data['username']
            password = data['password']
            password_confirmation = data['password_confirmation']

            if password != password_confirmation:
                raise ValueError('Passowrds do not match')

            new_user = User(username=username)
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            return new_user.to_dict(rules=('-_password_hash', )), 201
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

    def get(self):

        current_user_id = session.get('user_id')
        if current_user_id:
            user = db.session.get(User, current_user_id)
            if not user:
                return {}, 204
            return user.to_dict(rules=('-_password_hash', ))
        return {}, 204


class Login(Resource):

    def post(self):
        try:
            # Get the credentials from the request body
            credentials = request.json
            username = credentials['username']
            password = credentials['password']

            # Check if the user exists
            user = User.query.filter_by(username=username).first()
            if not user:
                raise ValueError('Invalid username/password')

            # Check the password
            if not user.authenticate(password):
                raise ValueError('Invalid username/password')

            # Log the user in
            session['user_id'] = user.id

            # Return the user object
            return user.to_dict(rules=('-_password', )), 200

        except KeyError as e:
            # Handle missing required fields
            errors = [f'Missing required field: {e}']
            return {'errors': errors}, 400

        except ValueError as e:
            # Handle invalid username/password
            errors = [str(e)]
            return {'errors': errors}, 400

        except:
            # Handle an unknown error
            return {'errors': ['An unknown error occurred']}, 500


class Logout(Resource):
    pass


api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
