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
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# generate sitemap with all your endpoints
@app.route('/characters', methods=['GET'])
def get_characters():
    characters=Characters.query.all()
    characters_list=[]
    for character in characters:
        character_data = {
            'uid': character.id,
            'name': character.name,
            'homeworld': character.homeworld,
            'url':character.url
        }
    characters_list.append(character_data)
    return jsonify(characters_list)

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character=Characters.query.get(character_id)
     # Check if the person exists
    if not character:
        return jsonify({'message': 'Character not found'}),400
    character_data = {
            'id': character.id,
            'name': character.name,
            'homeworld': character.homeworld,
            'url':character.url
        }
    return jsonify(character_data)

@app.route('/planets', methods=['GET'])
def get_planets():
    planet=Planet.query.all()
    planet_list=[]
    for planet in planet:
        planet_data = {
            'id': planet.id,
            'name': planet.name,
            'url':planet.url
        }
    planet_list.append(planet_data)
    return jsonify(planet_list)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
   planet=Planet.query.get(planet_id)
   if not planet:
        return jsonify({'message': 'Planet not found'}),400
   planet_data = {
            'id': planet.id,
            'name': planet.name,
            'url':planet.url
        }
   return jsonify(planet_data)

@app.route('/users', methods=['GET'])
def get_users():
    user=User.query.all()
    user_list=[]
    for user in user:
        user_data = {
            'id': user.id,
            'email': user.email,
            'is_active':user.is_active
        }
    user_list.append(user_data)
    return jsonify(user_list)

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    favorites = Favorites.query.all()
    serialized_favorites = [favorite.serialize() for favorite in favorites]
    return jsonify(serialized_favorites)
def create_favorite():
    user_id = request.json.get('user_id')
    character_id = request.json.get('character_id')
    planet_id = request.json.get('planet_id')
    existing_favorite = Favorites.query.filter_by(user_id=user_id, character_id=character_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({'message': 'Favorite already exists'})
    favorite = Favorites(user_id=user_id, character_id=character_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite created successfully'})

@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorites.query.get(favorite_id)
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite deleted successfully"})
    else:
        return jsonify({"message": "Favorite not found"})
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
