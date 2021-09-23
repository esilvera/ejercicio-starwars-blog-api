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
from models import db, User, Character, Planet, FavoritePlanet, FavoriteCharacter
from werkzeug.security import generate_password_hash, check_password_hash
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Extended extension
""" app.config["JWT_SECRET_KEY"] = "secret-key"  # Change this!
jwt = JWTManager(app) """

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/api/register', methods=['POST'])
def register():

    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    verify_username = User.query.filter_by(username=username).first()
    if verify_username: return jsonify({"msg": "Username ya esta en uso !"}), 400

    verify_email = User.query.filter_by(email=email).first()
    if verify_email: return jsonify({"msg": "Email ya esta en uso !"}), 400

    user = User()
    user.username = username
    user.password = generate_password_hash(password)
    user.email = email
    user.save()

    return jsonify(user.serialize()), 201

@app.route('/api/user', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

@app.route('/api/user/favorites', methods=['GET'])
def get_users_favorites():
    users = User.query.all()
    users = list(map(lambda user: user.serialize_with_favorites(), users))
    return jsonify(users), 200

@app.route('/api/user', methods=['POST'])
def post_users():

    name = request.json.get('name', " ")
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    is_active = request.json.get('is_active')

    user = User()
    user.name = name
    user.username = username
    user.password = password
    user.email = email
    user.is_active = is_active
    user.save()

    return jsonify(user.serialize()), 201

@app.route('/api/user/<int:id>', methods=['DELETE'])
def delete_users(id):

    user = User.query.get(id)

    if not user: return jsonify({"status": False, "msg": "User doesn't exist"}), 404

    user.delete()

    return jsonify({"status": True, "msg": "User deleted"}), 200

@app.route('/api/character', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), characters))
    return jsonify(characters), 200

@app.route('/api/character/<int:id>', methods=['GET'])
def get_characters_id(id):
    
    character = Character.query.get(id)
    if not character: return jsonify({"status": False, "msg": "Character doesn't exist"}), 404
    return jsonify(character.serialize()), 200

@app.route('/api/character', methods=['POST'])
def post_characters():

    name = request.json.get('name')
    hair_color = request.json.get('hair_color')
    eye_color = request.json.get('eye_color')
    gender = request.json.get('gender')
    description = request.json.get('description')
    planet_id = request.json.get('planet_id')

    character = Character()
    character.name = name
    character.hair_color = hair_color
    character.eye_color = eye_color
    character.gender = gender
    character.description = description
    character.planet_id = planet_id
    character.save()

    return jsonify(character.serialize()), 201

@app.route('/api/character/<int:id>', methods=['PUT'])
def put_characters(id):

    name = request.json.get('name')
    hair_color = request.json.get('hair_color')
    eye_color = request.json.get('eye_color')
    gender = request.json.get('gender')
    description = request.json.get('description')
    planet_id = request.json.get('planet_id')

    character = Character.query.get(id)
    character.name = name
    character.hair_color = hair_color
    character.eye_color = eye_color
    character.gender = gender
    character.description = description
    character.planet_id = planet_id
    character.update()

    return jsonify(character.serialize()), 200

@app.route('/api/character/<int:id>', methods=['DELETE'])
def delete_characters(id):

    character = Character.query.get(id)

    if not character: return jsonify({"status": False, "msg": "Character doesn't exist"}), 404

    character.delete()

    return jsonify({"status": True, "msg": "Character deleted"}), 200

@app.route('/api/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

@app.route('/api/planet/<int:id>', methods=['GET'])
def get_planets_id(id):
    
    planet = Planet.query.get(id)
    if not planet: return jsonify({"status": False, "msg": "Planet doesn't exist"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/api/planet', methods=['POST'])
def post_planets():

    name = request.json.get('name')
    diameter = request.json.get('diameter')
    rotation_period = request.json.get('rotation_period')
    population = request.json.get('population')
    climate = request.json.get('climate')
    terrain = request.json.get('terrain')

    planet = Planet()
    planet.name = name
    planet.diameter = diameter
    planet.rotation_period = rotation_period
    planet.population = population
    planet.climate = climate
    planet.terrain = terrain
    planet.save()

    return jsonify(planet.serialize()), 201

@app.route('/api/planet/<int:id>', methods=['PUT'])
def put_planets(id):

    name = request.json.get('name')
    diameter = request.json.get('diameter')
    rotation_period = request.json.get('rotation_period')
    population = request.json.get('population')
    climate = request.json.get('climate')
    terrain = request.json.get('terrain')

    planet = Planet.query.get(id)
    planet.name = name
    planet.diameter = diameter
    planet.rotation_period = rotation_period
    planet.population = population
    planet.climate = climate
    planet.terrain = terrain
    planet.update()

    return jsonify(planet.serialize()), 200

@app.route('/api/favorite/planet', methods=['POST'])
def post_favorites_planets():
    
    user_id = request.json.get('user_id')
    planet_id = request.json.get('planet_id')

    favorites_planet = FavoritePlanet()
    favorites_planet.user_id = user_id
    favorites_planet.planet_id = planet_id
    favorites_planet.save()

    return jsonify(favorites_planet.serialize()), 201

@app.route('/api/favorite/planet/<int:id_user>/<int:id_planet>', methods=['DELETE'])
def delete_favorites_planets(id_user, id_planet):

    planet = FavoritePlanet.query.filter_by(user_id = id_user, planet_id = id_planet).first() 

    if not planet: return jsonify({"status": False, "msg": "Favorite Planet doesn't exist"}), 404
    planet.delete()

    return jsonify({"status": True, "msg": "Favorite Planet deleted"}), 200

@app.route('/api/favorite/character', methods=['POST'])
def post_favorites_characters():
        
    user_id = request.json.get('user_id')
    character_id = request.json.get('character_id')

    favorites_character = FavoriteCharacter()
    favorites_character.user_id = user_id
    favorites_character.character_id = character_id
    favorites_character.save()

    return jsonify(favorites_character.serialize()), 201

@app.route('/api/favorite/character/<int:id_user>/<int:id_character>', methods=['DELETE'])
def delete_favorites_characters(id_user, id_character):

    character = FavoriteCharacter.query.filter_by(user_id = id_user, character_id = id_character).first() 

    if not character: return jsonify({"status": False, "msg": "Favorite Character doesn't exist"}), 404
    character.delete()

    return jsonify({"status": True, "msg": "Favorite Character deleted"}), 200




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
