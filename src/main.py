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
from models import db, User, Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/api/character', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), characters))
    return jsonify(characters), 200

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

@app.route('/api/planet', methods=['POST'])
def post_planets():

    name = request.json.get('name')
    diameter = request.json.get('diameter')
    rotation_period = request.json.get('rotation_period')
    population = request.json.get('population')
    climate = request.json.get('climate')
    terrain = request.json.get('terrain')
    #characters = request.json.get('characters') # No va porque se asigna con el character

    planet = Planet()
    planet.name = name
    planet.diameter = diameter
    planet.rotation_period = rotation_period
    planet.population = population
    planet.climate = climate
    planet.terrain = terrain
    #planet.characters = characters
    planet.save()

    return jsonify(planet.serialize()), 201









# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
