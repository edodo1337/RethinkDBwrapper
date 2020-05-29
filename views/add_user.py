from flask_restful import Resource, reqparse
from db.models.user import User


class AddUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='asdasd', required=True)
        parser.add_argument('age', type=int, help='asdasd', required=True)

        args = parser.parse_args()

        name = args.get('name')
        age = args.get('age')


        # u1 = User.create(name=name, age=age)
        # u2 = User.create(name=name, age=age)

        u1 = User.find("73eede85-79a4-45a2-908d-40449b893ba5")
        print("USER", u1)


        return {"status": [u1.id, u1.name]}
