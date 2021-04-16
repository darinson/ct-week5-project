from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow 

import secrets

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(300), nullable = False, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    character = db.relationship('Character', backref = 'owner', lazy = True)

    def __init__(self,email,name = '',password = ''):
        self.id = self.set_id()
        self.name = name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been created and added to database!'

class Character(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(300))
    comics_appeared_in = db.Column(db.Numeric(precision=4))
    super_power = db.Column(db.String(150))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_taken = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,name,description,comics_appeared_in,super_power,date_created,user_taken,id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.date_created = date_created
        self.user_token = user_token
        
    def __repr__(self):
        return f'{self.name} has been added to the MCD Collection!'

    def set_id(self):
        return secrets.token_urlsafe()

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id','name','description','comics_appeared_in','auper_power','date_created']


character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)