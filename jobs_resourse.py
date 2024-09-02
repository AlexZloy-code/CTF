from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.users import User
from data.jobs import Jobs
from flask import jsonify, abort

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, f"Jobs {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(
            only=('job', 'collaborators', 'work_size', 'team_leader', 'user_id', 'flag'))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('job', 'collaborators', 'work_size', 'team_leader', 'user_id', 'flag')) for item in jobs]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('job', required=True)
        parser.add_argument('collaborators', required=True)
        parser.add_argument('work_size', required=True, type=int)
        parser.add_argument('flag', required=True)
        parser.add_argument('user_id', required=True, type=int)

        args = parser.parse_args()
        session = db_session.create_session()

        jobs = Jobs()
        jobs.job = args['job']
        jobs.collaborators = args['collaborators']
        jobs.flag = args['flag']
        jobs.user_id = args['user_id']
        jobs.work_size = args['work_size']

        session.add(jobs)
        session.commit()
        return jsonify({'id': jobs.id})
