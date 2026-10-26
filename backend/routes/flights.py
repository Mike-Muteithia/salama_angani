from flask import Blueprint, jsonify
from models import Flight

flights_bp = Blueprint('flights', __name__, url_prefix='/api/flights')

@flights_bp.route('/', methods=['GET'])
def get_flights():
    flights = Flight.query.all()
    return jsonify([{
        'id': f.id,
        'flight_number': f.flight_number,
        'origin': f.origin,
        'destination': f.destination,
        'available_seats': f.available_seats,
        'base_price': f.base_price
    } for f in flights]), 200