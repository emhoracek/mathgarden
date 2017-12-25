from flask import Flask
from flask import abort, request
from flask import jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
db_uri = 'postgresql://mathgarden_admin:111@localhost/mathgarden_devel'
FRONTEND_URL = 'http://localhost:8080'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
CORS(app)

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = environ['SECRET_KEY']


# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
class Learner(db.Model):
    __tablename__ = 'learners'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text)
    slack_name = db.Column(db.Text)
    goal = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'slack_name': self.slack_name,
            'goal': self.goal,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
        }

    @staticmethod
    def create(email, name, slack_name, goal):
        if email is None:
            return None
        if Learner.query.filter_by(email=email).first() is not None:
            return None
        learner = Learner(email=email,
                          name=name,
                          slack_name=slack_name,
                          goal=goal,
                          created_at=datetime.utcnow())
        db.session.add(learner)
        db.session.commit()
        return learner


@app.route('/api/learners', methods=['POST'])
def create_learner():
    json = request.get_json()
    email = json["email"]
    name = json["name"]
    slack_name = json["slack_name"]
    goal = json["goal"]
    learner = Learner.create(email, name, slack_name, goal)
    return jsonify(learner.to_dict())


@app.route('/api/learners', methods=['GET'])
def get_learners():
    learners = Learner.query.all()
    return (jsonify(map(lambda l: l.to_dict(), learners)))


@app.route('/api/learners/<int:id>', methods=['GET'])
def get_learner(id):
    learner = Learner.query.filter_by(id=id).first()
    if learner is None:
        abort(400)
    return jsonify(learner.to_dict())
