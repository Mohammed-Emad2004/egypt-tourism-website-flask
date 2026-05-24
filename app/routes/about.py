from flask import Blueprint, render_template, request, session
from app.data import ui_texts

about_bp = Blueprint('about', __name__)

@about_bp.route('/about')
def about():
    lang = request.args.get('lang', session.get('lang', 'en'))
    session['lang'] = lang
    ui = ui_texts.get(lang, ui_texts.get('en'))
    return render_template('about.html', ui=ui, lang=lang, dir=ui['dir'])