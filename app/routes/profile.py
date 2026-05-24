from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models import db, User, FlightBooking, Review, PlaceTranslation
from app.data import ui_texts
from app.forms import EditProfileForm
from werkzeug.security import generate_password_hash

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    lang = request.args.get('lang', session.get('lang', 'en'))
    session['lang'] = lang
    ui = ui_texts.get(lang, ui_texts.get('en'))

    if 'user_id' not in session:
        flash(ui.get('msg_login_required', 'Please login first.'), 'danger')
        return redirect(url_for('auth.login', lang=lang))

    user = User.query.get(session['user_id'])
    edit_form = EditProfileForm()

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'cancel_booking':
            booking_id = request.form.get('booking_id')
            booking = FlightBooking.query.get(booking_id)
            if booking and booking.user_id == user.id and booking.status == 'Pending':
                db.session.delete(booking)
                db.session.commit()
                flash(ui.get('msg_booking_cancelled', 'Booking cancelled successfully!'), 'success')
                return redirect(url_for('profile.profile', lang=lang))
                
        elif action == 'edit_profile' and edit_form.validate_on_submit():
            user.email = edit_form.email.data
            if edit_form.password.data:
                user.password_hash = generate_password_hash(edit_form.password.data)
            db.session.commit()
            flash(ui.get('msg_profile_updated', 'Profile updated successfully!'), 'success')
            return redirect(url_for('profile.profile', lang=lang))

    if request.method == 'GET':
        edit_form.email.data = user.email

    bookings = FlightBooking.query.filter_by(user_id=user.id).order_by(FlightBooking.id.desc()).all()

    reviews_data = db.session.query(Review, PlaceTranslation.name).join(
        PlaceTranslation, Review.place_id == PlaceTranslation.place_id
    ).filter(
        Review.user_id == user.id, 
        PlaceTranslation.language_code == lang
    ).order_by(Review.created_at.desc()).all()

    return render_template('profile.html', ui=ui, lang=lang, dir=ui['dir'], user=user, bookings=bookings, reviews=reviews_data, edit_form=edit_form)