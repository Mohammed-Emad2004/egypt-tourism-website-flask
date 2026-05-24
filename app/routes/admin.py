from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models import db, User, FlightBooking, Review, Place, PlaceTranslation
from app.data import ui_texts
from app.forms import AddPlaceForm
import uuid

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    lang = request.args.get('lang', session.get('lang', 'en'))
    session['lang'] = lang
    ui = ui_texts.get(lang, ui_texts.get('en'))

    if session.get('role') != 'admin':
        flash(ui.get('msg_unauthorized', 'Unauthorized Access!'), 'danger')
        return redirect(url_for('home.home', lang=lang))

    add_place_form = AddPlaceForm()

    edit_place = None

    if request.method == 'GET':

        edit_id = request.args.get('edit_place')

        if edit_id:

            edit_place = Place.query.get(edit_id)

            if edit_place:

                trans = PlaceTranslation.query.filter_by(
                    place_id=edit_id,
                    language_code=lang
                ).first()

                if trans:
                    add_place_form.name.data = trans.name
                    add_place_form.city.data = trans.city
                    add_place_form.category.data = trans.category
                    add_place_form.hook.data = trans.hook
                    add_place_form.description.data = trans.description
                    add_place_form.transportation.data = trans.transportation
                    add_place_form.activities.data = trans.activities
                    add_place_form.best_time.data = trans.best_time

                add_place_form.image_file.data = edit_place.image_file
                add_place_form.rating.data = edit_place.rating
                add_place_form.booking_url.data = edit_place.booking_url
                add_place_form.location_url.data = edit_place.location_url

    if request.method == 'POST':
        action = request.form.get('action')

        if action in ['approve', 'reject']:
            booking_id = request.form.get('booking_id')
            booking = FlightBooking.query.get(booking_id)
            if booking:
                booking.status = 'Approved' if action == 'approve' else 'Rejected'
                db.session.commit()
                flash('Booking status updated successfully!', 'success')
                
        elif action == 'delete_review':
            review_id = request.form.get('review_id')
            review = Review.query.get(review_id)
            if review:
                db.session.delete(review)
                db.session.commit()
                flash(ui.get('msg_review_deleted', 'Review deleted successfully!'), 'success')
                
        elif action == 'delete_place':
            place_id = request.form.get('place_id')
            place = Place.query.get(place_id)
            if place:
                db.session.delete(place)
                db.session.commit()
                flash(ui.get('msg_place_deleted', 'Place deleted successfully!'), 'success')

        elif action == 'add_place' and add_place_form.validate_on_submit():

            edit_id = request.form.get('edit_place')
            if edit_id:
                place = Place.query.get(edit_id)
                place.image_file = add_place_form.image_file.data
                place.rating = float(add_place_form.rating.data or 0)
                place.booking_url = add_place_form.booking_url.data
                place.location_url = add_place_form.location_url.data
                translation = PlaceTranslation.query.filter_by(place_id=edit_id, language_code=lang).first()

                if translation:
                    translation.name = add_place_form.name.data
                    translation.city = add_place_form.city.data
                    translation.category = add_place_form.category.data
                    translation.hook = add_place_form.hook.data
                    translation.description = add_place_form.description.data
                    translation.transportation = add_place_form.transportation.data
                    translation.activities = add_place_form.activities.data
                    translation.best_time = add_place_form.best_time.data
                db.session.commit()
                flash("Place updated successfully", "success")
                return redirect(
                    url_for(
                        'admin.admin_dashboard',
                        lang=lang
                    )
                )

            from deep_translator import GoogleTranslator
            import uuid

            new_place_id = f"place_{uuid.uuid4().hex[:8]}"
            
            new_place = Place(
                id=new_place_id, 
                image_file=add_place_form.image_file.data, 
                rating=float(add_place_form.rating.data, default=0.0),
                booking_url=add_place_form.booking_url.data,
                location_url=add_place_form.location_url.data
            )
            db.session.add(new_place)
            languages = ['en', 'ar', 'fr', 'es', 'de']
            
            current_admin_lang = lang 

            for l in languages:
                if l == current_admin_lang:
                    name_l = add_place_form.name.data
                    category_l = add_place_form.category.data
                    hook_l = add_place_form.hook.data
                    description_l = add_place_form.description.data
                    city_l = add_place_form.city.data
                    transportation_l = add_place_form.transportation.data
                    activities_l = add_place_form.activities.data
                    best_time_l = add_place_form.best_time.data
                else:
                    try:
                        translator = GoogleTranslator(source='auto', target=l)
                        name_l = translator.translate(add_place_form.name.data)
                        category_l = translator.translate(add_place_form.category.data)
                        hook_l = translator.translate(add_place_form.hook.data)
                        description_l = translator.translate(add_place_form.description.data)
                        city_l = translator.translate(add_place_form.city.data)
                        transportation_l = translator.translate(add_place_form.transportation.data)
                        activities_l = translator.translate(add_place_form.activities.data)
                        best_time_l = translator.translate(add_place_form.best_time.data)
                    except Exception as e:
                        print(f"Translation failed for language {l}: {e}")
                        name_l = add_place_form.name.data
                        category_l = add_place_form.category.data
                        hook_l = add_place_form.hook.data
                        description_l = add_place_form.description.data
                        city_l = add_place_form.city.data
                        transportation_l = add_place_form.transportation.data
                        activities_l = add_place_form.activities.data
                        best_time_l = add_place_form.best_time.data

                trans = PlaceTranslation(
                    place_id=new_place_id,
                    language_code=l,
                    name=name_l,
                    category=category_l,
                    hook=hook_l,
                    description=description_l,
                    city=city_l,
                    transportation=transportation_l,
                    activities=activities_l,
                    best_time=best_time_l
                )
                db.session.add(trans)
            
            db.session.commit()
            flash(ui.get('msg_place_added', 'Place added successfully!'), 'success')
            return redirect(url_for('admin.admin_dashboard', lang=lang))
        
    users_count = User.query.count()
    bookings_count = FlightBooking.query.count()
    reviews_count = Review.query.count()
    pending_bookings = FlightBooking.query.filter_by(status='Pending').all()
    
    all_reviews = db.session.query(Review, User.username, PlaceTranslation.name).join(
        User, Review.user_id == User.id).join(PlaceTranslation, Review.place_id == PlaceTranslation.place_id).filter(PlaceTranslation.language_code == lang).order_by(Review.created_at.desc()).all()
    
    all_places = db.session.query(Place, PlaceTranslation.name, PlaceTranslation.city).join(
        PlaceTranslation, Place.id == PlaceTranslation.place_id
    ).filter(PlaceTranslation.language_code == lang).all()

    return render_template('admin.html', ui=ui, lang=lang, dir=ui['dir'], 
                           u_count=users_count, b_count=bookings_count, 
                           r_count=reviews_count, pending=pending_bookings,
                           reviews=all_reviews, places=all_places, add_form=add_place_form)