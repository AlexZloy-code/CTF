from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.users import User

from flask import abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, f"Command {user_id} not found")


class CommandResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        commands = session.query(User).get(user_id)
        return jsonify({'commands': commands.to_dict(
            only='name')})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        commands = session.query(User).get(user_id)
        session.delete(commands)
        session.commit()
        return jsonify({'success': 'OK'})


class CommandListResource(Resource):
    def get(self):
        session = db_session.create_session()
        commands = session.query(User).all()
        return jsonify({'commands': [item.to_dict(
            only='name') for item in commands]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)

        args = parser.parse_args()
        session = db_session.create_session()

        commands = User()
        commands.name = args['name']

        session.add(commands)
        session.commit()
        return jsonify({'id': commands.id})
