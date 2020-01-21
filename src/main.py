"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/create', methods=['POST'])
def handle_create():
    userdata=request.get_json()
    obj1=Person(username=userdata["username"],email=userdata["email"],address=userdata["address"],phone=userdata["phone"])
    db.session.add(obj1)
    db.session.commit()
    return "Successfully inserted the data"

@app.route('/get')
def handle_get():
    userdata1=Person.query.all()
    allpeople = list(map(lambda x: x.serialize(), userdata1))
    return jsonify(allpeople)
        
@app.route('/update/<id>',methods=['PUT'])
def handle_update(id):
    newobj=Person.query.get(id)
    newobj1=request.get_json()
    if 'username' in newobj1:
        newobj.username=newobj1["username"]
    if 'email' in newobj1:
        newobj.email=newobj1["email"]
    if 'address' in newobj1:
        newobj.address=newobj1["address"]
    if 'phone' in newobj1:
        newobj.phone=newobj1["phone"]
    db.session.merge(newobj)
    db.session.commit()
    return "updated is over"

@app.route('/delete/<id>',methods=['DELETE'])
def handle_delete(id):
    userdata3=Person.query.get(id)
    db.session.delete(userdata3)
    db.session.commit()
    return "deleted is done"

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
