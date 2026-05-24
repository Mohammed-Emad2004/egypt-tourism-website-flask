from flask import Blueprint, render_template, request, session, redirect, url_for
from app.data import ui_texts
from app.models import Place, PlaceTranslation

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def home():
    if session.get('role') == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    lang = request.args.get('lang', session.get('lang', 'en'))
    session['lang'] = lang
    
    ui = ui_texts.get(lang, ui_texts.get('en'))
    
    all_places = Place.query.limit(3).all()
    display_places = []
    
    for p in all_places:
        trans = PlaceTranslation.query.filter_by(place_id=p.id, language_code=lang).first()
        if trans:
            display_places.append({
                'id': p.id,
                'image_file': p.image_file,
                'rating': p.rating,
                'name': trans.name,
                'category': trans.category,
                'description': trans.description
            })
            
    return render_template('home.html', ui=ui, lang=lang, dir=ui['dir'], places=display_places)