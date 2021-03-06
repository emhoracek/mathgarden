from flask import Flask
from flask import abort, request, g
from flask import jsonify
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime
import logging
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature,
                          URLSafeSerializer, SignatureExpired)
from random import (SystemRandom as Random)
from string import (ascii_letters, digits)

auth = HTTPBasicAuth()
random = Random()

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
    privacy = db.Column(db.Text)
    login_token = db.Column(db.Text)
    activated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def generate_auth_token(self, expiration=2592000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slack_name': self.slack_name,
            'goal': self.goal,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
        }

    def to_authed_dict(self):
        dict = self.to_dict()
        authed_fields = {
            'email': self.email,
            'token': self.generate_auth_token(),
            'privacy': self.privacy,
            'activated_at': self.activated_at
        }
        dict.update(authed_fields)
        return dict

    @staticmethod
    def create(email, name, slack_name, goal, privacy):
        if email is None:
            raise Exception("An email is required.")
        if Learner.query.filter_by(email=email).first() is not None:
            raise Exception("That email is already in use.")
        learner = Learner(email=email,
                          name=name,
                          slack_name=slack_name,
                          goal=goal,
                          privacy=privacy,
                          login_token=Learner.generate_login_token(),
                          created_at=datetime.utcnow())
        db.session.add(learner)
        db.session.commit()
        return learner

    def update(self, name, slack_name, goal, privacy):
        self.name = name
        self.slack_name = slack_name
        self.privacy = privacy
        self.goal = goal
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        learner = Learner.query.get(data['id'])
        return learner

    @staticmethod
    def verify_email_token(token):
        s = URLSafeSerializer(app.config['SECRET_KEY'])
        try:
            email = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        learner = Learner.query.filter_by(email=email).first()
        learner.activated_at = datetime.utcnow()
        return learner

    @staticmethod
    def generate_login_token():
        alphabet = ascii_letters + digits
        chars = random.sample(alphabet, 30)
        return "".join(chars)

    def send_email_confirmation(self):
        s = URLSafeSerializer(app.config['SECRET_KEY'])
        serialized_email = s.dumps(self.email)
        print 'sending to ', self.email
        print 'http://localhost:8080/#/confirm_email/', serialized_email


@app.route('/api/learners', methods=['POST'])
def create_learner():
    json = request.get_json()
    email = json["email"]
    name = json["name"]
    slack_name = json["slack_name"]
    goal = json["goal"]
    privacy = json["privacy"]
    try:
        learner = Learner.create(email, name, slack_name, goal, privacy)
        if learner:
            learner.send_email_confirmation()
            return jsonify(learner.to_authed_dict())
    except Exception, msg:
        return jsonify({'error': str(msg)})


@app.route('/api/email_confirmations/<token>', methods=['POST'])
def confirm_email(token):
    learner = Learner.verify_email_token(token)
    if learner is None:
        abort(400)
    return jsonify(learner.to_authed_dict())


@app.route('/api/magic_links/request', methods=['POST'])
def request_magic_link():
    json = request.get_json()
    email = json["email"]
    learner = Learner.query.filter_by(email=email).first()
    if learner is None:
        abort(400)
    learner.login_token = Learner.generate_login_token()
    db.session.add(learner)
    db.session.commit()
    print 'http://localhost:8080/#/login/', learner.login_token
    return jsonify({'sent': True})


@app.route('/api/magic_links/verify/<token>', methods=['POST'])
def verify_magic_link(token):
    learner = Learner.query.filter_by(login_token=token).first()
    if learner is None:
        return jsonify({'error': 'Invalid login token'})
    learner.login_token = Learner.generate_login_token()
    db.session.add(learner)
    db.session.commit()
    return jsonify(learner.to_authed_dict())


@auth.verify_password
def verify_token(token, we_dont_use_passwords):
    learner = Learner.verify_auth_token(token)
    if not learner:
        return False
    g.learner = learner
    return True


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


@app.route('/api/learners/me', methods=['GET'])
@auth.login_required
def get_authed_learner():
    try:
        token = auth.username()
        learner = Learner.verify_auth_token(token)
        if learner is None:
            abort(400)
        return jsonify(learner.to_authed_dict())
    except Exception, msg:
        return jsonify({'error': str(msg)})


@app.route('/api/learners/me', methods=['POST'])
@auth.login_required
def update_authed_learner():
    json = request.get_json()
    name = json["name"]
    slack_name = json["slack_name"]
    goal = json["goal"]
    privacy = json["privacy"]
    try:
        g.learner.update(name, slack_name, goal, privacy)
        return jsonify(g.learner.to_authed_dict())
    except Exception, msg:
        return jsonify({'error': str(msg)})
