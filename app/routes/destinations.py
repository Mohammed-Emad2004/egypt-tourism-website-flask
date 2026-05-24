from flask import Blueprint, render_template, request, session
from app.data import ui_texts
from app.models import Place, PlaceTranslation

destinations_bp = Blueprint('destinations', __name__)

@destinations_bp.route('/destinations')
def destinations():
    lang = request.args.get('lang', session.get('lang', 'en'))
    session['lang'] = lang
    ui = ui_texts.get(lang, ui_texts.get('en'))
    
    search_query = request.args.get('q', '').lower()
    city_filter = request.args.get('city', 'all')
    category_filter = request.args.get('category', 'all')

    city_keywords = {
        'cairo': ['قاهرة', 'cairo', 'caire'],
        'luxor': ['أقصر', 'أسوان', 'luxor', 'aswan', 'louxor'],
        'alex': ['إسكندرية', 'alex', 'alejandría'],
        'sinai': ['سيناء', 'بحر', 'sinai', 'red sea', 'mer rouge']
    }
    
    category_keywords = {
        'historical': ['تاريخي', 'أثري', 'historical', 'historique', 'histórico', 'historisch'],
        'religious': ['ديني', 'religious', 'religieux', 'religioso', 'religiös'],
        'nature': ['طبيعة', 'شواطئ', 'nature', 'beaches', 'naturaleza', 'natur'],
        'modern': ['ثقافي', 'حديث', 'culture', 'modern', 'moderne', 'kultur']
    }

    all_places = Place.query.all()
    display_places = []
    
    for p in all_places:
        trans = PlaceTranslation.query.filter_by(place_id=p.id, language_code=lang).first()
        if trans:
            match_search = True
            if search_query:
                if search_query not in trans.name.lower() and search_query not in trans.description.lower():
                    match_search = False
            
            match_city = True
            if city_filter != 'all':
                keywords = city_keywords.get(city_filter, [])
                if not any(kw in trans.city.lower() for kw in keywords):
                    match_city = False

            match_category = True
            if category_filter != 'all':
                keywords = category_keywords.get(category_filter, [])
                if not any(kw in trans.category.lower() for kw in keywords):
                    match_category = False

            if match_search and match_city and match_category:
                display_places.append({
                    'id': p.id,
                    'image_file': p.image_file,
                    'rating': p.rating,
                    'name': trans.name,
                    'category': trans.category,
                    'description': trans.description,
                    'location': {'city': trans.city}
                })
    
    return render_template('destinations.html', ui=ui, lang=lang, dir=ui['dir'], places=display_places)