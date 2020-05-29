from flask import Flask, jsonify, g, Blueprint
from flask_restful import Api, reqparse
from views.add_user import AddUser
from db.utils import DBConnector
from db.models.user import User

app = Flask(__name__)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(AddUser, '/add_user/')
app.register_blueprint(api_bp, url_prefix='/api')

with app.app_context():
    db = DBConnector()
    db.init_app(api)

@app.route('/')
def hello():
    # db1 = DBConnector.get_solo()
    # db2 = DBConnector.get_solo()
    # print(db1.RDB_HOST, db2.RDB_HOST)
    # u = User.create(name="John", age=18, gender='male')
    # print(u.age)
    return jsonify("HELLO")

# app.run(debug=True)
