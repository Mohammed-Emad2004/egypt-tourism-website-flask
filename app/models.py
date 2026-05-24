from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.String(50), primary_key=True)
    image_file = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)
    booking_url = db.Column(db.String(2048))
    location_url = db.Column(db.String(2048))
    translations = db.relationship('PlaceTranslation', backref='place', lazy=True, cascade="all, delete-orphan")

class PlaceTranslation(db.Model):
    __tablename__ = 'place_translations'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.String(50), db.ForeignKey('places.id'), nullable=False)
    language_code = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    hook = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100))
    best_time = db.Column(db.String(100))
    transportation = db.Column(db.Text)
    activities = db.Column(db.Text)

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='user')
    reviews = db.relationship('Review', backref='author', lazy=True)
    bookings = db.relationship('FlightBooking', backref='passenger', lazy=True)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.String(50), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FlightBooking(db.Model):
    __tablename__ = 'flight_bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    airline_name = db.Column(db.String(100), nullable=False) 
    flight_number = db.Column(db.String(20), nullable=False)
    departure_city = db.Column(db.String(50), nullable=False)
    destination_city = db.Column(db.String(50), nullable=False)
    travel_date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Pending')