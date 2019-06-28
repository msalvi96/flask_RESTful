import os
from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from models.store import StoreModel
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = '5512637025Aparna96!'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

@app.route('/')
def intro():
    data = [store.json() for store in StoreModel.query.all()]
    r = json.dumps(data)
    loaded_r = json.loads(r)
    return render_template('index.html', page_title="StoresAround API", stores=loaded_r)

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
