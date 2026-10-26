from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
import uuid

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)

# Database Models
class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), unique=True, nullable=False)
    origin = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    base_price = db.Column(db.Float, nullable=False)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    booking_reference = db.Column(db.String(8), unique=True, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    passenger_name = db.Column(db.String(100), nullable=False)

# API Routes
@app.route('/api/flights', methods=['GET'])
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

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    flight = Flight.query.get_or_404(data.get('flight_id'))
    
    if flight.available_seats <= 0:
        return jsonify({'error': 'Flight fully booked'}), 400

    # Process Booking
    flight.available_seats -= 1
    pnr = str(uuid.uuid4())[:8].upper()
    new_booking = Booking(booking_reference=pnr, flight_id=flight.id, passenger_name=data.get('passenger_name'))
    
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({'booking_reference': pnr, 'status': 'SUCCESS'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)