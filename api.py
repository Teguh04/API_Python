from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from flask import jsonify
import json



mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'simple_api'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


mysql.init_app(app)

api = Api(app)

class UserReview(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('order_id', type=int, help="Name cannot be blank!")
            parser.add_argument('product_id', type=int, help="Name cannot be blank!")
            parser.add_argument('user_id', type=int, help="Name cannot be blank!")
            parser.add_argument('rating', type=float, help="Name cannot be blank!")
            parser.add_argument('review', type=str, help="Name cannot be blank!")
            args = parser.parse_args()

            _userOrder = args['order_id']
            _userProduct = args['product_id']
            _userUser = args['user_id']
            _userRating = args['rating']
            _userReview = args['review']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spUser',(_userOrder, _userProduct, _userUser, _userRating, _userReview))
            data = cursor.fetchall()
            conn.commit()
            return {'StatusCode':'200','Message': 'User creation success'}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            # Parse the arguments
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_review")
            conn.commit()

            r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]

            resp = jsonify(r)
            resp.status_code = 200
            return resp

        except Exception as e:
            return {'error': str(e)}

class UserReviewId(Resource):
    def put(self, id):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('order_id', type=int, help="Name cannot be blank!")
            parser.add_argument('product_id', type=int, help="Name cannot be blank!")
            parser.add_argument('user_id', type=int, help="Name cannot be blank!")
            parser.add_argument('rating', type=float, help="Name cannot be blank!")
            parser.add_argument('review', type=str, help="Name cannot be blank!")
            args = parser.parse_args()

            _userOrder = args['order_id']
            _userProduct = args['product_id']
            _userUser = args['user_id']
            _userRating = args['rating']
            _userReview = args['review']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spUpdateUser',(id, _userOrder, _userProduct, _userUser, _userRating, _userReview))
            conn.commit()
            data = cursor.fetchall()
            resp = jsonify('User update successfully!')
            resp.status_code = 200
            return resp

        except Exception as e:
            return {'error': str(e)}

    def get(self, id):
        try:
            # Parse the arguments
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_review WHERE id=%s", id)
            conn.commit()

            r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]

            resp = jsonify(r)
            resp.status_code = 200
            return resp


        except Exception as e:
            return {'error': str(e)}

    def delete(self, id):
        try:
            # Parse the arguments
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_review WHERE id=%s", id)
            conn.commit()
            resp = jsonify('User deleted successfully!')
            resp.status_code = 200
            return resp

        except Exception as e:
            return {'error': str(e)}


api.add_resource(UserReview, '/UserReview')
api.add_resource(UserReviewId, '/UserReview/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)