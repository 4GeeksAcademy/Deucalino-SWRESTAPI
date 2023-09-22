from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
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
            "is_active":self.is_active
            # do not serialize the password, its a security breach
        }
    
class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    homeworld = db.Column(db.String(250))
    url = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return '<Characters %r>' % self.uid
    
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    url = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return '<Planet %r>' % self.uid
    
    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "url":self.url
        }

class Favorites(db.Model):
    __tablename__='favorites'
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_type = db.Column(db.Enum('character', 'planet', name='favorite_item_type'), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<Favorites %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id":self.user_id,
            "item_type":self.item_type,
            "item_uid":self.item_id,
        }
