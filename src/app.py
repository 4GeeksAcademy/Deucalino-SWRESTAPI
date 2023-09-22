"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planet, Favorites
from flask_jwt_extended import get_jwt_identity
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    user = User.query.all()
    result = []
    for user in user:
        result.append(user.serialize())
        return jsonify(result), 200

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200
@app.route('/characters', methods=['GET'])
def handle_characters():
  characters = Characters.query.all()
  result = []
  for characters in characters:
    result.append(characters.serialize())
  return jsonify(result), 200
@app.route('/characters/<int:character_iud>', methods=['GET'])
def get_character(character_uid):
    character = Characters.query.get(character_uid)
    if character:
        return jsonify(character.serialize()), 200
@app.route('/planets', methods=['GET'])
def handle_planets():
    planet = Planet.query.all()
    result = []
    for planet in planet:
     result.append(planet.serialize())
    return jsonify(result), 200
@app.route('/planets/<int:planet_uid>', methods=['GET'])
def get_planet(planet_uid):
    planet = Planet.query.get(planet_uid)
    if planet:
        return jsonify(planet.serialize()), 200
@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    user_id = get_jwt_identity()
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    serialized_favorites = [favorite.serialize() for favorite in favorites]
    return jsonify(serialized_favorites), 200
@app.route('/favorite/planet/<int:planet_uid>', methods=['POST'])
def add_favorite_planet(planet_uid):
    user_id = get_jwt_identity()
    if user_id is None:
        return jsonify({"message": "User not authenticated"}), 401
    
    
    planet = Planet.query.get(planet_uid)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404
    
    
    valid_favorite = Favorites.query.filter_by(user_id=user_id, planet=planet, planet_uid=planet_uid).first()
    if valid_favorite:
        return jsonify({"message": "Planet is already a favorite"}), 400
    
    new_favorite = Favorites(user_id=user_id, planet=planet, planet_uid=planet_uid)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite planet added"}), 201
@app.route('/favorite/characters/<int:character_uid>', methods=['POST'])
def add_favorite_character(character_uid):
    user_id = get_jwt_identity()
    if user_id is None:
        return jsonify({"message": "User not authenticated"}), 401
    
    
    character = Characters.query.get(character_uid)
    if character is None:
        return jsonify({"message": "Character not found"}), 404
    
    
    valid_favorite = Favorites.query.filter_by(user_id=user_id,character_uid=character_uid).first()
    if valid_favorite:
        return jsonify({"message": "Character is already a facharacters=charactervorite"}), 400
    
    new_favorite = Favorites(user_id=user_id, characters=character, character_uid=character_uid)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite character added"}), 201

@app.route('/favorite/character_uid/<int:position>', methods=['DELETE'])
def delete_fav_characters(character_id):
    user_id = get_jwt_identity()
    if user_id is None:
        return jsonify({"message": "User not authenticated"}), 401
    favorite = Favorites.query.filter_by(user_id=user_id,character_uid=character_uid).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite character deleted"}), 200
    else:
        return jsonify({"message": "Favorite character not found"}), 404
   
@app.route('/favorite/planet_uid/<int:position>', methods=['DELETE'])
def delete_fav_planet(position):
    db.planet_uid.remove(db.planet_uid[position])
    print("This is the position to delete: ",position)
    return jsonify(db.planet_uid)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
