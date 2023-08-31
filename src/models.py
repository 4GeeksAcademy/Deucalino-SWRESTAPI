from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Characters(db.Model):
    __tablename__ = 'characters'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    homeworld = db.Column(db.String(250))
    url = db.Column(db.String(250), nullable=False)
    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "homeworld":self.homeworld,
            "url":self.url

            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__='planet'
    planet_uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    url = db.Column(db.String(250), nullable=False)

class Favorites(db.Model):
    __tablename__='favorites'
    id=db.Column(db.Integer, primary_key=True)
    bestcharacter_uid=db.Column(db.Integer,db.ForeignKey('characters.uid'))
    bestplanet_uid=db.Column(db.Integer, db.ForeignKey('planet.planet_uid'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    def __repr__(self):
        return '<Favorites %r>' % self.user

    def serialize(self):
        return {
            "id": self.id,
            "bestcharacter_uid":self.  bestcharacter_uid,
            " bestplanet_uid":self. bestplanet_uid,
            "user_id":self.user_id,
            "name": self.name,
            "user":self.user
            # do not serialize the password, its a security breach
        }
