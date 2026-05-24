import random
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from app.models import db, FlightBooking
from app.forms import FlightBookingForm
from app.data import ui_texts

flights_bp = Blueprint('flights', __name__)

@flights_bp.route('/book_flight/<destination>', methods=['GET', 'POST'])
def book_flight(destination):
    lang = request.args.get('lang', session.get('lang', 'en'))
    session['lang'] = lang
    ui = ui_texts.get(lang, ui_texts.get('en'))

    if 'user_id' not in session:
        flash(ui.get('msg_login_required', 'Please login to book a flight.'), 'danger')
        return redirect(url_for('auth.login', lang=lang))

    form = FlightBookingForm()

    if form.validate_on_submit():
        airlines = ['EgyptAir', 'Nile Air', 'FlyEgypt', 'Air Cairo']
        airline = random.choice(airlines)
        f_num = f"{airline[:2].upper()}{random.randint(100, 999)}"

        new_booking = FlightBooking(
            user_id=session['user_id'],
            airline_name=airline,
            flight_number=f_num,
            departure_city=form.departure.data,
            destination_city=destination,
            travel_date=form.travel_date.data,
            status='Pending'
        )
        db.session.add(new_booking)
        db.session.commit()

        flash(ui.get('flight_success', 'Flight booked successfully!'), 'success')
        return redirect(url_for('home.home', lang=lang))

    return render_template('book_flight.html', ui=ui, lang=lang, dir=ui['dir'], form=form, destination=destination)