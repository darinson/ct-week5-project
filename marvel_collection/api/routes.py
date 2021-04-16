from flask import Blueprint, request, jsonify
from marvel_collection.helpers import token_required
from marvel_collection.models import User, db, ma

api = Blueprint('api',__name__,url_prefix='/api') #the url that goes into insomnia

@api.route('/getdata')
def getdata():
    return {'some':'value'}

