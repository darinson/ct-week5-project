from flask import Blueprint, request, jsonify
from marvel_collection.helpers import token_required
from marvel_collection.models import User, Character, character_schema, characters_schema, db, ma

api = Blueprint('api',__name__,url_prefix='/api') #the url that goes into insomnia

#CREATE Character
@api.route('/characters', methods = ['POST']) #where is /cars referenced?
@token_required
def create_car(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    date_created = request.json['date_created']
    user_token = current_user_token.token

    character=Character(name,description,comics_appeared_in,super_power,date_created,user_token = user_token)

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

# RETRIEVE ALL Characters
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token = owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)

# RETRIEVE Character
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    character = Character.query.get(id)
    response = character_schema.dump(character)
    return jsonify(response)

# UPDATE CHARACTER ENDPOINT
@api.route('/characters/<id>', methods = ['POST', 'PUT'])
@token_required
def update_character(current_user_token, id):
    character = Character.query.get(id)

    character.name = request.json['name']
    character.description = request.json['description']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.super_power = request.json['super_power']
    character.date_created = request.json['date_created']
    character.user_token = current_user_token.token

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)

# DELETE Character
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token,id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)