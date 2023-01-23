from flask import request
from flask_restful import Resource
from api.v1.models.places import Place
from api.v1.models.cities import City
from api.v1.models.users import User

class PlaceView(Resource):
    def get(self, city_id, place_id=None):
        if place_id:
            place = Place.get(place_id)
            if place:
                return place.to_dict(), 200
            else:
                return {}, 404
        else:
            city = City.get(city_id)
            if city:
                places = city.places
                return [place.to_dict() for place in places], 200
            else:
                return {}, 404

    def post(self, city_id):
        data = request.get_json()
        if not data:
            return {'message': 'Not a JSON'}, 400
        if 'user_id' not in data:
            return {'message': 'Missing user_id'}, 400
        user = User.get(data['user_id'])
        if not user:
            return {}, 404
        if 'name' not in data:
            return {'message': 'Missing name'}, 400
        place = Place(name=data['name'], user_id=data['user_id'], city_id=city_id)
        place.save()
        return place.to_dict(), 201

    def put(self, place_id):
        data = request.get_json()
        if not data:
            return {'message': 'Not a JSON'}, 400
        place = Place.get(place_id)
        if not place:
            return {}, 404
        for key, value in data.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return place.to_dict(), 200

    def delete(self, place_id):
        place = Place.get(place_id)
        if not place:
            return {}, 404
        place.delete()
        return {}, 200
