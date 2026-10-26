import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000';

export default function App() {
  const [flights, setFlights] = useState([]);
  const [passengerName, setPassengerName] = useState('');
  const [bookingResult, setBookingResult] = useState(null);

  useEffect(() => {
    fetchFlights();
  }, []);

  const fetchFlights = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/flights`);
      setFlights(res.data);
    } catch (err) {
      console.error("Failed to fetch flights", err);
    }
  };

  const bookTicket = async (flightId) => {
    if (!passengerName.trim()) return alert("Passenger name is required.");
    
    try {
      const res = await axios.post(`${API_BASE}/api/bookings`, { 
        flight_id: flightId, 
        passenger_name: passengerName 
      });
      setBookingResult(res.data.booking_reference);
      fetchFlights(); // Refresh seat counts
    } catch (err) {
      alert(err.response?.data?.error || "Booking failed");
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '2rem auto', fontFamily: 'system-ui' }}>
      <h1>Salama Angani Ticketing</h1>
      
      {bookingResult && (
        <div style={{ background: '#d4edda', padding: '1rem', marginBottom: '1rem', color: '#155724' }}>
          Booking Confirmed! Your PNR is: <strong>{bookingResult}</strong>
        </div>
      )}

      <input 
        type="text" 
        placeholder="Enter Passenger Name" 
        value={passengerName}
        onChange={(e) => setPassengerName(e.target.value)}
        style={{ padding: '0.5rem', width: '100%', marginBottom: '1rem' }}
      />

      <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #ccc' }}>
            <th>Flight</th>
            <th>Route</th>
            <th>Seats</th>
            <th>Price</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {flights.map(f => (
            <tr key={f.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: '0.5rem 0' }}>{f.flight_number}</td>
              <td>{f.origin} → {f.destination}</td>
              <td>{f.available_seats}</td>
              <td>${f.base_price.toFixed(2)}</td>
              <td>
                <button 
                  disabled={f.available_seats === 0} 
                  onClick={() => bookTicket(f.id)}
                  style={{ padding: '0.5rem 1rem', cursor: f.available_seats === 0 ? 'not-allowed' : 'pointer' }}
                >
                  {f.available_seats > 0 ? "Book" : "Sold Out"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}