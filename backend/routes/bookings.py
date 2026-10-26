from flask import Blueprint, jsonify, request
from extensions import db
from models import Booking, Flight
import uuid

bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')

@bookings_bp.route('/', methods=['POST'])
def create_booking():
    data = request.get_json()
    flight = Flight.query.get_or_404(data.get('flight_id'))
    
    if flight.available_seats <= 0:
        return jsonify({'error': 'Flight fully booked'}), 400

    flight.available_seats -= 1
    pnr = str(uuid.uuid4())[:8].upper()
    new_booking = Booking(booking_reference=pnr, flight_id=flight.id, passenger_name=data.get('passenger_name'))
    
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({'booking_reference': pnr, 'status': 'SUCCESS'}), 201