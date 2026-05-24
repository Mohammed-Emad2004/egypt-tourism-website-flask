from flask import Blueprint, render_template, request, session
from app.data import ui_texts
from app.models import Place, PlaceTranslation

gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('/gallery')
def gallery():
    lang = request.args.get('lang', session.get('lang', 'en'))
    session['lang'] = lang
    ui = ui_texts.get(lang, ui_texts.get('en'))
    
    all_places = Place.query.all()
    images = []
    for p in all_places:
        trans = PlaceTranslation.query.filter_by(place_id=p.id, language_code=lang).first()
        if trans:
            images.append({'url': f"/static/images/{p.image_file}", 'title': trans.name})
            
    return render_template('gallery.html', ui=ui, lang=lang, dir=ui['dir'], images=images)