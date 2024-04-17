#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):
    def get(self):
        restaurants = [restaurant.to_dict(only=('id', 'address', 'name'))
                       for restaurant in Restaurant.query.all()]
        return restaurants, 200
    
class RestaurantsId(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if restaurant:
            return restaurant.to_dict(), 200
        else:
            return {"error": "Restaurant not found"}, 404
    def delete(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return {}, 204
        else:
            return {"error": "Restaurant not found"}, 404
        
class Pizzas(Resource):
    def get(self):
        pizzas = [pizza.to_dict(only=('id', 'name', 'ingredients'))
                  for pizza in Pizza.query.all()]
        return pizzas, 200

class RestaurantPizzas(Resource):
    def post(self):
        json = request.get_json()
        try:
            restaurant_pizza = RestaurantPizza(
                price=json['price'],
                pizza_id=json['pizza_id'],
                restaurant_id=json['restaurant_id']
            )
            db.session.add(restaurant_pizza)
            db.session.commit()
            return restaurant_pizza.to_dict(), 201
        except:
            return {"errors": ["validation errors"]}, 400

api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantsId, '/restaurants/<int:id>')
api.add_resource(Pizzas, '/pizzas')
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
