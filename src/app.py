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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

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
@app.route('/characters/<int:position>', methods=['GET'])
def handle_character():
   return jsonify(db.characters)
@app.route('/planets', methods=['GET'])
def handle_planets():
    planet = Planet.query.all()
    result = []
    for planet in planet:
     result.append(planet.serialize())
    return jsonify(result), 200
@app.route('/planets/<int:position>', methods=['GET'])
def handle_planet():
   return jsonify(db.planet)
@app.route('user/favorites', methods=['GET'])
def get_user_favorites():
    if request.method=='GET':
       favorites=[]
       db_result=Favorites.query.all()
       for favorite in db_result:
          favorites.append(favorite.serialize())
       return jsonify(favorites),200
       return "Invalid method",404

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
@app.route('/favorites', methods=['POST'])
def add_favorites():
    if request.method=='POST':
       print(request.get_json())
       return jsonify([]),200

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/favorite/characters/<int:position>', methods=['DELETE'])
def delete_fav_characters(position):
    db.characters.remove(db.characters[position])
    print("This is the position to delete: ",position)
    return jsonify(db.characters)
@app.route('/favorite/planet/<int:position>', methods=['DELETE'])
def delete_fav_planet(position):
    db.planet.remove(db.planet[position])
    print("This is the position to delete: ",position)
    return jsonify(db.planet)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
