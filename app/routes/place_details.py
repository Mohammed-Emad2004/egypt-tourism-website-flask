import requests
from flask import Blueprint, render_template, request, abort, session, flash, redirect, url_for
from app.data import ui_texts
from app.models import db, Place, PlaceTranslation, Review, User
from app.forms import ReviewForm

place_details_bp = Blueprint('place_details', __name__)

CITY_COORDS = {
    'cairo': {'lat': 30.0444, 'lon': 31.2357},
    'luxor': {'lat': 25.6872, 'lon': 32.6396},
    'aswan': {'lat': 24.0889, 'lon': 32.8998},
    'alexandria': {'lat': 31.2001, 'lon': 29.9187},
    'sinai': {'lat': 27.9158, 'lon': 34.3299},
    'default': {'lat': 30.0444, 'lon': 31.2357}
}

@place_details_bp.route('/place/<place_id>', methods=['GET', 'POST'])
def place_details(place_id):
    lang = request.args.get('lang', session.get('lang', 'en'))
    session['lang'] = lang
    ui = ui_texts.get(lang, ui_texts.get('en'))
    
    place_obj = Place.query.get(place_id)
    if not place_obj: abort(404)
        
    trans = PlaceTranslation.query.filter_by(place_id=place_id, language_code=lang).first()
    if not trans: abort(404)
        
    form = ReviewForm()
    
    if form.validate_on_submit():
        if 'user_id' not in session:
            flash(ui.get('msg_login_required', 'Please login to add a review.'), 'danger')
            return redirect(url_for('auth.login', lang=lang))
            
        new_review = Review(place_id=place_id, user_id=session['user_id'], rating=int(form.rating.data), comment=form.comment.data)
        db.session.add(new_review)
        db.session.commit()
        flash(ui.get('msg_review_added', 'Review added successfully!'), 'success')
        return redirect(url_for('place_details.place_details', place_id=place_id, lang=lang))
    
    reviews_data = db.session.query(Review, User).join(User, Review.user_id == User.id).filter(Review.place_id == place_id).order_by(Review.created_at.desc()).all()

    city_name_lower = trans.city.lower()
    coords = CITY_COORDS['default']
    
    if 'cairo' in city_name_lower or 'قاهرة' in city_name_lower: coords = CITY_COORDS['cairo']
    elif 'luxor' in city_name_lower or 'أقصر' in city_name_lower: coords = CITY_COORDS['luxor']
    elif 'alex' in city_name_lower or 'إسكندرية' in city_name_lower: coords = CITY_COORDS['alexandria']
    elif 'aswan' in city_name_lower or 'أسوان' in city_name_lower: coords = CITY_COORDS['aswan']
    elif 'sinai' in city_name_lower or 'سيناء' in city_name_lower or 'red sea' in city_name_lower: coords = CITY_COORDS['sinai']

    weather_data = None
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current_weather=true"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'temp': data['current_weather']['temperature'],
                'wind': data['current_weather']['windspeed']
            }
    except Exception as e:
        print("Error fetching weather:", e)

    formatted_place = {
        'id': place_obj.id,
        'name': trans.name,
        'image_file': place_obj.image_file,
        'category': trans.category,
        'hook': trans.hook,
        'rating': place_obj.rating,
        "booking_url": place_obj.booking_url,
        "location_url": place_obj.location_url,
        'location': trans.city,
        'best_time': trans.best_time,
        'description': trans.description,
        'activities': trans.activities,
        'transportation': ([x.strip() for x in trans.transportation.split(',')]
                if trans.transportation
                else [])
    }
    
    return render_template('place_details.html', ui=ui, lang=lang, dir=ui['dir'], place=formatted_place, form=form, reviews=reviews_data, weather=weather_data)